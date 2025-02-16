import unittest

from textnodeparser import *
from textnode import *

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_nodes_delimiter_no_change_eq(self):
        nodes = [TextNode("This is text with no inline markdown", TextType.TEXT)]
        actual_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        expected_nodes = nodes
        self.assertEqual(f"{expected_nodes}", f"{actual_nodes}")

    def test_split_nodes_delimiter_bold_eq(self):
        nodes = [TextNode("This is text with **inline bold** markdown", TextType.TEXT)]
        actual_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        expected_nodes = [
            TextNode("This is text with ", TextType.TEXT),
            TextNode("inline bold", TextType.BOLD),
            TextNode(" markdown", TextType.TEXT)
        ]
        self.assertEqual(f"{expected_nodes}", f"{actual_nodes}")

    def test_split_nodes_delimiter_starts_with_bold_eq(self):
        nodes = [TextNode("**This is text with inline bold** markdown", TextType.TEXT)]
        actual_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        expected_nodes = [
            TextNode("This is text with inline bold", TextType.BOLD),
            TextNode(" markdown", TextType.TEXT)
        ]
        self.assertEqual(f"{expected_nodes}", f"{actual_nodes}")

    def test_split_nodes_delimiter_ends_with_bold_eq(self):
        nodes = [TextNode("This is text with **inline bold markdown**", TextType.TEXT)]
        actual_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        expected_nodes = [
            TextNode("This is text with ", TextType.TEXT),
            TextNode("inline bold markdown", TextType.BOLD)
        ]
        self.assertEqual(f"{expected_nodes}", f"{actual_nodes}")

    def test_split_nodes_delimiter_all_bold_eq(self):
        nodes = [TextNode("**This is text with inline bold markdown**", TextType.TEXT)]
        actual_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        expected_nodes = [
            TextNode("This is text with inline bold markdown", TextType.BOLD)
        ]
        self.assertEqual(f"{expected_nodes}", f"{actual_nodes}")

    def test_split_nodes_delimiter_italic_eq(self):
        nodes = [TextNode("This is text with *inline italic* markdown", TextType.TEXT)]
        actual_nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
        expected_nodes = [
            TextNode("This is text with ", TextType.TEXT),
            TextNode("inline italic", TextType.ITALIC),
            TextNode(" markdown", TextType.TEXT)
        ]
        self.assertEqual(f"{expected_nodes}", f"{actual_nodes}")

    def test_split_nodes_delimiter_code_eq(self):
        nodes = [TextNode("This is text with `inline code` markdown", TextType.TEXT)]
        actual_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        expected_nodes = [
            TextNode("This is text with ", TextType.TEXT),
            TextNode("inline code", TextType.CODE),
            TextNode(" markdown", TextType.TEXT)
        ]
        self.assertEqual(f"{expected_nodes}", f"{actual_nodes}")

class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_markdown_images_no_images_eq(self):
        text = "This is text with no images"
        actual_images = extract_markdown_images(text)
        expected_images = []
        self.assertEqual(f"{expected_images}", f"{actual_images}")

    def test_extract_markdown_images_one_image_eq(self):
        text = "This is text with an ![image](https://www.boot.dev)"
        actual_images = extract_markdown_images(text)
        expected_images = [("image", "https://www.boot.dev")]
        self.assertEqual(f"{expected_images}", f"{actual_images}")

    def test_extract_markdown_images_two_images_eq(self):
        text = "This is text with an ![image](https://www.boot.dev) and another ![image](https://www.boot.dev)"
        actual_images = extract_markdown_images(text)
        expected_images = [("image", "https://www.boot.dev"), ("image", "https://www.boot.dev")]
        self.assertEqual(f"{expected_images}", f"{actual_images}")

    def test_extract_markdown_images_no_alt_text_eq(self):
        text = "This is text with an ![](https://www.boot.dev)"
        actual_images = extract_markdown_images(text)
        expected_images = [("", "https://www.boot.dev")]
        self.assertEqual(f"{expected_images}", f"{actual_images}")

class TestExtractMarkdownLinks(unittest.TestCase):
    def test_extract_markdown_links_no_links_eq(self):
        text = "This is text with no links"
        actual_links = extract_markdown_links(text)
        expected_links = []
        self.assertEqual(f"{expected_links}", f"{actual_links}")

    def test_extract_markdown_links_one_link_eq(self):
        text = "This is text with a [link](https://www.boot.dev)"
        actual_links = extract_markdown_links(text)
        expected_links = [("link", "https://www.boot.dev")]
        self.assertEqual(f"{expected_links}", f"{actual_links}")

    def test_extract_markdown_links_two_links_eq(self):
        text = "This is text with a [link](https://www.boot.dev) and another [link](https://www.boot.dev)"
        actual_links = extract_markdown_links(text)
        expected_links = [("link", "https://www.boot.dev"), ("link", "https://www.boot.dev")]
        self.assertEqual(f"{expected_links}", f"{actual_links}")

    def test_extract_markdown_links_no_alt_text_eq(self):
        text = "This is text with a [](https://www.boot.dev)"
        actual_links = extract_markdown_links(text)
        expected_links = [("", "https://www.boot.dev")]
        self.assertEqual(f"{expected_links}", f"{actual_links}")

