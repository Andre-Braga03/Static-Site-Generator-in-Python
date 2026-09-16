from enum import Enum
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
		new_nodes : list[TextNode] = []
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
