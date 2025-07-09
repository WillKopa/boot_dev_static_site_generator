import re

from src.textnode import TextNode, TextType
from src.htmlnode import HTMLNode
from src.leafnode import LeafNode

def text_node_to_html_node(text_node: TextNode) -> HTMLNode:
    if text_node.text_type not in TextType:
        raise Exception("Invalid TextNode type")
    
    tag = None
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

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_text = old_node.text.split(delimiter)
        if len(split_text) % 2 == 0:
            raise Exception(f"No closing {delimiter} found in {old_node.text}")
        for idx, text in enumerate(split_text):
            if text == "":
                continue
            elif idx % 2 == 1:
                new_nodes.append(TextNode(text, text_type=text_type))
            else:
                new_nodes.append(TextNode(text, text_type=TextType.TEXT))
    return new_nodes

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        images = extract_markdown_images(old_node.text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        text = old_node.text
        for image_tpl in images:
            new_text, text = text.split(f"![{image_tpl[0]}]({image_tpl[1]})", 1)
            if len(new_text) > 0:
                new_nodes.append(TextNode(new_text, TextType.TEXT))
            new_nodes.append(TextNode(image_tpl[0], TextType.IMAGE, url=image_tpl[1]))
    return new_nodes



def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        links = extract_markdown_links(old_node.text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        old_text = old_node.text
        for link_tpl in links:
            new_text, old_text = old_text.split(f"[{link_tpl[0]}]({link_tpl[1]})", 1)
            if new_text != "":
                new_nodes.append(TextNode(new_text, TextType.TEXT))
            new_nodes.append(TextNode(link_tpl[0], TextType.LINK, url=link_tpl[1]))
        if old_text != "":
            new_nodes.append(TextNode(old_text, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text: str) -> list[TextNode]:
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


def extract_markdown_images(text: str) -> list[tuple]:
    pattern = r"!\[(.*?)\]\((.*?)\)"
    return re.findall(pattern, text)

def extract_markdown_links(text: str) -> list[tuple]:
    pattern = r"(?<!!)\[(.*?)\]\((.*?)\)"
    return re.findall(pattern, text)
