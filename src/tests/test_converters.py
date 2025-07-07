import unittest

from src.converters import text_node_to_html_node
from src.leafnode import LeafNode
from src.textnode import TextNode, TextType

PROPS_STRING = 'href="hello" target="world"'
PROPS = {"href": "hello", "target": "world"}
TAG = "a"
VALUE = "Hello World"
URL = "github.com"
INVALID_TYPE = "INVALID_TYPE"

class TestConverters(unittest.TestCase):
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
    

if __name__ == "__main__":
    unittest.main()
