from enum import Enum
from htmlnode import LeafNode


class TextType(Enum):
    TEXT = "TEXT"
    BOLD = "BOLD"    
    ITALIC = "ITALIC"
    CODE = "CODE"
    LINK = "LINK"
    IMAGE = "IMAGE"
    






class TextNode:


    def __init__(self, text, text_type: TextType, url = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return False
        return self.text == other.text and self.url == other.url and self.text_type == other.text_type


    def __repr__(self):
        if self.url == None:
            return f'TextNode("{self.text}", {self.text_type})'
        return f'TextNode("{self.text}", {self.text_type}, {self.url})'



def text_node_to_html_node(text_node):
    match text_node.text_type:
        case text_node.text_type.TEXT:
            return LeafNode(tag=None, value=text_node.text)
        case text_node.text_type.BOLD:
            return LeafNode(tag="b",value=text_node.text)
        case text_node.text_type.ITALIC:
            return LeafNode(tag="i", value=text_node.text)
        case text_node.text_type.CODE:
            return LeafNode(tag="code", value=text_node.text)
        case text_node.text_type.LINK:
            return LeafNode(tag="a", value=text_node.text, props={"href":f"{text_node.url}"})
        case text_node.text_type.IMAGE:
            return LeafNode(tag="img", value="", props={"src":f"{text_node.url}", "alt":f"{text_node.text}"})
        case _:
            raise Exception("incorrect text_type")

    raise Exception("escaped from match")
