#!/usr/bin/env python3
import os
import sys
import csv
import argparse
from datetime import datetime

class CSVDuplicateChecker:
    def __init__(self, input_file, delimiter=',', encoding='utf-8', output_file=None):
        self.input_file = input_file
        self.delimiter = delimiter
        self.encoding = encoding
        self.output_file = output_file
        self.results = {
            'total_rows': 0,
            'unique_rows': 0,
            'duplicate_rows': 0,
            'duplicates': {}
        }
    
    def check_duplicates(self):
        """检查CSV文件中的重复数据"""
        if not os.path.exists(self.input_file):
            return False, f"错误: 文件 {self.input_file} 不存在"
        
        try:
            seen_rows = {}
            duplicate_rows = []
            
            with open(self.input_file, 'r', encoding=self.encoding, newline='') as infile:
                reader = csv.reader(infile, delimiter=self.delimiter, quotechar='"')
                header = next(reader, None)
                if not header:
                    return False, "错误: 文件没有标题行"
                
                row_count = 0
                for row in reader:
                    row_count += 1
                    # 将行转换为元组以便作为字典键
                    row_tuple = tuple(row)
                    if row_tuple in seen_rows:
                        # 记录重复行
                        if row_tuple not in self.results['duplicates']:
                            self.results['duplicates'][row_tuple] = {
                                'count': 1,
                                'first_occurrence': seen_rows[row_tuple],
                                'occurrences': [seen_rows[row_tuple]]
                            }
                        self.results['duplicates'][row_tuple]['count'] += 1
                        self.results['duplicates'][row_tuple]['occurrences'].append(row_count)
                        duplicate_rows.append(row)
                    else:
                        seen_rows[row_tuple] = row_count
            
            self.results['total_rows'] = row_count
            self.results['unique_rows'] = len(seen_rows)
            self.results['duplicate_rows'] = len(duplicate_rows)
            
            # 如果指定了输出文件，写入去重后的数据
            if self.output_file:
                self._write_unique_rows(header, seen_rows)
            
            return True, ""
        except Exception as e:
            return False, f"处理文件时出错: {str(e)}"
    
    def _write_unique_rows(self, header, seen_rows):
        """将去重后的数据写入输出文件"""
        try:
            with open(self.output_file, 'w', encoding=self.encoding, newline='') as outfile:
                writer = csv.writer(outfile, delimiter=self.delimiter, quotechar='"', quoting=csv.QUOTE_MINIMAL)
                writer.writerow(header)
                for row_tuple in seen_rows:
                    writer.writerow(row_tuple)
        except Exception as e:
            print(f"写入输出文件时出错: {str(e)}")
    
    def generate_report(self):
        """生成重复数据检查报告"""
        report = []
        report.append("===== CSV重复数据检查报告 =====")
        report.append(f"检查时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"输入文件: {self.input_file}")
        report.append(f"总数据行数: {self.results['total_rows']}")
        report.append(f"唯一数据行数: {self.results['unique_rows']}")
        report.append(f"重复数据行数: {self.results['duplicate_rows']}")
        
        if self.output_file:
            report.append(f"去重后输出文件: {self.output_file}")
        
        if self.results['duplicates']:
            report.append(f"\n重复数据详情 ({len(self.results['duplicates'])} 组重复):")
            for i, (row_tuple, info) in enumerate(self.results['duplicates'].items(), 1):
                report.append(f"\n组 {i}: 重复 {info['count']} 次")
                report.append(f"首次出现行号: {info['first_occurrence']}")
                report.append(f"所有出现行号: {', '.join(map(str, info['occurrences']))}")
                report.append(f"数据: {', '.join(row_tuple[:5])}{'...' if len(row_tuple) > 5 else ''}")
        
        report.append("========================")
        return '\n'.join(report)

def main():
    parser = argparse.ArgumentParser(description='CSV重复数据检查工具')
    parser.add_argument('input_file', help='要检查的CSV文件路径')
    parser.add_argument('-o', '--output', help='去重后的输出文件路径')
    parser.add_argument('-d', '--delimiter', default=',', help='CSV分隔符，默认是逗号')
    parser.add_argument('-e', '--encoding', default='utf-8', help='文件编码，默认是utf-8')
    
    args = parser.parse_args()
    
    checker = CSVDuplicateChecker(
        input_file=args.input_file,
        delimiter=args.delimiter,
        encoding=args.encoding,
        output_file=args.output
    )
    
    success, error_msg = checker.check_duplicates()
    report = checker.generate_report()
    
    print(report)
    
    if not success:
        print(f"错误: {error_msg}")
        sys.exit(1)

if __name__ == '__main__':
    main()