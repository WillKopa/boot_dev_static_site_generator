import unittest

from src.leafnode import LeafNode

PROPS_STRING = 'href="hello" target="world"'
PROPS = {"href": "hello", "target": "world"}
TAG = "a"
VALUE = "Hello World"

class TestLeafNode(unittest.TestCase):

    def test_default(self):
        node = LeafNode(tag=TAG, value=VALUE)
        self.assertEqual(node.props, None)
        self.assertEqual(node.tag, TAG)
        self.assertEqual(node.value, VALUE)
    
    def test_setting_all_values(self):
        node = LeafNode(tag=TAG, value=VALUE, props=PROPS)
        self.assertEqual(node.tag, TAG)
        self.assertEqual(node.value, VALUE)
        self.assertEqual(node.props, PROPS)

    def test_props_to_html(self):
        node = LeafNode(value=VALUE, tag=TAG, props=PROPS)
        self.assertEqual(node.props_to_html(), PROPS_STRING)

    def test_to_html_raises_error(self):
        node = LeafNode(value=VALUE, tag=TAG)
        node.value = None
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_with_no_props_no_tag(self):
        node = LeafNode(tag=None, value=VALUE)
        result = node.to_html()
        self.assertEqual(result, VALUE)
    
    def test_to_html_no_props(self):
        node = LeafNode(value=VALUE, tag=TAG)
        result = node.to_html()
        expected = f"<{TAG}>{VALUE}</{TAG}>"
        self.assertEqual(result, expected)

    def test_to_html_with_props(self):
        node = LeafNode(value=VALUE, tag=TAG, props=PROPS)
        result = node.to_html()
        keys = list(PROPS.keys())
        expected = f'<{TAG} {keys[0]}="{PROPS[keys[0]]}" {keys[1]}="{PROPS[keys[1]]}">{VALUE}</{TAG}>'
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
