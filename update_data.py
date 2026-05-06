import csv

with open('/workspace/中国民用航空飞行学院.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    rows = list(reader)

header = rows[0]
for row in rows[1:]:
    major_name = row[header.index('专业名称')]
    major_group = row[header.index('专业组ID')]
    
    if major_name == "信息与计算科学" and major_group == 'ZGMYHKFXYPBw02':
        row[header.index('2023最低分')] = "487"
        row[header.index('2023最低位次')] = "46865"
    elif major_name == "翻译" and major_group == 'ZGMYHKFXYPBw01':
        row[header.index('2023最低分')] = "487"
        row[header.index('2023最低位次')] = "46865"
    elif major_name == "智慧交通" and major_group == 'ZGMYHKFXYPBw02':
        row[header.index('2023最低分')] = "486"
        row[header.index('2023最低位次')] = "47425"
    elif major_name == "公共事业管理" and major_group == 'ZGMYHKFXYPBw01':
        row[header.index('2023最低分')] = "486"
        row[header.index('2023最低位次')] = "47425"
    elif major_name == "消防工程" and major_group == 'ZGMYHKFXYPBw02':
        row[header.index('2023最低分')] = "486"
        row[header.index('2023最低位次')] = "47425"
    elif major_name == "安全工程" and major_group == 'ZGMYHKFXYPBw02':
        row[header.index('2023最低分')] = "486"
        row[header.index('2023最低位次')] = "47425"
    elif major_name == "应用心理学" and major_group == 'ZGMYHKFXYPBw01':
        row[header.index('2023最低分')] = "486"
        row[header.index('2023最低位次')] = "47425"
    elif major_name == "英语" and major_group == 'ZGMYHKFXYPBw01':
        row[header.index('2023最低分')] = "486"
        row[header.index('2023最低位次')] = "47425"
    elif major_name == "市场营销" and major_group == 'ZGMYHKFXYPBw01':
        row[header.index('2023最低分')] = "441"
        row[header.index('2023最低位次')] = "76307"
    elif major_name == "思想政治教育" and major_group == 'ZGMYHKFXYPBw03':
        row[header.index('2023最低分')] = "438"
        row[header.index('2023最低位次')] = "78485"

with open('/workspace/中国民用航空飞行学院.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(rows)

print("2023年本科批B段第3页数据已更新完成")