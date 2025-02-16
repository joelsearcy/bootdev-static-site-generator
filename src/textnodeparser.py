import re
import os

from textnode import *
from htmlnode import *

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if not node.text or len(node.text) == 0:
            continue
        if isinstance(node, TextNode) and node.text_type == TextType.TEXT and delimiter and delimiter in node.text:
            parts = node.text.split(delimiter)
            if len(parts) % 2 == 0:
                raise Exception(f"Invalid markdown: no closing delimiter for {delimiter}")
            for i, part in enumerate(parts):
                if part == "":
                    continue
                elif i % 2 == 1:
                    new_nodes.append(TextNode(part, text_type))
                else:
                    new_nodes.append(TextNode(part, TextType.TEXT))
        else:
            new_nodes.append(node)
    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\]]*)\]\(([^\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\]]*)\]\(([^\)]*)\)", text)
    return matches

def format_markdown_url(format_string):
    def wrapper(text, url):
        return format_string.format(text, url)
    return wrapper

def split_nodes_with_url(old_nodes, extract_func, format_func, text_type):
    new_nodes = []
    for node in old_nodes:
        if isinstance(node, TextNode) and node.text_type == TextType.TEXT:
            urls = extract_func(node.text)
            remaining_text = node.text
            for url in urls:
                parts = remaining_text.split(format_func(url[0], url[1]), maxsplit=1)
                if parts[0] == "":
                    new_nodes.append(TextNode(url[0], text_type, url[1]))
                else:
                    new_nodes.append(TextNode(parts[0], TextType.TEXT))
                    new_nodes.append(TextNode(url[0], text_type, url[1]))
                remaining_text = parts[1]
            if remaining_text != "":
                new_nodes.append(TextNode(remaining_text, TextType.TEXT))
        else:
            new_nodes.append(node)
    return new_nodes

def split_nodes_images(old_nodes):
    return split_nodes_with_url(old_nodes, extract_markdown_images, format_markdown_url("![{}]({})"), TextType.IMAGE)

def split_nodes_links(old_nodes):
    return split_nodes_with_url(old_nodes, extract_markdown_links, format_markdown_url("[{}]({})"), TextType.LINK)

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_images(nodes)
    nodes = split_nodes_links(nodes)
    return nodes

def markdown_to_blocks(markdown):
    blocks = []
    for part in markdown.split("\n\n"):
        block = part.strip().strip("\n")
        if block != "":
            blocks.append(block)
    return blocks

def block_to_block_type(block):
    if re.match(r"^#{1,6} .*$", block):
        return "heading"
    if block.startswith("```") and block.endswith("```"):
        return "code"
    line_starts = [line.split(" ", 1)[0] for line in block.split("\n")]
    if all([prefix == ">" for prefix in line_starts]):
        return "quote"
    if all([prefix == "*" or prefix == "-" for prefix in line_starts]):
        return "unordered_list"
    if all([prefix == f"{i+1}." for i, prefix in enumerate(line_starts)]):
        return "ordered_list"
    return "paragraph"

def text_to_children(text):
    nodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in nodes]

def markdown_to_htmlnode(markdown):
    blocks = [(block_to_block_type(block), block) for block in markdown_to_blocks(markdown)]
    nodes = []
    for block_type, block in blocks:
        # print(f"block_type: {block_type}; block: {block}")
        tag = None
        text = None
        children = None

        if block_type == "heading":
            parts = block.split(" ", 1)
            tag = f"h{len(parts[0])}"
            text = parts[1]
            children = text_to_children(text)
        elif block_type == "code":
            tag = "pre"
            text = block[3:-3]
            children = [text_node_to_html_node(TextNode(text, TextType.CODE))]
        elif block_type == "quote":
            tag = "blockquote"
            text = "\n".join([line[2:] for line in block.split("\n")])
            children = text_to_children(text)
        elif block_type == "unordered_list":
            tag = "ul"
            children = [ParentNode("li", text_to_children(item[2:])) for item in block.split("\n")]
        elif block_type == "ordered_list":
            tag = "ol"
            children = [ParentNode("li", text_to_children(item.split(" ", 1)[1])) for item in block.split("\n")]
        else:
            tag = "p"
            children = text_to_children(block)
        if children:
            nodes.append(ParentNode(tag, children))
        parent = ParentNode("div", nodes)
    return parent

def extract_title(markdown):
    lines = markdown.split("\n")
    if len(lines) > 0 and lines[0].startswith("# "):
        return lines[0][2:].strip()
    raise Exception("No title found")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} usning {template_path}")

    with open(from_path, "r") as f:
        markdown = f.read()
    with open(template_path, "r") as f:
        template = f.read()

    page_title = extract_title(markdown)
    html_content = markdown_to_htmlnode(markdown).to_html()

    page_content = template.replace("{{ Title }}", page_title).replace("{{ Content }}", html_content)

    dest_dir = os.path.dirname(dest_path)
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    
    with open(dest_path, "w") as f:
        f.write(page_content)