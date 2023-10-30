# -*- coding: utf-8 -*-

from cat.file import file_grep


class CVI_1012():

    def __init__(self):

        self.svid = 1012
        self.language = "PHP"
        self.author = "JANNEY W"
        self.vulnerability = "Information Disclosure"
        self.description = "Information Disclosure"

        # status
        self.status = True

        # 部分配置
        self.match_mode = "function-param-regex"
        self.match = "(print_r|var_dump|show_source|highlight_file)\s*\("
        #输出信息的函数，调用时可能会输出敏感信息
        self.vul_function = None

    def main(self, regex_string):

        pass
