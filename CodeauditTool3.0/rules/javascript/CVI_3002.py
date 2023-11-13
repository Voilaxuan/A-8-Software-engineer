# -*- coding: utf-8 -*-

class CVI_3002():

    def __init__(self):

        self.svid = 3002
        self.language = "JavaScript"
        self.author = ""
        self.vulnerability = "SSTI"
        self.description = "Server-Side Template Injection"

        # status
        self.status = True

        # 部分配置
        self.match_mode = "function-param-regex"
        self.match = "eval|Function|setTimeout|setInterval|new Function"
        #Functions that might execute js
        self.vul_function = None

    def main(self, regex_string):
        pass