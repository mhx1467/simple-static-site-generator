import unittest

from src.textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("This is test text node", TextType.BOLD)
        node2 = TextNode("This is test text node", TextType.BOLD)

        self.assertEqual(node1, node2)
