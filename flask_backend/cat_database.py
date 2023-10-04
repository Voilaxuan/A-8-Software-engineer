import sqlite3

# 连接到SQLite数据库（将'your_database.db'替换为您的数据库文件路径）
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# 获取数据库中所有表的表名
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
table_names = cursor.fetchall()

# 遍历所有表
for table in table_names:
    table_name = table[0]
    print(f"表名: {table_name}")

    # 查询表中的所有数据
    cursor.execute(f"SELECT * FROM {table_name};")
    rows = cursor.fetchall()

    # 打印表中的数据
    for row in rows:
        print(row)

# 关闭数据库连接
conn.close()