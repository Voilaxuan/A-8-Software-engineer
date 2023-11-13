# -*- coding: utf-8 -*-

class CVI_3007():

    def __init__(self):

        self.svid = 3007
        self.language = "JavaScript"
        self.author = ""
        self.vulnerability = "unserialize vulerablity"
        self.description = "unserialize vulerablity"

        # status
        self.status = True

        # 部分配置
        self.match_mode = "function-param-regex"
        self.match = "location.href|window.open|location.assign|location.replace"
        #Functions that might execute js
        self.vul_function = None

    def main(self, regex_string):
        pass