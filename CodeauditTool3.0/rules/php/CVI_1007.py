# -*- coding: utf-8 -*-

from cat.file import file_grep


class CVI_1007():

    def __init__(self):

        self.svid = 1007
        self.language = "PHP"
        self.author = "JANNEY W"
        self.vulnerability = "RFI"
        self.description = "remote file include"

        # status
        self.status = True

        # 部分配置
        self.match_mode = "function-param-regex"
        self.match = "include|include_once|require|require_once|parsekit_compile_file|php_check_syntax|runkit_import|virtual"
        #可以造成文件包含的函数（执行文件）
        self.vul_function = None

    def main(self, regex_string):

        pass
