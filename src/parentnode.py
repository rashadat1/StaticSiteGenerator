from typing import Dict, List, Optional
from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: List[HTMLNode], props: Optional[Dict[str,str]] = None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if not self.children:
            # base case we reach a leaf node and call its to_html method
            return self.to_html()
        return_string = f"<{self.tag}" + f"{self.props_to_html()}>"
        for child in self.children:
            return_string += child.to_html()
        return_string += f"</{self.tag}>"
        return return_string
