import csv

with open('/workspace/清华大学.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    rows = list(reader)

header = rows[0]

new_2024_data = [
    ('土木类', 3),
    ('理科试验班（化生类）', 2),
    ('工科试验班（能动与电气类）', 2),
    ('工科试验班（电气信息类）', 2),
    ('建筑类', 5),
    ('工科试验班（机械工程）', 2),
    ('临床医学类（协和）', 1),
    ('工科试验班（强基书院）', 1),
    ('工科试验班（行健书院）', 1),
    ('工科试验班（为先书院）', 1),
    ('工科试验班（交叉工程）', 1),
    ('自动化类', 1)
]

matched_count = 0
unmatched_programs = []

for program_name, plan_2024 in new_2024_data:
    matched = False
    for row in rows[1:]:
        if row[10] == '本科批B段' and row[7] == 'QHDXPABw03':
            if program_name in row[13] or row[13] in program_name:
                row[23] = str(plan_2024)
                matched = True
                matched_count += 1
                break
    if not matched:
        unmatched_programs.append((program_name, plan_2024))

for program_name, plan_2024 in unmatched_programs:
    new_row = [
        '1103', '清华大学', '北京海淀区', '综合类', 
        '985、211、双一流、强基、101计划、C9、机械五虎、电气四虎、建筑老八校、公办、本科',
        '综合类', '教育部', 'QHDXPABw03', '专业组03', '物理组', '本科批B段', '物理、化学',
        f'QHDXPABw03{len(rows):02d}', program_name, 
        '0', '0', '0', '0', '0', '0', 
        '0', '0', '0', '0', '0', '0', 
        str(plan_2024), '0', '0', '0', '0', '0', 
        '0', '0', '0', '0', '0', '0', 
        '国家专项计划', '国家专项计划', f'（校本部；国家专项计划）选科要求：首选物理，再选化学,5000元/年'
    ]
    rows.append(new_row)

with open('/workspace/清华大学.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(rows)

print(f"匹配成功：{matched_count}个专业")
print(f"新增专业：{len(unmatched_programs)}个")
for prog, plan in unmatched_programs:
    print(f"  - {prog}：{plan}人")
