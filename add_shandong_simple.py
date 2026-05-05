
import csv

header = [
    "院校ID","院校名称","地区","类型","院校标签","行业标签","所属部委",
    "专业组ID","专业组名称","专业组类别","批次","选考科目",
    "专业ID","专业名称",
    "2026计划数","2026最低分","2026最低位次","2026平均分","2026最高分","2026最高位次",
    "2025计划数","2025最低分","2025最低位次","2025平均分","2025最高分","2025最高位次",
    "2024计划数","2024最低分","2024最低位次","2024平均分","2024最高分","2024最高位次",
    "2023计划数","2023最低分","2023最低位次","2023平均分","2023最高分","2023最高位次",
    "专业组标签","专业组备注","专业备注"
]

# 完整的数据，确保41个字段
data_lines = [
    "3729,山东交通学院,山东济南市,理工类,本科、公办,交通类,山东省,SDJTXY99,专业组99,物理组,本科提前批,化学,SDJTXY9901,船舶电子电气工程（航海类）,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,,航海类,（威海校区）无色盲无复视；双眼裸视力均能达到4.6（0.4）及以上或双眼裸视力均能达到4.0（0.1）及以上且矫正视力均能达到4.6（0.4）及以上。因专业培养要求，非英语语种考生慎重报考，6325元/年",
]

with open('/workspace/山东交通学院.csv', 'w', encoding='utf-8') as f:
    f.write(','.join(header) + '\n')
    for line in data_lines:
        f.write(line + '\n')

print("CSV文件已生成！验证字段数：")
all_correct = True
with open('/workspace/山东交通学院.csv', 'r', encoding='utf-8') as f:
    lines = [l.strip() for l in f.readlines() if l.strip()]
    for i, line in enumerate(lines):
        fields = len(line.split(','))
        status = '✓' if fields == 41 else f'✗ ({fields}个)'
        print(f'第{i+1}行: {status}字段')
        if fields != 41:
            all_correct = False

if all_correct:
    print("\n✅ 所有行都有41个字段，格式正确！")
else:
    print("\n❌ 部分行字段数不正确！")
