import unittest

from htmlnode import HTMLNode

PROPS_STRING = 'href="hello" target="world"'
PROPS = {"href": "hello", "target": "world"}
TAG = "<a"
VALUE = "Hello World"
CHILDREN = [HTMLNode(), HTMLNode()]

class TestHTMLNode(unittest.TestCase):

    def test_default(self):
        node = HTMLNode()
        self.assertEqual(node.props, None)
        self.assertEqual(node.tag, None)
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, None)
    
    def test_setting_all_values(self):
        node = HTMLNode(tag=TAG, value=VALUE, children=CHILDREN, props=PROPS)
        self.assertEqual(node.tag, TAG)
        self.assertEqual(node.value, VALUE)
        self.assertEqual(node.children, CHILDREN)
        self.assertEqual(node.props, PROPS)

    def test_props_to_html(self):
        node = HTMLNode(props=PROPS)
        self.assertEqual(node.props_to_html(), PROPS_STRING)

    def test_to_html_raises_error(self):
        node = HTMLNode()
        with self.assertRaises(NotImplementedError):
            node.to_html()


if __name__ == "__main__":
    unittest.main()
