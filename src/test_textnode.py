import unittest
from textnode import TextNode, TextType
from utility import split_nodes_delimiter


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode(text="abcd", text_type=TextType.BOLD)
        node2 = TextNode(text="abcd", text_type=TextType.BOLD)
        self.assertEqual(node1, node2)

    def test_neq_text(self):
        node1 = TextNode(text="abcd", text_type=TextType.ITALIC)
        node2 = TextNode(text="agha", text_type=TextType.ITALIC)
        self.assertNotEqual(node1, node2)

    def test_neq_textType(self):
        node1 = TextNode(text="hello", text_type=TextType.BOLD)
        node2 = TextNode(text="hello", text_type=TextType.TEXT)
        self.assertNotEqual(node1, node2)

    def test_neq_url(self):
        node1 = TextNode(
            text="hello", text_type=TextType.TEXT, url="https://www.google.com"
        )
        node2 = TextNode(
            text="hello",
            text_type=TextType.TEXT,
            url="https://www.wikipedia.com",
        )
        self.assertNotEqual(node1, node2)

class TestSplitDelimiter(unittest.TestCase):
    def test_exceptionRaise(self):
        with self.assertRaises(Exception) as context:
            old_nodes = [TextNode("This is sample text", TextType.TEXT), TextNode("BlahBlah Blah", TextType.ITALIC), TextNode("This is **also sample text", TextType.TEXT), TextNode("This text is bold type", TextType.BOLD)]
            split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        self.assertEqual(str(context.exception), "Invalid Markdown syntax one or more TextNode objects does not close its delimiter")

    def test_bold(self):
        old_nodes = [TextNode("This is sample text", TextType.TEXT), TextNode("BlahBlah Blah", TextType.ITALIC), TextNode("This is **also sample text** haha big dawg", TextType.TEXT), TextNode("This text is bold type", TextType.BOLD)]
        self.assertEqual(split_nodes_delimiter(old_nodes, "**", TextType.BOLD), [TextNode("This is sample text", TextType.TEXT), TextNode("BlahBlah Blah", TextType.ITALIC), TextNode("This is ", TextType.TEXT), TextNode("also sample text", TextType.BOLD), TextNode(" haha big dawg", TextType.TEXT), TextNode("This text is bold type", TextType.BOLD)])


if __name__ == "__main__":
    unittest.main()
