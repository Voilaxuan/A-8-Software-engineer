# -*- coding: utf-8 -*-

class CVI_2003():

    def __init__(self):

        self.svid = 2003
        self.language = "JAVA"
        self.author = ""
        self.vulnerability = "File upload vulnerability"
        self.description = "Upload malicious files to the server"

        # status
        self.status = True

        # 部分配置
        self.match_mode = "function-param-regex"
        self.match = "MultipartFile"
        self.vul_function = None

    def main(self, regex_string):
        pass