class TestSplitNodesImages(unittest.TestCase):
    def test_split_nodes_images_no_images_eq(self):
        nodes = [TextNode("This is text with no images", TextType.TEXT)]
        actual_nodes = split_nodes_images(nodes)
        expected_nodes = nodes
        self.assertEqual(f"{expected_nodes}", f"{actual_nodes}")

    def test_split_nodes_images_one_image_eq(self):
        nodes = [TextNode("This is text with an ![image](https://www.boot.dev)", TextType.TEXT)]
        actual_nodes = split_nodes_images(nodes)
        expected_nodes = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://www.boot.dev")
        ]
        self.assertEqual(f"{expected_nodes}", f"{actual_nodes}")

    def test_split_nodes_images_two_images_eq(self):
        nodes = [TextNode("This is text with an ![image](https://www.boot.dev) and another ![image](https://www.boot.dev)", TextType.TEXT)]
        actual_nodes = split_nodes_images(nodes)
        expected_nodes = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://www.boot.dev"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://www.boot.dev")
        ]
        self.assertEqual(f"{expected_nodes}", f"{actual_nodes}")

    def test_split_nodes_images_no_alt_text_eq(self):
        nodes = [TextNode("This is text with an ![](https://www.boot.dev)", TextType.TEXT)]
        actual_nodes = split_nodes_images(nodes)
        expected_nodes = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("", TextType.IMAGE, "https://www.boot.dev")
        ]
        self.assertEqual(f"{expected_nodes}", f"{actual_nodes}")

class TestSplitNodesLinks(unittest.TestCase):
    def test_split_nodes_links_no_links_eq(self):
        nodes = [TextNode("This is text with no links", TextType.TEXT)]
        actual_nodes = split_nodes_links(nodes)
        expected_nodes = nodes
        self.assertEqual(f"{expected_nodes}", f"{actual_nodes}")

    def test_split_nodes_links_one_link_eq(self):
        nodes = [TextNode("This is text with a [link](https://www.boot.dev)", TextType.TEXT)]
        actual_nodes = split_nodes_links(nodes)
        expected_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://www.boot.dev")
        ]
        self.assertEqual(f"{expected_nodes}", f"{actual_nodes}")

    def test_split_nodes_links_two_links_eq(self):
        nodes = [TextNode("This is text with a [link](https://www.boot.dev) and another [link](https://www.boot.dev)", TextType.TEXT)]
        actual_nodes = split_nodes_links(nodes)
        expected_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://www.boot.dev")
        ]
        self.assertEqual(f"{expected_nodes}", f"{actual_nodes}")

    def test_split_nodes_links_no_alt_text_eq(self):
        nodes = [TextNode("This is text with a [](https://www.boot.dev)", TextType.TEXT)]
        actual_nodes = split_nodes_links(nodes)
        expected_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("", TextType.LINK, "https://www.boot.dev")
        ]
        self.assertEqual(f"{expected_nodes}", f"{actual_nodes}")

class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_text_nodes_no_markdown_eq(self):
        text = "This is text with no markdown"
        actual_nodes = text_to_textnodes(text)
        expected_nodes = [TextNode("This is text with no markdown", TextType.TEXT)]
        self.assertEqual(f"{expected_nodes}", f"{actual_nodes}")

    def test_text_to_text_nodes_bold_eq(self):
        text = "This is text with **bold** markdown"
        actual_nodes = text_to_textnodes(text)
        expected_nodes = [
            TextNode("This is text with ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" markdown", TextType.TEXT)
        ]
        self.assertEqual(f"{expected_nodes}", f"{actual_nodes}")

    def test_text_to_text_nodes_italic_eq(self):
        text = "This is text with *italic* markdown"
        actual_nodes = text_to_textnodes(text)
        expected_nodes = [
            TextNode("This is text with ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" markdown", TextType.TEXT)
        ]
        self.assertEqual(f"{expected_nodes}", f"{actual_nodes}")

    def test_text_to_text_nodes_code_eq(self):
        text = "This is text with `code` markdown"
        actual_nodes = text_to_textnodes(text)
        expected_nodes = [
            TextNode("This is text with ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" markdown", TextType.TEXT)
        ]
        self.assertEqual(f"{expected_nodes}", f"{actual_nodes}")

    def test_text_to_text_nodes_link_eq(self):
        text = "This is text with a [link](https://www.boot.dev)"
        actual_nodes = text_to_textnodes(text)
        expected_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://www.boot.dev")
        ]
        self.assertEqual(f"{expected_nodes}", f"{actual_nodes}")

    def test_text_to_text_nodes_image_eq(self):
        text = "This is text with an ![image](https://www.boot.dev)"
        actual_nodes = text_to_textnodes(text)
        expected_nodes = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://www.boot.dev")
        ]
        self.assertEqual(f"{expected_nodes}", f"{actual_nodes}")

    def test_text_to_text_nodes_all_markdown_eq(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        actual_nodes = text_to_textnodes(text)
        expected_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev")
        ]
        self.assertEqual(f"{expected_nodes}", f"{actual_nodes}")

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks_eq(self):
        text = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item"""
        actual_blocks = markdown_to_blocks(text)
        expected_blocks = [
            """# This is a heading""",
            """This is a paragraph of text. It has some **bold** and *italic* words inside of it.""",
            """* This is the first list item in a list block
* This is a list item
* This is another list item"""
        ]
        self.assertEqual(f"{expected_blocks}", f"{actual_blocks}")

    def test_markdown_to_blocks_strip_eq(self):
        text = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.


