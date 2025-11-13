# base_models.py
from typing import List, Dict, Optional


class ParsedDocument:
    """单个文档的解析结果"""

    def __init__(self, doc_id: str, doc_type: str, source_path: str, content: str,
                 metadata: Optional[Dict] = None, tables: Optional[List[Dict]] = None,
                 images: Optional[List[Dict]] = None, structure: Optional[Dict] = None):
        self.doc_id = doc_id
        self.doc_type = doc_type
        self.source_path = source_path
        self.content = content
        self.metadata = metadata or {}
        self.tables = tables or []
        self.images = images or []
        self.structure = structure or {}

    def to_dict(self):
        """转换为字典格式，便于JSON序列化"""
        return {
            "doc_id": self.doc_id,
            "doc_type": self.doc_type,
            "source_path": self.source_path,
            "content": self.content,
            "metadata": self.metadata,
            "tables": self.tables,
            "images": self.images,
            "structure": self.structure
        }

    def __repr__(self):
        return f"ParsedDocument(doc_id={self.doc_id}, type={self.doc_type}, content_length={len(self.content)})"

    def __str__(self):
        return f"文档ID: {self.doc_id}, 类型: {self.doc_type}, 内容长度: {len(self.content)} 字符"