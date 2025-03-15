from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = 1,
    HEADING = 2,
    CODE = 3,
    QUOTE = 4,
    UNORDERED_LIST = 5,
    ORDERED_LIST = 6


def block_to_block_type(markdown: str) -> BlockType:
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

    



    
