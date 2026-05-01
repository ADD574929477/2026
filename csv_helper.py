#!/usr/bin/env python3
import csv
from typing import List, Dict, Any


class CSVHelper:
    def __init__(self, filename: str):
        self.filename = filename
        self.headers = []
        self.rows = []
        self.load()
    
    def load(self):
        """加载现有的CSV文件"""
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                for i, row in enumerate(reader):
                    if i == 0:
                        self.headers = row
                    else:
                        self.rows.append(row)
        except FileNotFoundError:
            print(f"文件 {self.filename} 不存在，将创建新文件")
    
    def set_headers(self, headers: List[str]):
        """设置表头"""
        self.headers = headers
    
    def add_row(self, row_data: Dict[str, Any]):
        """添加一行数据，使用字典形式，key为表头"""
        row = []
        for header in self.headers:
            value = row_data.get(header, '')
            if isinstance(value, (int, float)):
                row.append(str(value))
            else:
                row.append(value)
        self.rows.append(row)
    
    def add_rows(self, rows_data: List[Dict[str, Any]]):
        """批量添加多行"""
        for row_data in rows_data:
            self.add_row(row_data)
    
    def save(self):
        """保存到CSV文件"""
        with open(self.filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(self.headers)
            writer.writerows(self.rows)
        print(f"已保存 {len(self.rows)} 行数据到 {self.filename}")
    
    def validate_fields(self) -> bool:
        """验证所有行的字段数量是否正确"""
        expected = len(self.headers)
        valid = True
        for i, row in enumerate(self.rows, 1):
            if len(row) != expected:
                print(f"警告：第 {i} 行有 {len(row)} 个字段，期望 {expected} 个")
                valid = False
        if valid:
            print("所有行的字段数量都正确")
        return valid
    
    def get_field_index(self, field_name: str) -> int:
        """获取字段的索引"""
        try:
            return self.headers.index(field_name)
        except ValueError:
            return -1
    
    def print_headers(self):
        """打印表头和索引"""
        print("表头：")
        for i, header in enumerate(self.headers):
            print(f"  {i}: {header}")
    
    def print_sample(self, n: int = 3):
        """打印样本数据"""
        print(f"\n前 {min(n, len(self.rows))} 行数据：")
        for i, row in enumerate(self.rows[:n], 1):
            print(f"  第 {i} 行: {row[-5:]}")  # 只显示最后5个字段


def create_college_csv():
    """创建高校招生CSV文件的模板"""
    import os
    filename = '中国刑事警察学院.csv'
    # 删除旧文件，确保从干净的状态开始
    if os.path.exists(filename):
        os.remove(filename)
    helper = CSVHelper(filename)
    
    # 设置表头
    headers = [
        '院校ID', '院校名称', '地区', '类型', '院校标签', '行业标签', '所属部委',
        '专业组ID', '专业组名称', '专业组类别', '批次', '选考科目', '专业ID', '专业名称',
        '2026计划数', '2026最低分', '2026最低位次', '2026平均分', '2026最高分', '2026最高位次',
        '2025计划数', '2025最低分', '2025最低位次', '2025平均分', '2025最高分', '2025最高位次',
        '2024计划数', '2024最低分', '2024最低位次', '2024平均分', '2024最高分', '2024最高位次',
        '2023计划数', '2023最低分', '2023最低位次', '2023平均分', '2023最高分', '2023最高位次',
        '专业组标签', '专业组备注', '专业备注'
    ]
    helper.set_headers(headers)
    
    # 基础数据
    base_data = {
        '院校ID': '2124',
        '院校名称': '中国刑事警察学院',
        '地区': '辽宁沈阳市',
        '类型': '政法类',
        '院校标签': '警校、政法类、本科、公办',
        '行业标签': '警务类',
        '所属部委': '公安部直属',
    }
    
    # 填充0到所有分数相关字段
    for year in ['2026', '2025', '2024', '2023']:
        for field in ['计划数', '最低分', '最低位次', '平均分', '最高分', '最高位次']:
            base_data[f'{year}{field}'] = 0
    
    note = '（公安类）面向地方公安机关入警就业。须参加省公安厅组织的政治考察、面试，体检，体能测评，具体要求详见《2025年公安院校公安专业在滇招生报考须知》），5200元/年'
    
    # 专业组01 - 只招男生
    groups01 = [
        ('ZGXSZJXYTQBw01', '专业组01', '物理组', '提前本科批B段', '化学', 'ZGXSZJXYTQBw0101', '刑事科学技术（公安类）', 9),
        ('ZGXSZJXYTQBw01', '专业组01', '物理组', '提前本科批B段', '化学', 'ZGXSZJXYTQBw0102', '网络安全与执法（公安类）', 3),
        ('ZGXSZJXYTQBw01', '专业组01', '物理组', '提前本科批B段', '化学', 'ZGXSZJXYTQBw0103', '公安视听技术（公安类）', 2),
        ('ZGXSZJXYTQBw01', '专业组01', '物理组', '提前本科批B段', '化学', 'ZGXSZJXYTQBw0104', '数据警务技术（公安类）', 2),
    ]
    
    for g in groups01:
        row_data = base_data.copy()
        row_data.update({
            '专业组ID': g[0],
            '专业组名称': g[1],
            '专业组类别': g[2],
            '批次': g[3],
            '选考科目': g[4],
            '专业ID': g[5],
            '专业名称': g[6],
            '2025计划数': g[7],
            '专业组备注': '只招男生，面向地方公安机关入警就业',
            '专业备注': note,
        })
        helper.add_row(row_data)
    
    # 专业组02 - 只招女生
    groups02 = [
        ('ZGXSZJXYTQBw02', '专业组02', '物理组', '提前本科批B段', '化学', 'ZGXSZJXYTQBw0201', '刑事科学技术（公安类）', 1),
        ('ZGXSZJXYTQBw02', '专业组02', '物理组', '提前本科批B段', '化学', 'ZGXSZJXYTQBw0202', '公安视听技术（公安类）', 1),
        ('ZGXSZJXYTQBw02', '专业组02', '物理组', '提前本科批B段', '化学', 'ZGXSZJXYTQBw0203', '网络安全与执法（公安类）', 1),
        ('ZGXSZJXYTQBw02', '专业组02', '物理组', '提前本科批B段', '化学', 'ZGXSZJXYTQBw0204', '数据警务技术（公安类）', 1),
    ]
    
    for g in groups02:
        row_data = base_data.copy()
        row_data.update({
            '专业组ID': g[0],
            '专业组名称': g[1],
            '专业组类别': g[2],
            '批次': g[3],
            '选考科目': g[4],
            '专业ID': g[5],
            '专业名称': g[6],
            '2025计划数': g[7],
            '专业组备注': '只招女生，面向地方公安机关入警就业',
            '专业备注': note,
        })
        helper.add_row(row_data)
    
    helper.validate_fields()
    helper.save()
    helper.print_sample()


if __name__ == '__main__':
    create_college_csv()
