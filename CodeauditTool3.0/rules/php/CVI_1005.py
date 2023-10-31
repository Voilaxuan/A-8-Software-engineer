# -*- coding: utf-8 -*-

from cat.file import file_grep


class CVI_1005():
    def __init__(self):

        self.svid = 1005
        self.language = "PHP"
        self.author = "JANNEY W"
        self.vulnerability = "SQLI"
        self.description = "SQL injection"

        # status
        self.status = True

        # 部分配置
        self.match_mode = "function-param-regex"
        self.match = "(mysql_query|mysql_db_query)"#调用数据库的函数
        self.vul_function = None

    def main(self, regex_string):
        pass
