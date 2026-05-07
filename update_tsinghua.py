import csv

with open('/workspace/清华大学.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    rows = list(reader)

header = rows[0]

for row in rows[1:]:
    if row[8] == '专业组02':
        row[7] = 'QHDXTQDw02'
        row[10] = '提前本科批D段'
        if row[13] == '机械工程':
            row[23] = '1'
        elif row[13] == '核工程与核技术':
            row[23] = '1'
        print(f"更新：{row[13]} - 批次改为提前本科批D段，2024计划数1")

with open('/workspace/清华大学.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(rows)

print("清华大学专业组02数据已更新完成")
