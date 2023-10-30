
from phply.phplex import lexer  # 词法分析
from phply.phpparse import make_parser  # 语法分析
from phply import phpast as php

import esprima
import jsbeautifier

from .log import logger
from .const import ext_dict

import gc
import os
import sys
import re
import json
import time
import codecs
import traceback
import zipfile
import queue
import asyncio

could_ast_pase_lans = ["php", "chromeext", "javascript"]


class Pretreatment:

    def __init__(self):
        self.file_list = []
        self.target_queue = queue.Queue()
        self.target_directory = ""

        self.pre_result = {}
        self.define_dict = {}

        self.pre_ast_all()

    def init_pre(self, target_directory, files):
        self.file_list = files
        self.target_directory = target_directory

        self.target_directory = os.path.normpath(self.target_directory)

    def get_path(self, filepath):

        if os.path.isfile(os.path.join(os.path.dirname(self.target_directory), filepath)):
            return os.path.normpath(os.path.join(os.path.dirname(self.target_directory), filepath))

        if os.path.isfile(self.target_directory):
            return os.path.normpath(self.target_directory)
        else:
            return os.path.normpath(os.path.join(self.target_directory, filepath))

    def pre_ast_all(self, lan=None):

        if lan is not None:
            # 检查是否在可ast pasre列表中
            if not list(set(lan).intersection(set(could_ast_pase_lans))):
                logger.info("[AST][Pretreatment] Current scan target language does not require ast pretreatment...")
                return True

        for fileext in self.file_list:
            self.target_queue.put(fileext)

        loop = asyncio.get_event_loop()
        scan_list = (self.pre_ast() for i in range(10))
        loop.run_until_complete(asyncio.gather(*scan_list))

    async def pre_ast(self):

        while not self.target_queue.empty():

            fileext = self.target_queue.get()

            if fileext[0] in ext_dict['php']:
                # 下面是对于php文件的处理逻辑
                for filepath in fileext[1]['list']:
                    all_nodes = []

                    filepath = self.get_path(filepath)
                    self.pre_result[filepath] = {}
                    self.pre_result[filepath]['language'] = 'php'
                    self.pre_result[filepath]['ast_nodes'] = []

                    fi = codecs.open(filepath, "r", encoding='utf-8', errors='ignore')
                    code_content = fi.read()
                    fi.close()

                    self.pre_result[filepath]['content'] = code_content

                    try:
                        parser = make_parser()
                        all_nodes = parser.parse(code_content, debug=False, lexer=lexer.clone(), tracking=True)

                        # 合并字典
                        self.pre_result[filepath]['ast_nodes'] = all_nodes

                    except SyntaxError as e:
                        logger.warning('[AST] [ERROR] parser {}: {}'.format(filepath, traceback.format_exc()))

                    except AssertionError as e:
                        logger.warning('[AST] [ERROR] parser {}: {}'.format(filepath, traceback.format_exc()))

                    except:
                        logger.warning('[AST] something error, {}'.format(traceback.format_exc()))

                    # 搜索所有的常量
                    for node in all_nodes:
                        if isinstance(node, php.FunctionCall) and node.name == "define":
                            define_params = node.params
                            logger.debug(
                                "[AST][Pretreatment] new define {}={}".format(define_params[0].node,
                                                                              define_params[1].node))

                            self.define_dict[define_params[0].node] = define_params[1].node

            # 手动回收?
            gc.collect()

        return True

    def get_nodes(self, filepath, vul_lineno=None, lan=None):
        filepath = os.path.normpath(filepath)

        if filepath in self.pre_result:
            if vul_lineno:
                # 处理需求函数的问题
                # 主要应用于，函数定义之后才会调用才会触发
                if lan == 'javascript':
                    backnodes = []
                    allnodes = self.pre_result[filepath]['ast_nodes'].body

                    for node in allnodes:
                        if node.loc.start.line <= int(vul_lineno):
                            backnodes.append(node)

                    return backnodes

            return self.pre_result[filepath]['ast_nodes']

        elif os.path.join(self.target_directory, filepath) in self.pre_result:
            return self.pre_result[os.path.join(self.target_directory, filepath)]['ast_nodes']

        else:
            logger.warning("[AST] file {} parser not found...".format(filepath))
            return False

    def get_content(self, filepath):
        filepath = os.path.normpath(filepath)

        if filepath in self.pre_result:
            return self.pre_result[filepath]['content']

        else:
            logger.warning("[AST] file {} parser not found...".format(filepath))
            return False

    def get_object(self, filepath):
        filepath = os.path.normpath(filepath)

        if filepath in self.pre_result:
            return self.pre_result[filepath]
        else:
            logger.warning("[AST] file {} object not found...".format(filepath))
            return False

    def get_child_files(self, filepath):
        filepath = os.path.normpath(filepath)

        if filepath in self.pre_result and "child_files" in self.pre_result[filepath]:
            return self.pre_result[filepath]['child_files']

        elif os.path.join(self.target_directory, filepath) in self.pre_result and "child_files" in self.pre_result[
            os.path.join(self.target_directory, filepath)]:
            return self.pre_result[os.path.join(self.target_directory, filepath)]['child_files']

        else:
            logger.warning("[AST] file {} object or child files not found...".format(filepath))
            return False

    def get_define(self, define_name):
        if define_name in self.define_dict:
            return self.define_dict[define_name]

        else:
            logger.warning("[AST] [INCLUDE FOUND] Can't found this constart {}, pass it ".format(define_name))
            return "not_found"


ast_object = Pretreatment()
