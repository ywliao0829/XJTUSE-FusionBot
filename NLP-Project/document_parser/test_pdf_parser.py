# test_pdf_parser.py
import unittest
import os
import sys
import tempfile

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from base_models import ParsedDocument
from pdf_parser import PDFParser


class TestPDFParser(unittest.TestCase):
    def setUp(self):
        self.parser = PDFParser(enable_ocr=False)

    def test_parsedocument_creation(self):
        """测试ParsedDocument对象创建"""
        doc = ParsedDocument(
            doc_id="DOC_TEST_001",
            doc_type="pdf",
            source_path="/test/path.pdf",
            content="测试内容",
            metadata={"title": "测试文档"},
            tables=[{"header": ["列1"], "rows": [["数据1"]]}],
            structure={"sections": []}
        )

        self.assertEqual(doc.doc_id, "DOC_TEST_001")
        self.assertEqual(doc.doc_type, "pdf")
        self.assertEqual(doc.content, "测试内容")
        self.assertIsInstance(doc.to_dict(), dict)

        # 测试字典转换
        doc_dict = doc.to_dict()
        self.assertIn("doc_id", doc_dict)
        self.assertIn("content", doc_dict)
        self.assertIn("metadata", doc_dict)

    def test_pdf_parser_initialization(self):
        """测试PDF解析器初始化"""
        self.assertIsNotNone(self.parser)
        self.assertEqual(self.parser.ocr_enabled, False)

        # 测试启用OCR的解析器
        parser_with_ocr = PDFParser(enable_ocr=True)
        self.assertEqual(parser_with_ocr.ocr_enabled, True)

    def test_error_handling(self):
        """测试错误处理"""
        # 测试不存在的文件
        result = self.parser.parse_pdf("nonexistent.pdf", "DOC_ERROR_001")
        self.assertEqual(result.doc_type, "pdf")
        # 应该包含错误信息


if __name__ == '__main__':
    unittest.main()