"""回归测试：HTML 图片和 Markdown 标题之间的块边界。"""

import unittest

from catalog_pages import section
from check_markdown import check_document


class MarkdownBoundaryTests(unittest.TestCase):
    def test_rejects_heading_swallowed_by_html_image(self):
        text = '<img src="skills.svg" alt="技能" />\n### 十二列技能图标\n\n内容\n'
        with self.assertRaisesRegex(ValueError, '标题未正确渲染'):
            check_document(text)

    def test_generated_image_sections_render_all_headings(self):
        text = section('六列技能图标', '<img src="six.svg" alt="六列" />')
        text += section('十二列技能图标', '<img src="twelve.svg" alt="十二列" />')
        check_document(text)


if __name__ == '__main__':
    unittest.main()
