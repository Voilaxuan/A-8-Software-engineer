# -*- coding: utf-8 -*-

import re#正则表达式模块
import os
import time
import codecs
import traceback
from .log import logger
from .pretreatment import ast_object
from .const import ext_dict

try:
    from urllib import quote
except ImportError:
    from urllib.parse import quote


ext_list = []
for e in ext_dict:
    ext_list += ext_dict[e]


def file_list_parse(filelist, language=None):
    result = []
    self_ext_list = ext_list

    if not filelist:
        return result

    if language is not None and language in ext_dict:
        self_ext_list = ext_dict[language]

    for file in filelist:
        if file[0] in self_ext_list:
            result.extend(file[1]['list'])

    return result


def get_line(file_path, line_rule):
    """
    搜索指定文件的指定行到指定行的内容
    :param file_path: 指定文件
    :param line_rule: 指定行规则
    :return: 
    """
    s_line = int(line_rule.split(',')[0])
    e_line = int(line_rule.split(',')[1][:-1])
    result = []

    file = codecs.open(file_path, "r", encoding='utf-8', errors='ignore')
    line_number = 0
    for line in file:
        line_number += 1
        if s_line <= line_number <= e_line:
            result.append(line)

    return result


def file_grep(file_path, rule_reg):
    """
    获取指定文件匹配的行    
    :param file_path: 
    :param rule_reg: 
    :return: 
    """
    result = []

    if os.path.isfile(file_path):
        file = codecs.open(file_path, "r", encoding='utf-8', errors='ignore')
        line_number = 0
        for line in file:
            line_number += 1
            if re.search(rule_reg, line, re.I):
                result.append((file_path, str(line_number), line))

        return result
    else:
        logger.warning("[FILE_GREP] Try to open a undefined file")
        return result


def check_filepath(target, filepath):
    if os.path.isfile(target):
        return target
    else:
        return os.path.join(target, filepath)


