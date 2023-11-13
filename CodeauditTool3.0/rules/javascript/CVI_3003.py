# -*- coding: utf-8 -*-

class CVI_3003():

    def __init__(self):

        self.svid = 3003
        self.language = "JavaScript"
        self.author = ""
        self.vulnerability = "RCE"
        self.description = "Remote Code Execution"

        # status
        self.status = True

        # 部分配置
        self.match_mode = "function-param-regex"
        self.match = "eval|Function|setTimeout|setInterval|new Function|child_process/.exec|child_process/.spawn|os/.system|os/.exec"
        #Functions that might execute js
        self.vul_function = None

    def main(self, regex_string):
        pass