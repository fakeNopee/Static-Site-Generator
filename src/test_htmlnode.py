import unittest

from htmlnode import *



class TestHTMLNode(unittest.TestCase):
    def test_str(self):
        
        joe = HTMLNode(props={
            "href": "https://www.google.com",
            "target": "_blank",
        })

        coc = HTMLNode(props=joe)


        self.assertTrue(coc.props)
        self.assertFalse(coc.children)
        self.assertIsNone(coc.value)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
        
        anode = LeafNode("a", "Click me!", props ={
            "href": "https://www.google.com"
            }) 

        self.assertEqual(anode.to_html(),'<a href="https://www.google.com">Click me!</a>' )
        

    def test_parent(self):

        node = ParentNode(
        "p",
        [
        LeafNode("b", "Bold text"),
        LeafNode(None, "Normal text"),
        LeafNode("i", "italic text"),
        LeafNode(None, "Normal text"),
        ],
    )

        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")


    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )


    if __name__ == "__main__":
        unittest.main()

            