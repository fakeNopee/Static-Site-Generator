from textnode import *
import re




def split_nodes_delimiter(old_nodes, delimiter, text_type):
    result = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue
            
        result.extend(replace_markdowns(delimiter, node.text, text_type))
                     
    return result


    
def replace_markdowns(delimiter, text, text_type):

    result = []

    splitted = text.split(delimiter)
    for i in range(len(splitted)):
        if splitted[i] == "":
            continue
        if i % 2 == 0:
            result.append(TextNode(splitted[i], TextType.TEXT))
        else:
            result.append(TextNode(splitted[i], text_type))
    return result
        


def split_nodes_image(old_nodes):

    result = []

    for node in old_nodes:
        
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue
        appendindex = 0
        start = 0
        extracted = extract_markdown_images(node.text)

        if extracted == []:
            result.append(TextNode(node.text,TextType.TEXT))
            continue



        for i in range(0, len(node.text)):
            checked = False
            if node.text[i:i+2] == "![":
                for n in range(i + 2, len(node.text)):
                    if node.text[n:n+2] == "](":
                        checked = True
                        continue
                    if node.text[n] == ")" and checked:
                        ex_txt = extracted[appendindex][0]
                        ex_url = extracted[appendindex][1]
                        
                        
                        if i == 0:
                            if ex_txt != "":
                                result.append(TextNode(ex_txt, TextType.IMAGE, ex_url))
                            appendindex += 1
                            start = n + 1
                            break
                        else:
                            if node.text[start:i] != "":
                                result.append(TextNode(node.text[start:i], TextType.TEXT))
                            if ex_txt != "":
                                result.append(TextNode(ex_txt, TextType.IMAGE, url=ex_url))
                            appendindex += 1
                            start = n + 1
                            break
            
            if appendindex >= len(extracted):
                break
        if start < len(node.text):
            result.append(TextNode(node.text[start:len(node.text)], TextType.TEXT))
    
    return result






def split_nodes_links(old_nodes):
    result = []



    for node in old_nodes:


        if node.text_type != TextType.TEXT:
            result.append(node)
            continue
        extracted = extract_markdown_links(node.text)

        if len(extracted) == 0:
            result.append(TextNode(node.text, TextType.TEXT))
            continue
        sections = ["", node.text]
        for i in range(len(extracted)):

            link_txt = extracted[i][0]
            link = extracted[i][1]


            if len(sections) > 1:
                if sections[1] == "":
                    break
                sections = sections[1].split(f"[{link_txt}]({link})", 1)
            
            
            if sections[0] != "":
                result.append(TextNode(sections[0], TextType.TEXT))
            
            
            if link_txt != "":
                result.append(TextNode(link_txt, TextType.LINK, link))

            if len(sections) > 1:
                if i + 1 >= len(extracted) and sections[1] != "":
                    result.append(TextNode(sections[1], TextType.TEXT))

        
    return result    
        













def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)





def text_to_textnodes(text):
    base = TextNode(text, TextType.TEXT)

    
    
    
    nodes = split_nodes_links([base])
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    
    
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    return nodes






def markdown_to_blocks(markdown):
    splitted = markdown.split('\n\n')
    new = []
    for spit in splitted:
        new.append(spit.strip())
        
    
    return new




