# -*- coding: utf-8 -*-

from cat.file import file_grep


class CVI_1006():
    def __init__(self):

        self.svid = 1006
        self.language = "PHP"
        self.author = "JANNEY W"
        self.vulnerability = "SQLI"
        self.description = "SQL injection"

        # status
        self.status = True

        # 部分配置
        self.match_mode = "function-param-regex"
        self.match = "(mysqli_query|pg_execute|pg_insert|pg_query|pg_select|pg_update|sqlite_query|msql_query|mssql_query|odbc_exec|fbsql_query|sybase_query|ibase_query|dbx_query|ingres_query|ifx_query|oci_parse|sqlsrv_query|maxdb_query|db2_exec)\s?\(]"
        #其他一些可以调用sql语句的函数
        self.vul_function = None

    def main(self, regex_string):

        pass
