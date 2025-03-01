import unittest

from htmlnode import HTMLNode, LeafNode


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







if __name__ == "__main__":
    unittest.main()