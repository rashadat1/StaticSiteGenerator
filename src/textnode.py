from enum import Enum
from typing import Optional

from leafnode import LeafNode


class TextType(Enum):
    """
    Enum for representing different types of inline text.

    Attributes:
        NORMAL_TEXT: Represents normal text.
        BOLD_TEXT: Represents bold text.
        ITALIC_TEXT: Represents italic text.
        CODE_TEXT: Represents text used as code.
        LINK_TEXT: Represents a hyperlink with anchor text.
        IMAGE_TEXT: Represents an image with alt text.
    """

    TEXT = 1
    BOLD = 2
    ITALIC = 3
    CODE = 4
    LINK = 5
    IMAGE = 6


class TextNode:
    """
    Represents a node of inline text with details about its type and associated URL if applicable.

    Attributes:
        text (str): The content of the text node.
        text_type (TextType): The type of the text node, specified as a member of the TextType enum.
        url (Optional[str]): The URL associated with the text (e.g., for a link or image). Defaults to None.
    """

    def __init__(self, text: str, text_type: TextType, url: Optional[str] = None):
        """
        Initializes a TextNode object.

        Args:
            text (str): The content of the text node.
            text_type (TextType): The type of the text node, specified as a member of the TextType enum.
            url (Optional[str]): The URL associated with the text (e.g., for a link or image). Defaults to None.
        """
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        """
        Compares two TextNode objects for equality.

        Args:
            other (object): The object to compare the current TextNode to.

        Returns:
            bool: True if all properties (text, text_type, and url) are equal; otherwise, False.
        """
        if (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        ):
            return True
        else:
            return False

    def __repr__(self):
        return f"TextNode({self.text},{self.text_type.value},{self.url})"


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    """
    Converts a TextNode to an HTMLNode (specifically a LeafNode).
    
    Args:
        text_node: The TextNode to convert
        
    Returns:
        LeafNode: A new LeafNode with properties based on the TextNode's type
        
    Raises:
        AssertionError: If URL is missing for LINK or IMAGE types
        ValueError: If the TextNode has an unsupported TextType
    """
    text_type = text_node.text_type
    match (text_type):
        case TextType.TEXT:
            return LeafNode(value=text_node.text)
        case TextType.BOLD:
            return LeafNode(value=text_node.text, tag="b")
        case TextType.ITALIC:
            return LeafNode(value=text_node.text, tag="i")
        case TextType.CODE:
            return LeafNode(value=text_node.text, tag="code")
        case TextType.LINK:
            assert text_node.url is not None
            return LeafNode(value=text_node.text, tag="a", props={"href": text_node.url})
        case TextType.IMAGE:
            assert text_node.url is not None
            return LeafNode(value="", tag="img", props={"src": text_node.url, "alt": text_node.text})