class FileParseAll:
    def __init__(self, filelist, target, language=None):
        self.filelist = filelist
        self.t_filelist = file_list_parse(filelist, language)
        self.target = target

    def grep(self, reg):
        """
        遍历目标filelist，匹配文件内容
        :param reg: 内容匹配正则
        :return: 
        """
        result = []

        for ffile in self.t_filelist:
            filepath = check_filepath(self.target, ffile)

            file = codecs.open(filepath, "r", encoding='utf-8', errors='ignore')#以指定编码方式读取文件数据
            line_number = 0
            for line in file:
                line_number += 1#逐行匹配
                # print line, line_number
                if re.search(reg, line, re.I):#扫描整个字符串并返回第一个成功的匹配，忽略大小写
                    result.append((filepath, str(line_number), line))#记录结果

        return result

    def multi_grep(self, reg):
        """
        多行匹配，对全文做匹配
        :param reg: 
        :return: 
        """
        result = []
        line_number = 0

        for ffile in self.t_filelist:
            filepath = check_filepath(self.target, ffile)#检查目标文件

            file = codecs.open(filepath, "r", encoding='utf-8', errors='ignore')#以指定编码方式读取文件数据
            content = file.read()
            file.close()

            r_con_obj = re.search(reg, content, re.I)#扫描整个字符串并返回第一个成功的匹配，忽略大小写
            #reg为正则表达式，content为带匹配字符串，为所有代码

            if r_con_obj:#匹配到了
                start_pos = r_con_obj.regs[0][0]
                line_number = len(content[:start_pos].split('\n'))#获取行号
                result.append((filepath, str(line_number), r_con_obj.group(0)))#记录结果

        return result
    
    def multi_grep_content(self, reg, content):
        content_tmp = content
        result = []
        while 1:
            r_con_obj = re.search(reg, content_tmp, re.I)
            if r_con_obj:
                start_pos = r_con_obj.regs[0][0]
                line_number = len(content[:start_pos].split('\n'))
                result.append([str(line_number), r_con_obj.group(0)])

                content_tmp = content_tmp[r_con_obj.regs[0][1]:]
            else:
                break
        return result

    def multi_grep_name(self, matchs, unmatchs, matchs_name, black_list):
        """
        匹配变量/函数名
        :param matchs: 全中则为漏洞
        :param unmatchs: 中一个则忽略漏洞
        :param matchs_name: 匹配变量名或函数名或其他名称
        :param black_list: 黑名单，根据reg中选择的组，过滤整个匹配结果或只过滤匹配的name
        :return: 返回匹配结果的list
        """
        result = []

        for ffile in self.t_filelist:
            filepath = check_filepath(self.target, ffile)

            file = codecs.open(filepath, "r", encoding='utf-8', errors='ignore')
            content = file.read()
            file.close()

            # 变量名
            name = []
            re_result_list = re.findall(matchs_name,content)

            for re_result in re_result_list:
                re_flag = True
                # 正确使用，即reg = '(function aloha (_to) aloha)'，re_result形如 ("function balanceOf(address owner);","_to")
                if len(re_result) == 2:# ['owner','function xxx(address owner)']
                    for black in black_list:
                        if black in re_result[0] or black in re_result[1]:
                            re_flag = False
                            logger.debug('[DEBUG] [GREP_NAME_BLACK_LIST] match varname {0} in black list {1}'.format(re_result[0], black))
                    if re_flag:
                        name.append(re_result[1])
                        logger.debug('[DEBUG] [GREP_NAME_WITH_GROUP(0)_BLACK_CHECK] success match varname:{0}'.format(re_result[0]))
                elif len(re_result) == 1: # ['owner']
                    for black in black_list:
                        if black in re_result[0]:
                            re_flag = False
                            logger.debug('[DEBUG] [GREP_NAME_BLACK_LIST] match varname {0} in black list {1}'.format(re_result[0], black))
                    if re_flag:
                        name.append(re_result[0])
                        logger.debug('[DEBUG] [GREP_NAME_SINGLE_VARNAME] success match varname:{0}'.format(re_result[0]))
                elif isinstance(re_result,str): #字符串'owner'
                    for black in black_list:
                        if black in re_result:
                            re_flag = False
                            logger.debug('[DEBUG] [GREP_NAME_BLACK_LIST] match varname {0} in black list {1}'.format(re_result, black))
                    if re_flag:
                        name.append(re_result)
                        logger.debug('[DEBUG] [GREP_NAME_STR] success match varname:{0}'.format(re_result))
                else:
                    name.append(re_result)
                    logger.warning('[WARNING] [GREP_NAME_ERROR] match unknown-type varname {0}'.format(re_result))

            name = list(set(name))
            for n in name:
                if len(n) >= 32:
                    name.remove(n)

            for n in name:
                matchs_tmp = [match.replace("=padding=", n) for match in matchs]
                unmatchs_tmp = [unmatch.replace("=padding=", n) for unmatch in unmatchs]

                re_flag = True
                line_number = 0

                # 只要一次成功，则不是漏洞
                for unmatch in unmatchs_tmp:
                    result_tmp = self.multi_grep_content(unmatch, content)
                    if result_tmp is not None and result_tmp != []:
                        re_flag = False
                        logger.debug('[DEBUG] [UNMATCH_REGEX_RETURN_REGEX] unmatch grep:{0} by rule {1}'.format(n, unmatch))
                        continue

                if re_flag:
                    # 例如CVI2100中，没有match，只要不含unmatch即为漏洞的，没有行数
                    if matchs_tmp == []:
                        result.append(tuple([filepath, str(line_number), 'name:<'+n+'>']))
                        logger.debug('[DEBUG] [MATCH_REGEX_RETURN_REGEX] success match:{0} in line {1}'.format(n, str(line_number)))
                        continue

                    # 正常的match，但条件为或
                    for match in matchs_tmp:
                        result_list_tmp = self.multi_grep_content(match, content)

                        if result_list_tmp is not None and result_list_tmp != []:
                            for result_tmp in result_list_tmp:
                                result.append(tuple([filepath, str(line_number), 'name:<'+result_tmp[0]+'>, point:<'+result_tmp[1]+'>']))
                                logger.debug('[DEBUG] [MATCH_REGEX_RETURN_REGEX] success match:{0} in line {1}'.format(n, str(line_number)))
                        else:
                            re_flag = False

        return result

    def keyword_object_parse(self, keywords, object, index=0):
        tmp_manifest = object
        value_list = []

        for key in keywords[index:]:

            if index+1 == len(keywords):

                if key not in tmp_manifest:
                    value_list.extend([None])
                    break

                value_list.extend([str(tmp_manifest[key])])
                break

            if key is not "*":
                if key in tmp_manifest:
                    tmp_manifest = tmp_manifest[key]
                    index += 1
                else:
                    value_list.extend([None])
                    logger.warning("[REGEX][FILE] Special keyword {} Not found in object {}".format(key, object))
                    break
            else:
                for i in tmp_manifest:
                    value_list.extend(self.keyword_object_parse(keywords=keywords, object=i, index=index+1))

                break

        return value_list


