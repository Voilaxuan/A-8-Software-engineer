# -*- coding: utf-8 -*-

class CVI_2006():

    def __init__(self):

        self.svid = 2006
        self.language = "JAVA"
        self.author = ""
        self.vulnerability = "CSRF"
        self.description = "Cross-site request forgery"

        # status
        self.status = True

        # 部分配置
        self.match_mode = "function-param-regex"
        self.match = "token|Formtoken"
        self.vul_function = None

    def main(self, regex_string):
        pass