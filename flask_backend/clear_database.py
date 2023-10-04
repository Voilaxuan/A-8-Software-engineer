import shutil
import sqlite3
import os

def delete_folder_contents(folder_path):
    try:
        # 确保路径存在
        if os.path.exists(folder_path):
            # 遍历文件夹内的所有项
            for item in os.listdir(folder_path):
                item_path = os.path.join(folder_path, item)
                if os.path.isfile(item_path):
                    # 如果是文件，删除文件
                    os.remove(item_path)
                elif os.path.isdir(item_path):
                    # 如果是文件夹，递归删除文件夹及其内容
                    shutil.rmtree(item_path)
                    # 连接到数据库
                    conn = sqlite3.connect('users.db')
                    cursor = conn.cursor()
                    # 删除列表中的所有数据
                    cursor.execute('DELETE FROM files')
                    conn.commit()
                    conn.close()
            print(f"成功删除文件夹内的所有内容：{folder_path}，以及数据库内容")
        else:
            print(f"文件夹不存在：{folder_path}")
    except Exception as e:
        print(f"删除文件夹内内容时出错：{e}")

# 用法示例：指定要删除内容的文件夹路径
folder_to_clear = "./usersfiles"
delete_folder_contents(folder_to_clear)