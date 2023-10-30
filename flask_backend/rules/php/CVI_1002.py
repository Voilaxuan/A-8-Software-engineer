# -*- coding: utf-8 -*-

from cat.file import file_grep


class CVI_1002():

    def __init__(self):

        self.svid = 1002
        self.language = "PHP"
        self.author = "JANNEY W"
        self.vulnerability = "SSRF"
        self.description = "file_get_contents SSRF"

        # status
        self.status = True

        # 部分配置
        self.match_mode = "function-param-regex"
        self.match = "file_get_contents"#是否可以加fsockopen()
        self.vul_function = None

    def main(self, regex_string):
        pass
