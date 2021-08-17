import consts
import os

from PyInquirer import print_json, prompt

from notion_renderer.renderer import objectify_notion_blocks
# from utils import handleImage
import utils
import json
import getopt
import sys
import re
from urllib.parse import unquote


class MDX(object):
    def __init__(self, page):
        self.text = """---
title: "%s"
---""" % (page.title)
        self.add_newlines(2)

        self.property_block_opened = False
        self.column_properties = ""

    def update_mdx(self, newText):
        self.text += newText

    def add_newlines(self, lineNum):
        for i in range(lineNum):
            self.update_mdx("\n")

    def set_post_path(self, path):
        self.postPath = path

    def set_static_path(self, path):
        self.staticPath = path

    def set_page_id(self, id):
        self.pageId = id

    def set_category(self, category):
        self.category = category

    def handle_block(self, block):
        print("block.type", block.type)
        # print("block", block)
        if block.type == "header":
            self.update_mdx("# " + block.title)
        elif block.type == "sub_header":
            self.update_mdx("## " + block.title)
        elif block.type == "text":
            self.update_mdx(block.title)
        elif block.type == "image":
            url = unquote(block.source)
            if "comp-" in utils.getMediaName(url):
                compName = utils.getCompNamefromImageName(url)
                self.update_mdx(
                    f'<{compName} {utils.getJsxPropertiesFromStr(block.caption)}>')
                self.update_mdx(
                    f'</{compName}>')
            else:
                print('block.caption', block.caption)
                self.update_mdx(
                    f'<Block width="{block.width}px" {utils.getJsxPropertiesFromStr(block.caption)}>')
                self.add_newlines(2)
                self.update_mdx(
                    f'{utils.handleImage(block.source, self.staticPath)}')
                self.add_newlines(2)
                self.update_mdx(f'</Block>')
        elif block.type == "video":
            self.update_mdx(
                f'{utils.handleVideo(block.source, self.staticPath, block.width)}')
        elif block.type == "callout":
            self.update_mdx(
                f"<button {utils.getJsxPropertiesFromStr(block.title)}>{utils.getPureTitle(block.title)}</button>")
        elif block.type == "toggle":
            self.handle_toggle_block(block)
        # elif block.type == "collection_view_page":
        #     rows = block.collection.get_rows()
        #     print('rows', rows)
        elif block.type == "quote":
            print("Open Quote Block!")
            self.property_block_opened = True
            self.update_mdx(
                f'<Block {utils.getJsxPropertiesFromStr(block.title)}>')
        elif block.type == "column_list":
            self.update_mdx(f'<FlexBox>')
            self.add_newlines(2)
            for idx, column in enumerate(block.children):
                firstColumnBlock = column.children[0]
                if (firstColumnBlock.type == 'code'):
                    self.column_properties = utils.getJsxPropertiesFromStr(
                        firstColumnBlock.title)

                self.update_mdx(
                    f'<FlexItem{"" if utils.shouldShrink(column) else " noShrink"}{" " if self.column_properties else ""}{self.column_properties}>')
                self.column_properties = ""
                self.add_newlines(2)
                for idx, childBlock in enumerate(column.children):
                    self.handle_block(childBlock)
                self.update_mdx(f'</FlexItem>')
                self.add_newlines(2)
            self.update_mdx(f'</FlexBox>')
        elif block.type == "embed":
            self.update_mdx(
                f'<iframe src="{block.source}" width="{block.width}px" height="{block.height}px" />')
        elif block.type == "page":
            self.update_mdx(
                f'[{block.title}](/{self.category}/{block.id.replace("-","")})')

        if (self.property_block_opened and block.type != "quote"):
            print("Close Quote Block!")
            self.update_mdx("</Block>")
            self.property_block_opened = False

        self.add_newlines(2)  # add a newline

    def handle_toggle_block(self, block):
        properties = utils.get_properties_from_toggle(block.title)
        self.update_mdx(
            f"<{properties.title}{properties.properties_string}>")
        self.add_newlines(2)

        # handle child blocks recursively
        toggleChildren = block.children
        for idx, childBlock in enumerate(toggleChildren):
            if (childBlock.type == "toggle"):
                self.handle_toggle_block(childBlock)
            else:
                self.handle_block(childBlock)
                # if (idx + 1) < len(toggleChildren):
                #     self.update_mdx("<br/>")
                #     self.add_newlines(2)

        self.update_mdx(f"</{properties.title}>")
        self.add_newlines(2)


def convert():

    argumentList = sys.argv[1:]
    params = utils.JsonPage()
    basePath = "./site-templates/template-nextjs-lighthouse/"

    if argumentList:
        print('argumentList', argumentList)
        setattr(params, 'pageId', argumentList[0])
        setattr(params, 'fileName', argumentList[1])
        setattr(params, 'category', argumentList[2])
        setattr(params, 'assetsPath', argumentList[3])
    else:
        # start_prompt
        questions = [
            {
                "type": "input",
                "name": "pageId",
                "message": "pageId",
            },
            {
                "type": "input",
                "name": "fileName",
                "message": "fileName",
                "default": "index.mdx",
            },
            {
                "type": "input",
                "name": "category",
                "message": "Where you want to generate MDX files?",
                "default": "landing-page",
            },
            {
                "type": "input",
                "name": "assetsPath",
                "message": "Where you want to save asset files? (image, video)",
                "default": "public",
            },
        ]
        answers = prompt(questions)

        for key, value in answers.items():
            setattr(params, key, value)

    # get the notion_blocks
    # targetPath = f"{basePath}/{params.category}"
    postPath = f'{basePath}/{params.category}'
    # staticPath = f'{consts.STATIC_DIR}/{basePath}/{params.category}/{params.pageId}' # for gatsbyjs
    staticPath = params.assetsPath  # for nextjs

    if not os.path.exists(basePath):
        os.makedirs(basePath)

    if not os.path.exists(postPath):
        os.makedirs(postPath)

    if not os.path.exists(staticPath):
        os.makedirs(staticPath)

    [page, blocks] = objectify_notion_blocks(
        "7f03ff0043f4f1b5367552a37201efb3e815abf50eb7170db3df48f1ac4a69fc998e42fbdfcb0f57f57c296226f10d51c96f218ad27e1b6067c68fcd191f55bda1dced6b384f159b9184974eb3bb",
        params.pageId,
    )

    # start generate MDX
    mdx = MDX(page)
    mdx.set_post_path(postPath)
    mdx.set_static_path(staticPath)
    mdx.set_page_id(params.pageId)
    mdx.set_category(params.category)

    for idx, block in enumerate(blocks):
        mdx.handle_block(block)

    file = open(f'{postPath}/{params.fileName}', "w")
    file.write(mdx.text)


if __name__ == "__main__":
    convert()
