import os
import shutil

from textnode import TextNode, TextType
from htmlnode import LeafNode, ParentNode
from textnodeparser import *

def copy_files(src, dest):
    if os.path.exists(dest):
        print(f"Removing {dest}")
        shutil.rmtree(dest)
    if not os.path.exists(dest):
        print(f"Creating {dest}")
        os.mkdir(dest)

    for item in os.listdir(src):
        src_item = os.path.join(src, item)
        dest_item = os.path.join(dest, item)

        if os.path.isdir(src_item):
            print(f"Copying directory {src_item} to {dest_item}")
            copy_files(src_item, dest_item)
        else:
            print(f"Copying file {src_item} to {dest_item}")
            shutil.copy(src_item, dest_item)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for item in os.listdir(dir_path_content):
        item_path = os.path.join(dir_path_content, item)
        if os.path.isdir(item_path):
            dest_path = os.path.join(dest_dir_path, item)
            generate_pages_recursive(item_path, template_path, dest_path)
        else:
            if item.endswith(".md"):
                dest_path = os.path.join(dest_dir_path, item[:-3] + ".html")
                generate_page(item_path, template_path, dest_path)

def main():
    copy_files("./static", "./public")
    generate_pages_recursive("./content", "./template.html", "./public")


if __name__ == "__main__":
    main()