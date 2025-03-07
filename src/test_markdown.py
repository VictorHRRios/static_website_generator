import unittest

from markdown import markdown_to_blocks, markdown_to_html_node

class TestTextNode(unittest.TestCase):
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

    def test_ul(self):
            md = """
        - title
        - paragraph
        - other
        """

            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(
                html,
                "<div><ul><li>title</li><li>paragraph</li><li>other</li></ul></div>",
            )

    def test_ol(self):
            md = """
        1. **title**
        2. paragraph
        3. other
        """

            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(
                html,
                "<div><ol><li><b>title</b></li><li>paragraph</li><li>other</li></ol></div>",
            )

    def test_quote(self):
            md = """
        > **title**
        > paragraph
        > other
        """

            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(
                html,
                "<div><blockquote><b>title</b> paragraph other</blockquote></div>",
            )

    def test_heading(self):
            md = """
        ## **title**

        # paragraph

        ### other
        """

            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(
                html,
                "<div><h2><b>title</b></h2><h1>paragraph</h1><h3>other</h3></div>"
            )