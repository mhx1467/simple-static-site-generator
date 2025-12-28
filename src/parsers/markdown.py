import re
from enum import Enum
from src.textnode import TextNode, TextType
from typing import Callable, Dict, List,Tuple

class BlockType(Enum):
    PARAGRAPH = 'paragraph',
    HEADING = 'heading'
    CODE = 'code'
    QUOTE = 'quote'
    UNORDERED_LIST = 'unordered_list'
    ORDERED_LIST = 'ordered_list'

class MarkdownParser:
    def text_to_textnodes(self, text: str) -> List[TextNode]:
        nodes = [TextNode(text, TextType.TEXT)]
        
        nodes = self.split_nodes_image(nodes)
        nodes = self.split_nodes_link(nodes)

        text_type_to_delimiter: Dict[TextType, str] = {
            TextType.BOLD: "**",
            TextType.ITALIC: "_",
            TextType.CODE: "`",
        }

        for text_type, delimiter in text_type_to_delimiter.items():
            nodes = self.split_nodes(nodes, delimiter, text_type)

        return nodes

    def split_nodes(self, old_nodes: List[TextNode], delimiter: str, text_type: TextType) -> List[TextNode]:
        new_nodes = []
        pattern = self.__get_split_pattern(delimiter)

        for node in old_nodes:

            if node.text_type != TextType.TEXT or len(node.text.strip()) == 0:
                new_nodes.append(node)
                continue

            parts = re.split(pattern, node.text)
            if node.text == " ":
                print(parts)

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

                    new_nodes.append(TextNode(text=part, text_type=text_type))
                else:
                    new_nodes.append(TextNode(text=part, text_type=node.text_type))

                start = end + len(delimiter)

        return new_nodes

    def split_nodes_image(self, old_nodes: List[TextNode]) -> List[TextNode]:
        return self.__split_link_based_nodes(old_nodes, self.extract_markdown_images, self.__get_image_pattern(), TextType.IMAGE)

    def split_nodes_link(self, old_nodes: List[TextNode]) -> List[TextNode]:
        return self.__split_link_based_nodes(old_nodes, self.extract_markdown_links, self.__get_link_pattern(), TextType.LINK)

    def extract_markdown_images(self, text: str) -> List[Tuple[str, str]]:
        pattern = self.__get_image_pattern()
        matches = re.findall(pattern, text)

        return matches

    def extract_markdown_links(self, text: str) -> List[Tuple[str, str]]:
        pattern = self.__get_link_pattern()
        matches = re.findall(pattern, text)

        return matches

    def markdown_to_blocks(self, markdown: str) -> List[str]:
        # TODO: For now, only care about simple and valid markdown.
        blocks = markdown.split("\n\n")

        return list(filter(lambda block: len(block) > 0, map(lambda block: block.strip(), blocks)))

    def __split_link_based_nodes(self, old_nodes: List[TextNode], get_links_callback: Callable, pattern: str, text_type: TextType) -> List[TextNode]:
        new_nodes = []

        for node in old_nodes:
            if node.text_type != TextType.TEXT or len(node.text.strip()) == 0:
                new_nodes.append(node)
                continue

            start, end = 0, len(node.text) - 1
            links = get_links_callback(node.text)
            links_positions = [
                (m.start(), m.end() - 1)
                for m in re.finditer(pattern, node.text)
            ]

            if len(links) != len(links_positions):
                raise Exception("Links length and positions matches mismatch")

            for i, match in enumerate(links_positions):
                assert len(match) == 2
                assert match[0] is not None and match[1] is not None

                end = max(0, match[0] - 1)
                normal_text = node.text[start:end + 1]

                if start < end:
                    new_nodes.append(TextNode(text=normal_text, text_type=node.text_type))

                new_nodes.append(TextNode(text=links[i][0], text_type=text_type, url=links[i][1])) 
                start = min(match[1] + 1, len(node.text))


            if start < len(node.text):
                new_nodes.append(TextNode(text=node.text[max(0, start):], text_type=TextType.TEXT))

        return new_nodes

    def block_to_block_type(self, block: str) -> BlockType:
        regex_to_block_type: Dict[str, BlockType] = {
            r"^#{1,6}\s": BlockType.HEADING,
            r"^```": BlockType.CODE,
            r"^>": BlockType.QUOTE,
            r"^\d+\.\s": BlockType.ORDERED_LIST,
            r"^[-*+]\s": BlockType.UNORDERED_LIST,
            r".*": BlockType.PARAGRAPH,
        }

        first_line = block.split("\n", 1)[0]
        for regex, block_type in regex_to_block_type.items():
            if re.match(regex, first_line):
                return block_type

        raise ValueError("Unknown block encountered")

    def __get_split_pattern(self, delimiter: str) -> str:
        d = re.escape(delimiter)
        # (?<!{d}) - negative lookbehind: ensures the delimiter is NOT preceded by another delimiter
        # {d} - matches exactly one instance of the delimiter
        # (?!{d}) - negative lookahead: ensures the delimiter is NOT followed by another delimiter
        # Result: matches a single, standalone delimiter and ignores runs like '**' or '***'

        # TODO: Improve on contigous sections such as "_one__two_ **a****b**"
        return rf'(?<!{d}){d}(?!{d})'

    def __get_image_pattern(self) -> str:
        return rf'!\[([^\[\]]*)\]\(([^\(\)]*)\)'

    def __get_link_pattern(self) -> str:
        return rf'(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)'
