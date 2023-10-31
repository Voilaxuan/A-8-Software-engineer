# -*- coding: utf-8 -*-

PHP_IS_REPAIR_DEFAULT = {
    "urlencode": [1000, 10001],
    "rawurlencode": [1000, 10001],
    "htmlspecialchars": [1000, 10001],
    "htmlentities": [1000, 10001],
    "ldap_escape": [1010],
    "mysql_real_escape_string": [1004, 1005, 1006],
    "addslashes": [1004, 1005, 1006],
    "intval": [1004, 1005, 1006],
    "escapeshellcmd": [1009, 1011],
    "escapeshellarg": [1009, 1011],
}

PHP_IS_CONTROLLED_DEFAULT = [
    "$_GET",
    "$_POST",
    "$_REQUEST",
]
