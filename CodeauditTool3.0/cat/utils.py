# -*- coding: utf-8 -*-

import hashlib
import os
import random
import re
import string
import sys
import time

from .config import rules_path
from .log import logger

TARGET_MODE_FILE = 'file'
TARGET_MODE_FOLDER = 'folder'

OUTPUT_MODE_STREAM = 'stream'
PY2 = sys.version_info[0] == 2


class ParseArgs(object):
    def __init__(self, target, formatter, output, special_rules=None, language=None, black_path=None, a_sid=None):
        self.target = target
        self.formatter = formatter
        self.output = output

        if special_rules is not None and special_rules is not '':
            self.special_rules = []
            extension = '.py'
            start_name = 'CVI_'

            if ',' in special_rules:#多条规则
                # check rule name
                s_rules = special_rules.split(',')#以逗号切分字符串
                #加入新规则
                for sr in s_rules:
                    if extension not in sr:
                        sr += extension
                    if start_name not in sr:
                        sr = start_name + sr

                    if self._check_rule_name(sr):
                        self.special_rules.append(sr)#规则在规则文件中存在则添加此特别规则
                    else:
                        logger.critical('[PARSE-ARGS] Rule {sr} not exist'.format(sr=sr))#反之则记录
            else:#一条规则
                special_rules = start_name + special_rules + extension

                if self._check_rule_name(special_rules):
                    self.special_rules = [special_rules]
                else:
                    logger.critical(
                        '[PARSE-ARGS] Exception special rule name(e.g: CVI-110001): {sr}'.format(sr=special_rules))
        else:
            self.special_rules = None

        self.black_path_list = []

        # check and deal language
        if language is not None and language is not "":
            self.language = []

            if ',' in language:
                self.language = [x.strip() for x in language.split(',') if x != ""]
                logger.info("[INIT][PARSE_ARGS] Language is {}".format(self.language))
            else:
                self.language = [language.strip()]
                logger.warning("[INIT][PARSE_ARGS] Language parse error.")

        self.sid = a_sid

    @staticmethod
    #检查规则文件中是否存在name规则，如果存在返回true
    def _check_rule_name(name):
        paths = os.listdir(rules_path)#返回rules_path下的文件和文件夹列表，rules_path)在.config中（rules文件）

        for p in paths:
            try:
                if name in os.listdir(rules_path + "/" + p):
                    return True
            except:
                continue

        return False


    @property
    def target_mode(self):
        target_mode = None

        if os.path.isfile(self.target):
            target_mode = TARGET_MODE_FILE
        if os.path.isdir(self.target):
            target_mode = TARGET_MODE_FOLDER
        if target_mode is None:
            logger.critical('[PARSE-ARGS] [-t <target>] can\'t empty!')#严重错误信息写入日志
            exit()
        logger.debug('[PARSE-ARGS] Target Mode: {mode}'.format(mode=target_mode))
        return target_mode#返回目标类型（文件，目录，git）

    @property
    def output_mode(self):
        return 'stream'#返回输出类型

    def target_directory(self, target_mode):
        target_directory = None
        if target_mode == TARGET_MODE_FOLDER:
            target_directory = self.target
        elif target_mode == TARGET_MODE_FILE:
            target_directory = self.target
            return target_directory
        #目标为文件或文件夹类型时，路径为目标本身
        else:
            logger.critical('[PARSE-ARGS] exception target mode ({mode})'.format(mode=target_mode))
            exit()

        logger.debug('[PARSE-ARGS] target directory: {directory}'.format(directory=target_directory))
        target_directory = os.path.abspath(target_directory)#返回绝对路径
        if target_directory[-1] == '/':
            return target_directory
        else:
            return u'{t}/'.format(t=target_directory)


def to_bool(value):
    """Converts 'something' to boolean. Raises exception for invalid formats"""
    if str(value).lower() in ("on", "yes", "y", "true", "t", "1"):
        return True
    if str(value).lower() in ("off", "no", "n", "false", "f", "0", "0.0", "", "none", "[]", "{}"):
        return False
    raise Exception('Invalid value for boolean conversion: ' + str(value))


def convert_time(seconds):
    one_minute = 60
    minute = seconds / one_minute
    if minute == 0:
        return str(seconds % one_minute) + "\""
    else:
        return str(int(minute)) + "'" + str(seconds % one_minute) + "\""


