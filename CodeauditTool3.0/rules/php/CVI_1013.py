# -*- coding: utf-8 -*-


from cat.file import file_grep


class CVI_1013():

    def __init__(self):

        self.svid = 1013
        self.language = "PHP"
        self.author = "JANNEY W"
        self.vulnerability = "URL Redirector Abuse"
        #url重定向
        self.description = "URL Redirector Abuse"

        # status
        self.status = True

        # 部分配置
        self.match_mode = "function-param-regex"
        self.match = "header"
        #$redirect_url = $_GET['url'];header("Location: " . $redirect_url)针对这种情况
        #过滤方法：
        # $redirect_url = GET[′url′];if (strstr(_GET[ &  # x27;url&#x27;];
        #                                       if (strstr(G​ET[′url′]; if (strstr(redirect_url, “www.landgrey.me”) !=
        # = false){
        # header(“Location: " . $redirect_url);
        # }
        # else {
        #     die(“Forbidden”);
        # }
        self.vul_function = None

    def main(self, regex_string):

        pass
