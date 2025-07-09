import unittest

from src.markdown_to_html import markdown_to_html_node

class TestMarkDownToHtml(unittest.TestCase):
    def test_markdown_to_html_converts_markdown(self):

        self.assertFalse(False)

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph text in a p tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_code_block(self):
        md = """
```This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_unordered_list_block(self):
        md = """- **The Gift of Rebirth**: Glorfindel's return to Middle-earth after his heroic demise is a profound testament to his worth, as the Valar saw fit to restore him to life, laden with greater wisdom and power.
- **The Role of a Guide**: Serving as an advisor and protector in Rivendell, his presence provided not only counsel but a formidable bulwark against dark forces."""
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(html,
        """<div><ul><li><b>The Gift of Rebirth</b>: Glorfindel's return to Middle-earth after his heroic demise is a profound testament to his worth, as the Valar saw fit to restore him to life, laden with greater wisdom and power.</li><li><b>The Role of a Guide</b>: Serving as an advisor and protector in Rivendell, his presence provided not only counsel but a formidable bulwark against dark forces.</li></ul></div>"""
                         )
