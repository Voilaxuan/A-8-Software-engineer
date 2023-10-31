# -*- coding: utf-8 -*-

class CVI_2004():

    def __init__(self):

        self.svid = 2004
        self.language = "JAVA"
        self.author = ""
        self.vulnerability = "URL Redirector Abuse"
        self.description = "Attackers construct malicious jump links"

        # status
        self.status = True

        # 部分配置
        self.match_mode = "function-param-regex"
        self.match = "sendRedirect|setHeader|forward"
        self.vul_function = None

    def main(self, regex_string):
        pass