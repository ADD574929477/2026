import csv

with open('/workspace/清华大学.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    rows = list(reader)

header = rows[0]
data_rows = rows[1:]

def batch_order(batch):
    order = {
        '提前本科批D段': 1,
        '本科批A段': 2,
        '本科批B段': 3
    }
    return order.get(batch, 99)

data_rows.sort(key=lambda x: (batch_order(x[10]), x[8], x[13]))

with open('/workspace/清华大学.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(data_rows)

print("清华大学CSV文件已按批次排序完成")
print("顺序：提前本科批D段 → 本科批A段 → 本科批B段")
