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


class JsonPage:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


# code from https://stackoverflow.com/a/39894555/4047204
class MDX(object):
    def __init__(self, page):
        self.text = """---
title: "%s"
---""" % (page.title)
        self.add_newlines(2)

    def update_mdx(self, newText):
        self.text += newText

    def add_newlines(self, lineNum):
        for i in range(lineNum):
            self.update_mdx("\n")

    def set_post_path(self, path):
        self.postPath = path

    def set_static_path(self, path):
        self.staticPath = path

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
            self.update_mdx(
                f'{utils.handleImage(block.source, self.postPath)}')
        elif block.type == "video":
            self.update_mdx(
                f'{utils.handleVideo(block.source, self.staticPath, block.width)}')
        elif block.type == "callout":
            [pure_title, property] = self.get_properties_from_title(
                block.title)
            self.update_mdx(
                f"<button {f'{property.key}={property.value}'}>{pure_title}</button>")
        elif block.type == "toggle":
            self.handle_toggle_block(block)
        elif block.type == "collection_view_page":
            rows = block.collection.get_rows()
            print('rows', rows)
        elif block.type == "column_list":
            self.update_mdx(f'<FlexBox>')
            self.add_newlines(2)
            for idx, column in enumerate(block.children):
                self.update_mdx(f'<FlexItem>')
                self.add_newlines(2)
                for idx, childBlock in enumerate(column.children):
                    self.handle_block(childBlock)
                self.update_mdx(f'</FlexItem>')
                self.add_newlines(2)
            self.update_mdx(f'</FlexBox>')

        self.add_newlines(2)  # add a newline

    def handle_toggle_block(self, block):
        properties = self.get_properties_from_toggle(block.title)
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

    def get_properties_from_toggle(self, title):
        jsonPage = JsonPage()

        splited = title.split(" ")
        setattr(jsonPage, 'title', splited[0])

        properties_string = ""
        for i in range(1, len(splited)):
            properties_string += splited[i] + " "

        if (properties_string):
            setattr(jsonPage, 'properties_string',
                    ' ' + properties_string[:-1])  # add space before the last character (jsx syntax)
        else:
            setattr(jsonPage, 'properties_string', '')

        return jsonPage

    def get_properties_from_title(self, title):
        s_without_parens = re.sub('\(.+?\)', '', title)
        text_in_brackets = re.findall('{(.+?)}', s_without_parens)

        pure_title = title.replace(f' {{{text_in_brackets[0]}}}', '')

        splited = text_in_brackets[0].split(":")
        property = JsonPage()
        setattr(property, 'key', splited[0].replace(' ', ''))
        setattr(property, 'value', splited[1].replace(' ', ''))

        return [pure_title, property]


def convert():

    argumentList = sys.argv[1:]
    params = JsonPage()
    basePath = "mdx-pages"

    if argumentList:
        print('argumentList', argumentList)
        setattr(params, 'category', argumentList[0])
        setattr(params, 'fileName', argumentList[1])
        setattr(params, 'pageId', argumentList[2])
    else:
        # start_prompt
        questions = [
            {
                "type": "input",
                "name": "category",
                "message": "Where you want to generate MDX files?",
                "default": "landing-page",
            },
            {
                "type": "input",
                "name": "fileName",
                "message": "fileName",
                "default": "index.mdx",
            },
            {
                "type": "input",
                "name": "pageId",
                "message": "pageId",
            },
        ]
        answers = prompt(questions)

        for key, value in answers.items():
            setattr(params, key, value)

    # get the notion_blocks
    # targetPath = f"{basePath}/{params.category}"
    postPath = f'{basePath}/{params.category}/{params.pageId}'
    staticPath = f'{consts.STATIC_DIR}/{basePath}/{params.category}/{params.pageId}'

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

    for idx, block in enumerate(blocks):
        mdx.handle_block(block)

    file = open(f'{postPath}/{params.fileName}', "w")
    file.write(mdx.text)


if __name__ == "__main__":
    convert()
