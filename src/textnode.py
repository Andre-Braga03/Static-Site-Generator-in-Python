from enum import Enum

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