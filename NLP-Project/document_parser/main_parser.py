# main_parser.py
import os
import json
from typing import List
from pdf_parser import PDFParser
from office_parser import OfficeParser
from base_models import ParsedDocument


class DocumentParser:
    def __init__(self, enable_ocr=True):
        self.pdf_parser = PDFParser(enable_ocr=enable_ocr)
        self.office_parser = OfficeParser()

    def parse_document(self, file_path: str, doc_id: str) -> ParsedDocument:
        """根据文件类型分发给相应的解析器"""
        if not os.path.exists(file_path):
            return self._create_not_found_document(doc_id, file_path)

        ext = os.path.splitext(file_path)[1].lower()

        if ext == '.pdf':
            return self.pdf_parser.parse_pdf(file_path, doc_id)
        elif ext in ['.doc', '.docx']:
            return self.office_parser.parse_word(file_path, doc_id)
        elif ext in ['.xls', '.xlsx']:
            return self.office_parser.parse_excel(file_path, doc_id)
        elif ext in ['.ppt', '.pptx']:
            return self.office_parser.parse_ppt(file_path, doc_id)
        elif ext in ['.png', '.jpg', '.jpeg']:
            return self.pdf_parser.parse_image(file_path, doc_id)
        elif ext in ['.txt', '.md']:
            return self._parse_text_file(file_path, doc_id)
        else:
            return self._create_unsupported_document(doc_id, file_path, ext)

    def batch_parse(self, input_dir: str, output_file: str = "parsed_docs.json") -> List[dict]:
        """批量解析目录中的所有文档"""
        parsed_documents = []

        if not os.path.exists(input_dir):
            print(f"输入目录不存在: {input_dir}")
            return []

        # 遍历目录中的所有文件
        for root, dirs, files in os.walk(input_dir):
            for filename in files:
                if not self._is_supported_file(filename):
                    continue

                file_path = os.path.join(root, filename)
                doc_id = f"DOC_{len(parsed_documents) + 1:03d}"

                print(f"正在解析: {filename} -> {doc_id}")

                # 解析文档
                parsed_doc = self.parse_document(file_path, doc_id)
                parsed_documents.append(parsed_doc.to_dict())

        # 保存结果
        self._save_results(parsed_documents, output_file)

        print(f"解析完成! 共处理 {len(parsed_documents)} 个文档，结果保存至: {output_file}")
        return parsed_documents

    def _is_supported_file(self, filename: str) -> bool:
        """检查文件是否支持解析"""
        supported_extensions = [
            '.pdf', '.doc', '.docx', '.xls', '.xlsx',
            '.ppt', '.pptx', '.png', '.jpg', '.jpeg',
            '.txt', '.md'
        ]
        return any(filename.lower().endswith(ext) for ext in supported_extensions)

    def _parse_text_file(self, file_path: str, doc_id: str) -> ParsedDocument:
        """解析文本文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            return ParsedDocument(
                doc_id=doc_id,
                doc_type="txt",
                source_path=file_path,
                content=content,
                metadata={
                    "filename": os.path.basename(file_path),
                    "file_size": os.path.getsize(file_path)
                }
            )
        except UnicodeDecodeError:
            try:
                with open(file_path, 'r', encoding='gbk') as f:
                    content = f.read()

                return ParsedDocument(
                    doc_id=doc_id,
                    doc_type="txt",
                    source_path=file_path,
                    content=content,
                    metadata={
                        "filename": os.path.basename(file_path),
                        "file_size": os.path.getsize(file_path),
                        "encoding": "gbk"
                    }
                )
            except Exception as e:
                print(f"文本文件解析错误 {file_path}: {e}")
                return self._create_error_document(doc_id, file_path, "txt")
        except Exception as e:
            print(f"文本文件解析错误 {file_path}: {e}")
            return self._create_error_document(doc_id, file_path, "txt")

    def _save_results(self, documents: List[dict], output_file: str):
        """保存解析结果"""
        try:
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(documents, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存结果失败: {e}")

    def _create_error_document(self, doc_id: str, file_path: str, doc_type: str) -> ParsedDocument:
        """创建错误文档"""
        return ParsedDocument(
            doc_id=doc_id,
            doc_type=doc_type,
            source_path=file_path,
            content=f"文档解析失败: {file_path}",
            metadata={"error": True}
        )

    def _create_not_found_document(self, doc_id: str, file_path: str) -> ParsedDocument:
        """创建文件未找到文档"""
        return ParsedDocument(
            doc_id=doc_id,
            doc_type="unknown",
            source_path=file_path,
            content=f"文件未找到: {file_path}",
            metadata={"error": "file_not_found"}
        )

    def _create_unsupported_document(self, doc_id: str, file_path: str, ext: str) -> ParsedDocument:
        """创建不支持格式文档"""
        return ParsedDocument(
            doc_id=doc_id,
            doc_type="unsupported",
            source_path=file_path,
            content=f"不支持的文件格式: {ext}",
            metadata={"error": "unsupported_format"}
        )