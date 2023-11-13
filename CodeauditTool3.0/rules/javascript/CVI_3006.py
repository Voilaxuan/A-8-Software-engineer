# -*- coding: utf-8 -*-

class CVI_3006():

    def __init__(self):

        self.svid = 3006
        self.language = "JavaScript"
        self.author = ""
        self.vulnerability = "RFI"
        self.description = "remote file include"

        # status
        self.status = True

        # 部分配置
        self.match_mode = "function-param-regex"
        self.match = "fs|sendFile|path/.resolve|path/.join|path/.normalize"
        #Functions that might execute js
        self.vul_function = None

    def main(self, regex_string):
        pass