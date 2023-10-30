# -*- coding: utf-8 -*-

from cat.file import file_grep


class CVI_1003():
    def __init__(self):

        self.svid = 1003
        self.language = "PHP"
        self.author = "JANNEY W"
        self.vulnerability = "SSRF"
        self.description = "get_headers SSRF"

        # status
        self.status = True

        # 部分配置
        self.match_mode = "function-param-regex"
        self.match = "get_headers"#参数为url，可以触发ssrf
        self.vul_function = None

    def main(self, regex_string):
        pass
