import os
import pathlib
import re
import urllib.request
from os import path
from urllib.parse import unquote
import consts

import requests


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
