from enum import Enum


class BlockType(Enum):
    paragraph = "p"
    heading = "h"
    code = "code"
    quote = "blockquote"
    unordered_list = "ul"
    ordered_list = "ol"


def block_to_block_type(block: str) -> BlockType:
    if not block or not block.strip():
        return BlockType.paragraph

    lines = block.split("\n")
    stripped_lines = [line.strip() for line in lines if line.strip()]
    first_line = stripped_lines[0] if stripped_lines else ""

    if first_line.startswith("```") and block.rstrip().endswith("```"):
        return BlockType.code

    if first_line.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.heading

    if stripped_lines and all(line.startswith(">") for line in stripped_lines):
        return BlockType.quote

    if stripped_lines and all(line.startswith(("- ", "* ")) for line in stripped_lines):
        return BlockType.unordered_list

    import re

    ordered = True
    expected = 1
    for line in stripped_lines:
        match = re.match(r"^(\d+)\.\s", line)
        if not match or int(match.group(1)) != expected:
            ordered = False
            break
        expected += 1
    if ordered and expected > 1:
        return BlockType.ordered_list

    return BlockType.paragraph
