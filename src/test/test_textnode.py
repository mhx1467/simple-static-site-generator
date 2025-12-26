import unittest

from src.textnode import TextNode, TextType

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
