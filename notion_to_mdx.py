import os

from PyInquirer import print_json, prompt

from notion_renderer.renderer import objectify_notion_blocks
from utils import handleImage


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
            "name": "pageId",
            "message": "pageId",
        },
    ]
    answers = prompt(questions)

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

    text = """---
title: "%s"
---""" % (
        "My Notion Page"
    )
    # text += "\n\n" + 'import * as System from "@harborschool/lighthouse"' + "\n\n"

    for idx, block in enumerate(blocks):
        if block.type == "header":
            text += "# " + block.title
        elif block.type == "sub_header":
            text += "## " + block.title
        elif block.type == "text":
            text += block.title
        elif block.type == "image":
            text += handleImage(block.source, idx, postPath)
        text += "\n"

    file = open(f'{postPath}/index.mdx', "w")
    file.write(text)


if __name__ == "__main__":
    convert()
