from enum import Enum

class TextType(Enum):
    BOLD = "BOLD"
    ITALIC = "ITALIC"
    CODE = "CODE"
    LINK = "LINK"
    IMAGE = "IMAGE"
    TEXT = "TEXT"


class TextNode():
    def __init__(self, text: str, text_type: "TextType", url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other_node: "TextNode") -> bool:
        return self.text == other_node.text and self.text_type == other_node.text_type and self.url == other_node.url

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
