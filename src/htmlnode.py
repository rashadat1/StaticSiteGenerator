from typing import Dict, List, Optional


class HTMLNode:
    def __init__(self, tag: Optional[str] = None, value: Optional[str] = None, children: Optional[List["HTMLNode"]] = None, props: Optional[Dict[str, str]] = None):
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props if props is not None else {}

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self) -> str:
        return_string = ""
        if self.props:
            for key, val in self.props.items():
                return_string += f" {key}={val}"
        return return_string

    def __repr__(self):
        children_ = [repr(child) for child in self.children]
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={children_}, props={self.props})"





    

