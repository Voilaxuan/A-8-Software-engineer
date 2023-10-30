# -*- coding: utf-8 -*-

import re


class CVI_1004():
    def __init__(self):

        self.svid = 1004
        self.language = "PHP"
        self.author = "JANNEY W"
        self.vulnerability = "SQLI"
        self.description = "SQL injection"

        # status
        self.status = True

        # 部分配置
        self.match_mode = "vustomize-match"
        self.match = "([\"\']+\s*(select|SELECT|insert|INSERT|update|UPDATE)\s+([^;]\s*)(.*)\$(.+?)[\'\"]+(.+?)?;)"
        #匹配查询、插入、更新语句
        self.vul_function = None

    def main(self, regex_string):
        sql_sen = regex_string[0][0]
        reg = "\$\w+"#一个变量
        if re.search(reg, sql_sen, re.I):

            p = re.compile(reg)
            match = p.findall(sql_sen)
            return match
        return None

