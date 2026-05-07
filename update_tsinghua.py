import csv

with open('/workspace/清华大学.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    rows = list(reader)

header = rows[0]

for row in rows[1:]:
    if row[10] == '提前本科批C段' and row[7] == 'QHDXTQCw02':
        if row[13] == '机械工程':
            row[23] = '1'
            print("更新：机械工程 - 2024计划数：1")
        elif row[13] == '核工程与核技术':
            row[23] = '1'
            print("更新：核工程与核技术 - 2024计划数：1")

with open('/workspace/清华大学.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(rows)

print("清华大学2024年提前本科批C段数据已更新完成")
