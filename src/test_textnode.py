import unittest
from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode(text="abcd", text_type=TextType.BOLD_TEXT)
        node2 = TextNode(text="abcd", text_type=TextType.BOLD_TEXT)
        self.assertEqual(node1, node2)

    def test_neq_text(self):
        node1 = TextNode(text="abcd", text_type=TextType.ITALIC_TEXT)
        node2 = TextNode(text="agha", text_type=TextType.ITALIC_TEXT)
        self.assertNotEqual(node1, node2)

    def test_neq_textType(self):
        node1 = TextNode(text="hello", text_type=TextType.BOLD_TEXT)
        node2 = TextNode(text="hello", text_type=TextType.NORMAL_TEXT)
        self.assertNotEqual(node1, node2)

    def test_neq_url(self):
        node1 = TextNode(
            text="hello", text_type=TextType.NORMAL_TEXT, url="https://www.google.com"
        )
        node2 = TextNode(
            text="hello",
            text_type=TextType.NORMAL_TEXT,
            url="https://www.wikipedia.com",
        )
        self.assertNotEqual(node1, node2)


if __name__ == "__main__":
    unittest.main()
