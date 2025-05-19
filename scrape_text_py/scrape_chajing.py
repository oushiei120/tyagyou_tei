import os
import requests
from bs4 import BeautifulSoup
import time
import re

# 创建保存文件的目录
output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'chajing')
os.makedirs(output_dir, exist_ok=True)

# 茶经的章节链接
chapter_links = [
    ("一之源", "https://www.gushiwen.cn/guwen/bookv_f7261af3689e.aspx"),
    ("二之具", "https://www.gushiwen.cn/guwen/bookv_d03dd444089e.aspx"),
    ("三之造", "https://www.gushiwen.cn/guwen/bookv_061a279383e2.aspx"),
    ("四之器", "https://www.gushiwen.cn/guwen/bookv_beb21592d6a6.aspx"),
    ("五之煮", "https://www.gushiwen.cn/guwen/bookv_f5b63367110e.aspx"),
    ("六之饮", "https://www.gushiwen.cn/guwen/bookv_0b1c02f4e61c.aspx"),
    ("七之事", "https://www.gushiwen.cn/guwen/bookv_91f61468241a.aspx"),
    ("八之出", "https://www.gushiwen.cn/guwen/bookv_13bd57b0fda6.aspx"),
    ("九之略", "https://www.gushiwen.cn/guwen/bookv_4b7258a82e03.aspx"),
    ("十之图", "https://www.gushiwen.cn/guwen/bookv_b50079f95b99.aspx")
]

print(f"准备抓取《茶经》共 {len(chapter_links)} 个章节")

# 抓取每个章节内容并保存
for i, (title, url) in enumerate(chapter_links):
    print(f"正在抓取: {title} - {url}")
    
    # 添加延迟避免请求过于频繁
    if i > 0:
        time.sleep(2)
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 提取内容 - 查找class为"contson"的div标签
        content_div = soup.find('div', class_='contson')
        if content_div:
            # 获取纯文本
            content = content_div.get_text().strip()
            
            # 清理文本，移除多余空白
            content = re.sub(r'\n+', '\n', content)
            content = re.sub(r' +', ' ', content)
            
            # 保存文件名
            filename = f"{i+1:02d}_{title}.txt"
            filepath = os.path.join(output_dir, filename)
            
            # 写入文件
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"《茶经》 {title}\n\n")
                f.write(content)
            
            print(f"已保存: {filepath}")
        else:
            print(f"未找到内容: {title}")
    
    except Exception as e:
        print(f"抓取 {title} 时出错: {e}")

print("所有章节抓取完成!")

# 创建一个合并版本
try:
    print("正在创建合并版本...")
    merged_file = os.path.join(output_dir, "00_茶经全文.txt")
    with open(merged_file, 'w', encoding='utf-8') as outfile:
        outfile.write("《茶经》全文\n陆羽 著\n\n")
        
        for i, (title, _) in enumerate(chapter_links):
            filename = f"{i+1:02d}_{title}.txt"
            filepath = os.path.join(output_dir, filename)
            
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as infile:
                    # 跳过第一行标题
                    infile.readline()
                    
                    # 写入章节标题
                    outfile.write(f"【{title}】\n\n")
                    
                    # 复制内容
                    outfile.write(infile.read())
                    outfile.write("\n\n")
    
    print(f"合并文件已保存: {merged_file}")
except Exception as e:
    print(f"创建合并文件时出错: {e}")
