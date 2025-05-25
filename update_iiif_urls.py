import json
import os

# --- 配置 ---
# 旧的基础 URL，需要被替换
OLD_BASE_URL = "http://localhost:8000/"
# 新的 GitHub Pages 基础 URL
NEW_BASE_URL = "https://oushiei120.github.io/tyagyou_tei/"

# 项目中 'docs' 目录的绝对路径
DOCS_ROOT_DIR = "/Users/oushiei/Documents/GitHub/tyagyou_tei/docs"

# 需要直接处理的文件列表 (相对于 DOCS_ROOT_DIR)
FILES_TO_PROCESS = [
    "manifest.json"
]

# 需要处理的目录列表 (相对于 DOCS_ROOT_DIR)，脚本会递归查找其中的 .json 文件
DIRS_TO_PROCESS = [
    "images"
]
# --- 配置结束 ---

def update_json_data(data, old_base, new_base):
    """
    递归更新 JSON 数据结构中的字符串。
    如果字符串以 old_base 开头，则将其替换为 new_base。
    """
    if isinstance(data, dict):
        return {k: update_json_data(v, old_base, new_base) for k, v in data.items()}
    elif isinstance(data, list):
        return [update_json_data(elem, old_base, new_base) for elem in data]
    elif isinstance(data, str):
        if data.startswith(old_base):
            return new_base + data[len(old_base):]
    return data

def process_json_file(file_path, old_base, new_base):
    """
    读取、更新并写回单个 JSON 文件。
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = json.load(f)
        
        updated_content = update_json_data(content, old_base, new_base)
        
        # 检查内容是否有实际变化，避免不必要的写操作
        # (json.dumps 用于比较，因为原始加载和递归处理可能改变对象实例但不改变值)
        if json.dumps(content) != json.dumps(updated_content):
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(updated_content, f, ensure_ascii=False, indent=2)
            print(f"Updated: {file_path}")
        else:
            print(f"No changes needed: {file_path}")

    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON - {file_path}")
    except Exception as e:
        print(f"An unexpected error occurred with {file_path}: {e}")

def main():
    print(f"Starting URL update process...")
    print(f"Replacing '{OLD_BASE_URL}' with '{NEW_BASE_URL}'")
    print(f"Processing files in and under: {DOCS_ROOT_DIR}\n")

    # 处理指定的文件
    for file_name in FILES_TO_PROCESS:
        abs_file_path = os.path.join(DOCS_ROOT_DIR, file_name)
        if os.path.isfile(abs_file_path):
            print(f"Processing file: {abs_file_path}")
            process_json_file(abs_file_path, OLD_BASE_URL, NEW_BASE_URL)
        else:
            print(f"Warning: Specified file not found - {abs_file_path}")
    
    print("\n--- Processing directories ---")
    # 处理指定目录中的所有 .json 文件
    for dir_name in DIRS_TO_PROCESS:
        abs_dir_path = os.path.join(DOCS_ROOT_DIR, dir_name)
        if os.path.isdir(abs_dir_path):
            print(f"Scanning directory: {abs_dir_path}")
            for root, _, files in os.walk(abs_dir_path):
                for file in files:
                    if file.endswith(".json"):
                        json_file_path = os.path.join(root, file)
                        print(f"Processing file: {json_file_path}")
                        process_json_file(json_file_path, OLD_BASE_URL, NEW_BASE_URL)
        else:
            print(f"Warning: Specified directory not found - {abs_dir_path}")
            
    print("\nUpdate process finished.")

if __name__ == "__main__":
    # 强烈建议在运行此脚本前备份您的 docs 文件夹。
    # confirm = input("IMPORTANT: This script will modify files in place. Have you backed up your 'docs' directory? (yes/no): ")
    # if confirm.lower() == 'yes':
    #     main()
    # else:
    #     print("Operation cancelled. Please back up your files before running the script.")
    main() # 直接运行，如果需要确认，请取消注释上面的确认代码块

