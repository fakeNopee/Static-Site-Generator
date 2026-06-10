import re

from blocktype import block_to_block_type
from htmlnode import ParentNode
from split_nodes_delimiter import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node


def markdown_to_blocks(markdown: str) -> list[str]:
    """Split markdown into blocks, keeping fenced code blocks intact."""
    blocks = []
    current_block = []
    in_code = False

    for line in markdown.split("\n"):
        stripped = line.strip()

        if stripped.startswith("```"):
            if in_code:
                current_block.append(line)
                blocks.append("\n".join(current_block))
                current_block = []
                in_code = False
            else:
                if current_block:
                    blocks.append("\n".join(current_block))
                    current_block = []
                current_block.append(line)
                in_code = True
            continue

        if not stripped and not in_code:
            if current_block:
                blocks.append("\n".join(current_block))
                current_block = []
            continue

        current_block.append(line)

    if current_block:
        blocks.append("\n".join(current_block))

    return [b for b in blocks if b.strip()]


def markdown_to_html_node(markdown: str) -> ParentNode:
    blocks = markdown_to_blocks(markdown)
    new_blocks = []

    for block in blocks:
        block_type = block_to_block_type(block)
        tag = block_type.value
        text, tag = strip_block_markdowns(block, tag)

        if tag in ("ul", "ol"):
            parent = ParentNode(tag, text)
        elif tag == "code":
            parent = ParentNode(
                "pre",
                [
                    ParentNode(
                        tag, [text_node_to_html_node(TextNode(text, TextType.TEXT))]
                    )
                ],
            )
        else:
            parent = ParentNode(tag, text_to_children(text))

        new_blocks.append(parent)

    return ParentNode("div", new_blocks)


def strip_block_markdowns(text: str, tag: str):
    if not text:
        raise Exception("block text is empty")

    match tag:
        case "h":
            for i in range(1, 7):
                if text.startswith("#" * i + " "):
                    return text[i + 1 :].strip(), f"h{i}"
            raise Exception("heading parsing failed")

        case "p":
            # Join lines but keep it as one paragraph
            lines = [line.strip() for line in text.split("\n") if line.strip()]
            return " ".join(lines), tag

        case "ul":
            items = []
            for line in text.split("\n"):
                line = line.strip()
                if line.startswith(("- ", "* ")):
                    items.append(ParentNode("li", text_to_children(line[2:].strip())))
            return items, tag

        case "ol":
            items = []
            for line in text.split("\n"):
                line = line.strip()
                if re.match(r"^\d+\.\s", line):
                    content = re.sub(r"^\d+\.\s", "", line)
                    items.append(ParentNode("li", text_to_children(content)))
            return items, tag

        case "code":
            lines = text.split("\n")
            if lines and lines[0].strip().startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].strip().startswith("```"):
                lines = lines[:-1]
            return "\n".join(lines), tag

        case "blockquote":
            lines = [line[1:].strip() for line in text.split("\n") if line.strip()]
            return " ".join(lines), tag

        case _:
            raise Exception(f"Unknown tag: {tag}")


def text_to_children(text: str):
    textnodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in textnodes]
