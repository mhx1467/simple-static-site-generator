import unittest
from src.htmlnode import HTMLNode, LeafNode

class HTMLNodeTestCase(unittest.TestCase):
    def test_repr(self):
        node = HTMLNode("p", "This is test text", None, {"style": "color: red"})
        self.assertEqual(repr(node), "HTMLNode(p, This is test text, None, {'style': 'color: red'})")

    def test_props_to_html_with_valid_value(self):
        node = HTMLNode(props={"target": "_blank", "href": "http://dummyurl.com"})
        result = node.props_to_html().strip()
        self.assertEqual(result, f"target='_blank' href='http://dummyurl.com'")

    def test_props_to_html_with_no_values(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_should_skip_empty_value(self):
        node = HTMLNode(props={
            "href": None, # type: ignore[dict-item]
            "target": "_blank"
        })

        result =node.props_to_html().strip()
        self.assertEqual(result, "target='_blank'")


    def test_leaf_node_html_without_tag(self):
        node = LeafNode("", "This is just text")
        self.assertEqual(node.to_html(), "This is just text")

    def test_leaf_node_html_with_tag(self):
        node = LeafNode("p", "This is paragraph text")
        self.assertEqual(node.to_html(), "<p>This is paragraph text</p>")

    def test_leaf_node_with_tag_and_params(self):
        node = LeafNode("a", "This is my link", props={"href": "http://dummyurl.com"})
        self.assertEqual(node.to_html(), "<a href='http://dummyurl.com'>This is my link</a>")