* This is the first list item in a list block   
* This is a list item
* This is another list item     


"""
        actual_blocks = markdown_to_blocks(text)
        expected_blocks = [
            """# This is a heading""",
            """This is a paragraph of text. It has some **bold** and *italic* words inside of it.""",
            """* This is the first list item in a list block   
* This is a list item
* This is another list item"""
        ]
        self.assertEqual(f"{expected_blocks}", f"{actual_blocks}")

class TestBlockToBlockType(unittest.TestCase):
    def test_block_to_block_type_heading_eq(self):
        block = "# This is a heading"
        actual_block_type = block_to_block_type(block)
        expected_block_type = "heading"
        self.assertEqual(expected_block_type, actual_block_type)

    def test_block_to_block_type_code_eq(self):
        block = """```python
print("Hello, World!")
```"""
        actual_block_type = block_to_block_type(block)
        expected_block_type = "code"
        self.assertEqual(expected_block_type, actual_block_type)

    def test_block_to_block_type_quote_eq(self):
        block = "> This is a quote"
        actual_block_type = block_to_block_type(block)
        expected_block_type = "quote"
        self.assertEqual(expected_block_type, actual_block_type)

    def test_block_to_block_type_unordered_list_star_eq(self):
        block = """* first list item
* second list item
* third list item"""
        actual_block_type = block_to_block_type(block)
        expected_block_type = "unordered_list"
        self.assertEqual(expected_block_type, actual_block_type)

    def test_block_to_block_type_unordered_list_dash_eq(self):
        block = """- first list item
- second list item
- third list item"""
        actual_block_type = block_to_block_type(block)
        expected_block_type = "unordered_list"
        self.assertEqual(expected_block_type, actual_block_type)

    def test_block_to_block_type_ordered_list_eq(self):
        block = """1. first list item
2. second list item
3. third list item"""
        actual_block_type = block_to_block_type(block)
        expected_block_type = "ordered_list"
        self.assertEqual(expected_block_type, actual_block_type)

    def test_block_to_block_type_paragraph_eq(self):
        block = "This is a paragraph of text. Blah blah blah."
        actual_block_type = block_to_block_type(block)
        expected_block_type = "paragraph"
        self.assertEqual(expected_block_type, actual_block_type)

class TestMarkdownToHtmlNodes(unittest.TestCase):
    def test_text_to_html_nodes_eq(self):
        text = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it. ![This is an image](https://www.boot.dev)

[This is a link](https://www.boot.dev)

```python
print("This is a code block")
```

* This is the first list item in a list block   
* This is a list item
* This is another list item

- This is the first list item in a list block   
- This is a list item
- This is another list item

1. This is the first list item in a list block   
2. This is a list item
3. This is another list item

> This is a quote block line 1.
> This is a quote block line 2.

"""
        actual_html = markdown_to_htmlnode(text).to_html()
        expected_html = """<div><h1>This is a heading</h1><p>This is a paragraph of text. It has some <b>bold</b> and <i>italic</i> words inside of it. <img src="https://www.boot.dev" alt="This is an image"></p><p><a href="https://www.boot.dev">This is a link</a></p><pre><code>python
print("This is a code block")
</code></pre><ul><li>This is the first list item in a list block   </li><li>This is a list item</li><li>This is another list item</li></ul><ul><li>This is the first list item in a list block   </li><li>This is a list item</li><li>This is another list item</li></ul><ol><li>This is the first list item in a list block   </li><li>This is a list item</li><li>This is another list item</li></ol><blockquote>This is a quote block line 1.
This is a quote block line 2.</blockquote></div>"""
        self.assertEqual(f"{expected_html}", f"{actual_html}")

class TestExtractTitle(unittest.TestCase):
    def test_extract_title_eq(self):
        text = """# This is a heading"""
        actual_title = extract_title(text)
        expected_title = "This is a heading"
        self.assertEqual(expected_title, actual_title)

    def test_extract_title_eq(self):
        text = """# This is a heading
        
        # This is also a heading"""
        actual_title = extract_title(text)
        expected_title = "This is a heading"
        self.assertEqual(expected_title, actual_title)

    def test_extract_title_no_title_exception(self):
        text = """This is a paragraph of text."""
        self.assertRaises(Exception, extract_title, text)

if __name__ == "__main__":
    unittest.main()