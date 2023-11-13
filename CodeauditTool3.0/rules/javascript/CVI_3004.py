# -*- coding: utf-8 -*-

class CVI_3004():

    def __init__(self):

        self.svid = 3004
        self.language = "JavaScript"
        self.author = ""
        self.vulnerability = "SQLI"
        self.description = "SQL Injection"

        # status
        self.status = True

        # 部分配置
        self.match_mode = "function-param-regex"
        self.match = "execute|query|prepare|exec|execSQL"
        #Functions that might execute js
        self.vul_function = None

    def main(self, regex_string):
        pass