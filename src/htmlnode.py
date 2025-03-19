from typing import Dict, List, Optional


class HTMLNode:
    """
    A class that represents an HTML node in a document tree.

    This class is designed to represent block-level or inline-level HTML nodes,
    such as tags (`<p>`, `<a>`, `<h1>`) and their contents. It supports attributes
    (props), textual values, and child nodes.

    Attributes:
        tag (Optional[str]): The HTML tag name (e.g., "div", "p", "a"). Defaults to None.
        value (Optional[str]): The textual content of the HTML node, if any. Defaults to None.
        children (Optional[List[HTMLNode]]): A list of child `HTMLNode` objects. Defaults to an empty list.
        props (Optional[Dict[str, str]]): A dictionary of HTML attributes (like `href`, `class`). Defaults to an empty dictionary.
    """
    def __init__(self, tag: Optional[str] = None, value: Optional[str] = None, children: Optional[List["HTMLNode"]] = None, props: Optional[Dict[str, str]] = None):
        """
        Constructor for the HTMLNode class.

        Args:
            tag (Optional[str]): The HTML tag name.
            value (Optional[str]): The textual value inside the HTML node (e.g., content of a paragraph).
            children (Optional[List["HTMLNode"]]): A list of child HTMLNode objects that the current node contains.
            props (Optional[Dict[str, str]]): A dictionary of HTML attributes (e.g., {"href": "example.com", "class": "link"}).
        """
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props if props is not None else {}

    def to_html(self):
        """

        """
        # Base case: if no tag and has a value, it's pure textual
        if not self.tag:
            return self.value or ""

        html = f"<{self.tag}{self.props_to_html()}>"

        if self.value:
            if self.tag == "p":
                html += self.value.replace("\n", " ")
            else:
                html += self.value


        for child in self.children:
            html += child.to_html()

        html += f"</{self.tag}>"
        return html


    def props_to_html(self) -> str:
        """
        Converts the props (attributes) of the HTMLNode into a formatted string suitable for inclusion in an HTML tag.

        The method iterates over the `props` dictionary and generates a string where each key-value pair is formatted
        as ` key="value"`. A leading space is included, so the result can easily be appended to an opening tag.

        Returns:
            str: A string representation of the node's properties. For example, if `props` is:

            {
                "href": "https://www.google.com",
                "target": "_blank"
            }

            Then the returned string will be:
             ' href="https://www.google.com" target="_blank"'

        Notes:
            - If `props` is empty, the method returns an empty string.
            - The leading space is intentional and ensures compatibility when embedding the properties inside an HTML tag.
        """
        return_string = ""
        if self.props:
            for key, val in self.props.items():
                return_string += f' {key}="{val}"'
        return return_string

    def __repr__(self):
        children_ = [repr(child) for child in self.children]
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={children_}, props={self.props})"





    

