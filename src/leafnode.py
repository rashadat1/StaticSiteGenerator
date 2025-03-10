from typing import Dict, Optional
from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    """
    Represents an HTML node that cannot contain child nodes.
    
    A LeafNode is used for HTML elements that only contain text or are self-closing,
    such as text content, img, input, etc.
    
    Attributes:
        value: The text content of the node
        tag: Optional HTML tag name (None for raw text)
        props: Optional dictionary of HTML attributes
    """
    def __init__(self, value: str, tag: Optional[str] = None, props: Optional[Dict[str,str]] = None):
        """
        Initialize a new LeafNode.
        
        Args:
            value: The text content of the node
            tag: Optional HTML tag name (None for raw text nodes)
            props: Optional dictionary of HTML attributes (e.g., {"href": "https://example.com"})
        """
        super().__init__(tag=tag, value=value, props=props)
    
    def to_html(self):
        """
        Convert the LeafNode to an HTML string.
        
        If no tag is specified, returns the raw text value.
        Otherwise, returns the value wrapped in the appropriate HTML tags with properties.
        
        Returns:
            str: HTML representation of this node
        """
        if not self.tag:
            return self.value
        return_string = ""
        return_string += f"<{self.tag}" + f"{self.props_to_html()}>{self.value}</{self.tag}>"
        return return_string





        
