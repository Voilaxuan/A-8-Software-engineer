# -*- coding: utf-8 -*-

class CVI_3000():

    def __init__(self):

        self.svid = 3000
        self.language = "JavaScript"
        self.author = ""
        self.vulnerability = "XSS"
        self.description = "Cross-site scripting"
        #Inject malicious js code into web pages

        # status
        self.status = True

        # 部分配置
        self.match_mode = "function-param-regex"
        self.match = "innerHTML|outerHTML|document.write|eval|setTimeout|setInterval"
        #Functions that might execute js
        self.vul_function = None

    def main(self, regex_string):
        pass