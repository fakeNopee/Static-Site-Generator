from enum import Enum




class BlockType(Enum):
    
    paragraph = "p"
    heading = "h"
    code = "code"
    quote = "blockquote"
    unordered_list = "ul"
    ordered_list = "ol"


def block_to_block_type(block):

    heading = False
    if block[:7] == "#######":
        return BlockType.paragraph
    for i in range(7):
        if i < len(block):
            if "\n" in block:
                break
            if block[i] == "#":
                heading = True
            elif block[i] == " ":
                break
            else:
                heading = False
                break
    if heading:
        return BlockType.heading

    if block[:4] == "```\n" or block[:4] == "\n```" and block[-3:] == "```" or block[-4:] == "```\n":
        return BlockType.code



    quote = False
    new = block.split("\n")
    for stuff in new:
        if stuff == "":
            continue
        if stuff[0] != ">":
            quote = False
            break
        quote = True
  
    if quote:
        return BlockType.quote
    
    
    unordered = False
    for stuff in new:
        if stuff == "":
            continue
        if stuff[0:2] != "- ":
            unordered = False
            break
        unordered = True
  
    if unordered:
        return BlockType.unordered_list

    
    ordered_list = False
    counter = 1
    for stuff in new:
        if stuff == "":
            continue
        if stuff[0:2] != f"{counter}.":
            ordered_list = False
            break
        counter += 1
        ordered_list = True

    if ordered_list:
        return BlockType.ordered_list

    return BlockType.paragraph 



block = '''```
stuff and stuff
testing something
what is this
still ordered
```'''

print(block[0:5] == "```\n")

