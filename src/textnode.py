from enum import Enum
from typing import Optional


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

    NORMAL_TEXT = 1
    BOLD_TEXT = 2
    ITALIC_TEXT = 3
    CODE_TEXT = 4
    LINK_TEXT = 5
    IMAGE_TEXT = 6


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
