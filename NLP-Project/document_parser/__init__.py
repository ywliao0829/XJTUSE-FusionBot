"""
金融多模态知识库项目 - 文档解析模块
"""

__version__ = "1.0.0"
__author__ = "文档解析团队"

from .base_models import ParsedDocument
from .pdf_parser import PDFParser
from .office_parser import OfficeParser
from .main_parser import DocumentParser

__all__ = [
    "ParsedDocument",
    "PDFParser",
    "OfficeParser",
    "DocumentParser"
]