timport unittest

from split_nodes_delimiter import *
from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        node3 = TextNode("boogoa", TextType.LINK, "uruuruarale")
        self.assertEqual(node, node2)
        self.assertNotEqual(node, node3)

    def test_url(self):
        doi = TextNode("bingus", TextType.BOLD, "randomurl")
        boi = TextNode("i try", TextType.BOLD)
        self.assertNotEqual(boi.url, doi.url)
        self.assertEqual(boi.url, None)
        self.assertEqual(boi.text_type, TextType.BOLD)

    def test_text(self):
        text = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(text)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

        bold = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html_node(bold)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.to_html(), "<b>This is a text node</b>")

        italic = TextNode("This is a text node", TextType.ITALIC)
        html_node = text_node_to_html_node(italic)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.to_html(), "<i>This is a text node</i>")

        code = TextNode("This is a text node", TextType.CODE)
        html_node = text_node_to_html_node(code)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.to_html(), "<code>This is a text node</code>")

        link = TextNode("This is a text node", TextType.LINK, "com.url.httlps")
        html_node = text_node_to_html_node(link)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.to_html(), '<a href="com.url.httlps">This is a text node</a>')

        image = TextNode("This is a text node", TextType.IMAGE, "com.url.httlps")
        html_node = text_node_to_html_node(image)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.to_html(), '<img src="com.url.httlps" alt="This is a text node">')




    def test_split_delimiters(self):

        node = TextNode("**This", TextType.TEXT)
        node2 = TextNode("**test**nothing", TextType.TEXT)
        node3 = TextNode("This **is** text with a **bold block** word", TextType.TEXT)
        node4 = TextNode("This is **text with a `code block` word", TextType.TEXT)
        node5 = TextNode("This is text with** a `code block` **word", TextType.TEXT)


        nodes = [node, node2, node3, node4, node5]

        single = split_nodes_delimiter([node2], "**", TextType.BOLD)

        group = split_nodes_delimiter(nodes, "**", TextType.BOLD)        

        self.assertEqual(single[0].text, "test")
        self.assertEqual(single[0].text_type, TextType.BOLD)
        self.assertEqual(group[-1].text, "word")

        splits = 0        
        bolds = 0
        for node in group:
            if node.text_type == TextType.BOLD:
                bolds +=1
            splits += 1
        self.assertEqual(bolds, 6)
        self.assertEqual(splits, 13)

        
    def test_markdown_link_extract(self):
        text1 = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        text2 = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)       links : [link](httspe://stuff/idc.com)                 no![t]l(ink)    idun![n](ooo)"


        matches = extract_markdown_images(text1)
        self.assertListEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], matches)
        

        matches = extract_markdown_links(text2)
        self.assertListEqual([("link", "httspe://stuff/idc.com")], matches)


    def test_split_images(self):



        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_image([node])


        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )


        node2 = TextNode(
            "![]()![](img)![notimg]notimg)![notimg)![img](url)![img]()",
            TextType.TEXT,
        )

        new_nodes = split_nodes_image([node2])

        for nodes in new_nodes:
            self.assertTrue(nodes.text != "")

    def test_split_links(self):



        node = TextNode(
            "This is text with an [not image](https://i.imgur.com/zjjcJKZ) and another [second link](https://i.imgur.com/)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_links([node])


        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("not image", TextType.LINK, "https://i.imgur.com/zjjcJKZ"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/"
                ),
            ],
            new_nodes,
        )


        node2 = TextNode(
            "[]()[](img)[notimg]notimg)[notimg)[img](url)[img]()",
            TextType.TEXT,
        )

        new_nodes = split_nodes_links([node2])

        for nodes in new_nodes:
            self.assertTrue(nodes.text != "")



    def test_text_to_nodes(self):
        example = text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")

        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ], 
            example
        )


    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )



if __name__ == "__main__":
    unittest.main()