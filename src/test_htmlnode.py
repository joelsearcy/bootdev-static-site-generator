import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode(tag="p", value="Hello, World!")
        node2 = HTMLNode(tag="p", value="Hello, World!")
        self.assertEqual(repr(node), repr(node2))

    def test_tag_not_eq(self):
        node = HTMLNode(tag="p", value="Hello, World!")
        node2 = HTMLNode(tag="b", value="Hello, World!")
        self.assertNotEqual(repr(node), repr(node2))

    def test_value_not_eq(self):
        node = HTMLNode(tag="p", value="Hello, World!")
        node2 = HTMLNode(tag="p", value="Hello, World!!")
        self.assertNotEqual(repr(node), repr(node2))

    def test_props_to_html_eq(self):
        node = HTMLNode(props={"href": "https://www.boot.dev", "target": "_blank"})
        compare_to_value = ' href="https://www.boot.dev" target="_blank"'
        self.assertEqual(node.props_to_html(), compare_to_value)

class TestLeafNode(unittest.TestCase):
    def test_eq(self):
        node = LeafNode("p", "Hello, World!")
        node2 = LeafNode("p", "Hello, World!")
        self.assertEqual(repr(node), repr(node2))

    def test_tag_not_eq(self):
        node = LeafNode("p", "Hello, World!")
        node2 = LeafNode("b", "Hello, World!")
        self.assertNotEqual(repr(node), repr(node2))

    def test_value_not_eq(self):
        node = LeafNode("p", "Hello, World!")
        node2 = LeafNode("p", "Hello, World!!")
        self.assertNotEqual(repr(node), repr(node2))

    def test_props_to_html_eq(self):
        node = LeafNode(None, None, props={"href": "https://www.boot.dev", "target": "_blank"})
        compare_to_value = ' href="https://www.boot.dev" target="_blank"'
        self.assertEqual(node.props_to_html(), compare_to_value)

    def test_to_html_with_tag_eq(self):
        node = LeafNode("a", "boot.dev", {"href": "https://www.boot.dev", "target": "_blank"})
        compare_to_value = '<a href="https://www.boot.dev" target="_blank">boot.dev</a>'
        self.assertEqual(node.to_html(), compare_to_value)

    def test_to_html_without_tag_eq(self):
        node = LeafNode(None, "boot.dev", {"href": "https://www.boot.dev", "target": "_blank"})
        compare_to_value = "boot.dev"
        self.assertEqual(node.to_html(), compare_to_value)

    def test_to_html_without_value_exception(self):
        node = LeafNode(None, None)
        self.assertRaises(ValueError, node.to_html)

class TestParentNode(unittest.TestCase):
    def test_eq(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        node2 = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(repr(node), repr(node2))

    def test_tag_not_eq(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        node2 = ParentNode(
            "div",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertNotEqual(repr(node), repr(node2))

    def test_child_not_eq(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        node2 = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text!"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertNotEqual(repr(node), repr(node2))

    def test_to_html_eq(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
            {"class": "text"},
        )
        compare_to_value = '<p class="text"><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>'
        self.assertEqual(node.to_html(), compare_to_value)

    def test_to_html_without_tag_exception(self):
        node = ParentNode(None, [LeafNode(None, None)])
        self.assertRaises(ValueError, node.to_html)

    def test_to_html_without_children_exception(self):
        node = ParentNode("p", None)
        self.assertRaises(ValueError, node.to_html)


if __name__ == "__main__":
    unittest.main()