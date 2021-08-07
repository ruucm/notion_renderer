import os

from PyInquirer import print_json, prompt

from notion_renderer.renderer import objectify_notion_blocks
from utils import handleImage
import json
import getopt
import sys


class JsonPage:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


# code from https://stackoverflow.com/a/39894555/4047204
class MDX(object):
    def __init__(self):
        self.text = """---
title: "%s"
---\n""" % ("My Notion Page")

    def update_mdx(self, newText):
        self.text += newText

    def set_post_path(self, path):
        self.postPath = path

    def handle_block(self, block):
        if block.type == "header":
            self.update_mdx("# " + block.title)
        elif block.type == "sub_header":
            self.update_mdx("## " + block.title)
        elif block.type == "text":
            self.update_mdx(block.title)
        elif block.type == "image":
            self.update_mdx(
                f'\n\n{handleImage(block.source, self.postPath)}\n')
        elif block.type == "toggle":
            self.handle_toggle_block(block)
        elif block.type == "collection_view_page":
            rows = block.collection.get_rows()
            print('rows', rows)

        self.update_mdx("\n")  # add a newline

    def handle_toggle_block(self, block):
        properties = self.get_properties_from_title(block.title)
        self.update_mdx(
            f"<{properties.title}{properties.properties_string}>")

        # handle child blocks recursively
        toggleChildren = block.children
        for idx, childBlock in enumerate(toggleChildren):
            if (childBlock.type == "toggle"):
                self.handle_toggle_block(childBlock)
            else:
                self.handle_block(childBlock)
                if (idx + 1) < len(toggleChildren):
                    self.update_mdx("<br/>")

        self.update_mdx(f"</{properties.title}>")

    def get_properties_from_title(self, title):
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


def convert():

    argumentList = sys.argv[1:]
    params = JsonPage()

    if argumentList:
        print('argumentList', argumentList)
        setattr(params, 'targetPath', argumentList[0])
        setattr(params, 'fileName', argumentList[1])
        setattr(params, 'pageId', argumentList[2])
    else:
        # start_prompt
        questions = [
            {
                "type": "input",
                "name": "targetPath",
                "message": "Where you want to generate MDX files?",
                "default": "./mdx/posts",
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
    targetPath = params.targetPath
    postPath = f'{targetPath}/{params.pageId}'

    if not os.path.exists(targetPath):
        os.makedirs(targetPath)

    if not os.path.exists(postPath):
        os.makedirs(postPath)

    blocks = objectify_notion_blocks(
        "7f03ff0043f4f1b5367552a37201efb3e815abf50eb7170db3df48f1ac4a69fc998e42fbdfcb0f57f57c296226f10d51c96f218ad27e1b6067c68fcd191f55bda1dced6b384f159b9184974eb3bb",
        params.pageId,
    )

    # start generate MDX
    mdx = MDX()
    mdx.set_post_path(postPath)

    for idx, block in enumerate(blocks):
        mdx.handle_block(block)

    file = open(f'{postPath}/{params.fileName}', "w")
    file.write(mdx.text)


if __name__ == "__main__":
    convert()
