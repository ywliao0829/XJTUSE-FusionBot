# example_usage.py
import os
import sys
import json

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main_parser import DocumentParser


def main():
    # 初始化解析器
    parser = DocumentParser(enable_ocr=True)

    # 单文档解析示例
    print("=== 单文档解析示例 ===")
    sample_file = "sample_documents/pdf_samples/sample.pdf"  # 替换为实际文件路径

    if os.path.exists(sample_file):
        try:
            result = parser.parse_document(sample_file, "DOC_001")
            print(f"解析成功: {result}")
            print(f"内容长度: {len(result.content)} 字符")
            print(f"表格数量: {len(result.tables)}")
            print(f"图像数量: {len(result.images)}")
            print(f"元数据: {result.metadata}")
        except Exception as e:
            print(f"解析失败: {e}")
    else:
        print(f"示例文件不存在: {sample_file}")
        print("请先准备测试文档")

    # 批量解析示例
    print("\n=== 批量解析示例 ===")
    input_directory = "sample_documents"  # 替换为实际目录路径
    output_file = "parsed_docs.json"

    if os.path.exists(input_directory):
        results = parser.batch_parse(input_directory, output_file)

        # 验证输出格式
        print(f"\n=== 验证输出格式 ===")
        try:
            with open(output_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            print(f"输出文件包含 {len(data)} 个文档")
            if data:
                sample_doc = data[0]
                required_fields = ['doc_id', 'doc_type', 'source_path', 'content']
                if all(field in sample_doc for field in required_fields):
                    print("✓ 输出格式符合接口规范")
                else:
                    print("✗ 输出格式不符合接口规范")

                # 显示第一个文档的摘要信息
                print(f"\n第一个文档摘要:")
                print(f"  ID: {sample_doc['doc_id']}")
                print(f"  类型: {sample_doc['doc_type']}")
                print(f"  内容预览: {sample_doc['content'][:100]}...")
        except Exception as e:
            print(f"验证失败: {e}")
    else:
        print(f"输入目录不存在: {input_directory}")
        print("请创建 sample_documents 目录并放入测试文档")


if __name__ == "__main__":
    main()