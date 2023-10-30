# -*- coding: utf-8 -*-


from cat.file import file_grep


class CVI_1015():


    def __init__(self):

        self.svid = 1015
        self.language = "PHP"
        self.author = "JANNEY W"
        self.vulnerability = "unserialize vulerablity"
        self.description = "unserialize vulerablity"
        #反序列化漏洞

        # status
        self.status = True

        # 部分配置
        self.match_mode = "function-param-regex"
        self.match = "is_a|unserialize"
        #如果变量可控，输入序列化的类可以控制类中的变量
        self.vul_function = None

    def main(self, regex_string):

        pass
