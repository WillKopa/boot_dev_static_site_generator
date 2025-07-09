import re

from block_enum import BlockType
from htmlnode import HTMLNode
from parentnode import ParentNode
from markdown_block_helpers import markdown_to_blocks, block_to_block_type
from helpers import text_to_textnodes, text_node_to_html_node, split_nodes_delimiter
from textnode import TextNode, TextType

def markdown_to_html_node(markdown: str) -> HTMLNode:
    child_list = []
    parent_tag = "div"

    blocks = markdown_to_blocks(markdown)

    for block in blocks:
        child_list.append(block_to_html(block))
    
    return ParentNode(tag=parent_tag, children=child_list)

def text_to_child_nodes(text: str) -> list[HTMLNode]:
    text_nodes = text_to_textnodes(text)
    children = []
    for node in text_nodes:
        html_node = text_node_to_html_node(node)
        children.append(html_node)
    return children

def block_to_html(block: str) -> HTMLNode:
    block_type = block_to_block_type(block)
    match block_type:
        case BlockType.CODE:
            return code_block_to_html(block)
        case BlockType.PARAGRAPH:
            return paragraph_to_html(block)
        case BlockType.HEADING:
            return heading_to_html(block)
        case BlockType.QUOTE:
            return quote_to_html(block)
        case BlockType.UNORDERED_LIST:
            return unordered_list_to_html(block)
        case BlockType.ORDERED_LIST:
            return ordered_list_to_html(block)
        
        
def code_block_to_html(block: str) -> HTMLNode:
    code_delim = "```"
    if block.startswith(code_delim) and block.endswith(code_delim):
        text = block.strip(code_delim)
        child_node = text_node_to_html_node(TextNode(text, TextType.TEXT))
        return ParentNode("pre", [ParentNode("code", [child_node])])
    else:
        raise ValueError("Code block not formatted correctly")

def paragraph_to_html(block: str)-> HTMLNode:
    children = text_to_child_nodes(" ".join(block.split("\n")))
    return ParentNode("p", children)

def heading_to_html(block: str) -> HTMLNode:
    head_level = 0
    for ch in block:
        if ch == "#":
            head_level += 1
        else:
            break
    children = text_to_child_nodes(block.lstrip("#").strip())
    return ParentNode(f"h{head_level}", children)

def quote_to_html(block: str) -> HTMLNode:
    lines = []
    for line in block.split("\n"):
        lines.append(line.lstrip(">").strip())
    children = text_to_child_nodes(" ".join(lines))
    return ParentNode("blockquote", children)

def unordered_list_to_html(block):
    children = []
    for line in block.split("\n"):
        text = line.lstrip("- ").lstrip("* ")
        child_node = text_to_child_nodes(text)
        children.append(ParentNode("li", child_node))
    return ParentNode("ul", children)

def ordered_list_to_html(block):
    children = []
    for line in block.split("\n"):
        text = line[3:]
        child_nodes = text_to_child_nodes(text)
        children.append(ParentNode("li", child_nodes))
    return ParentNode("ol", children)


def code_block_to_text_node(code_block: str):
    return split_nodes_delimiter([TextNode(code_block, TextType.TEXT)], delimiter="```", text_type=TextType.CODE)