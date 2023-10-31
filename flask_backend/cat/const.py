# -*- coding: utf-8 -*-

# Match-Mode
mm_function_param_controllable = 'function-param-regex'  # 函数正则匹配
mm_regex_param_controllable = 'vustomize-match'  # 自定义匹配
mm_regex_only_match = 'only-regex'
mm_regex_return_regex = 'regex-return-regex'
sp_crx_keyword_match = "special-crx-keyword-match"  # crx特殊匹配

match_modes = [
    mm_regex_only_match,
    mm_regex_param_controllable,
    mm_function_param_controllable,
    mm_regex_return_regex,
    sp_crx_keyword_match,
]

fpc = '\s*\((.*)(?:\))'
fpc_single = '[f]{fpc}'.format(fpc=fpc)
fpc_multi = '(?:[f]){fpc}'.format(fpc=fpc)
fpc_loose = '(?:[f])({fpc})?\\b'.format(fpc=fpc)


fav = '\$([a-zA-Z_\x7f-\xff][a-zA-Z0-9_\x7f-\xff]*)'

ext_dict = {
    "php": ['.php', '.php3', '.php4', '.php5', '.php7', '.pht', '.phs', '.phtml'],
    "solidity": ['.sol'],
    "javascript": ['.js'],
    "chromeext": ['.crx'],
}
