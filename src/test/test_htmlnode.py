import unittest
from src.htmlnode import HTMLNode, LeafNode, ParentNode

class HTMLNodeTestCase(unittest.TestCase):
    def test_repr(self):
        node = HTMLNode(tag="p", value="This is test text", children=None, props={"style": "color: red"})
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
        node = LeafNode(tag=None, value="This is just text")
        self.assertEqual(node.to_html(), "This is just text")

    def test_leaf_node_html_with_tag(self):
        node = LeafNode(tag="p", value="This is paragraph text")
        self.assertEqual(node.to_html(), "<p>This is paragraph text</p>")

    def test_leaf_node_with_tag_and_params(self):
        node = LeafNode(tag="a", value="This is my link", props={"href": "http://dummyurl.com"})
        self.assertEqual(node.to_html(), "<a href='http://dummyurl.com'>This is my link</a>")

    def test_single_parent_node(self):
        node = ParentNode(
            tag="p",
            children=[
                LeafNode(tag="b", value="Bold text"),
                LeafNode(tag=None, value="Normal text"),
                LeafNode(tag="i", value="italic text"),
                LeafNode(tag=None, value="Normal text")
            ]
        )
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    def test_to_html_with_children(self):
        child_node = LeafNode(tag="span", value="child")
        parent_node = ParentNode(tag="div", children=[child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode(tag="b", value="grandchild")
        child_node = ParentNode(tag="span", children=[grandchild_node])
        parent_node = ParentNode(tag="div", children=[child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_no_children(self):
        node = ParentNode(tag="div", children=[])
        self.assertRaises(ValueError, node.to_html)
