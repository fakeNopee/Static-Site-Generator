from split_nodes_delimiter import *
from blocktype import *
from htmlnode import *
from textnode import text_node_to_html_node

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)

    new_blocks= []
    for block in blocks:
        tag = block_to_block_type(block).value
        text, tag = strip_block_markdowns(block, tag)
        if tag == "ul" or tag == "ol":
            parent = ParentNode(tag, text)
            new_blocks.append(parent)
            continue
        if tag == "code":
            parent = ParentNode("pre", [ParentNode(tag, [text_node_to_html_node(TextNode(text, TextType.TEXT))])])
            new_blocks.append(parent)
            continue
        parent = ParentNode(tag, text_to_children(text))
        new_blocks.append(parent)
    return ParentNode("div", new_blocks)







def strip_block_markdowns(text, tag):
    if text == "":
        raise Exception("block text is empty")
    
    match tag:
        
        
        case "h":
            for i in range(7):
                if text[i] == " ":
                    tag = f"h{i}"
                    return text[i+1:], tag
            raise Exception("h loop fail")
        
        
        case "p":
            stripped = text.split("\n")
            fixed = []
            for strip in stripped:
                fixed.append(strip.strip())
            stripped = " ".join(fixed)
            return stripped, tag
        
        
        case "ul":
            splitted = text.split("\n")
            new_text = []
            for new_line in splitted:
                if new_line == "":
                    continue
                line = new_line[2:]
                new_text.append(ParentNode("li", text_to_children(line)))
                
            return new_text, tag
        
        
        case "ol":
            splitted = text.split("\n")
            new_text = []
            i = 1
            for new_line in splitted:
                if new_line == "":
                    continue
                line = new_line.replace(f"{i}. ", "", 1)
                i+= 1
                new_text.append(ParentNode("li", text_to_children(line)))
            return new_text, tag
        
        
        case "code":
            stripped = text.split("\n")
            fixed = []
            for strip in stripped:
                if strip.strip() == "":
                    continue
                fixed.append(strip.strip())
            fixed.append("")
            text = "\n".join(fixed)
            return text[4:-4], tag
        
        
        case "blockquote":
            new_text = text.split("\n")
            fixed = []
            for new in new_text:
                fixed.append(new[1:])
            new_text = "".join(fixed)
            return new_text.strip(), tag
                
        case _:
            raise Exception("tag not found")

    



def text_to_children(text):
    textnodes = text_to_textnodes(text)
    leafnodes = []
    for textnode in textnodes:
        leafnodes.append(text_node_to_html_node(textnode))
    return leafnodes
