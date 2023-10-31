# -*- coding: utf-8 -*-

from cat.file import file_grep


class CVI_1014():

    def __init__(self):

        self.svid = 1014
        self.language = "PHP"
        self.author = "JANNEY W"
        self.vulnerability = "variable shadowing"
        self.description = "variable shadowing"

        # status
        self.status = True

        # 部分配置
        self.match_mode = "function-param-regex"
        self.match = "import_request_variables|parse_str|mb_parse_str|extract"
        #容易在接收变量时造成变量覆盖的函数
        self.vul_function = None

    def main(self, regex_string):

        pass
