
# 读取正确的中国刑事警察学院.csv第2行
with open('/workspace/中国刑事警察学院.csv', 'r', encoding='utf-8') as f:
    correct_line = f.readlines()[1].strip()

print(f'正确行数: {len(correct_line.split(","))}')
print(f'正确行内容: {correct_line}')
