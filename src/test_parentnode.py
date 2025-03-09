import unittest
from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode(tag="span", value="child")
        parent_node = ParentNode(tag="div", children=[child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")
    
    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode(tag="p", value="grandchild")
        child_node1 = ParentNode(tag="h2", children=[grandchild_node])
        child_node2 = LeafNode(tag="a", value="This is a child", props={"href": "https://www.google.com"})
        parent_node = ParentNode(tag="h1", props={"fakeprop": "babubabu"}, children=[child_node2, child_node1])
        self.assertEqual(parent_node.to_html(), '<h1 fakeprop="babubabu"><a href="https://www.google.com">This is a child</a><h2><p>grandchild</p></h2></h1>',None)

    def test_to_html_with_grandchildren_second(self):
        grandchild_node = LeafNode(tag="b", value="grandchild")
        child_node = ParentNode(tag="span", children=[grandchild_node])
        parent_node = ParentNode(tag="div", children=[child_node])
        self.assertEqual(parent_node.to_html(), "<div><span><b>grandchild</b></span></div>")
if __name__ == "__main__":
    unittest.main()
