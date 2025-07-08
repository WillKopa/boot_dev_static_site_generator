import unittest

from src.helpers import (
    text_node_to_html_node, 
    split_nodes_delimiter, 
    extract_markdown_images, 
    extract_markdown_links, 
    split_nodes_image, 
    split_nodes_link,
    text_to_textnodes
)
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
NODE_WITH_MORE_DELIMITERS = TextNode(TEXT_WITH_MORE_DELIMITERS, TextType.TEXT)
NODE_MISSING_DELIMITER = TextNode(TEXT_MISSING_DELIMITER, TextType.TEXT)
NODE_WITH_DELIMITERS = TextNode(TEXT_WITH_DELIMITERS, TextType.TEXT)
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

MATCH_1_TEXT = "rick roll"
MATCH_1_SRC = "https://i.imgur.com/aKaOqIh.gif"
MATCH_2_TEXT = "obi wan"
MATCH_2_SRC = "https://i.imgur.com/fJRm4Vk.jpeg"
IMAGE_TEXT_WITH_MATCH = f"This is text with a ![{MATCH_1_TEXT}]({MATCH_1_SRC}) and ![{MATCH_2_TEXT}]({MATCH_2_SRC})"
LINK_TEXT_WITH_MATCH = f"This is text with a [{MATCH_1_TEXT}]({MATCH_1_SRC}) and [{MATCH_2_TEXT}]({MATCH_2_SRC})"
class TestExtractMarkDownImages(unittest.TestCase):
    def test_extract_markdown_images(self):
        expected_result = [(MATCH_1_TEXT, MATCH_1_SRC), (MATCH_2_TEXT, MATCH_2_SRC)]
        result = extract_markdown_images(IMAGE_TEXT_WITH_MATCH)
        self.assertEqual(result, expected_result)

    def test_extract_does_not_extract_links(self):
        result = extract_markdown_images(LINK_TEXT_WITH_MATCH)
        self.assertEqual(len(result), 0)

class TestExtractMarkdownLinks(unittest.TestCase):
    def test_extract_markdown_links(self):
        expected_result = [(MATCH_1_TEXT, MATCH_1_SRC), (MATCH_2_TEXT, MATCH_2_SRC)]
        result = extract_markdown_links(LINK_TEXT_WITH_MATCH)
        self.assertEqual(result, expected_result)

    def test_extract_does_not_extract_images(self):
        result = extract_markdown_links(IMAGE_TEXT_WITH_MATCH)
        self.assertEqual(len(result), 0)



class TestSplitNodesImage(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

class TestSplitNodesLink(unittest.TestCase):
    def test_split_links(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

class TestTestTextToTextNodes(unittest.TestCase):
    def test_text_to_text_nodes(self):
        text ="This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected_result = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        result = text_to_textnodes(text)
        self.assertEqual(result, expected_result)


if __name__ == "__main__":
    unittest.main()


