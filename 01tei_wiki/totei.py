import os
from bs4 import BeautifulSoup
from lxml import etree

# 所有 XHTML 文件路径（按顺序）
input_files = [
    "/Users/oushiei/Documents/GitHub/tyagyou_tei/茶經/totei/c1_cha_jing_juan_shang.xhtml",
    "/Users/oushiei/Documents/GitHub/tyagyou_tei/茶經/totei/c2_cha_jing_yi_zhi_yuan.xhtml",
    "/Users/oushiei/Documents/GitHub/tyagyou_tei/茶經/totei/c3_cha_jing_er_zhi_ju.xhtml",
    "/Users/oushiei/Documents/GitHub/tyagyou_tei/茶經/totei/c4_cha_jing_san_zhi_zao.xhtml",
    "/Users/oushiei/Documents/GitHub/tyagyou_tei/茶經/totei/c5_cha_jing_juan_zhong.xhtml",
    "/Users/oushiei/Documents/GitHub/tyagyou_tei/茶經/totei/c6_cha_jing_si_zhi_qi.xhtml",
    "/Users/oushiei/Documents/GitHub/tyagyou_tei/茶經/totei/c7_cha_jing_juan_xia.xhtml",
    "/Users/oushiei/Documents/GitHub/tyagyou_tei/茶經/totei/c8_cha_jing_wu_zhi_zhu.xhtml",
    "/Users/oushiei/Documents/GitHub/tyagyou_tei/茶經/totei/c9_cha_jing_liu_zhi_yin.xhtml",
    "/Users/oushiei/Documents/GitHub/tyagyou_tei/茶經/totei/c10_cha_jing_qi_zhi_shi.xhtml",
    "/Users/oushiei/Documents/GitHub/tyagyou_tei/茶經/totei/c11_cha_jing_ba_zhi_chu.xhtml",
    "/Users/oushiei/Documents/GitHub/tyagyou_tei/茶經/totei/c12_cha_jing_jiu_zhi_lue.xhtml",
    "/Users/oushiei/Documents/GitHub/tyagyou_tei/茶經/totei/c13_cha_jing_shi_zhi_tu.xhtml"
]

# 输出路径
output_path = "/Users/oushiei/Documents/GitHub/tyagyou_tei/茶經/totei/cha_jing_all.xml"

# 创建 TEI 文本结构（无 teiHeader）
TEI = etree.Element("TEI")
text = etree.SubElement(TEI, "text")
body = etree.SubElement(text, "body")

# 遍历每个文件
for idx, file_path in enumerate(input_files, start=1):
    with open(file_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "xml")  # 使用 XML 解析器更安全

    div = etree.SubElement(body, "div", attrib={"id": f"div{idx}"})

    # 章节标题
    h2 = soup.find("h2")
    if h2:
        head = etree.SubElement(div, "head")
        head.text = h2.get_text()

    # 段落
    for p in soup.find_all("p"):
        p_elem = etree.SubElement(div, "p")
        for child in p.children:
            if isinstance(child, str):
                p_elem.text = (p_elem.text or "") + child
            elif child.name == "small":
                note_elem = etree.SubElement(p_elem, "note")
                note_elem.text = child.get_text()
            else:
                p_elem.text = (p_elem.text or "") + child.get_text()

# 写入输出文件（带缩进）
tree = etree.ElementTree(TEI)
tree.write(output_path, pretty_print=True, xml_declaration=True, encoding="utf-8")

print(f"✅ TEI 文件已生成（无元数据）：{output_path}")
