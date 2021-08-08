import os
import pathlib
import re
import urllib.request
from os import path
from urllib.parse import unquote
import consts
import json

import requests


class JsonPage:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


def handleImage(source, postPath):
    url = unquote(source)

    for filename in re.findall(r"/([^/]+\.(?:jpg|jpeg|gif|png))", url):
        download(postPath, f"{postPath}/{filename}", url)
        return f"![{filename}](./{filename})"


def handleVideo(source, staticPath, width):
    url = unquote(source)

    for filename in re.findall(r"/([^/]+\.(?:mov|mp4))", url):
        download(staticPath, f"{staticPath}/{filename}", url)
        return f'<video src="{f"{staticPath}/{filename}".replace(consts.STATIC_DIR, "")}" width="{width}" />'


def getFileExtension(fileName):
    return os.path.splitext(fileName)[1]


def checkNeedDownload(existingFilePath, newSource):
    # check existing file
    if path.exists(existingFilePath):
        existingVidFileSize = os.path.getsize(existingFilePath)
    else:
        existingVidFileSize = 0
    # check the new file
    with urllib.request.urlopen(newSource) as site:
        meta = site.info()
    newVidFileSize = int(meta["Content-Length"])
    if existingVidFileSize != newVidFileSize:
        print("🔻 need to download!")
        print("existingFilePath", existingFilePath)
        return True
    else:
        return False


def download(base, filePath, source):
    if source != None and checkNeedDownload(filePath, source):
        try:
            os.mkdir(base)
        except:
            pass
        # download
        file_data = requests.get(source).content
        with open(filePath, "wb") as handler:
            handler.write(file_data)


def shouldShrink(column):
    result = False
    for idx, childBlock in enumerate(column.children):
        if childBlock.type == "text":  # if column has a text, it shouldn't be shrinked.
            result = True

    return result


def get_properties_from_toggle(title):
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


def getPureTitle(title):
    s_without_parens = re.sub('\(.+?\)', '', title)
    text_in_brackets = re.findall('{(.+?)}', s_without_parens)
    jsonStr = f'{{{text_in_brackets[0]}}}'

    pure_title = title.replace(f' {jsonStr}', '')

    return pure_title


def getJsxProperties(title):
    s_without_parens = re.sub('\(.+?\)', '', title)
    text_in_brackets = re.findall('{(.+?)}', s_without_parens)
    jsonStr = f'{{{text_in_brackets[0]}}}'
    print('jsonStr', jsonStr)

    pure_title = title.replace(f' {jsonStr}', '')

    propertiesDict = stringJsonToDict(jsonStr)

    return propertiesDictToJsx(propertiesDict)


def stringJsonToDict(jsonString):
    return json.loads(jsonString)


def propertiesDictToJsx(propertiesDict):
    result = ""
    for index, (key, value) in enumerate(propertiesDict.items()):
        result += f'{key}="{value}"'
        if (index < len(propertiesDict) - 1):
            result += " "
    return result
