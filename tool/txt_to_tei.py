import re
import xml.etree.ElementTree as ET
from xml.dom import minidom
import argparse

def prettify_xml(elem):
    """Return a pretty-printed XML string for the Element."""
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="    ")

def process_text_file(text_file, output_file):
    # 读取文本文件
    with open(text_file, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # 创建TEI根元素
    tei = ET.Element("TEI")
    tei.set("xmlns", "http://www.tei-c.org/ns/1.0")
    
    # 创建text和body元素
    text_elem = ET.SubElement(tei, "text")
    body = ET.SubElement(text_elem, "body")
    
    # 将文本分割成页
    pages = re.split(r'(\[\d+_\d+ \d+[A-Z]\])', text)
    
    page_counter = 0
    
    # 处理每一页
    i = 0
    while i < len(pages):
        page_marker = pages[i].strip()
        
        # 如果是页面标记
        if re.match(r'\[\d+_\d+ \d+[A-Z]\]', page_marker):
            page_id = re.match(r'\[(\d+_\d+ \d+[A-Z])\]', page_marker).group(1)
            page_counter += 1
            
            # 添加页面分隔符 - 放在页面开始
            pb = ET.SubElement(body, "pb")
            pb.set("n", str(page_counter))
            pb.set("facs", f"#surface_{page_counter}")
            pb.set("xml:id", f"page_{page_counter}")
            pb.set("corresp", page_id)
            
            # 创建页面div
            page_div = ET.SubElement(body, "div")
            page_div.set("type", "pageContent")
            page_div.set("n", str(page_counter))
            
            # 处理页面内容
            if i + 1 < len(pages):
                page_content = pages[i + 1].strip()
                if page_content:
                    # 创建匿名块(ab)来包含页面内容
                    ab = ET.SubElement(page_div, "ab")
                    
                    # 分割页面内容成行
                    lines = page_content.split('\n')
                    line_counter = 0
                    
                    for line in lines:
                        line = line.strip()
                        if not line:
                            continue
                        
                        # 如果行以<p>开头，去掉它
                        if line.startswith('<p>'):
                            line = line[3:].strip()
                        
                        line_counter += 1
                        
                        # 添加行分隔符
                        lb = ET.SubElement(ab, "lb")
                        lb.set("n", str(line_counter))
                        
                        # 处理注释
                        notes = []
                        for match in re.finditer(r'（(.*?)）', line):
                            notes.append(match.group(1))
                        
                        # 移除注释，保留主文本
                        main_text = re.sub(r'（.*?）', '', line).strip()
                        
                        # 添加主文本
                        if main_text:
                            # 对于第一行，使用上一个元素的tail
                            if line_counter == 1:
                                if len(ab) > 0 and ab[-1].tag.endswith('lb'):
                                    ab[-1].tail = main_text
                            else:
                                # 对于后续行，添加到上一个元素的tail
                                if len(ab) > 0:
                                    if ab[-1].tail is None:
                                        ab[-1].tail = main_text
                                    else:
                                        ab[-1].tail += " " + main_text
                        
                        # 添加注释
                        for note_text in notes:
                            note = ET.SubElement(ab, "note")
                            note.set("place", "inline")
                            note.text = note_text
            
            # 跳过页面内容
            i += 2
        else:
            # 跳过非页面标记
            i += 1
    
    # 生成XML并写入文件
    xml_str = prettify_xml(tei)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(xml_str)
    
    print(f"TEI文本部分已生成，输出文件：{output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='将文本文件转换为TEI格式')
    parser.add_argument('--text', required=True, help='文本文件路径')
    parser.add_argument('--output', required=True, help='输出XML文件路径')
    
    args = parser.parse_args()
    
    process_text_file(args.text, args.output) 