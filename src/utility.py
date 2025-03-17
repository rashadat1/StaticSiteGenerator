from typing import List, Tuple
from textnode import TextNode, TextType, text_node_to_html_node
from functools import reduce
import re
from leafnode import LeafNode

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

def extract_markdown_images(text: str) -> List[Tuple[str,str]]:
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

def extract_markdown_links(text: str) -> List[Tuple[str,str]]:
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

def append_nodes_helper(lst1: List[TextNode], lst2: List[TextNode]) -> List[TextNode]:
    i, j = 0, 0
    nodes_in_order = []
    while i < len(lst1) and j < len(lst2):
        if lst1[i].text:
            nodes_in_order.append(lst1[i])
        if lst2[j].text:
            nodes_in_order.append(lst2[j])
        i += 1
        j += 1
    while i < len(lst1):
        if lst1[i].text:
            nodes_in_order.append(lst1[i])
        i += 1
    while j < len(lst2):
        if lst2[j].text:
            nodes_in_order.append(lst2[j])
        j += 1
    return nodes_in_order

def split_nodes_image(old_nodes: List[TextNode]) -> List[TextNode]:
    result = []
    def helper(node: TextNode) -> List[TextNode]:
        result = []
        if node.text_type == TextType.TEXT:
            intermediate = node.text
            image_parts = extract_markdown_images(node.text)
            for i in range(len(image_parts)):
                intermediate = ("seqbreakabc".join(intermediate.split(f"![{image_parts[i][0]}]({image_parts[i][1]})")))
            non_image_parts = intermediate.split("seqbreakabc")
            
            non_image_text_nodes = [TextNode(text=text_frag, text_type=TextType.TEXT) for text_frag in non_image_parts]
            image_text_nodes = [TextNode(text=altText, text_type=TextType.IMAGE, url=urlText) for altText, urlText in image_parts]
            if node.text.startswith(non_image_parts[0]):
                lst1 = non_image_text_nodes
                lst2 = image_text_nodes
            else:
                lst1 = image_text_nodes
                lst2 = non_image_text_nodes
            result = append_nodes_helper(lst1, lst2)
        return result
     
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            result.extend(helper(node))
        else:
            result.append(node)

    
    return result

def split_nodes_link(old_nodes: List[TextNode]) -> List[TextNode]:
    result = []
    def helper(node: TextNode) -> List[TextNode]:
        result = []
        intermediate = node.text
        link_parts = extract_markdown_links(node.text)
        for i in range(len(link_parts)):
            intermediate = ("seqbreakabc".join(intermediate.split(f"[{link_parts[i][0]}]({link_parts[i][1]})")))
        non_link_parts = intermediate.split("seqbreakabc")
    
        non_link_text_nodes = [TextNode(text=text_frag, text_type=node.text_type) for text_frag in non_link_parts]
        link_text_nodes = [TextNode(text=altText, text_type=TextType.LINK, url=urlText) for altText, urlText in link_parts]
    
        if node.text.startswith(non_link_parts[0]):
            lst1 = non_link_text_nodes
            lst2 = link_text_nodes
        else:
            lst1 = link_text_nodes
            lst2 = non_link_text_nodes
        result = append_nodes_helper(lst1, lst2)
        return result
     
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            result.extend(helper(node))
        else:
            result.append(node)
    
    return result 

def text_to_textnodes(text: str) -> List[TextNode]:
    textNode = TextNode(text=text, text_type=TextType.TEXT)
    result = []
    result.extend(split_nodes_link(split_nodes_image([textNode])))
    delimiters = ["`","**","_"]
    textTypes = [TextType.CODE, TextType.BOLD, TextType.ITALIC]
    for delimiter, textType in zip(delimiters, textTypes):
        result = split_nodes_delimiter(result, delimiter, textType)
    return result

def markdown_to_blocks(markdown: str) -> List[str]:
    blocks = markdown.split("\n\n")
    return list(filter(lambda block: block != "" and block != "\n", list(map(lambda block: block.strip(), blocks))))

def text_to_children(text: str):
    pureTextNodes = text_to_textnodes(text)
    listLeafNodes = list(map(lambda x: text_node_to_html_node(x), pureTextNodes))
    return listLeafNodes


if __name__ == "__main__":
    node = TextNode(
    "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
    TextType.TEXT)

    new_nodes = split_nodes_link([node])
    #print(new_nodes)

    node2 = TextNode(
    "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev), ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg))",
    TextType.TEXT)

    #new_nodes = split_nodes_image([node2])
    #print(new_nodes)

    text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
    
    print(text_to_textnodes(text))

