# -*- coding: utf-8 -*-

class CVI_3001():

    def __init__(self):

        self.svid = 3001
        self.language = "JavaScript"
        self.author = ""
        self.vulnerability = "CSRF"
        self.description = "Cross-site request forgery"

        # status
        self.status = True

        # 部分配置
        self.match_mode = "function-param-regex"
        self.match = "XMLHttpRequest|fetch|ajax|axios"
        #Functions that might execute js
        self.vul_function = None

    def main(self, regex_string):
        pass