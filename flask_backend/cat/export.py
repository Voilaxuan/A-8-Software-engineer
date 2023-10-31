# -*- coding: utf-8 -*-

import csv
import json
import os
import re
from codecs import open, BOM_UTF8

from prettytable import PrettyTable

from .config import running_path, export_path, default_result_path
from .log import logger

import html

try:
    # Python 2
    _unicode = unicode
except NameError:
    # Python 3
    _unicode = str


def dict_to_xml(dict_obj, line_padding=''):
    result_list = []
    if isinstance(dict_obj, list):
        for list_id, sub_elem in enumerate(dict_obj):
            result_list.append(' ' * 4 + '<vul>')
            result_list.append(dict_to_xml(sub_elem, line_padding))
            result_list.append(' ' * 4 + '</vul>')

        return '\n'.join(result_list)

    if isinstance(dict_obj, dict):
        for tag_name in dict_obj:
            sub_obj = dict_obj[tag_name]
            if isinstance(sub_obj, _unicode):
                sub_obj = html.escape(sub_obj)
            result_list.append('%s<%s>' % (line_padding, tag_name))
            result_list.append(dict_to_xml(sub_obj, ' ' * 4 + line_padding))
            result_list.append('%s</%s>' % (line_padding, tag_name))

        return '\n'.join(result_list)

    return '%s%s' % (line_padding, dict_obj)


def dict_to_json(dict_obj):
    """
    Convert scan result to JSON string.
    :param dict_obj: a dict object
    :return: JSON String
    """
    return json.dumps(dict_obj, ensure_ascii=False)


def dict_to_csv(vul_list, filename):
    # 排序并将 target 调整到第一列
    for i in range(len(vul_list)):
        vul_list[i]['commit_author'] = 'JANNEY W'
    header = sorted(vul_list[0].keys())
    header.remove('target')
    header.insert(0, 'target')

    # 去除列表中的换行符
    if not os.path.exists(filename):
        with open(filename, 'w+', encoding='utf-8', errors='ignore') as f:
            # 防止在 Excel 中中文显示乱码
            # f.write(BOM_UTF8)
            csv_writer = csv.DictWriter(f, header)
            csv_writer.writeheader()
            csv_writer.writerows(vul_list)
    else:
        with open(filename, 'a', encoding='utf-8', errors='ignore') as f:
            csv_writer = csv.DictWriter(f, header)
            csv_writer.writerows(vul_list)


def dict_to_pretty_table(vul_list):
    row_list = PrettyTable()
    row_list.field_names = ['#', 'CVI', 'Vulnerability', 'File', 'Code Content']
    row_list.align = 'l'
    for _id, vul in enumerate(vul_list):
        row_list.add_row(
            [_id+1, vul.get('id'), vul.get('rule_name'), vul.get('file_path') + ':' + str(vul.get('line_number')), vul.get('code_content').strip()]
        )
    return row_list


def write_to_file(target, sid, output_format='', filename=None):#format默认值为csv
    """
    Export scan result to file.
    :param target: scan target
    :param sid: scan sid
    :param output_format: output format
    :param filename: filename to save
    :return:
    """
    if not filename:
        logger.info('[EXPORT] No filename given, save into default path(result/).')#不指定输出文件则存入默认路径

        targetlist = re.split("[\\\/]", target)
        if target.endswith("/") or target.endswith("\\"):
            filename = targetlist[-2]#倒数第二个target赋值给文件名
        else:
            filename = targetlist[-1]
        filename = default_result_path + filename + "." + output_format#以format的格式将结果存入result文件夹
    #     return False

    scan_data_file = os.path.join(running_path, '{sid}_data'.format(sid=sid))#存入扫描数据文件


    if not os.path.exists(scan_data_file):
        logger.warn("[EXPORT] {} not found".format(scan_data_file))
        return False

    with open(scan_data_file, 'r') as f:
        scan_data = json.load(f).get('result')#获取扫描数据

    if len(scan_data.get('vulnerabilities')) == 0:#是否发现漏洞
        logger.info("[EXPORT] Not found vulnerability, break export...")
        return False

    os.chdir(export_path)
    scan_data['target'] = target

    vul_list1=scan_data.get('vulnerabilities')
    for i in range(len(vul_list1)):
        vul_list1[i]['commit_author'] = 'JANNEY W'

    if output_format == '' or output_format == 'stream':
        logger.info('Vulnerabilities\n' + str(dict_to_pretty_table(scan_data.get('vulnerabilities'))))#规整的写入漏洞信息


    elif output_format == 'xml' or output_format == 'XML':
        xml_data = {
            sid: scan_data,
        }
        if not os.path.exists(filename):
            with open(filename, 'w+', encoding='utf-8', errors='ignore') as f:
                f.write("""<?xml version="1.0" encoding="UTF-8"?>\n""")
                f.write("""<results>\n""")
                f.write(dict_to_xml(xml_data))
                f.write("""\n</results>\n""")
        else:
            # 在倒数第二行插入
            with open(filename, 'r+', encoding='utf-8', errors='ignore') as f:
                results = f.readlines()
                results.insert(len(results) - 1, '\n' + dict_to_xml(xml_data) + '\n')
                f.seek(0)
                f.truncate()
                f.writelines(results)

    elif output_format == 'csv' or output_format == 'CSV':

        for vul in scan_data.get('vulnerabilities'):
            vul['target'] = scan_data.get('target')
        dict_to_csv(scan_data.get('vulnerabilities'), filename)



    else:
        logger.warning('[EXPORT] Unknown output format.')
        return False

    logger.info('[EXPORT] Scan result exported successfully: {fn}'.format(fn=filename))
    return True
