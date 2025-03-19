from typing import Dict, List, Optional
from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    """
    Represents an HTML node that can contain child nodes.
    
    A ParentNode is used for HTML elements that can contain other elements,
    such as div, p, ul, etc.
    
    Attributes:
        tag: The HTML tag name
        children: List of child HTMLNode objects
        props: Optional dictionary of HTML attributes
    """
    def __init__(self, tag: str, children: List[HTMLNode], props: Optional[Dict[str,str]] = None):
        """
        Initialize a new ParentNode.
        
        Args:
            tag: The HTML tag name (e.g., "div", "p")
            children: List of child HTMLNode objects
            props: Optional dictionary of HTML attributes (e.g., {"class": "container"})
        """
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        """
        Convert the ParentNode and all its children to an HTML string.
        
        Returns:
            str: HTML representation of this node and its children
        """
        if not self.children:
            # base case we reach a leaf node and call its to_html method
            return self.to_html()
        return_string = f"<{self.tag}" + f"{self.props_to_html()}>"

        for child in self.children:
            return_string += child.to_html()
        return_string = return_string.replace("\n", " ") if self.tag == "p" else return_string

        return_string += f"</{self.tag}>"
        return return_string
