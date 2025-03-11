from typing import List
from textnode import TextNode, TextType
from functools import reduce
import re

def split_nodes_delimiter(old_nodes: List[TextNode], delimiter: str, text_type: TextType) -> List[TextNode]:
    for node in old_nodes:
        if node.text.find(delimiter) != -1 and node.text[node.text.find(delimiter)+1:].find(delimiter) == -1:
            raise Exception("Invalid Markdown syntax one or more TextNode objects does not close its delimiter")

    return list(filter(lambda t: t.text, list(reduce(lambda x, y: x + ([y] if y.text_type != TextType.TEXT else list(map(lambda i_z: TextNode(i_z[1], text_type if i_z[0] % 2 else TextType.TEXT), enumerate(y.text.split(delimiter))))), old_nodes, []))))

def extract_markdown_images(text: str):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\[\]\(\)]*)\)", text)
    return matches

def extract_markdown_links(text: str):
    matches = re.findall(r"\[([^\[\]]*)\]\(([^\[\]\(\)]*)\)", text)
    return matches


if __name__ == "__main__":
    old_nodes = [TextNode("This is sample text", TextType.TEXT), TextNode("BlahBlah Blah", TextType.ITALIC), TextNode("This is **also sample text** haha big dawg", TextType.TEXT), TextNode("This text is bold type", TextType.BOLD)]
    print(split_nodes_delimiter(old_nodes,"**",TextType.BOLD))
    
