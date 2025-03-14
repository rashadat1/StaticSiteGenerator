from textnode import text_node_to_html_node, TextType, TextNode
from utility import markdown_to_blocks
import unittest

class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode(text="This is a text node", text_type=TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode(text="This is a bold text node", text_type=TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text node")

    def test_link(self):
        node = TextNode(text="This is a link text node", text_type=TextType.LINK, url="https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link text node")
        self.assertEqual(html_node.props, {"href": "https://www.google.com"})

    def test_image(self):
        node = TextNode(text="This is alt text", text_type=TextType.IMAGE, url="https://scaler.com/topics/images/none-in-python-1.webp")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://scaler.com/topics/images/none-in-python-1.webp", "alt": "This is alt text"})

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        markdown = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
""" 
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ]
    )
    def test_markdown_to_blocks2(self):
        markdown = """

# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.






- This is the first list item in a list block
- This is a list item
- This is another list item


"""
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(
            blocks,
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
                "- This is the first list item in a list block\n- This is a list item\n- This is another list item"
            ]
        )

if __name__ == "__main__":
    unittest.main
