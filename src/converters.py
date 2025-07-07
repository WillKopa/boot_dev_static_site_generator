from src.textnode import TextNode, TextType
from src.htmlnode import HTMLNode
from src.leafnode import LeafNode

def text_node_to_html_node(text_node: TextNode) -> HTMLNode:
    if text_node.text_type not in TextType:
        raise Exception("Invalid TextNode type")
    
    tag=None
    props = None

    match text_node.text_type: 
        case TextType.TEXT:
            pass
        case TextType.BOLD:
            tag = "b"
        case TextType.ITALIC:
            tag = "i"
        case TextType.CODE:
            tag = "code"
        case TextType.LINK:
            tag = "a" 
            props = {"href": text_node.url}
        case TextType.IMAGE:
            tag = "img"
            props = {"alt": text_node.text, "src": text_node.url}
            text_node.text = ""
    
    return LeafNode(tag=tag, value=text_node.text, props=props)