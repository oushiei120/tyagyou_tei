import difflib
import os

def find_and_tag_annotations(text_with_notes, text_no_notes):
    """
    比较有注疏和无注疏的文本，用<note>标签标记注疏部分。

    Args:
        text_with_notes (str): 包含注疏的文本内容。
        text_no_notes (str): 不含注疏的文本内容。

    Returns:
        str: 标记了注疏的文本内容。
    """
    # 使用 SequenceMatcher 进行比较
    # text_no_notes 是序列 a, text_with_notes 是序列 b
    s = difflib.SequenceMatcher(None, text_no_notes, text_with_notes, autojunk=False)
    
    output_parts = []
    for tag, i1, i2, j1, j2 in s.get_opcodes():
        segment_from_with_notes = text_with_notes[j1:j2]
        if tag == 'equal': # 两部分文本相同
            output_parts.append(segment_from_with_notes)
        elif tag == 'insert': # 文本只存在于 text_with_notes (相对于 text_no_notes 是插入)
            output_parts.append(f"<note>{segment_from_with_notes}</note>")
        elif tag == 'replace': # text_no_notes 中的文本被 text_with_notes 中的文本替换
                              # 我们将 text_with_notes 中的这部分视为注疏
            output_parts.append(f"<note>{segment_from_with_notes}</note>")
        # 如果 tag == 'delete'，意味着 text_no_notes 中的某些文本在 text_with_notes 中不存在。
        # 由于我们是基于 text_with_notes 重建文本，这部分会自动被忽略。
        
    return "".join(output_parts)

def process_files(dir_with_notes, dir_no_notes, output_dir):
    """
    处理指定文件夹中的文件对，生成带标签的输出文件。

    Args:
        dir_with_notes (str): 包含注疏文件的文件夹路径。
        dir_no_notes (str): 不含注疏文件的文件夹路径。
        output_dir (str): 保存处理后文件的输出文件夹路径。
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"创建输出文件夹: {output_dir}")
    else:
        print(f"输出文件夹 '{output_dir}' 已存在。文件可能会被覆盖。")

    for i in range(1, 11):  # 文件名为 1 到 10
        file_base_name = str(i)
        
        # 尝试几种常见的文件名格式 (如 "1.txt" 或 "1")
        possible_filenames = [file_base_name + ".txt", file_base_name]
        
        actual_file_name_used = None
        path_with_notes = None
        path_no_notes = None

        for fname_candidate in possible_filenames:
            temp_path_with_notes = os.path.join(dir_with_notes, fname_candidate)
            temp_path_no_notes = os.path.join(dir_no_notes, fname_candidate)
            if os.path.exists(temp_path_with_notes) and os.path.exists(temp_path_no_notes):
                path_with_notes = temp_path_with_notes
                path_no_notes = temp_path_no_notes
                actual_file_name_used = fname_candidate
                break
        
        if not actual_file_name_used:
            print(f"警告: 未能找到文件对 '{file_base_name}' (尝试了 {possible_filenames})。已跳过。")
            continue

        try:
            print(f"正在处理文件: {actual_file_name_used}")
            with open(path_with_notes, 'r', encoding='utf-8') as f_with:
                text_with_notes_content = f_with.read()
            with open(path_no_notes, 'r', encoding='utf-8') as f_no:
                text_no_notes_content = f_no.read()

            tagged_text = find_and_tag_annotations(text_with_notes_content, text_no_notes_content)

            output_file_path = os.path.join(output_dir, actual_file_name_used)
            with open(output_file_path, 'w', encoding='utf-8') as f_out:
                f_out.write(tagged_text)
            print(f"已保存处理后的文件: {output_file_path}")

        except Exception as e:
            print(f"处理文件 '{actual_file_name_used}' 时发生错误: {e}")

# --- 请在这里配置您的路径 ---
# 包含注疏文件的文件夹路径
directory_with_notes = "/Users/oushiei/Documents/GitHub/tyagyou_tei/00tyagyou_text_bypku_注あり"
# 不含注疏文件的文件夹路径
directory_no_notes = "/Users/oushiei/Documents/GitHub/tyagyou_tei/00tyagyou_text_bypku_注なし"
# 处理后文件的输出文件夹路径 (脚本会自动创建)
output_directory = "/Users/oushiei/Documents/GitHub/tyagyou_tei/00tyagyou_text_bypku_注あり_tagged"
# --- 配置结束 ---

if __name__ == "__main__":
    # 检查路径是否存在
    if not os.path.isdir(directory_with_notes):
        print(f"错误: 包含注疏的文件夹路径不存在: {directory_with_notes}")
    elif not os.path.isdir(directory_no_notes):
        print(f"错误: 不含注疏的文件夹路径不存在: {directory_no_notes}")
    else:
        process_files(directory_with_notes, directory_no_notes, output_directory)
        print("处理完成。")