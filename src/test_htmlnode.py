import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_props(self):
        node = HTMLNode("p", 'Hello', None, {"href": "https://www.google.com",
                                             "target": "_blank",})
        self.assertEqual(f' href="https://www.google.com" target="_blank"' ,node.props_to_html())

    def test_repr(self):
        node = HTMLNode("p", 'Hello', None, {"href": "https://www.google.com"})
        self.assertEqual(f'HTMLNode({node.tag}, {node.value}, {node.children}, {node.props})' ,repr(node))
    def test_props_empty(self):
        node = HTMLNode("p", 'Hello', None, None)
        self.assertEqual(f'' ,node.props_to_html())
    def test_props_empty_2(self):
        node = HTMLNode("p", 'Hello', None, {"href" : ""})
        self.assertEqual(f' href=""' ,node.props_to_html())
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    def test_leaf_to_html_a_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com", 
                                           "target": "_blank",})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com" target="_blank">Click me!</a>')
    def test_leaf_no_tag(self):
        node = LeafNode(None, "Hello")
        self.assertEqual("Hello", node.to_html())

class TestTextNodeChildren(unittest.TestCase):

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
    def test_to_html_no_children(self):
        parent_node = ParentNode("div", None)
        self.assertRaises(ValueError, parent_node.to_html)
    def test_to_html_no_tag(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(None, [child_node])
        self.assertRaises(ValueError, parent_node.to_html)

class TestTextNodeToHtmlNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'b')
        self.assertEqual(html_node.value, "This is a text node")

    def test_italic(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'i')
        self.assertEqual(html_node.value, "This is a text node")

    def test_code(self):
        node = TextNode("This is a text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'code')
        self.assertEqual(html_node.value, "This is a text node")

    def test_link(self):
        node = TextNode("This is a text node", TextType.LINKS, "google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'a')
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props_to_html(), ' href="google.com"')

    def test_image(self):
        node = TextNode("This is a text node", TextType.IMAGES, "https:google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'img')
        self.assertEqual(html_node.value, '')
        self.assertEqual(html_node.props_to_html(), ' src="https:google.com" alt="This is a text node"')
 



if __name__ == "__main__":
    unittest.main()