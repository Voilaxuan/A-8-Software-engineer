# -*- coding: utf-8 -*-

class CVI_1000():

    def __init__(self):

        self.svid = 1000
        self.language = "PHP"
        self.author = "JANNEY W"
        self.vulnerability = "Reflected XSS"
        self.description = "Reflected XSS"

        # status
        self.status = True

        # 部分配置
        self.match_mode = "function-param-regex"
        self.match = "print|print_r|exit|die|printf|vprintf|trigger_error|user_error|odbc_result_all|ovrimos_result_all|ifx_htmltbl_result"
        #都是有输出变量功能的函数，如果被输出的变量没有被过滤，会导致反射型xss
        self.vul_function = None

    def main(self, regex_string):
        pass