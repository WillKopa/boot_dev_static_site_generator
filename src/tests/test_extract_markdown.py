import unittest
from src.extract_title import extract_title

class TestExtractMarkdownHeader(unittest.TestCase):
    def test_extract_markdown_header(self):
        md1 = "# Hello"
        md2 = "# Testing       "
        md3 = """
# This is a markdown title    

This should not be included
"""
        md4 = "## Invalid Title"
        md5 = "#       Valid Title     "
        result_1 = extract_title(md1)
        result_2 = extract_title(md2)
        result_3 = extract_title(md3)
        result_5 = extract_title(md5)
        self.assertEqual(result_1, "Hello")
        self.assertEqual(result_2, "Testing")
        self.assertEqual(result_3, "This is a markdown title")
        with self.assertRaises(Exception) as context:
            extract_title(md4)
        self.assertEqual(str(context.exception), "Invalid starting header in markdown file")

        self.assertEqual(result_5, "Valid Title")