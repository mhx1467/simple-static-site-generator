import unittest
from src.parsers.markdown import MarkdownParser
from src.textnode import TextNode, TextType


class MarkdownParserSplitNodesTestCase(unittest.TestCase):

    def setUp(self):
        self.parser = MarkdownParser()

    # Basic delimiter behavior

    def test_single_code_span(self):
        node = TextNode("This is `code` text", TextType.TEXT)
        result = self.parser.split_nodes([node], "`", TextType.CODE)

        self.assertEqual(result, [
            TextNode("This is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text", TextType.TEXT),
        ])

    def test_multiple_code_spans(self):
        node = TextNode("`one` and `two`", TextType.TEXT)
        result = self.parser.split_nodes([node], "`", TextType.CODE)

        self.assertEqual(result, [
            TextNode("one", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("two", TextType.CODE),
        ])

    def test_no_delimiter_present(self):
        node = TextNode("plain text only", TextType.TEXT)
        result = self.parser.split_nodes([node], "`", TextType.CODE)

        self.assertEqual(result, [node])

    # Bold delimiter

    def test_bold_text(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        result = self.parser.split_nodes([node], "**", TextType.BOLD)

        self.assertEqual(result, [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ])

    def test_multiple_bold_sections(self):
        node = TextNode("**one** and **two**", TextType.TEXT)
        result = self.parser.split_nodes([node], "**", TextType.BOLD)

        self.assertEqual(result, [
            TextNode("one", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("two", TextType.BOLD),
        ])

    # Italics delimiter

    def test_italic_text(self):
        node = TextNode("This is *italic* text", TextType.TEXT)
        result = self.parser.split_nodes([node], "*", TextType.ITALIC)

        self.assertEqual(result, [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ])

    # Mixed but non-nested delimiters

    def test_mixed_delimiters_not_nested(self):
        node = TextNode("This is *italic* and **bold**", TextType.TEXT)

        result = self.parser.split_nodes([node], "*", TextType.ITALIC)
        result = self.parser.split_nodes(result, "**", TextType.BOLD)

        self.assertEqual(result, [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
        ])

    # Invalid / edge cases

    def test_unbalanced_delimiter_raises(self):
        node = TextNode("This is `broken code", TextType.TEXT)

        with self.assertRaises(Exception):
            self.parser.split_nodes([node], "`", TextType.CODE)

    def test_text_type_not_split(self):
        node = TextNode("`code`", TextType.CODE)
        result = self.parser.split_nodes([node], "`", TextType.CODE)

        self.assertEqual(result, [node])

    def test_empty_string(self):
        node = TextNode("", TextType.TEXT)
        result = self.parser.split_nodes([node], "*", TextType.ITALIC)

        self.assertEqual(result, [node])
