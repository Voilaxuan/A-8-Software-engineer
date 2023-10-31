# -*- coding: utf-8 -*-

from cat.file import file_grep


class CVI_1011():

    def __init__(self):

        self.svid = 1011
        self.language = "PHP"
        self.author = "JANNEY W"
        self.vulnerability = "RCE"
        self.description = "Remote command execute"

        # status
        self.status = True

        # 部分配置
        self.match_mode = "function-param-regex"
        self.match = "(system|passthru|exec|pcntl_exec|shell_exec|popen|proc_open|ob_start|expect_popen|mb_send_mail|w32api_register_function|w32api_invoke_function|ssh2_exec)"
        #可以执行命令的函数
        self.vul_function = None

    def main(self, regex_string):

        pass
