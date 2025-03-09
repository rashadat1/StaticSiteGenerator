import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_repr1(self):
        node = HTMLNode(tag="p", value="This is a paragraph text")
        self.assertEqual(repr(node), "HTMLNode(tag=p, value=This is a paragraph text, children=[], props={})")
    
    def test_repr2(self):
        self.maxDiff=None
        child1 = HTMLNode(tag="p", value="This is a child.")
        child2 = HTMLNode(tag="h2", value="This is also a childnode")
        node = HTMLNode(tag="h1", value="This is an h1 inline text. Do with me what you will.", children=[child1, child2])
        self.assertEqual(repr(node), "HTMLNode(tag=h1, value=This is an h1 inline text. Do with me what you will., children=['HTMLNode(tag=p, value=This is a child., children=[], props={})', 'HTMLNode(tag=h2, value=This is also a childnode, children=[], props={})'], props={})")

    def test_repr3(self):
        child = HTMLNode(tag="p")
        node = HTMLNode(tag="a", value="This is a link tag", children=[child], props={"href": "https://www.google.com"})
        self.assertEqual(repr(node), "HTMLNode(tag=a, value=This is a link tag, children=['HTMLNode(tag=p, value=None, children=[], props={})'], props={'href': 'https://www.google.com'})")

if __name__ == "__main__":
    unittest.main()
