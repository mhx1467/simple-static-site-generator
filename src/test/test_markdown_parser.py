import unittest
from src.parsers.markdown import MarkdownParser, BlockType
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
        node = TextNode("This is _italic_ and **bold**", TextType.TEXT)

        result = self.parser.split_nodes([node], "_", TextType.ITALIC)
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

   # Image extraction

    def test_single_image(self):
        text = "Here is an image ![alt text](https://example.com/image.png)"
        result = self.parser.extract_markdown_images(text)

        self.assertEqual(result, [
            ("alt text", "https://example.com/image.png")
        ])

    def test_multiple_images(self):
        text = (
            "First ![one](https://example.com/one.png) "
            "and second ![two](https://example.com/two.png)"
        )
        result = self.parser.extract_markdown_images(text)

        self.assertEqual(result, [
            ("one", "https://example.com/one.png"),
            ("two", "https://example.com/two.png"),
        ])

    def test_no_images(self):
        text = "There are no images here"
        result = self.parser.extract_markdown_images(text)

        self.assertEqual(result, [])

    def test_image_like_text_but_invalid(self):
        text = "This looks like ![alt text](missing end"
        result = self.parser.extract_markdown_images(text)

        self.assertEqual(result, [])

    # Link extraction

    def test_single_link(self):
        text = "Visit [example](https://example.com)"
        result = self.parser.extract_markdown_links(text)

        self.assertEqual(result, [
            ("example", "https://example.com")
        ])

    def test_multiple_links(self):
        text = (
            "Links: [one](https://one.com) "
            "and [two](https://two.com)"
        )
        result = self.parser.extract_markdown_links(text)

        self.assertEqual(result, [
            ("one", "https://one.com"),
            ("two", "https://two.com"),
        ])

    def test_no_links(self):
        text = "Plain text with no links"
        result = self.parser.extract_markdown_links(text)

        self.assertEqual(result, [])

    def test_image_not_treated_as_link(self):
        text = "This is an image ![alt](https://example.com/image.png)"
        result = self.parser.extract_markdown_links(text)

        self.assertEqual(result, [])


    def test_single_link_node(self):
        node = TextNode("Visit [example](https://example.com)", TextType.TEXT)
        result = self.parser.split_nodes_link([node])

        self.assertEqual(result, [
            TextNode("Visit ", TextType.TEXT),
            TextNode("example", TextType.LINK, url="https://example.com")
        ])

    def test_multiple_links_in_node(self):
        node = TextNode("Links: [one](https://one.com) and [two](https://two.com)", TextType.TEXT)
        result = self.parser.split_nodes_link([node])

        self.assertEqual(result, [
            TextNode("Links: ", TextType.TEXT),
            TextNode("one", TextType.LINK, url="https://one.com"),
            TextNode(" and ", TextType.TEXT),
            TextNode("two", TextType.LINK, url="https://two.com"),
        ])

    def test_sequential_links_in_node(self):
        node = TextNode("[a](a.com)[b](b.com)", TextType.TEXT)
        result = self.parser.split_nodes_link([node])

        self.assertEqual(result, [
            TextNode("a", TextType.LINK, url="a.com"),
            TextNode("b", TextType.LINK, url="b.com"),
        ])

    def test_links_and_text_mixed_nodes(self):
        node = TextNode("Before [link](url) after", TextType.TEXT)
        result = self.parser.split_nodes_link([node])

        self.assertEqual(result, [
            TextNode("Before ", TextType.TEXT),
            TextNode("link", TextType.LINK, url="url"),
            TextNode(" after", TextType.TEXT),
        ])

    def test_no_links_in_node(self):
        node = TextNode("Plain text only", TextType.TEXT)
        result = self.parser.split_nodes_link([node])
        self.assertEqual(result, [node])

    def test_invalid_link_in_node(self):
        node = TextNode("Broken [link](missing end", TextType.TEXT)
        result = self.parser.split_nodes_link([node])
        self.assertEqual(result, [node])

    def test_link_node_already_link(self):
        node = TextNode("link", TextType.LINK, url="url")
        result = self.parser.split_nodes_link([node])
        self.assertEqual(result, [node])

    def test_empty_text_node(self):
        node = TextNode("", TextType.TEXT)
        result = self.parser.split_nodes_link([node])
        self.assertEqual(result, [node])

    def test_single_image_node(self):
        node = TextNode("Here is an image ![alt](url)", TextType.TEXT)
        result = self.parser.split_nodes_image([node])

        self.assertEqual(result, [
            TextNode("Here is an image ", TextType.TEXT),
            TextNode("alt", TextType.IMAGE, url="url")
        ])

    def test_multiple_images_in_node(self):
        node = TextNode("![one](one.png) text ![two](two.png)", TextType.TEXT)
        result = self.parser.split_nodes_image([node])

        self.assertEqual(result, [
            TextNode("one", TextType.IMAGE, url="one.png"),
            TextNode(" text ", TextType.TEXT),
            TextNode("two", TextType.IMAGE, url="two.png"),
        ])

    def test_sequential_images_node(self):
        node = TextNode("![a](a.png)![b](b.png)", TextType.TEXT)
        result = self.parser.split_nodes_image([node])

        self.assertEqual(result, [
            TextNode("a", TextType.IMAGE, url="a.png"),
            TextNode("b", TextType.IMAGE, url="b.png"),
        ])

    def test_images_and_text_mixed_node(self):
        node = TextNode("Text before ![img](url) after", TextType.TEXT)
        result = self.parser.split_nodes_image([node])

        self.assertEqual(result, [
            TextNode("Text before ", TextType.TEXT),
            TextNode("img", TextType.IMAGE, url="url"),
            TextNode(" after", TextType.TEXT),
        ])

    def test_no_images_in_node(self):
        node = TextNode("Plain text", TextType.TEXT)
        result = self.parser.split_nodes_image([node])
        self.assertEqual(result, [node])

    def test_invalid_image_node(self):
        node = TextNode("Broken ![alt](missing end", TextType.TEXT)
        result = self.parser.split_nodes_image([node])
        self.assertEqual(result, [node])

    def test_image_node_already_image(self):
        node = TextNode("img", TextType.IMAGE, url="url")
        result = self.parser.split_nodes_image([node])
        self.assertEqual(result, [node])

    def test_empty_text_node_image(self):
        node = TextNode("", TextType.TEXT)
        result = self.parser.split_nodes_image([node])
        self.assertEqual(result, [node])

    def test_node_with_link_and_image(self):
        node = TextNode("Start ![img](img.png) middle [link](url) end", TextType.TEXT)
        # First extract images
        result = self.parser.split_nodes_image([node])
        # Then extract links
        result = self.parser.split_nodes_link(result)

        self.assertEqual(result, [
            TextNode("Start ", TextType.TEXT),
            TextNode("img", TextType.IMAGE, url="img.png"),
            TextNode(" middle ", TextType.TEXT),
            TextNode("link", TextType.LINK, url="url"),
            TextNode(" end", TextType.TEXT),
        ])

    # -----------------------------
    # Plain text
    # -----------------------------
    def test_plain_text_full(self):
        text = "Just plain text"
        result = self.parser.text_to_textnodes(text)
        self.assertEqual(result, [
            TextNode("Just plain text", TextType.TEXT)
        ])

    # -----------------------------
    # Italic text
    # -----------------------------
    def test_italic_text_full(self):
        text = "This is _italic_ text"
        result = self.parser.text_to_textnodes(text)
        self.assertEqual(result, [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT)
        ])

    # -----------------------------
    # Bold text
    # -----------------------------
    def test_bold_text_full(self):
        text = "This is **bold** text"
        result = self.parser.text_to_textnodes(text)
        self.assertEqual(result, [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT)
        ])

    # -----------------------------
    # Code span
    # -----------------------------
    def test_code_text_full(self):
        text = "Code: `print('hi')` end"
        result = self.parser.text_to_textnodes(text)
        self.assertEqual(result, [
            TextNode("Code: ", TextType.TEXT),
            TextNode("print('hi')", TextType.CODE),
            TextNode(" end", TextType.TEXT)
        ])

    # -----------------------------
    # Link
    # -----------------------------
    def test_single_link_full(self):
        text = "Visit [example](https://example.com)"
        result = self.parser.text_to_textnodes(text)
        self.assertEqual(result, [
            TextNode("Visit ", TextType.TEXT),
            TextNode("example", TextType.LINK, url="https://example.com")
        ])

    def test_multiple_links_full(self):
        text = "Links: [one](https://one.com) and [two](https://two.com)"
        result = self.parser.text_to_textnodes(text)
        self.assertEqual(result, [
            TextNode("Links: ", TextType.TEXT),
            TextNode("one", TextType.LINK, url="https://one.com"),
            TextNode(" and ", TextType.TEXT),
            TextNode("two", TextType.LINK, url="https://two.com"),
        ])

    # -----------------------------
    # Images
    # -----------------------------
    def test_single_image_full(self):
        text = "Image: ![alt](https://example.com/image.png)"
        result = self.parser.text_to_textnodes(text)
        self.assertEqual(result, [
            TextNode("Image: ", TextType.TEXT),
            TextNode("alt", TextType.IMAGE, url="https://example.com/image.png")
        ])

    def test_multiple_images_full(self):
        text = "![one](one.png) and ![two](two.png)"
        result = self.parser.text_to_textnodes(text)
        self.assertEqual(result, [
            TextNode("one", TextType.IMAGE, url="one.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode("two", TextType.IMAGE, url="two.png"),
        ])

    # -----------------------------
    # Mixed markdown
    # -----------------------------
    def test_mixed_markdown_full(self):
        text = "Start _italic_ **bold** `code` [link](url) ![img](img.png) end"
        result = self.parser.text_to_textnodes(text)
        
        # print("Result", result)

        self.assertEqual(result, [
            TextNode("Start ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" ", TextType.TEXT),
            TextNode("link", TextType.LINK, url="url"),
            TextNode(" ", TextType.TEXT),
            TextNode("img", TextType.IMAGE, url="img.png"),
            TextNode(" end", TextType.TEXT)
        ])

    # -----------------------------
    # Edge cases
    # -----------------------------
    def test_unbalanced_markdown_raises_full(self):
        text = "This is _broken and **bold"
        with self.assertRaises(Exception):
            self.parser.text_to_textnodes(text)

    def test_empty_string_full(self):
        text = ""
        result = self.parser.text_to_textnodes(text)
        self.assertEqual(result, [TextNode("", TextType.TEXT)])

    def test_markdown_to_blocks(self):
        md = (
            "This is **bolded** paragraph\n"
            "\n"
            "This is another paragraph with _italic_ text and `code` here\n"
            "This is the same paragraph on a new line\n"
            "\n"
            "- This is a list\n"
            "- with items"
        )

        blocks = self.parser.markdown_to_blocks(md)

        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(self.parser.block_to_block_type(block), BlockType.HEADING)
        block = "```\ncode\n```"
        self.assertEqual(self.parser.block_to_block_type(block), BlockType.CODE)
        block = "> quote\n> more quote"
        self.assertEqual(self.parser.block_to_block_type(block), BlockType.QUOTE)
        block = "- list\n- items"
        self.assertEqual(self.parser.block_to_block_type(block), BlockType.UNORDERED_LIST)
        block = "1. list\n2. items"
        self.assertEqual(self.parser.block_to_block_type(block), BlockType.ORDERED_LIST)
        block = "paragraph"
        self.assertEqual(self.parser.block_to_block_type(block), BlockType.PARAGRAPH)
