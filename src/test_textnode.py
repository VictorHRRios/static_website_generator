import unittest

from textnode import TextNode, TextType, BlockType
from split_nodes import split_nodes_delimiter, split_nodes_image, split_nodes_link, markdown_to_blocks, block_to_block_type


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    def test_eq_false(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)
    def test_eq_false_2(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node2", TextType.BOLD)
        self.assertNotEqual(node, node2)
    def test_repr(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(f"TextNode(This is a text node, bold, None)",
                         repr(node))
class TextTextNodeSplitNodes(unittest.TestCase):
    def test_code_center(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(repr(new_nodes[0]), f"TextNode(This is text with a , text, None)")
        self.assertEqual(repr(new_nodes[1]), f"TextNode(code block, code, None)")
        self.assertEqual(repr(new_nodes[2]), f"TextNode( word, text, None)")
    def test_code_left(self):
        node = TextNode("**This is text** with a code block word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(repr(new_nodes[0]), f"TextNode(This is text, bold, None)")
        self.assertEqual(repr(new_nodes[1]), f"TextNode( with a code block word, text, None)")
    def test_code_right(self):
        node = TextNode("This is text with a code block **word**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(repr(new_nodes[0]), f"TextNode(This is text with a code block , text, None)")
        self.assertEqual(repr(new_nodes[1]), f"TextNode(word, bold, None)")

    def test_code_err_no_closing(self):
        node = TextNode("This is text with a code block **word", TextType.TEXT)
        #new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertRaises(Exception, split_nodes_delimiter, ([node], "**", TextType.BOLD))
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGES, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGES, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGES, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGES, "https://www.example.COM/IMAGE.PNG"),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGES, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGES, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINKS, "https://boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("another link", TextType.LINKS, "https://blog.boot.dev"),
                TextNode(" with text that follows", TextType.TEXT),
            ],
            new_nodes,
        )
    def test_split(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGES, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINKS, "https://boot.dev"),
        ]
class TextMarkDownToBlocks(unittest.TestCase):
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


class BlockToBlockType(unittest.TestCase):
    def test_block_code(self):
        md = """
    This is **bolded** paragraph

    This is another paragraph with _italic_ text and `code` here
    This is the same paragraph on a new line

    ```
    This is a list
    with items
    ```
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            block_to_block_type(blocks[0]), BlockType.PARAGRAPH,
        )
        self.assertEqual(
            block_to_block_type(blocks[1]), BlockType.PARAGRAPH,
        )
        self.assertEqual(
            block_to_block_type(blocks[2]), BlockType.CODE
        )

    def test_block_quote(self):
        md = """
    This is **bolded** paragraph

    This is another paragraph with _italic_ text and `code` here
    This is the same paragraph on a new line

    > This is a list
    > with items
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            block_to_block_type(blocks[0]), BlockType.PARAGRAPH,
        )
        self.assertEqual(
            block_to_block_type(blocks[1]), BlockType.PARAGRAPH,
        )
        self.assertEqual(
            block_to_block_type(blocks[2]), BlockType.QUOTE
        )

    def test_block_heading(self):
        md = """
    ##### EJEMPLO

    This is **bolded** paragraph

    This is another paragraph with _italic_ text and `code` here
    This is the same paragraph on a new line
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            block_to_block_type(blocks[0]), BlockType.HEADING,
        )
        self.assertEqual(
            block_to_block_type(blocks[1]), BlockType.PARAGRAPH,
        )
        self.assertEqual(
            block_to_block_type(blocks[2]), BlockType.PARAGRAPH
        )



if __name__ == "__main__":
    unittest.main()