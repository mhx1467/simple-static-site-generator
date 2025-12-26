import unittest

from src.textnode import TextNode, TextType, text_node_to_html_node

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("This is test text node", TextType.BOLD)
        node2 = TextNode("This is test text node", TextType.BOLD)

        self.assertEqual(node1, node2)

    def test_not_eq_text(self):
        node1 = TextNode("This is test text node1", TextType.ITALIC)
        node2 = TextNode("This is test text node2", TextType.ITALIC)

        self.assertNotEqual(node1, node2)

    def test_not_eq_type(self):
        node1 = TextNode("This is test text node1", TextType.ITALIC)
        node2 = TextNode("This is test text node1", TextType.BOLD)

        self.assertNotEqual(node1, node2)


    def test_not_eq_url(self):
        node1 = TextNode("This is test text node1", TextType.BOLD, "http://dummyurl.com")
        node2 = TextNode("This is test text node1", TextType.BOLD)

        self.assertNotEqual(node1, node2)

    def test_if_url_not_provided(self):
        node_without_url = TextNode("This is node without any URL", TextType.BOLD)

        self.assertIsNone(node_without_url.url)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text")
        self.assertIsNone(html_node.props)

    def test_italic(self):
        node = TextNode("Italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic text")
        self.assertIsNone(html_node.props)

    def test_code(self):
        node = TextNode("print('hello')", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print('hello')")
        self.assertIsNone(html_node.props)

    def test_link(self):
        node = TextNode(
            "Example.com",
            TextType.LINK,
            "https://example.com"
        )
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Example.com")
        self.assertEqual(html_node.props, {"href": "https://example.com"})

    def test_link_without_url_raises(self):
        node = TextNode("Broken link", TextType.LINK)
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

    def test_image(self):
        node = TextNode(
            "An image",
            TextType.IMAGE,
            "https://example.com/image.png"
        )
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"href": "https://example.com/image.png", "alt": "An image"}
        )

    def test_image_without_url_raises(self):
        node = TextNode("Broken image", TextType.IMAGE)
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

