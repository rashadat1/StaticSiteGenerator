import unittest
from blocktype import BlockType, block_to_block_type

class TestBlockToBlockType(unittest.TestCase):
    def test_heading(self):
        self.assertEqual(block_to_block_type("# Heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Small Heading"), BlockType.HEADING)
        self.assertNotEqual(block_to_block_type("#Heading"), BlockType.HEADING)  # No space after #

    def test_code_block(self):
        self.assertEqual(block_to_block_type("```\ncode here\n```"), BlockType.CODE)
        self.assertNotEqual(block_to_block_type("`` code ```"), BlockType.CODE)  # Missing triple backticks

    def test_quote_block(self):
        self.assertEqual(block_to_block_type("> Quote\n> Another"), BlockType.QUOTE)
        self.assertNotEqual(block_to_block_type("> Quote\nNo quote"), BlockType.QUOTE)  # One line is missing '>'

    def test_unordered_list(self):
        self.assertEqual(block_to_block_type("- Item 1\n- Item 2"), BlockType.UNORDERED_LIST)
        self.assertNotEqual(block_to_block_type("- Item 1\n1. Item 2"), BlockType.UNORDERED_LIST)  # Mixed list types

    def test_ordered_list(self):
        self.assertEqual(block_to_block_type("1. First\n2. Second\n3. Third"), BlockType.ORDERED_LIST)
        self.assertNotEqual(block_to_block_type("1. First\n3. Second"), BlockType.ORDERED_LIST)  # Numbers must be sequential

    def test_paragraph(self):
        self.assertEqual(block_to_block_type("This is a normal paragraph."), BlockType.PARAGRAPH)



if __name__ == "__main__":
    unittest.main()
