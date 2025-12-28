import re
from src.textnode import TextNode, TextType
from typing import List

class MarkdownParser:
    def split_nodes(self, old_nodes: List[TextNode], delimiter: str, text_type: TextType) -> List[TextNode]:
        new_nodes = []

        for node in old_nodes:
            if node.text_type != TextType.TEXT or len(node.text) == 0:
                new_nodes.append(node)
                continue

            d = re.escape(delimiter)

            # (?<!{d}) - negative lookbehind: ensures the delimiter is NOT preceded by another delimiter
            # {d} - matches exactly one instance of the delimiter
            # (?!{d}) - negative lookahead: ensures the delimiter is NOT followed by another delimiter
            # Result: matches a single, standalone delimiter and ignores runs like '**' or '***'
            pattern = rf'(?<!{d}){d}(?!{d})'

            parts = re.split(pattern, node.text)
        
            start = 0
            for i, part in enumerate(parts):
                end = start + len(part)

                if len(part) == 0:
                    start = end + len(delimiter)
                    continue

                is_delimited_part = i % 2 != 0
                if is_delimited_part:
                    prev_index = max(0, start - 1)
 
                    if node.text[prev_index] == delimiter and node.text[end] != delimiter:
                        raise ValueError(f"Invalid markdown element. Element starting at index {prev_index} was not correctly closed")

                    new_nodes.append(TextNode(text=part, text_type=text_type, url=None))
                else:
                    new_nodes.append(TextNode(text=part, text_type=node.text_type, url=node.url))

                start = end + len(delimiter)

        return new_nodes
