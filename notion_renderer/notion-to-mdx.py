import os

from PyInquirer import print_json, prompt
from renderer import objectify_notion_blocks, objectify_notion_collection


def main():
    # start_prompt
    questions = [
        {
            "type": "input",
            "name": "targetPath",
            "message": "Where you want to generate MDX files?",
            "default": "./mdx",
        },
    ]
    answers = prompt(questions)
    targetPath = answers["targetPath"]

    # results1 = objectify_notion_collection(
    #     '7f03ff0043f4f1b5367552a37201efb3e815abf50eb7170db3df48f1ac4a69fc998e42fbdfcb0f57f57c296226f10d51c96f218ad27e1b6067c68fcd191f55bda1dced6b384f159b9184974eb3bb', 'https://www.notion.so/harbor/69c9e458364d4df4afa33118d4240f6e?v=32136518f6b544629d5a92cd979ccd2d', 'email,title,profileImage')
    # print('results1', results1)

    results2 = objectify_notion_blocks(
        "7f03ff0043f4f1b5367552a37201efb3e815abf50eb7170db3df48f1ac4a69fc998e42fbdfcb0f57f57c296226f10d51c96f218ad27e1b6067c68fcd191f55bda1dced6b384f159b9184974eb3bb",
        "fbbffdea4b544cde91243d79abf9712c",
    )
    print("results2", results2)

    text = """---
title: "%s"
---""" % (
        "My Notion Page"
    )
    text += "\n\n" + 'import * as System from "@harborschool/lighthouse"' + "\n\n"

    # for idx, block in enumerate(results2):
    #     print('block', block)
    #     if (block.type == 'text'):
    #         text += block.title

    if not os.path.exists(targetPath):
        os.makedirs(targetPath)

    file = open(targetPath + "/test" + ".mdx", "w")
    file.write(text)


if __name__ == "__main__":
    main()
