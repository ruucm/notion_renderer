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


def objectify_notion_blocks(token_v2, pageId, stringfy=False):
    """Convert a Notion Page to a Python object."""

    client = NotionClient(token_v2)
    page = client.get_block("https://www.notion.so/" + pageId)

    # results = []

    # for idx, block in enumerate(page.children):
    #     jsonPage = JsonPage()
    #     setattr(jsonPage, "type", block.type)
    #     if (
    #         block.type == "text"
    #         or block.type == "header"
    #         or block.type == "sub_header"
    #     ):
    #         setattr(jsonPage, "title", block.title)
    #     elif block.type == "image":
    #         setattr(jsonPage, "source", block.source)
    #     elif block.type == "toggle":
    #         setattr(jsonPage, "title", block.title)
    #         setattr(jsonPage, "children", block.children)
    #     elif block.type == "collection_view_page":
    #         setattr(jsonPage, "title", block.title)
    #         setattr(jsonPage, "collection", block.collection)

    #     if (stringfy):
    #         jsonStr = jsonPage.toJSON()
    #         results.append(jsonStr)
    #     else:
    #         results.append(jsonPage)

    return [page, page.children]
