from typing import List
from textnode import TextNode, TextType
from functools import reduce
import re

def split_nodes_delimiter(old_nodes: List[TextNode], delimiter: str, text_type: TextType) -> List[TextNode]:
    """
    Splits text nodes based on a delimiter and assigns a specific text type to the delimited sections.
    
    Args:
        old_nodes (List[TextNode]): A list of TextNode objects to process
        delimiter (str): The string delimiter to split on
        text_type (TextType): The TextType to assign to text between delimiters
        
    Returns:
        List[TextNode]: A new list of TextNode]
    """
    for node in old_nodes:
        if node.text.find(delimiter) != -1 and node.text[node.text.find(delimiter)+1:].find(delimiter) == -1:
            raise Exception("Invalid Markdown syntax one or more TextNode objects does not close its delimiter")

    return list(filter(lambda t: t.text, list(reduce(lambda x, y: x + ([y] if y.text_type != TextType.TEXT else list(map(lambda i_z: TextNode(i_z[1], text_type if i_z[0] % 2 else TextType.TEXT), enumerate(y.text.split(delimiter))))), old_nodes, []))))

def extract_markdown_images(text: str):
    """
    Extracts all markdown image references from a text string.
    
    Args:
        text (str): A string containing markdown text to be parsed
        
    Returns:
        list: A list of tuples where each tuple contains (alt_text, image_url)
              for each markdown image found in the text
              
    Example:
        >>> extract_markdown_images("Here is an ![example image](https://example.com/img.png)")
        [('example image', 'https://example.com/img.png')]
    """
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\[\]\(\)]*)\)", text)
    return matches

def extract_markdown_links(text: str):
    """
    Extracts all markdown links from a text string.
    
    Args:
        text (str): A string containing markdown text to be parsed
        
    Returns:
        list: A list of tuples where each tuple contains (anchor_text, url)
              for each markdown link found in the text
              
    Example:
        >>> extract_markdown_links("Check out [this site](https://example.com)")
        [('this site', 'https://example.com')]
    """
    matches = re.findall(r"\[([^\[\]]*)\]\(([^\[\]\(\)]*)\)", text)
    return matches

