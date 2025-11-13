# pdf_parser.py
import pdfplumber
import pytesseract
from PIL import Image
import io
import re
import os
from base_models import ParsedDocument


class PDFParser:
    def __init__(self, enable_ocr=True):
        self.ocr_enabled = enable_ocr

    def parse_pdf(self, file_path: str, doc_id: str) -> ParsedDocument:
        """
        解析PDF文档，区分文本型和扫描型
        """
        content = ""
        tables = []
        images = []
        structure = {"sections": []}
        metadata = {}

        try:
            # 尝试作为文本型PDF解析
            with pdfplumber.open(file_path) as pdf:
                # 提取元数据
                metadata = self._extract_metadata(pdf, file_path)

                # 提取文本内容
                content = self._extract_text(pdf)

                # 提取表格
                tables = self._extract_tables(pdf)

                # 提取文档结构
                structure = self._extract_structure(content)

                # 如果文本内容过少，可能是扫描型PDF，启用OCR
                if len(content.strip()) < 100 and self.ocr_enabled:
                    print(f"检测到扫描型PDF，启用OCR处理: {file_path}")
                    ocr_content, ocr_images = self._process_with_ocr(file_path)
                    content += "\n" + ocr_content
                    images.extend(ocr_images)

        except Exception as e:
            print(f"PDF解析错误 {file_path}: {e}")
            # 如果常规解析失败，尝试OCR
            if self.ocr_enabled:
                content, images = self._process_with_ocr(file_path)

        return ParsedDocument(
            doc_id=doc_id,
            doc_type="pdf",
            source_path=file_path,
            content=content,
            metadata=metadata,
            tables=tables,
            images=images,
            structure=structure
        )

    def _extract_metadata(self, pdf, file_path: str) -> Dict:
        """提取PDF元数据"""
        metadata = {
            "filename": os.path.basename(file_path),
            "file_size": os.path.getsize(file_path),
            "page_count": len(pdf.pages) if hasattr(pdf, 'pages') else 0
        }
        try:
            if hasattr(pdf, 'metadata') and pdf.metadata:
                metadata.update({
                    "title": pdf.metadata.get('Title', ''),
                    "author": pdf.metadata.get('Author', ''),
                    "subject": pdf.metadata.get('Subject', ''),
                    "creator": pdf.metadata.get('Creator', ''),
                    "producer": pdf.metadata.get('Producer', ''),
                    "creation_date": str(pdf.metadata.get('CreationDate', '')),
                    "modification_date": str(pdf.metadata.get('ModDate', ''))
                })
        except Exception as e:
            print(f"元数据提取失败: {e}")

        return metadata

    def _extract_text(self, pdf) -> str:
        """提取PDF文本内容"""
        content_parts = []
        for page_num, page in enumerate(pdf.pages):
            try:
                text = page.extract_text()
                if text and text.strip():
                    content_parts.append(f"=== 第{page_num + 1}页 ===\n{text}")
            except Exception as e:
                print(f"第{page_num + 1}页文本提取失败: {e}")
                continue
        return "\n\n".join(content_parts)

    def _extract_tables(self, pdf) -> List[Dict]:
        """提取PDF表格数据"""
        tables = []
        for page_num, page in enumerate(pdf.pages):
            try:
                page_tables = page.extract_tables()
                for table_num, table in enumerate(page_tables):
                    if table and any(any(cell for cell in row) for row in table):
                        # 清理表格数据
                        cleaned_table = []
                        for row in table:
                            cleaned_row = [str(cell).strip() if cell is not None else "" for cell in row]
                            if any(cleaned_row):  # 只保留非空行
                                cleaned_table.append(cleaned_row)

                        if cleaned_table:
                            structured_table = {
                                "page": page_num + 1,
                                "table_index": table_num,
                                "header": cleaned_table[0] if cleaned_table else [],
                                "rows": cleaned_table[1:] if len(cleaned_table) > 1 else []
                            }
                            tables.append(structured_table)
            except Exception as e:
                print(f"第{page_num + 1}页表格提取失败: {e}")
                continue
        return tables

    def _extract_structure(self, content: str) -> Dict:
        """提取文档结构信息"""
        sections = []
        lines = content.split('\n')

        for i, line in enumerate(lines):
            line = line.strip()
            # 检测章节标题（金融文档常见的章节格式）
            if (re.match(r'^第[一二三四五六七八九十]+章', line) or
                    re.match(r'^[0-9]+\.[0-9]*', line) or
                    re.match(r'^[一二三四五六七八九十]+、', line) or
                    (len(line) < 50 and any(keyword in line for keyword in
                                            ['总则', '定义', '条款', '条例', '规定', '通知', '办法', '章节', '目录']))):
                sections.append({
                    "title": line,
                    "start": i,
                    "end": min(i + 10, len(lines) - 1)
                })

        return {"sections": sections}

    def _process_with_ocr(self, file_path: str):
        """使用OCR处理扫描型PDF"""
        content_parts = []
        images = []

        try:
            with pdfplumber.open(file_path) as pdf:
                for page_num, page in enumerate(pdf.pages):
                    try:
                        # 提取页面图像进行OCR
                        page_image = page.to_image()
                        img_bytes = io.BytesIO()
                        page_image.save(img_bytes, format='PNG')

                        # OCR处理
                        ocr_text = pytesseract.image_to_string(
                            Image.open(img_bytes),
                            lang='chi_sim+eng'
                        )

                        if ocr_text.strip():
                            content_parts.append(f"=== 第{page_num + 1}页(OCR) ===\n{ocr_text}")

                            # 存储图像信息
                            images.append({
                                "type": "page_image",
                                "description": f"第{page_num + 1}页扫描图像",
                                "extracted_text": ocr_text[:500],
                                "page": page_num + 1
                            })
                    except Exception as e:
                        print(f"第{page_num + 1}页OCR处理失败: {e}")
                        continue
        except Exception as e:
            print(f"OCR处理失败 {file_path}: {e}")

        return "\n\n".join(content_parts), images

    def parse_image(self, file_path: str, doc_id: str) -> ParsedDocument:
        """解析图像文件"""
        try:
            # OCR处理
            ocr_text = pytesseract.image_to_string(
                Image.open(file_path),
                lang='chi_sim+eng'
            )

            return ParsedDocument(
                doc_id=doc_id,
                doc_type="image",
                source_path=file_path,
                content=ocr_text,
                metadata={
                    "filename": os.path.basename(file_path),
                    "file_size": os.path.getsize(file_path)
                },
                images=[{
                    "type": "original",
                    "description": "原始图像",
                    "extracted_text": ocr_text
                }]
            )
        except Exception as e:
            print(f"图像解析错误 {file_path}: {e}")
            return ParsedDocument(
                doc_id=doc_id,
                doc_type="image",
                source_path=file_path,
                content=f"图像解析失败: {file_path}",
                metadata={"error": True}
            )