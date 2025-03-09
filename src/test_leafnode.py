import unittest
from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("Hello, World!", "p")
        self.assertEqual(node.to_html(), "<p>Hello, World!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("Hello, Testing Testing Testing", "a", {"href": "https://www.google.com", "ref2": "idkidkidk"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com" ref2="idkidkidk">Hello, Testing Testing Testing</a>')

if __name__ == "__main__":
    unittest.main()
