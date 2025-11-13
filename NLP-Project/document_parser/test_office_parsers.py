# test_office_parsers.py
import unittest
import os
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from base_models import ParsedDocument
from office_parser import OfficeParser


class TestOfficeParser(unittest.TestCase):
    def setUp(self):
        self.parser = OfficeParser()

    def test_office_parser_creation(self):
        """测试Office解析器创建"""
        self.assertIsNotNone(self.parser)

    def test_error_handling(self):
        """测试错误处理"""
        # 测试不存在的文件
        result = self.parser.parse_word("nonexistent.docx", "DOC_ERROR_001")
        self.assertEqual(result.doc_type, "word")
        self.assertTrue("错误" in result.content or "失败" in result.content)

        result = self.parser.parse_excel("nonexistent.xlsx", "DOC_ERROR_002")
        self.assertEqual(result.doc_type, "excel")

        result = self.parser.parse_ppt("nonexistent.pptx", "DOC_ERROR_003")
        self.assertEqual(result.doc_type, "ppt")


if __name__ == '__main__':
    unittest.main()