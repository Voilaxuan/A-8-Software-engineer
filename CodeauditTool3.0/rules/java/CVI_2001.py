# -*- coding: utf-8 -*-

class CVI_2001():

    def __init__(self):

        self.svid = 2001
        self.language = "JAVA"
        self.author = ""
        self.vulnerability = "unserialize vulerablity"
        self.description = "vulnerability of command execution during deserialization"

        # status
        self.status = True

        # 部分配置
        self.match_mode = "function-param-regex"
        self.match = "readObject|readUnshared|fromXML|toXML|readValue|parseObject|load"
        self.vul_function = None

    def main(self, regex_string):
        pass