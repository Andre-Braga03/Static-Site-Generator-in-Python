from enum import Enum
from htmlnode import ParentNode
from textnode import TextNode, TextType, text_to_textnodes, text_node_to_html_node
import os


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADER = "header"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = []
    for block in markdown.split("\n\n"):
        block = block.strip()
        if block:
            blocks.append(block)
    return blocks


def block_to_block_type(block: str) -> BlockType:
    lines = block.split("\n")

    if block.startswith("#"):
        hashes = 0
        for char in block:
            if char == "#":
                hashes += 1
            else:
                break
        if 1 <= hashes <= 6 and hashes < len(block) and block[hashes] == " ":
            return BlockType.HEADER

    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    if all(line.startswith(f"{i + 1}. ") for i, line in enumerate(lines)):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown: str) -> ParentNode:
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        children.append(block_to_html_node(block))
    return ParentNode("div", children)


def text_to_children(text: str) -> list:
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        children.append(text_node_to_html_node(text_node))
    return children


def paragraph_to_html_node(block: str) -> ParentNode:
    paragraph = " ".join(block.split("\n"))
    return ParentNode("p", text_to_children(paragraph))


def heading_to_html_node(block: str) -> ParentNode:
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    text = block[level + 1 :]
    return ParentNode(f"h{level}", text_to_children(text))


def code_to_html_node(block: str) -> ParentNode:
    text = block[3:-3].lstrip("\n")
    raw = TextNode(text, TextType.TEXT)
    code = ParentNode("code", [text_node_to_html_node(raw)])
    return ParentNode("pre", [code])


def quote_to_html_node(block: str) -> ParentNode:
    lines = []
    for line in block.split("\n"):
        lines.append(line.lstrip(">").strip())
    content = " ".join(lines)
    return ParentNode("blockquote", text_to_children(content))


def unordered_list_to_html_node(block: str) -> ParentNode:
    items = []
    for line in block.split("\n"):
        text = line[2:]
        items.append(ParentNode("li", text_to_children(text)))
    return ParentNode("ul", items)


def ordered_list_to_html_node(block: str) -> ParentNode:
    items = []
    for line in block.split("\n"):
        text = line[3:]
        items.append(ParentNode("li", text_to_children(text)))
    return ParentNode("ol", items)


def block_to_html_node(block: str) -> ParentNode:
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADER:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    if block_type == BlockType.UNORDERED_LIST:
        return unordered_list_to_html_node(block)
    if block_type == BlockType.ORDERED_LIST:
        return ordered_list_to_html_node(block)
    raise ValueError(f"invalid block type: {block_type}")


def extract_title(markdown: str) -> str:
    if not markdown.startswith("#"):
        raise ValueError("markdown does not start with a header")
    
    return markdown.split("\n")[0].strip("#").strip()

def generate_page(from_path: str, template_path: str, dest_path: str, basepath: str) -> None:
    print( f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as file:
        markdown = file.read()
    with open(template_path, "r") as file:
        templace = file.read()
    
    htmlString = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    page = (
        templace.replace("{{ Title }}", title)
        .replace("{{ Content }}", htmlString)
        .replace('href="/', f'href="{basepath}')
        .replace('src="/', f'src="{basepath}')
    )
    
    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path))
   
    with open(dest_path, "w") as dest:
        dest.write(page)

def generate_pages_recurvise(dir_path_content: str, template_path: str, dest_dir_path: str, basepath: str) -> None:
    for name in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content,name)
        dest_path = os.path.join(dest_dir_path,name)
        if os.path.isfile(from_path):
            if from_path.endswith(".md"):
                dest_path = dest_path.replace(".md", ".html")
                generate_page(from_path, template_path, dest_path, basepath)
        else:
            generate_pages_recurvise(from_path, template_path, dest_path, basepath)
