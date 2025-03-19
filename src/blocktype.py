from enum import Enum
import re
from typing import List

from htmlnode import HTMLNode
from parentnode import ParentNode
from leafnode import LeafNode
from utility import markdown_to_blocks, text_to_textnodes, text_to_children

class BlockType(Enum):
    """
    Enum representing the different types of markdown blocks.
    
    Attributes:
        PARAGRAPH (int): Regular paragraph text.
        HEADING (int): Heading text starting with # (1-6 hash symbols).
        CODE (int): Code block enclosed in triple backticks.
        QUOTE (int): Quote block where each line starts with >.
        UNORDERED_LIST (int): List where each line starts with "- ".
        ORDERED_LIST (int): List where each line starts with a number followed by ". ".
    """
    PARAGRAPH = 1
    HEADING = 2
    CODE = 3
    QUOTE = 4
    UNORDERED_LIST = 5
    ORDERED_LIST = 6


def block_to_block_type(markdown: str) -> BlockType:
    """
    Determines the type of a markdown block.
    
    Args:
        markdown (str): A single block of markdown text with leading/trailing whitespace removed.
    
    Returns:
        BlockType: The type of the markdown block.
        
    Rules:
        - Headings start with 1-6 # characters, followed by a space and text.
        - Code blocks start with three backticks and end with three backticks.
        - Quote blocks have each line starting with a > character.
        - Unordered lists have each line starting with "- " (hyphen and space).
        - Ordered lists have each line starting with a number, period, and space (e.g., "1. ").
          Numbers must start at 1 and increment by 1 for each line.
        - If none of the above conditions are met, the block is a paragraph.
    """
    header_match = re.findall("(^[#]{1,6} )", markdown)
    if header_match:
        return BlockType.HEADING

    code_match = re.findall("(^`{3}[\s\S]*`{3}$)", markdown)
    if code_match:
        return BlockType.CODE

    parts = markdown.split('\n')
    quote_match = (len([part for part in parts if part.startswith('>')])) == len(parts)
    if quote_match:
        return BlockType.QUOTE

    unordered_list_match = (len([part for part in parts if part.startswith('- ')])) == len(parts)
    if unordered_list_match:
        return BlockType.UNORDERED_LIST
    
    ordered_list_match = True
    for i, part in enumerate(parts):
        if not part.startswith(f"{i + 1}. "):
            ordered_list_match = False
            break
    if ordered_list_match:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH

    
def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    list_of_block_types = list(map(lambda x: block_to_block_type(x), blocks))
    newChildrenHTMLNodes: List[HTMLNode] = []
    
    for i, blockType in enumerate(list_of_block_types):
        block_text = blocks[i]

        if blockType == BlockType.HEADING:
            num_hashes = len(re.findall(r"^[#]{1,6}", blocks[i])[0])
            block_content = block_text[num_hashes + 1:]
            leafNodes = text_to_children(block_content) 
            newNode = ParentNode(tag=f"h{num_hashes}", children=leafNodes)
            newChildrenHTMLNodes.append(newNode)

        elif blockType == BlockType.PARAGRAPH:
            block_content = block_text
            leafNodes = text_to_children(block_content)
            newNode = ParentNode(tag="p",children=leafNodes)
            newChildrenHTMLNodes.append(newNode)
            

        elif blockType == BlockType.QUOTE:
            block_content = "\n".join([line[1:].strip() for line in block_text.split("\n")])
            leafNodes = text_to_children(block_content)
            newNode = ParentNode(tag="blockquote", children=leafNodes)
            newChildrenHTMLNodes.append(newNode)

        elif blockType == BlockType.ORDERED_LIST:
            list_items = re.findall(r"^\d+\. (.+)", block_text, re.MULTILINE)
            allHTMLNodes = [text_to_children(item) for item in list_items]
            li_nodes = [HTMLNode(tag="li", children=allHTMLNodes[i]) for i in range(len(allHTMLNodes))]
            
            newNode = ParentNode(tag="ol", children=li_nodes)
            newChildrenHTMLNodes.append(newNode)

        elif blockType == BlockType.UNORDERED_LIST:
            list_items = re.findall(r"^[-] (.+)", block_text, re.MULTILINE)
            allHTMLNodes = [text_to_children(item) for item in list_items]
            li_nodes = [HTMLNode(tag="li", children=allHTMLNodes[i]) for i in range(len(allHTMLNodes))]
            
            newNode = ParentNode(tag="ul", children=li_nodes)
            newChildrenHTMLNodes.append(newNode)

        elif blockType == BlockType.CODE:
            block_content = re.findall(r"^`{3}([\s\S]+)`{3}$", block_text)[0]
            code_node = HTMLNode(tag="code", value=block_content)
            newNode = ParentNode(tag="pre", children=[code_node])

            newChildrenHTMLNodes.append(newNode)

    finalHTMLNode = HTMLNode(tag="div", children=newChildrenHTMLNodes)
    return finalHTMLNode



    




 




        
            
            
            
            