class Directory(object):
    def __init__(self, absolute_path, black_path_list=[]):
        self.absolute_path = absolute_path
        self.black_path_list = ['.crx_files']

        self.black_path_list.extend(black_path_list)

    file_sum = 0
    type_nums = {}
    result = {}
    file = []

    """
    :return {'.php': {'count': 2, 'list': ['/path/a.php', '/path/b.php']}}, file_sum, time_consume
    """

    def collect_files(self):
        t1 = time.time()
        self.files(self.absolute_path)
        self.result['no_extension'] = {'count': 0, 'list': []}#初始化结果
        for extension, values in self.type_nums.items():
            extension = extension.strip()#去除字符串首尾的空格或换行符
            self.result[extension] = {'count': len(values), 'list': []}#计算数量
            # .php : 123
            logger.debug('[PICKUP] [EXTENSION-COUNT] {0} : {1}'.format(extension, len(values)))
            for f in self.file:
                es = f.split(os.extsep)#对字符串进行分片
                if len(es) >= 2:
                    # Exists Extension
                    # os.extsep + es[len(es) - 1]
                    if f.endswith(extension):#若f以extension结尾，则返回true
                        self.result[extension]['list'].append(f)#在result列表末尾添加f字符串
                else:
                    # Didn't have extension
                    self.result['no_extension']['count'] = int(self.result['no_extension']['count']) + 1#计数器+1
                    self.result['no_extension']['list'].append(f)
        if self.result['no_extension']['count'] == 0:
            del self.result['no_extension']
        t2 = time.time()
        # reverse list count
        self.result = sorted(self.result.items(), key=lambda t: t[0], reverse=False)#对结果排序
        return self.result, self.file_sum, t2 - t1#返回结果，文件数，用时

    def files(self, absolute_path, level=1):
        if level == 1:
            logger.debug('[PICKUP] ' + absolute_path)
        try:
            if os.path.isfile(absolute_path):
                filename, directory = os.path.split(absolute_path)
                self.file_info(directory, filename)
            else:
                for filename in os.listdir(absolute_path):
                    directory = os.path.join(absolute_path, filename)

                    flag = 0

                    # check black path list
                    if self.black_path_list:
                        for black_path in self.black_path_list:
                            if black_path in filename:
                                flag = 1

                    if flag:
                        continue

                    # Directory Structure
                    logger.debug('[PICKUP] [FILES] ' + '|  ' * (level - 1) + '|--' + filename)
                    if os.path.isdir(directory):
                        self.files(directory, level + 1)
                    if os.path.isfile(directory):
                        self.file_info(directory, filename)
        except OSError as e:
            logger.error("[PICKUP] {}".format(traceback.format_exc()))
            logger.critical('[PICKUP] {msg}'.format(msg=e))
            exit()

    def file_info(self, path, filename):
        # Statistic File Type Count
        file_name, file_extension = os.path.splitext(path)
        self.type_nums.setdefault(file_extension.lower(), []).append(filename)

        path = path.replace(self.absolute_path, '')
        self.file.append(path)
        self.file_sum += 1


class File(object):
    def __init__(self, file_path):
        self.file_path = file_path

    def read_file(self):
        """
        读取文件内容
        :return:
        """
        file = codecs.open(self.file_path, "r", encoding='utf-8', errors='ignore')
        f = file.read()
        return f

    def lines(self, line_rule):
        """
        获取指定行内容
        :param line_rule:
        :return:
        """
        result = get_line(self.file_path, line_rule)
        result = "\n".join(result)

        if len(result):
            try:
                content = result.decode('utf-8')
            except AttributeError as e:
                content = result
            if content == '':
                content = False
        else:
            content = False
        return content

