from typing import Dict, Optional
from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, value: str, tag: Optional[str] = None, props: Optional[Dict[str,str]] = None):
        super().__init__(tag=tag, value=value, props=props)
    
    def to_html(self):
        if not self.tag:
            return self.value
        return_string = ""
        return_string += f"<{self.tag}" + f"{self.props_to_html()}>{self.value}</{self.tag}>"
        return return_string





        