def convert_number(n):
    if n is None:
        return '0'
    n = str(n)
    if '.' in n:
        dollars, cents = n.split('.')
    else:
        dollars, cents = n, None

    r = []
    for i, c in enumerate(str(dollars)[::-1]):
        if i and (not (i % 3)):
            r.insert(0, ',')
        r.insert(0, c)
    out = ''.join(r)
    if cents:
        out += '.' + cents
    return out


def md5(content):
    """
    MD5 Hash
    :param content:
    :return:
    """
    content = content.encode('utf8')
    return hashlib.md5(content).hexdigest()


def path_to_short(path, max_length=36):
    if len(path) < max_length:
        return path
    paths = path.split('/')
    paths = filter(None, paths)
    paths = list(paths)
    tmp_path = ''
    for i in range(0, len(paths)):
        logger.debug((i, str(paths[i]), str(paths[len(paths) - i - 1])))
        tmp_path = tmp_path + str(paths[i]) + '/' + str(paths[len(paths) - i - 1])
        if len(tmp_path) > max_length:
            tmp_path = ''
            for j in range(0, i):
                tmp_path = tmp_path + '/' + str(paths[j])
            tmp_path += '/...'
            for k in range(i, 0, -1):
                tmp_path = tmp_path + '/' + str(paths[len(paths) - k])
            if tmp_path == '/...':
                return '.../{0}'.format(paths[len(paths) - 1])
            elif tmp_path[0] == '/':
                return tmp_path[1:]
            else:
                return tmp_path


def path_to_file(path):
    paths = path.split('/')
    paths = list(filter(None, paths))
    length = len(paths)
    return '.../{0}'.format(paths[length - 1])


def percent(part, whole, need_per=True):
    if need_per:
        per = '%'
    else:
        per = ''
    if part == 0 and whole == 0:
        return 0
    return '{0}{1}'.format(100 * float(part) / float(whole), per)


def timestamp():
    """Get timestamp"""
    return int(time.time())


def format_gmt(time_gmt, time_format=None):
    if time_format is None:
        time_format = '%Y-%m-%d %X'
    t = time.strptime(time_gmt, "%a, %d %b %Y %H:%M:%S GMT")
    return time.strftime(time_format, t)


def random_generator(size=6, chars=string.ascii_uppercase + string.digits):#chars为大写字母和数字
    return ''.join(random.choice(chars) for _ in range(size))#随机6个大写字母或数字用空格隔开


def is_list(value):
    """
    Returns True if the given value is a list-like instance

    >>> is_list([1, 2, 3])
    True
    >>> is_list(u'2')
    False
    """

    return isinstance(value, (list, tuple, set))


def get_unicode(value, encoding=None, none_to_null=False):
    """
    Return the unicode representation of the supplied value:

    >>> get_unicode(u'test')
    u'test'
    >>> get_unicode('test')
    u'test'
    >>> get_unicode(1)
    u'1'
    """

    if none_to_null and value is None:
        return None
    if str(type(value)) == "<class 'bytes'>":
        value = value.encode('utf8')
        return value
    elif str(type(value)) == "<type 'unicode'>":
        return value
    elif is_list(value):
        value = list(get_unicode(_, encoding, none_to_null) for _ in value)
        return value
    else:
        try:
            return value.encode('utf8')
        except UnicodeDecodeError:
            return value.encode('utf8', errors="ignore")


def get_safe_ex_string(ex, encoding=None):
    """
    Safe way how to get the proper exception represtation as a string
    (Note: errors to be avoided: 1) "%s" % Exception(u'\u0161') and 2) "%s" % str(Exception(u'\u0161'))

    >>> get_safe_ex_string(Exception('foobar'))
    u'foobar'
    """

    ret = ex

    if getattr(ex, "message", None):
        ret = ex.message
    elif getattr(ex, "msg", None):
        ret = ex.msg

    return get_unicode(ret or "", encoding=encoding).strip()


class Tool:
    def __init__(self):

        # `grep` (`ggrep` on Mac)
        #查找字符串
        if os.path.isfile('/bin/grep'):
            self.grep = '/bin/grep'
        elif os.path.isfile('/usr/bin/grep'):
            self.grep = '/usr/bin/grep'
        elif os.path.isfile('/usr/local/bin/grep'):
            self.grep='/usr/local/bin/grep'
        else:
            self.grep = 'grep'


        # `find` (`gfind` on Mac)
        #查找文件
        if os.path.isfile('/bin/find'):
            self.find = '/bin/find'
        elif os.path.isfile('/usr/bin/find'):
            self.find = '/usr/bin/find'
        elif os.path.isfile('/usr/local/bin/find'):
            self.find='/usr/local/bin/find'
        else:
            self.find = 'find'

