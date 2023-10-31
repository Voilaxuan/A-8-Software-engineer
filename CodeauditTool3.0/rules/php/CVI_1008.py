# -*- coding: utf-8 -*-

from cat.file import file_grep


class CVI_1008():


    def __init__(self):

        self.svid = 1008
        self.language = "PHP"
        self.author = "JANNEY W"
        self.vulnerability = "Xml injection"
        self.description = "Xml injection"

        # status
        self.status = True

        # 部分配置
        self.match_mode = "function-param-regex"
        self.match = "simplexml_load_file|simplexml_load_string"
        #执行xml的函数
        self.vul_function = None

    def main(self, regex_string):

        pass
