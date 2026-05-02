
def make_row(
    yuanxiao_id, yuanxiao_name, diqu, leixing, yuanxiao_biaoqian, hangye_biaoqian, suoshu_buwei,
    zhuanyezu_id, zhuanyezu_name, zhuanyezu_leibie, pici, xuanke_kemu,
    zhuanye_id, zhuanye_name,
    plan26, min26, min_p26, avg26, max26, max_p26,
    plan25, min25, min_p25, avg25, max25, max_p25,
    plan24, min24, min_p24, avg24, max24, max_p24,
    plan23, min23, min_p23, avg23, max23, max_p23,
    zhuanyezu_biaoqian, zhuanyezu_beizhu, zhuanye_beizhu
):
    return [
        yuanxiao_id, yuanxiao_name, diqu, leixing, yuanxiao_biaoqian, hangye_biaoqian, suoshu_buwei,
        zhuanyezu_id, zhuanyezu_name, zhuanyezu_leibie, pici, xuanke_kemu,
        zhuanye_id, zhuanye_name,
        plan26, min26, min_p26, avg26, max26, max_p26,
        plan25, min25, min_p25, avg25, max25, max_p25,
        plan24, min24, min_p24, avg24, max24, max_p24,
        plan23, min23, min_p23, avg23, max23, max_p23,
        zhuanyezu_biaoqian, zhuanyezu_beizhu, zhuanye_beizhu
    ]

print("参数数量：", make_row.__code__.co_argcount)

row = make_row(
    "5319","云南警官学院","云南昆明市","政法类","警校、政法类、本科、公办","警务类","云南省",
    "YNJGXYTQBw01","专业组01","物理组","提前本科批B段","化学","YNJGXYTQBw0101","刑事科学技术（公安类）",
    "0","0","0","0","0","0","132","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","",
    "只招男生、面向地方公安机关入警就业",
    "（公安类）须参加省公安厅组织的政治考察、面试、体检、体能测评，具体要求详见《2025年公安院校公安专业在滇招生报考须知》，5000元/年"
)
print("返回的字段数：", len(row))
print("最后几个字段：", row[-3:])