def secure_filename(filename):
    _filename_utf8_strip_re = re.compile(u"[^\u4e00-\u9fa5A-Za-z0-9_.\-\+]")
    _windows_device_files = ('CON', 'AUX', 'COM1', 'COM2', 'COM3', 'COM4', 'LPT1', 'LPT2', 'LPT3', 'PRN', 'NUL')

    try:
        text_type = unicode  # Python 2
    except NameError:
        text_type = str      # Python 3

    if isinstance(filename, text_type):
        from unicodedata import normalize
        filename = normalize('NFKD', filename).encode('utf-8', 'ignore')
        if not PY2:
            filename = filename.decode('utf-8')
    for sep in os.path.sep, os.path.altsep:
        if sep:
            filename = filename.replace(sep, ' ')
    if PY2:
        filename = filename.decode('utf-8')
    filename = _filename_utf8_strip_re.sub('', '_'.join(filename.split()))

    # on nt a couple of special files are present in each folder.  We
    # have to ensure that the target file is not such a filename.  In
    # this case we prepend an underline
    if os.name == 'nt' and filename and filename.split('.')[0].upper() in _windows_device_files:
        filename = '_' + filename

    return filename

def pretty_code_js(code):
    """
    美化代码使代码可读
    :param code:
    :return:
    """
    lines = code.split('\n')

    indent = 0
    formatted = []

    oldchar = '\0'
    is_comment = False
    is_function = False
    is_array = False
    is_tuple = False
    is_dict = False

    for line in lines:
        newline = []

        is_string = False
        is_regex = False

        for char in line:

            nowoldchar = oldchar
            oldchar = char

            # 处理大括号
            if nowoldchar == '{' and char == '}' and len(newline):
                newline.pop(-1)
                newline.pop(-1)
                newline.append(char)
                is_dict = False
                continue

            # 多行注释
            if char == '*' and nowoldchar == '/':
                if len(newline):
                    newline.pop(-1)
                is_comment = True
                break

            if is_comment and char == '/' and nowoldchar == '*':
                is_comment = False
                continue

            if is_comment:
                continue

            newline.append(char)

            # 一个特殊问题，正则表达式
            if not is_regex and not is_string and nowoldchar == '(' and char == '/':
                is_regex = True
                continue

            if is_regex and char == '/' and nowoldchar != '\\':
                is_regex = False
                continue

            if is_regex:
                continue

            # 处理字符串
            if not is_string and char == '`':
                is_string = '`'
                continue

            if is_string == '`' and char == '`' and nowoldchar != '\\':
                is_string = False
                continue

            if not is_string and char == '"':
                is_string = '"'
                continue

            if is_string == '"' and char == '"' and nowoldchar != '\\':
                is_string = False
                continue

            if not is_string and char == "'":
                is_string = "'"
                continue

            if is_string == "'" and char == "'" and nowoldchar != '\\':
                is_string = False
                continue

            if is_string:
                continue

            # 处理注释
            if char == '/' and nowoldchar == '/':
                # is_comment = True
                newline.append('\n')
                break

            if char == '!' and nowoldchar == '<':
                # is_comment = True
                newline.append('\n')
                break

            # 处理特殊对象
            if char == "[":
                is_array = True
                continue

            if is_array and char == ']':
                is_array = False
                continue

            if char == "(":
                is_tuple = True
                continue

            if is_tuple and char == ')':
                is_tuple = False
                continue

            if (is_dict or is_array) and not is_tuple and char == ',':
                newline.append("\n")
                newline.append("\t" * indent)

            if char == ';':
                newline.append("\n")
                newline.append("\t" * indent)

            if char == '{' and nowoldchar == 'n':
                indent += 1
                newline.append("\n")
                newline.append("\t" * indent)
                is_function = True

            if char == '{' and nowoldchar != 'n':
                indent += 1
                newline.append("\n")
                newline.append("\t" * indent)
                is_dict = True

            if char == "}":
                indent -= 1
                newline.append("\n")
                newline.append("\t" * indent)
                is_function = True if is_dict else False
                is_dict = False

        formatted.append("\t" * indent + "".join(newline))

    return "".join(formatted)
