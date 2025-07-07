import unittest

from src.parentnode import ParentNode
from src.leafnode import LeafNode

PROPS_STRING = 'href="hello" target="world"'
PROPS = {"href": "hello", "target": "world"}
TAG_1 = "a"
TAG_2 = "div"
VALUE_1 = "Hello World"
VALUE_2 = "Goodbye World"
CHILDREN = [LeafNode(tag=TAG_1, value=VALUE_1), LeafNode(tag=TAG_2, value=VALUE_2)]

class TestHTMLNode(unittest.TestCase):
    def test_to_html_no_tag(self):
        node = ParentNode(tag=TAG_1, children=CHILDREN)
        node.tag = None
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertEqual(str(context.exception), "ParentNode must have tag")
    
    def test_to_html_no_children(self):
        node = ParentNode(tag=TAG_1, children=CHILDREN)
        node.children = None
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertEqual(str(context.exception), "ParentNode must have children")


    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_grandchildren_with_props(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node], props=PROPS)
        self.assertEqual(
            parent_node.to_html(),
            '<div href="hello" target="world"><span><b>grandchild</b></span></div>',
        )


if __name__ == "__main__":
    unittest.main()
