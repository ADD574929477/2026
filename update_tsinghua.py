import csv

with open('/workspace/清华大学.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    rows = list(reader)

header = rows[0]

new_row = [
    '1103', '清华大学', '北京海淀区', '综合类', 
    '985、211、双一流、强基、101计划、C9、机械五虎、电气四虎、建筑老八校、公办、本科',
    '综合类', '教育部', 'QHDXPABw03', '专业组03', '物理组', '本科批B段', '物理、化学',
    f'QHDXPABw03{len(rows):02d}', '理科试验班（数理类）', 
    '0', '0', '0', '0', '0', '0', 
    '0', '0', '0', '0', '0', '0', 
    '1', '0', '0', '0', '0', '0', 
    '0', '0', '0', '0', '0', '0', 
    '国家专项计划', '国家专项计划', '（校本部；国家专项计划；包含专业：数学与应用数学、物理学、数理基础科学、工程物理、工程管理（能源实验班））选科要求：首选物理，再选化学,5000元/年'
]

rows.append(new_row)

with open('/workspace/清华大学.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(rows)

print("清华大学2024年国家专项计划第2页数据已添加完成")
print(f"新增专业：理科试验班（数理类），2024计划数：1人")
