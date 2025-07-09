from src.block_enum import BlockType
from src.htmlnode import HTMLNode
from src.parentnode import ParentNode
from src.markdown_block_helpers import markdown_to_blocks, block_to_block_type
from src.helpers import text_to_textnodes, text_node_to_html_node

def markdown_to_html_node(markdown: str) -> HTMLNode:
    child_list = []
    text_node_list_tuple = []
    parent_tag = "div"

    # Split the document into blocks
    blocks = markdown_to_blocks(markdown)
    
    # For each block convert the string into a tuple. 
    # The 0th index is the block type and the 1st index is a list of text nodes in that block.
    for block in blocks:
        text_node_list_tuple.append((block_to_block_type(block), text_to_textnodes(block)))

    # For each node_list convert them into html nodes
    for text_node_tuple in text_node_list_tuple:
        html_node_list = []
        for text_node in text_node_tuple[1]:
            if text_node_tuple[0] == BlockType.CODE:
                
                html_node_list.append(text_node_to_html_node(text_node))
        # Add a parent list to the list of children with all newly converted HTMLNodes as children
        child_list.append(ParentNode(tag=text_node_tuple[0].value, children=html_node_list))

    # Return a ParentNode with all other ParentNodes as children
    return ParentNode(tag=parent_tag, children=child_list)