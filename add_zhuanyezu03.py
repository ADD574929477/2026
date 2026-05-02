
# 正确构建每个字段
def build_row(yuanxiao_id, yuanxiao_name, diqu, leixing, yuanxiao_biaoqian, hangye_biaoqian, suoshu_buwei,
              zhuanyezu_id, zhuanyezu_name, zhuanyezu_leibie, pici, xuanke_kemu,
              zhuanye_id, zhuanye_name,
              plan26, min26, min_p26, avg26, max26, max_p26,
              plan25, min25, min_p25, avg25, max25, max_p25,
              plan24, min24, min_p24, avg24, max24, max_p24,
              plan23, min23, min_p23, avg23, max23, max_p23,
              zhuanyezu_biaoqian, zhuanyezu_beizhu, zhuanye_beizhu):
    return (f'{yuanxiao_id},{yuanxiao_name},{diqu},{leixing},{yuanxiao_biaoqian},{hangye_biaoqian},{suoshu_buwei},'
            f'{zhuanyezu_id},{zhuanyezu_name},{zhuanyezu_leibie},{pici},{xuanke_kemu},'
            f'{zhuanye_id},{zhuanye_name},'
            f'{plan26},{min26},{min_p26},{avg26},{max26},{max_p26},'
            f'{plan25},{min25},{min_p25},{avg25},{max25},{max_p25},'
            f'{plan24},{min24},{min_p24},{avg24},{max24},{max_p24},'
            f'{plan23},{min23},{min_p23},{avg23},{max23},{max_p23},'
            f'{zhuanyezu_biaoqian},{zhuanyezu_beizhu},{zhuanye_beizhu}')

# 读取现有文件
with open('/workspace/云南警官学院.csv', 'r', encoding='utf-8') as f:
    lines = f.readlines()

header = lines[0].strip()
data_lines = [line.strip() for line in lines[1:] if line.strip()]

# 添加专业组03数据
new_row = build_row('5319','云南警官学院','云南昆明市','政法类','警校、政法类、本科、公办','警务类','云南省',
              'YNJGXYTQBw03','专业组03','物理组','提前本科批B段','思想政治','YNJGXYTQBw0301','禁毒学（公安类）',
              '0','0','0','0','0','0',
              '6','0','0','0','0','0',
              '0','0','0','0','0','0',
              '0','0','0','0','0','0',
              '','只招男生、面向移民管理机构入警就业','（公安类）须参加省公安厅组织的政治考察、面试、体检、体能测评，具体要求详见《2025年公安院校公安专业在滇招生报考须知》，4950元/年')
data_lines.append(new_row)

# 写入文件
with open('/workspace/云南警官学院.csv', 'w', encoding='utf-8') as f:
    f.write(header + '\n')
    for line in data_lines:
        f.write(line + '\n')

print('专业组03已添加！')
print(f'现在有{len(data_lines)}个专业')
for i, line in enumerate([header] + data_lines):
    print(f'第{i+1}行: {line.count(",")}个逗号')
