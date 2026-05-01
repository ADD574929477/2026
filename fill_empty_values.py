#!/usr/bin/env python3
import csv

def fill_empty_values(filename):
    # 读取CSV文件
    rows = []
    headers = []
    
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            if i == 0:
                headers = row
            else:
                rows.append(row)
    
    # 需要填充为0的字段：所有年份的计划数、最低分、最低位次、平均分、最高分、最高位次
    score_fields = []
    for year in ['2026', '2025', '2024', '2023']:
        for field in ['计划数', '最低分', '最低位次', '平均分', '最高分', '最高位次']:
            score_fields.append(f'{year}{field}')
    
    # 获取这些字段的索引
    field_indices = []
    for field in score_fields:
        if field in headers:
            field_indices.append(headers.index(field))
    
    # 填充空值为0
    filled_count = 0
    for row in rows:
        for idx in field_indices:
            if idx < len(row) and row[idx] == '':
                row[idx] = '0'
                filled_count += 1
    
    # 保存修改后的文件
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)
    
    print(f"已填充 {filled_count} 个空值为0")
    return filled_count

if __name__ == '__main__':
    fill_empty_values('中国刑事警察学院.csv')
