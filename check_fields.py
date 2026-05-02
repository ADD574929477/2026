
with open('/workspace/云南警官学院.csv', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if line.strip():
        fields = line.strip().split(',')
        print(f'第{i+1}行: {len(fields)}个字段')
