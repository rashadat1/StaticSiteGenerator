import unittest
from textnode import TextType, TextNode
from utility import text_to_textnodes


class TestTextToTextNode(unittest.TestCase):
    def test_splitTextNodesTest1(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        self.assertEqual(text_to_textnodes(text), [TextNode("This is ",TextType.TEXT,None), TextNode("text",TextType.BOLD,None), TextNode(" with an ",TextType.TEXT,None), TextNode("italic",TextType.ITALIC,None), TextNode(" word and a ",TextType.TEXT,None), TextNode("code block",TextType.CODE,None), TextNode(" and an ",TextType.TEXT,None), TextNode("obi wan image",TextType.IMAGE,"https://i.imgur.com/fJRm4Vk.jpeg"), TextNode(" and a ",TextType.TEXT,None), TextNode("link",TextType.LINK,"https://boot.dev")])
    
if __name__ == "__main__":
    unittest.main
