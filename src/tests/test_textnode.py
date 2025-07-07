import unittest

from src.textnode import TextNode, TextType

TEXT = "This is a text node"
class TestTextNode(unittest.TestCase):

    def test_eq(self):
        node = TextNode(TEXT, TextType.BOLD)
        node2 = TextNode(TEXT, TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_different_url(self):
        node = TextNode(TEXT, TextType.BOLD)
        node2 = TextNode(TEXT, TextType.BOLD, url="URL")
        self.assertNotEqual(node, node2)

    def test_eq_different_text(self):
        node = TextNode(TEXT, TextType.BOLD)
        node2 = TextNode("This", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_eq_different_font(self):
        node = TextNode(TEXT, TextType.BOLD)
        node2 = TextNode(TEXT, TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_eq_with_url(self):
        node = TextNode(TEXT, TextType.LINK, url="URL")
        node2 = TextNode(TEXT, TextType.LINK, url="URL")
        self.assertEqual(node, node2)



if __name__ == "__main__":
    unittest.main()
