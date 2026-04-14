import unittest
from markdown_to_html_node import markdown_to_html_node


class TestMarkdownToHTML(unittest.TestCase):


    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )



    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )



    def test_list(self):
        md = """
1. list
2. lost
3. last


- i
- forgor
- how to do stuff
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>list</li><li>lost</li><li>last</li></ol><ul><li>i</li><li>forgor</li><li>how to do stuff</li></ul></div>"
        )



    def test_blockquote(self):
        md = """
>For 60 years, WWF has worked to help people and nature thrive. As the world's leading conservation organization, WWF works 
>in nearly 100 countries. At every level, we collaborate with people around the world to develop and deliver innovative 
>solutions that protect communities, wildlife, and the places in which they live.
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
"<div><blockquote>For 60 years, WWF has worked to help people and nature thrive. As the world's leading conservation organization, WWF works in nearly 100 countries. At every level, we collaborate with people around the world to develop and deliver innovative solutions that protect communities, wildlife, and the places in which they live.</blockquote></div>"
        )

    def test_headlines(self):

        md = """
### test h3

# test h1

###### test h6


####### h7?

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
"<div><h3>test h3</h3><h1>test h1</h1><h6>test h6</h6><p>####### h7?</p></div>"
        )