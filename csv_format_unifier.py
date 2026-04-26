#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CSV文件格式统一工具
将字段内的英文逗号替换为中文逗号，避免错误分段
"""

import csv
import argparse
import sys
from datetime import datetime


def parse_csv_line(line):
    """手动解析CSV行，处理带引号的字段"""
    fields = []
    current_field = []
    in_quotes = False
    i = 0
    while i < len(line):
        char = line[i]
        if char == '"':
            if in_quotes:
                if i + 1 < len(line) and line[i + 1] == '"':
                    # 处理双引号转义
                    current_field.append('"')
                    i += 1
                else:
                    # 结束引号
                    in_quotes = False
            else:
                # 开始引号
                in_quotes = True
        elif char == ',' and not in_quotes:
            # 字段分隔符
            fields.append(''.join(current_field))
            current_field = []
        else:
            # 普通字符
            current_field.append(char)
        i += 1
    # 添加最后一个字段
    fields.append(''.join(current_field))
    return fields


def format_field(field):
    """格式化字段，将英文逗号替换为中文逗号"""
    if not field:
        return field
    # 将英文逗号替换为中文逗号
    field = field.replace(',', '，')
    return field


def unify_csv_format(input_file, output_file, delimiter=',', encoding='utf-8'):
    """统一CSV文件格式"""
    print(f"开始处理文件: {input_file}")
    print(f"输出文件: {output_file}")
    
    total_lines = 0
    processed_fields = 0
    
    try:
        with open(input_file, 'r', encoding=encoding) as infile, \
             open(output_file, 'w', encoding=encoding, newline='') as outfile:
            
            # 读取第一行
            line = infile.readline().rstrip('\r\n')
            if not line:
                print("错误: 文件为空")
                return False
            
            # 解析表头
            headers = parse_csv_line(line)
            total_lines += 1
            
            # 处理表头
            processed_headers = [format_field(h) for h in headers]
            writer = csv.writer(outfile, quoting=csv.QUOTE_MINIMAL)
            writer.writerow(processed_headers)
            
            # 处理数据行
            for line in infile:
                line = line.rstrip('\r\n')
                if not line:
                    continue
                total_lines += 1
                
                # 解析行
                fields = parse_csv_line(line)
                
                # 处理每个字段
                processed_fields_list = []
                for field in fields:
                    processed_field = format_field(field)
                    processed_fields_list.append(processed_field)
                    if field != processed_field:
                        processed_fields += 1
                
                # 写入处理后的行
                writer.writerow(processed_fields_list)
        
        print("\n===== CSV格式统一报告 =====")
        print(f"处理时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"输入文件: {input_file}")
        print(f"输出文件: {output_file}")
        print(f"处理行数: {total_lines}")
        print(f"处理字段数: {processed_fields}")
        print("===========================")
        
        return True
        
    except Exception as e:
        print(f"处理失败: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description='CSV文件格式统一工具 - 将字段内英文逗号替换为中文逗号')
    parser.add_argument('input_files', nargs='+', help='要处理的CSV文件路径')
    parser.add_argument('-o', '--output', required=True, help='输出文件路径')
    parser.add_argument('-d', '--delimiter', default=',', help='CSV分隔符 (默认: ,)')
    parser.add_argument('-e', '--encoding', default='utf-8', help='文件编码 (默认: utf-8)')
    
    args = parser.parse_args()
    
    if len(args.input_files) > 1:
        print("错误: 一次只能处理一个文件")
        sys.exit(1)
    
    success = unify_csv_format(args.input_files[0], args.output, args.delimiter, args.encoding)
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
