import re

from src.block_enum import BlockType
from src.htmlnode import HTMLNode

def markdown_to_blocks(markdown: str) -> list[str]:
    """
    Takes a given markdown document and breaks it into a list of strings. 
    Each string is a markdown block
    """
    return [block.strip() for block in markdown.split("\n\n") if block.strip()]

def block_to_block_type(md: str) -> BlockType:
    HEADING_PATTERN = r"^#{1,6} .*"
    CODE_PATTERN = r"^`{3}[\s\S]*`{3}$"
    QUOTE_PATTERN = r"^(>.*(?:\n>.*)*)$"
    UNORDERED_LIST_PATTERN = r"^(- .*(?:\n- .*)*)$"
    ORDERED_LIST_PATTERN = r"\d\. "

    if re.findall(HEADING_PATTERN, md):
        return BlockType.HEADING
    elif re.findall(CODE_PATTERN, md):
        return BlockType.CODE
    elif re.findall(QUOTE_PATTERN, md):
        return BlockType.QUOTE
    elif re.findall(UNORDERED_LIST_PATTERN, md):
        return BlockType.UNORDERED_LIST
    else:
        ordered_list = [line for line in md.split("\n") if line]
        for idx, ol in enumerate(ordered_list):
            pattern_found = re.findall(ORDERED_LIST_PATTERN, ol)
            if not pattern_found or pattern_found[0][0] != f"{idx + 1}":
                return BlockType.PARAGRAPH
        return BlockType.ORDERED_LIST