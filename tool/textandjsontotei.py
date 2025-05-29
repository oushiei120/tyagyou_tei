import json
import re
import xml.etree.ElementTree as ET
import os
from xml.dom import minidom

def prettify_xml(elem):
    """Return a pretty-printed XML string for the Element."""
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="    ")

def process_text_and_images(text_file, manifest_file, output_file):
    # 读取manifest文件
    with open(manifest_file, 'r', encoding='utf-8') as f:
        manifest = json.load(f)
    
    # 读取文本文件
    with open(text_file, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # 创建TEI文档
    tei = ET.Element("TEI")
    tei.set("xmlns", "http://www.tei-c.org/ns/1.0")
    
    # 添加facsimile部分
    facsimile = ET.SubElement(tei, "facsimile")
    for i, canvas in enumerate(manifest['sequences'][0]['canvases']):
        surface = ET.SubElement(facsimile, "surface")
        surface.set("xml:id", f"surface_{i+1}")
        surface.set("n", f"{i+1}")
        surface.set("sameAs", canvas['@id'])
        graphic = ET.SubElement(surface, "graphic")
        graphic.set("url", canvas['images'][0]['resource']['@id'])
        graphic.set("width", str(canvas['width']))
        graphic.set("height", str(canvas['height']))
    
    # 创建text和body元素
    text_elem = ET.SubElement(tei, "text")
    body = ET.SubElement(text_elem, "body")
    
    # 分割页面 - 使用正则表达式匹配[496936_00002 00000B]格式的页面标记
    pages = re.split(r'(\[\d+_\d+ \d+[A-Z]\])', text)
    
    current_div = None
    page_counter = 0
    chapter_counter = 0
    line_counter = 0
    
    # 创建初始div
    current_div = ET.SubElement(body, "div")
    current_div.set("type", "text")
    
    # 处理每一页
    for i in range(len(pages)):
        content = pages[i].strip()
        
        # 如果是页面标记
        if re.match(r'\[\d+_\d+ \d+[A-Z]\]', content):
            page_id = content
            page_counter += 1
            line_counter = 0
            
            # 创建pb元素
            if page_counter <= len(manifest['sequences'][0]['canvases']):
                canvas = manifest['sequences'][0]['canvases'][page_counter-1]
                pb = ET.SubElement(body, "pb")
                pb.set("n", str(page_counter))
                pb.set("facs", f"#surface_{page_counter}")
                pb.set("sameAs", canvas['@id'])
        
        # 如果是内容
        elif content and i > 0:  # 确保不是第一个元素且不为空
            # 将内容分割为段落
            paragraphs = content.split('<p>')
            
            for p_content in paragraphs:
                if not p_content.strip():
                    continue
                
                # 检查是否是章节标题
                is_chapter_title = re.match(r'^[一二三四五六七八九十]+之[源具造]', p_content.strip())
                
                if is_chapter_title:
                    chapter_counter += 1
                    # 创建新的章节div
                    current_div = ET.SubElement(body, "div")
                    current_div.set("type", "chapter")
                    current_div.set("n", str(chapter_counter))
                    current_div.set("xml:id", f"c{chapter_counter}")
                
                # 创建一个段落
                p = ET.SubElement(current_div, "p")
                
                # 分割段落内的行
                lines = p_content.strip().split('\n')
                
                # 处理所有行
                for j, line in enumerate(lines):
                    line = line.strip()
                    if not line:
                        continue
                    
                    # 增加行号计数
                    line_counter += 1
                    
                    # 如果不是第一行，添加行分隔符
                    if j > 0:
                        lb = ET.SubElement(p, "lb")
                        lb.set("n", str(line_counter))
                    
                    # 处理注释
                    notes = []
                    for match in re.finditer(r'（(.*?)）', line):
                        notes.append(match.group(1))
                    
                    # 移除注释
                    main_text = re.sub(r'（.*?）', '', line).strip()
                    
                    # 添加主文本
                    if main_text:
                        if j == 0:  # 第一行
                            p.text = main_text
                        else:  # 后续行
                            if len(p) > 0:
                                # 如果前面的元素有尾部文本，则在其上添加当前文本
                                if p[-1].tail:
                                    p[-1].tail += ' ' + main_text
                                else:
                                    p[-1].tail = main_text
                            else:
                                # 如果没有前面的元素但有text
                                if p.text:
                                    # 创建一个span元素
                                    span = ET.SubElement(p, "seg")
                                    span.text = main_text
                                else:
                                    p.text = main_text
                    
                    # 添加注释
                    for note_text in notes:
                        note = ET.SubElement(p, "note")
                        note.text = note_text
    
    # 转换为漂亮的XML格式
    xml_str = prettify_xml(tei)
    
    # 写入文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(xml_str)
    
    print(f"处理完成，输出文件：{output_file}")

# 创建output目录
os.makedirs('output', exist_ok=True)

# 添加命令行参数解析
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='将文本和IIIF Manifest转换为TEI XML')
    parser.add_argument('--text', required=True, help='文本文件路径')
    parser.add_argument('--manifest', required=True, help='IIIF Manifest文件路径')
    parser.add_argument('--output', required=True, help='输出XML文件路径')
    
    args = parser.parse_args()
    
    process_text_and_images(
        args.text,
        args.manifest,
        args.output
    )