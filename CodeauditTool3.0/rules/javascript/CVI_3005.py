# -*- coding: utf-8 -*-

class CVI_3005():

    def __init__(self):

        self.svid = 3005
        self.language = "JavaScript"
        self.author = ""
        self.vulnerability = "Command Injection"
        self.description = "Command Injection"

        # status
        self.status = True

        # 部分配置
        self.match_mode = "function-param-regex"
        self.match = "child_process|exec|child_process|spawn|os/.system"
        #Functions that might execute js
        self.vul_function = None

    def main(self, regex_string):
        pass