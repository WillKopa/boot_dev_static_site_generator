import unittest

from src.block_enum import BlockType
from src.markdown_block_helpers import markdown_to_blocks, block_to_block_type

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_too_many_new_lines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line





- This is a list
- with items
""" 
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_markdown_to_blocks_empty_markdown(self):
        md = ""
        result = markdown_to_blocks(md)
        self.assertEqual(result, [])    
        
    def test_markdown_to_blocks_new_line_markdown(self):
        md = "\n\n\n\n\n\n"
        result = markdown_to_blocks(md)
        self.assertEqual(result, [])

class TestBlockToBlock(unittest.TestCase):
    def test_block_to_block_heading(self):
        heading_text = " Heading Text"
        heading_block_1 = "# Heading Text"
        heading_block_6 = "#" * 6 + heading_text
        heading_block_7 = "#" * 7 + heading_text
        self.assertEqual(block_to_block_type(heading_block_1), BlockType.HEADING)
        self.assertEqual(block_to_block_type(heading_block_6), BlockType.HEADING)
        self.assertEqual(block_to_block_type(heading_block_7), BlockType.PARAGRAPH)

    def test_block_to_block_code(self):
        code_text = "```Code Block```"
        not_code_text_1 = "```Not Code Block"
        not_code_text_2 = "`Not Code Block```"
        not_code_text_3 = "``Not Code Block``"

        self.assertEqual(block_to_block_type(code_text), BlockType.CODE)
        self.assertEqual(block_to_block_type(not_code_text_1), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(not_code_text_2), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(not_code_text_3), BlockType.PARAGRAPH)

    def test_block_to_block_quote(self):
        quote_text = """>Quote 0
>Quote 1
> Quote 2
>  Quote 3
>>  Quote 4
"""
        invalid_quote = """
> Quote 1
Not a quote
> quote 2
"""
        self.assertEqual(block_to_block_type(quote_text), BlockType.QUOTE)
        self.assertEqual(block_to_block_type(invalid_quote), BlockType.PARAGRAPH)

    def test_block_to_block_ul(self):
        ul_text = """- step 1
- step2
-  step 3
"""
        not_ul_text = """- step1
not a step
- step 3
"""
        self.assertEqual(block_to_block_type(ul_text), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type(not_ul_text), BlockType.PARAGRAPH)

    def test_block_to_block_ol(self):
        ol_text = """1. step 1
2. step 2
3. step 3
"""

        not_ol_text = """1. step 1
not a step
2. step 3
"""
        not_ol_text_2 = """1. step1
2. step 2
2. step 2 again
"""

        not_ol_text_3 = """1. step 1
2.step 2
3. step 3
"""

        self.assertEqual(block_to_block_type(ol_text), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type(not_ol_text), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(not_ol_text_2), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(not_ol_text_3), BlockType.PARAGRAPH)