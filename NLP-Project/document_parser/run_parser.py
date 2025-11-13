# run_parser.py
# !/usr/bin/env python3
"""
文档解析模块 - 主运行文件
"""
import os
import sys
import argparse

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main_parser import DocumentParser


def main():
    parser = argparse.ArgumentParser(description='金融文档解析器')
    parser.add_argument('--input', '-i', required=True, help='输入文档目录路径')
    parser.add_argument('--output', '-o', default='parsed_docs.json', help='输出JSON文件路径')
    parser.add_argument('--disable-ocr', action='store_true', help='禁用OCR功能')

    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"错误: 输入目录不存在: {args.input}")
        return

    # 初始化解析器
    document_parser = DocumentParser(enable_ocr=not args.disable_ocr)

    print(f"开始解析文档目录: {args.input}")
    print(f"输出文件: {args.output}")
    print(f"OCR功能: {'启用' if not args.disable_ocr else '禁用'}")
    print("-" * 50)

    # 执行批量解析
    results = document_parser.batch_parse(args.input, args.output)

    print("-" * 50)
    print(f"解析完成! 共处理 {len(results)} 个文档")


if __name__ == "__main__":
    main()