# -*- coding: utf-8 -*-

import os
import traceback
from .log import logger

try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser

project_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))#返回向上一级的绝对路径
code_path = './tmp'
if os.path.isdir(code_path) is not True:
    os.mkdir(code_path)
running_path = os.path.join(project_directory, code_path, 'running')
if os.path.isdir(running_path) is not True:
    os.mkdir(running_path)
package_path = os.path.join(project_directory, code_path, 'package')
if os.path.isdir(package_path) is not True:
    os.mkdir(package_path)
source_path = os.path.join(project_directory, code_path, 'git')

if os.path.isdir(source_path) is not True:
    os.mkdir(source_path)

issue_path = os.path.join(project_directory, code_path, 'issue')
if os.path.isdir(issue_path) is not True:
    os.mkdir(issue_path)

export_path = os.path.join(project_directory, code_path, 'export')
if not os.path.exists(export_path):
    os.mkdir(export_path)

if os.path.isdir('./result') is not True:
    os.mkdir('./result')
default_result_path = os.path.join(project_directory, 'result/')

issue_history_path = os.path.join(issue_path, 'history')
cobra_main = os.path.join(project_directory, 'cobra.py')
core_path = os.path.join(project_directory, 'cobra')
tests_path = os.path.join(project_directory, 'tests')
examples_path = os.path.join(tests_path, 'examples')
rules_path = os.path.join(project_directory, 'rules')#拼接路径为project_directory/rules
config_path = os.path.join(project_directory, 'config')
rule_path = os.path.join(project_directory, 'rule.cobra')

