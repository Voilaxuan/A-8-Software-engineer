# -*- coding: utf-8 -*-

from cat.file import file_grep


class CVI_1010():

    def __init__(self):

        self.svid = 1010
        self.language = "PHP"
        self.author = "JANNEY W"
        self.vulnerability = "LDAPI"
        self.description = "LDAP injection"
        #轻量级目录访问协议注入

        # status
        self.status = True

        # 部分配置
        self.match_mode = "function-param-regex"
        self.match = "(ldap_add|ldap_delete|ldap_list|ldap_read|ldap_search|ldap_bind)"
        #LADP操作函数
        self.vul_function = None

    def main(self, regex_string):

        pass
