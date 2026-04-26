#!/usr/bin/env python3
import os
import sys
import csv
import argparse
from datetime import datetime

class CSVMerger:
    def __init__(self, input_files, output_file, delimiter=',', encoding='utf-8'):
        self.input_files = input_files
        self.output_file = output_file
        self.delimiter = delimiter
        self.encoding = encoding
        self.results = {
            'files_processed': 0,
            'total_rows': 0,
            'errors': [],
            'warnings': []
        }
    
    def check_csv_file(self, file_path):
        """检查CSV文件的有效性"""
        try:
            with open(file_path, 'r', encoding=self.encoding, newline='') as f:
                # 使用csv.reader正确处理带引号的字段
                reader = csv.reader(f, delimiter=self.delimiter, quotechar='"')
                header = next(reader, None)
                if not header:
                    self.results['warnings'].append(f"文件 {file_path} 没有标题行")
                    return False, None
                
                # 清理标题行的空格
                header = [h.strip() for h in header]
                
                # 不再检查列数，因为用户确认表头一致，且带引号的字段可能包含逗号
                # 只检查文件是否能正常读取
                row_count = 0
                for row in reader:
                    row_count += 1
                
                return True, header
        except Exception as e:
            self.results['errors'].append(f"文件 {file_path} 读取错误: {str(e)}")
            return False, None
    
    def merge_files(self):
        """合并多个CSV文件"""
        if not self.input_files:
            print("错误: 没有提供输入文件")
            return False
        
        # 检查所有文件
        headers = []
        valid_files = []
        
        for file_path in self.input_files:
            if not os.path.exists(file_path):
                self.results['errors'].append(f"文件 {file_path} 不存在")
                continue
            
            is_valid, header = self.check_csv_file(file_path)
            if is_valid:
                headers.append(header)
                valid_files.append(file_path)
        
        if not valid_files:
            print("错误: 没有有效的CSV文件可以处理")
            return False
        
        # 使用第一个文件的标题行为标准
        first_header = headers[0]
        header_length = len(first_header)
        
        # 检查所有文件的标题行是否一致
        for i, header in enumerate(headers[1:], 1):
            if header != first_header:
                self.results['warnings'].append(f"文件 {valid_files[i]} 的标题行与第一个文件不一致")
        
        # 合并文件
        try:
            with open(self.output_file, 'w', encoding=self.encoding, newline='') as outfile:
                # 使用正确的writer配置，只对包含特殊字符的字段加引号
                writer = csv.writer(outfile, delimiter=self.delimiter, quotechar='"', quoting=csv.QUOTE_MINIMAL)
                
                # 写入标题行
                writer.writerow(first_header)
                
                # 写入数据行
                for file_path in valid_files:
                    with open(file_path, 'r', encoding=self.encoding, newline='') as infile:
                        lines = infile.readlines()
                        # 跳过标题行
                        for line in lines[1:]:
                            # 手动解析CSV行，处理带引号的字段
                            line = line.strip()
                            if not line:
                                continue
                            
                            # 解析CSV行
                            cells = []
                            current_cell = []
                            in_quote = False
                            quote_count = 0
                            
                            for char in line:
                                if char == '"':
                                    in_quote = not in_quote
                                    quote_count += 1
                                elif char == self.delimiter and not in_quote:
                                    # 完成一个单元格
                                    cell_content = ''.join(current_cell).strip()
                                    # 移除可能的引号
                                    if cell_content.startswith('"') and cell_content.endswith('"'):
                                        cell_content = cell_content[1:-1]
                                    cells.append(cell_content)
                                    current_cell = []
                                else:
                                    current_cell.append(char)
                            
                            # 添加最后一个单元格
                            if current_cell:
                                cell_content = ''.join(current_cell).strip()
                                # 移除可能的引号
                                if cell_content.startswith('"') and cell_content.endswith('"'):
                                    cell_content = cell_content[1:-1]
                                cells.append(cell_content)
                            
                            # 确保列数与标题行一致
                            if len(cells) < header_length:
                                # 填充空值
                                cells.extend([''] * (header_length - len(cells)))
                            elif len(cells) > header_length:
                                # 只在确实列数过多时才截断
                                # 但由于用户确认表头一致，这应该不会发生
                                cells = cells[:header_length]
                            
                            writer.writerow(cells)
                            self.results['total_rows'] += 1
                
                self.results['files_processed'] = len(valid_files)
                return True
        except Exception as e:
            self.results['errors'].append(f"合并文件时出错: {str(e)}")
            return False
    
    def generate_report(self):
        """生成处理报告"""
        report = []
        report.append("===== CSV文件处理报告 =====")
        report.append(f"处理时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"处理文件数: {self.results['files_processed']}")
        report.append(f"总数据行数: {self.results['total_rows']}")
        report.append(f"输出文件: {self.output_file}")
        
        if self.results['warnings']:
            report.append("\n警告:")
            for warning in self.results['warnings']:
                report.append(f"- {warning}")
        
        if self.results['errors']:
            report.append("\n错误:")
            for error in self.results['errors']:
                report.append(f"- {error}")
        
        report.append("========================")
        return '\n'.join(report)

def main():
    parser = argparse.ArgumentParser(description='CSV文件合并工具')
    parser.add_argument('input_files', nargs='+', help='要合并的CSV文件路径')
    parser.add_argument('-o', '--output', required=True, help='输出文件路径')
    parser.add_argument('-d', '--delimiter', default=',', help='CSV分隔符，默认是逗号')
    parser.add_argument('-e', '--encoding', default='utf-8', help='文件编码，默认是utf-8')
    
    args = parser.parse_args()
    
    merger = CSVMerger(
        input_files=args.input_files,
        output_file=args.output,
        delimiter=args.delimiter,
        encoding=args.encoding
    )
    
    success = merger.merge_files()
    report = merger.generate_report()
    
    print(report)
    
    if not success:
        sys.exit(1)

if __name__ == '__main__':
    main()