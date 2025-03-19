import unittest
from blocktype import markdown_to_html_node
from htmlnode import HTMLNode


class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>"
            
        )
    def test_code(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>")
    def test_unordered_list(self):
        md = """
- Item 1
- Item 2
- Item 3
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul></div>"
        )

    def test_ordered_list(self):
        md = """
1. First item
2. Second item
3. Third item
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First item</li><li>Second item</li><li>Third item</li></ol></div>"
        )

    def test_paragraph(self):
        md = """
This is a **bold** paragraph with _italic_ text and `code`.
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is a <b>bold</b> paragraph with <i>italic</i> text and <code>code</code>.</p></div>"
        )

    def test_blockquote(self):
        md = """
> This is a blockquote with **bold** text and _italic_ text.
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote with <b>bold</b> text and <i>italic</i> text.</blockquote></div>"
        )
    
    def test_mixed_block(self):
        md = """
# Heading 1

This is a **bold** paragraph.

> A blockquote with _italic_ text.

- Item 1
- Item 2

```
Code block here
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1><p>This is a <b>bold</b> paragraph.</p><blockquote>A blockquote with <i>italic</i> text.</blockquote><ul><li>Item 1</li><li>Item 2</li></ul><pre><code>Code block here\n</code></pre></div>"

        ) 
