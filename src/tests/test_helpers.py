import unittest

from src.helpers import text_node_to_html_node, split_nodes_delimiter
from src.textnode import TextNode, TextType

PROPS_STRING = 'href="hello" target="world"'
PROPS = {"href": "hello", "target": "world"}
TAG = "a"
VALUE = "Hello World"
URL = "github.com"
INVALID_TYPE = "INVALID_TYPE"

class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode(VALUE, TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, VALUE)

    def test_bold(self):
        node = TextNode(VALUE, TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, VALUE)

    def test_italic(self):
        node = TextNode(VALUE, TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, VALUE)

    def test_code(self):
        node = TextNode(VALUE, TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, VALUE)

    def test_link(self):
        node = TextNode(VALUE, TextType.LINK, url=URL)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, VALUE)
        self.assertEqual(html_node.props, {"href": URL})

    def test_image(self):
        node = TextNode(VALUE, TextType.IMAGE, url=URL)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"alt": VALUE, "src": URL})

    def test_invalid_text_type(self):
        node = TextNode(VALUE, INVALID_TYPE)
        with self.assertRaises(Exception) as context:
            text_node_to_html_node(node)

        self.assertEqual(str(context.exception), "Invalid TextNode type")

TEXT_ONLY = "This is a text node"
TEXT_MISSING_DELIMITER = "This is `missing a delimiter"
TEXT_WITH_DELIMITERS = "This `code block` has proper delimiters"
TEXT_WITH_MORE_DELIMITERS = "This `code block` has even `more` delimiters"
NODE_WITH_MORE_DELIMITERS = TextNode(TEXT_WITH_MORE_DELIMITERS, TextType.CODE)
NODE_MISSING_DELIMITER = TextNode(TEXT_MISSING_DELIMITER, TextType.CODE)
NODE_WITH_DELIMITERS = TextNode(TEXT_WITH_DELIMITERS, TextType.CODE)
NODE_TEXT_ONLY = TextNode(TEXT_ONLY, TextType.TEXT)
LIST_SINGLE_CODE_NODE = [NODE_WITH_DELIMITERS]
LIST_SINGLE_CODE_WITH_MORE_DELIMITERS_NODE = [NODE_WITH_MORE_DELIMITERS]
LIST_SINGLE_TEXT_NODE = [NODE_TEXT_ONLY]
LIST_MIXED_NODES = [NODE_WITH_DELIMITERS, NODE_TEXT_ONLY, NODE_WITH_MORE_DELIMITERS]
LIST_MISSING_DELIMITER = [NODE_MISSING_DELIMITER]
EXPECTED_DELIMITER_SPLIT = [
            TextNode("This ", TextType.TEXT), 
            TextNode("code block", TextType.CODE), 
            TextNode(" has proper delimiters", TextType.TEXT)
            ]
EXPECTED_MORE_DELIMITERS_SPLIT = [
            TextNode("This ", TextType.TEXT), 
            TextNode("code block", TextType.CODE), 
            TextNode(" has even ", TextType.TEXT),
            TextNode("more", TextType.CODE),
            TextNode(" delimiters", TextType.TEXT)
            ]
EXPECTED_MIXED_RESULT = EXPECTED_DELIMITER_SPLIT + [NODE_TEXT_ONLY] + EXPECTED_MORE_DELIMITERS_SPLIT

DELIMITER_CODE = "`"

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_with_only_text(self):
        result = split_nodes_delimiter(LIST_SINGLE_TEXT_NODE, DELIMITER_CODE, TextType.CODE)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], NODE_TEXT_ONLY)

    def test_split_with_delimiter(self):
        result = split_nodes_delimiter(LIST_SINGLE_CODE_NODE, DELIMITER_CODE, TextType.CODE)
        self.assertEqual(len(result), len(EXPECTED_DELIMITER_SPLIT))

        for i in range (len(result)):
            self.assertEqual(result[i], EXPECTED_DELIMITER_SPLIT[i])

    def test_split_with_more_delimiters(self):
        result = split_nodes_delimiter(LIST_SINGLE_CODE_WITH_MORE_DELIMITERS_NODE, DELIMITER_CODE, TextType.CODE)
        self.assertEqual(len(result), len(EXPECTED_MORE_DELIMITERS_SPLIT))

        for i in range (len(result)):
            self.assertEqual(result[i], EXPECTED_MORE_DELIMITERS_SPLIT[i])

    def test_split_with_mixed_nodes(self):
        result = split_nodes_delimiter(LIST_MIXED_NODES, DELIMITER_CODE, TextType.CODE)
        self.assertEqual(len(result), len(EXPECTED_MIXED_RESULT))

        for i in range (len(result)):
            self.assertEqual(result[i], EXPECTED_MIXED_RESULT[i])

    def test_split_with_missing_delimiter(self):
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter(LIST_MISSING_DELIMITER, DELIMITER_CODE, TextType.CODE)
        
        self.assertEqual(str(context.exception), f"No closing {DELIMITER_CODE} found in {TEXT_MISSING_DELIMITER}")

    

if __name__ == "__main__":
    unittest.main()
