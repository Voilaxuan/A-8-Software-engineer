# -*- coding: utf-8 -*-

import re

class CVI_1001():

    def __init__(self):

        self.svid = 1001
        self.language = "PHP"
        self.author = "JANNEY W"
        self.vulnerability = "SSRF"
        self.description = "cURL SSRF"

        # status
        self.status = True

        # 部分配置
        self.match_mode = "vustomize-match"
        self.match = "curl_setopt\s*\(.*,\s*CURLOPT_URL\s*,(.*)\)"
        self.vul_function = None

    def main(self, regex_string):
        sql_sen = regex_string[0]
        reg = "\$[\w+\->]*"
        if re.search(reg, sql_sen, re.I):

            p = re.compile(reg)
            match = p.findall(sql_sen)
            return match
        return None

