import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import LeafNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_text_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node!", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_text_type_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_url_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
        self.assertEqual(repr(node), "TextNode(This is a text node, bold, https://www.boot.dev)")


class TestTextNodeToHtmlNode(unittest.TestCase):
    def test_normal_text_type_eq(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = LeafNode(None, "This is a text node")
        self.assertEqual(text_node_to_html_node(node), node2)

    def test_bold_text_type_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = LeafNode("b", "This is a text node")
        self.assertEqual(text_node_to_html_node(node), node2)

    def test_italic_text_type_eq(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = LeafNode("i", "This is a text node")
        self.assertEqual(text_node_to_html_node(node), node2)

    def test_code_text_type_eq(self):
        node = TextNode("This is a text node", TextType.CODE)
        node2 = LeafNode("code", "This is a text node")
        self.assertEqual(text_node_to_html_node(node), node2)

    def test_link_text_type_eq(self):
        node = TextNode("This is a text node", TextType.LINK, "https://www.boot.dev")
        node2 = LeafNode("a", "This is a text node", {"href": "https://www.boot.dev"})
        self.assertEqual(text_node_to_html_node(node), node2)

    def test_image_text_type_eq(self):
        node = TextNode("This is a text node", TextType.IMAGE, "https://www.boot.dev")
        node2 = LeafNode("img", "https://www.boot.dev", {"alt": "This is a text node"})
        self.assertEqual(text_node_to_html_node(node), node2)

    def test_unkown_text_type_exception(self):
        node = TextNode("This is a text node", None)
        self.assertRaises(ValueError, text_node_to_html_node, node)

if __name__ == "__main__":
    unittest.main()