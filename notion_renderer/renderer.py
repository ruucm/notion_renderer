import json

from .notion.client import NotionClient


class JsonPage:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


def objectify_notion_collection(token_v2, collectionUrl, properties):
    """Convert a Notion collection to a Python object."""

    client = NotionClient(token_v2=token_v2)
    cv = client.get_collection_view(collectionUrl)
    properties = properties.split(",")

    # collectionTitle = cv.collection.name
    collection_default = cv.default_query().execute()

    results = []

    for idx, page in enumerate(collection_default):
        jsonPage = JsonPage()

        for idx, property in enumerate(properties):
            setattr(jsonPage, property, getattr(page, property))

        jsonStr = jsonPage.toJSON()
        results.append(jsonStr)

    return results


def objectify_notion_blocks(token_v2, pageId):
    """Convert a Notion Page to a Python object."""

    client = NotionClient(token_v2)
    page = client.get_block("https://www.notion.so/" + pageId)

    results = []

    for idx, content in enumerate(page.children):
        jsonPage = JsonPage()
        print("content.type", content.type)
        setattr(jsonPage, "type", content.type)
        if (
            content.type == "text"
            or content.type == "header"
            or content.type == "sub_header"
        ):
            setattr(jsonPage, "title", content.title)
        elif content.type == "image":
            # TODO: Store image locally
            # imagePath = utils.handleNotionImageSource(idx, content.source)
            # setattr(jsonPage, 'imagePath', imagePath)
            setattr(jsonPage, "imagePath", content.source)

        jsonStr = jsonPage.toJSON()
        results.append(jsonStr)

    return results
