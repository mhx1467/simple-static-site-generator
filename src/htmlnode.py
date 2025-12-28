from __future__ import annotations
from typing import List, Dict, Optional
from enum import Enum

class HTMLTag(Enum):
    PARAGRAPH = 'p',
    HEADING = 'h'
    BLOCKQUOTE = 'blockquote'
    UNORDERED_LIST = 'ul'
    ORDERED_LIST = 'ol'
    LIST_ITEM = 'li'
    CODE = 'code'

class HTMLNode:
    def __init__(self, tag: Optional[str] = None, value: Optional[str] = None, children: Optional[List[HTMLNode]] = None, props: Optional[Dict[str, str]] = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        props_string = ""
        if self.props and len(self.props.keys()) > 0:
            for key, value in self.props.items():
                if value is None:
                    continue
                props_string += f"{key}='{value}' "
            props_string = props_string.rstrip()

        return props_string if len(props_string) == 0 else f" {props_string}"

    def __repr__(self) -> str:
        return f'HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})'

class LeafNode(HTMLNode):
    def __init__(self, value: str, tag: Optional[str] = None, props: Optional[Dict[str, str]] = None):
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self):
        if not self.value:
            raise ValueError("LeafNode must have a value")

        if not self.tag:
            return self.value

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: List[HTMLNode], props: Optional[Dict[str, str]] = None):
        super().__init__(tag=tag, value=None, children=children, props=props)
    
    def to_html(self):
        if not self.tag:
            raise ValueError(f"{self.__class__} must have a tag")

        if not self.children:
            raise ValueError(f"{self.__class__} must have children")

        return f"<{self.tag}{self.props_to_html()}>{"".join([child.to_html() for child in self.children])}</{self.tag}>"
