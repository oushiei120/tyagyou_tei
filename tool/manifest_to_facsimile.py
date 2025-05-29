import json
import xml.etree.ElementTree as ET
from xml.dom import minidom
import argparse

def prettify_xml(elem):
    """Return a pretty-printed XML string for the Element."""
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="    ")

def create_facsimile_from_manifest(manifest_file, output_file):
    # 读取manifest文件
    with open(manifest_file, 'r', encoding='utf-8') as f:
        manifest = json.load(f)
    
    # 创建TEI根元素
    tei = ET.Element("TEI")
    tei.set("xmlns", "http://www.tei-c.org/ns/1.0")
    
    # 创建facsimile元素
    facsimile = ET.SubElement(tei, "facsimile")
    
    # 处理每个画布
    for i, canvas in enumerate(manifest['sequences'][0]['canvases']):
        # 创建surface元素
        surface = ET.SubElement(facsimile, "surface")
        surface.set("xml:id", f"surface_{i+1}")
        surface.set("n", str(i+1))
        surface.set("sameAs", canvas['@id'])
        
        # 添加图像信息
        graphic = ET.SubElement(surface, "graphic")
        graphic.set("url", canvas['images'][0]['resource']['@id'])
        graphic.set("width", str(canvas['width']))
        graphic.set("height", str(canvas['height']))
    
    # 生成XML并写入文件
    xml_str = prettify_xml(tei)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(xml_str)
    
    print(f"Facsimile部分已生成，输出文件：{output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='将IIIF Manifest转换为TEI facsimile部分')
    parser.add_argument('--manifest', required=True, help='IIIF Manifest文件路径')
    parser.add_argument('--output', required=True, help='输出XML文件路径')
    
    args = parser.parse_args()
    
    create_facsimile_from_manifest(args.manifest, args.output) 