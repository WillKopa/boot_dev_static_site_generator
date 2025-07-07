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

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type == TextType.TEXT:
            new_nodes.append(old_node)
        else:
            split_text = old_node.text.split(delimiter)
            if len(split_text) % 2 == 0:
                raise Exception(f"No closing {delimiter} found in {old_node.text}")
            for idx, text in enumerate(split_text):
                if idx % 2 == 1:
                    new_nodes.append(TextNode(text, text_type=text_type, url=old_node.url))
                else:
                    new_nodes.append(TextNode(text, text_type=TextType.TEXT))

    return new_nodes

