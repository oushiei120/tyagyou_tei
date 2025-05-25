from pdf2image import convert_from_path
import os

# 设置PDF路径和输出目录
pdf_path = "/Users/oushiei/Documents/GitHub/tyagyou_tei/茶书.四种.茶经.茶具图赞.茶谱.茶集.明万历时期陈文烛校刊本 第10 - 37页.pdf"
output_dir = "images"
os.makedirs(output_dir, exist_ok=True)

# 转换PDF为JPEG（第10到37页）
images = convert_from_path(pdf_path, dpi=300, first_page=10, last_page=37)
for i, image in enumerate(images):
    image.save(f"{output_dir}/page-{i+10:03d}.jpg", "JPEG")