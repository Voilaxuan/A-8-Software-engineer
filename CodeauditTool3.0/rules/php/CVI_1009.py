# -*- coding: utf-8 -*-

from cat.file import file_grep


class CVI_1009():

    def __init__(self):

        self.svid = 1009
        self.language = "PHP"
        self.author = "JANNEY W"
        self.vulnerability = "RCE"
        self.description = "Remote code execute"

        # status
        self.status = True

        # 部分配置
        self.match_mode = "function-param-regex"
        # preg_replace  preg_replace_callback
        self.match = "(array_map|create_function|call_user_func|call_user_func_array|assert|eval|dl|register_tick_function|register_shutdown_function)"
        #preg_replace(),ob_start()？可以执行php代码的函数
        self.vul_function = None

    def main(self, regex_string):

        pass
