import csv

with open('/workspace/清华大学.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    rows = list(reader)

header = rows[0]

for row in rows[1:]:
    if row[8] == '专业组99':
        row[7] = 'QHDXPAAw99'
        row[10] = '本科批A段'
        print(f"更新：{row[13]} - 批次改为本科批A段")

with open('/workspace/清华大学.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(rows)

print("清华大学专业组99批次已更正为本科批A段")
