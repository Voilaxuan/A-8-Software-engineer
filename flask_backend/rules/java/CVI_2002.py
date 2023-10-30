# -*- coding: utf-8 -*-

class CVI_2002():

    def __init__(self):

        self.svid = 2002
        self.language = "JAVA"
        self.author = ""
        self.vulnerability = "SSRF"
        self.description = "Server-Side Request Forgery"

        # status
        self.status = True

        # 部分配置
        self.match_mode = "function-param-regex"
        self.match = "URLConnection|HttpClient|HttpGet|okHttpclient|okHttpclient|new URL"
        self.vul_function = None

    def main(self, regex_string):
        pass