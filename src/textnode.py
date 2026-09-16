from enum import Enum
import re
from htmlnode import LeafNode

class Bender(Enum):
	AIR_BENDER = "air"
	WATER_BENDER = "water"
	EARTH_BENDER = "earth"
	FIRE_BENDER = "fire"

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
	def __init__(self, text: str, text_type: TextType, url: str = None):
		self.text = text
		self.text_type = text_type
		self.url = url

	def __eq__(self, other) -> bool:
		return self.text == other.text and self.text_type == other.text_type and self.url == other.url
	
	def __repr__(self) -> str:
		return f"TextNode({self.text}, {self.text_type}, {self.url})"


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
	new_nodes: list[TextNode] = []
	for node in old_nodes:
		if node.text_type != TextType.TEXT:
			new_nodes.append(node)
			continue

		sections = node.text.split(delimiter)
		if len(sections) % 2 == 0:
			raise ValueError("Invalid Markdown syntax")

		for i, section in enumerate(sections):
			if section == "":
				continue
			if i % 2 == 0:
				new_nodes.append(TextNode(section, TextType.TEXT))
			else:
				new_nodes.append(TextNode(section, text_type))

	return new_nodes


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
	new_nodes: list[TextNode] = []
	for old_node in old_nodes:
		if old_node.text_type != TextType.TEXT:
			new_nodes.append(old_node)
			continue
		original_text = old_node.text
		images = extract_markdown_images(original_text)
		if not images:
			new_nodes.append(old_node)
			continue
		for alt, url in images:
			sections = original_text.split(f"![{alt}]({url})", 1)
			if len(sections) != 2:
				raise ValueError("Invalid Markdown syntax")
			if sections[0]:
				new_nodes.append(TextNode(sections[0], TextType.TEXT))
			new_nodes.append(TextNode(alt, TextType.IMAGE, url))
			original_text = sections[1]
		if original_text:
			new_nodes.append(TextNode(original_text, TextType.TEXT))
	return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
	new_nodes: list[TextNode] = []
	for old_node in old_nodes:
		if old_node.text_type != TextType.TEXT:
			new_nodes.append(old_node)
			continue
		original_text = old_node.text
		links = extract_markdown_links(original_text)
		if not links:
			new_nodes.append(old_node)
			continue
		for anchor, url in links:
			sections = original_text.split(f"[{anchor}]({url})", 1)
			if len(sections) != 2:
				raise ValueError("Invalid Markdown syntax")
			if sections[0]:
				new_nodes.append(TextNode(sections[0], TextType.TEXT))
			new_nodes.append(TextNode(anchor, TextType.LINK, url))
			original_text = sections[1]
		if original_text:
			new_nodes.append(TextNode(original_text, TextType.TEXT))
	return new_nodes


def text_to_textnodes(text: str) -> list[TextNode]:
	nodes = [TextNode(text, TextType.TEXT)]
	nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
	nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
	nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
	nodes = split_nodes_image(nodes)
	nodes = split_nodes_link(nodes)
	return nodes


def text_node_to_html_node(text_node: TextNode) -> LeafNode:

	match text_node.text_type:
		case TextType.TEXT:
			return LeafNode(None, text_node.text)
		case TextType.BOLD:
			return LeafNode("b", text_node.text)
		case TextType.ITALIC:
			return LeafNode("i", text_node.text)
		case TextType.CODE:
			return LeafNode("code", text_node.text)
		case TextType.LINK:
			return LeafNode("a", text_node.text, {"href": text_node.url})
		case TextType.IMAGE:
			return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
		case _:
			raise ValueError(f"Invalid text type: {text_node.text_type}")


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
	pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
	return re.findall(pattern, text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
	pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
	return re.findall(pattern, text)


