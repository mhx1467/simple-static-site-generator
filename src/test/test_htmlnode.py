import unittest
from src.htmlnode import HTMLNode

class HTMLNodeTestCase(unittest.TestCase):
    def test_repr(self):
        node = HTMLNode("p", "This is test text", None, {"style": "color: red"})
        self.assertEqual(repr(node), "HTMLNode(p, This is test text, None, {'style': 'color: red'})")

    def test_props_to_html_with_valid_value(self):
        node = HTMLNode(props={"target": "_blank", "href": "http://dummyurl.com"})
        self.assertEqual(node.props_to_html(), f"target='_blank' href='http://dummyurl.com'")

    def test_props_to_html_with_no_values(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_should_skip_empty_value(self):
        node = HTMLNode(props={
            "href": None, # type: ignore[dict-item]
            "target": "_blank"
        })

        self.assertEqual(node.props_to_html(), "target='_blank'")

