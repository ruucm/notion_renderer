import os

from PyInquirer import print_json, prompt

from notion_renderer.renderer import objectify_notion_blocks
from utils import handleImage


# code from https://stackoverflow.com/a/39894555/4047204
class MDX(object):
    def __init__(self):
        self.text = """---
title: "%s"
---\n""" % ("My Notion Page")

    def update_mdx(self, newText):
        self.text += newText

    def handle_toggle_block(self, block):
        toggleChildren = block.children
        self.update_mdx(f"<{block.title}>")
        for idx, childBlock in enumerate(toggleChildren):
            self.update_mdx(childBlock.title)
            if (idx + 1) < len(toggleChildren):
                self.update_mdx("<br/>")
        self.update_mdx(f"</{block.title}>")


def convert():
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

    # get the notion_blocks
    targetPath = answers["targetPath"]
    postPath = f'{targetPath}/{answers["pageId"]}'

    if not os.path.exists(targetPath):
        os.makedirs(targetPath)

    if not os.path.exists(postPath):
        os.makedirs(postPath)

    blocks = objectify_notion_blocks(
        "7f03ff0043f4f1b5367552a37201efb3e815abf50eb7170db3df48f1ac4a69fc998e42fbdfcb0f57f57c296226f10d51c96f218ad27e1b6067c68fcd191f55bda1dced6b384f159b9184974eb3bb",
        answers["pageId"],
    )

    # start generate MDX
    mdx = MDX()

    for idx, block in enumerate(blocks):
        if block.type == "header":
            mdx.update_mdx("# " + block.title)
        elif block.type == "sub_header":
            mdx.update_mdx("## " + block.title)
        elif block.type == "text":
            mdx.update_mdx(block.title)
        elif block.type == "image":
            mdx.update_mdx(handleImage(block.source, idx, postPath))
        elif block.type == "toggle":
            mdx.handle_toggle_block(block)

        mdx.update_mdx("\n")  # add a newline

    file = open(f'{postPath}/{answers["fileName"]}', "w")
    file.write(mdx.text)


if __name__ == "__main__":
    convert()
