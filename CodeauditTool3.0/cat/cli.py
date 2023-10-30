# -*- coding: utf-8 -*-

from .detection import Detection
from .engine import scan, Running
from .exceptions import PickupException
from .export import write_to_file
from .log import logger
from .file import Directory
from .utils import ParseArgs
from .utils import md5, random_generator
from .pretreatment import ast_object


def get_sid(target, is_a_sid=False):#区分不同扫描项目
    target = target
    if isinstance(target, list):#判断target的类型为list
        target = ';'.join(target)#将target的内容以分号隔开
    sid = md5(target)[:5]#sid为md5加密后的target的前五个元素
    if is_a_sid:
        pre = 'a'
    else:
        pre = 's'
    sid = '{p}{sid}{r}'.format(p=pre, sid=sid, r=random_generator())#三个值按顺序输出，
    return sid.lower()#大写字母变为小写后返回


def start(target, formatter, output, special_rules, a_sid=None, language=None, secret_name=None, black_path=None):
    #扫描目标，输出格式，输出文件，指定规则编号
    #对变量初始化赋值
    global ast_object
    # generate single scan id
    s_sid = get_sid(target)
    r = Running(a_sid)
    data = (s_sid, target)
    r.init_list(data=target)
    r.list(data)

    report = '?sid={a_sid}'.format(a_sid=a_sid)
    d = r.status()
    d['report'] = report
    r.status(d)

    # parse target mode and output mode
    pa = ParseArgs(target, formatter, output, special_rules, language, black_path, a_sid=None)#实例化ParseArgs类
    #目标类型和输出类型
    target_mode = pa.target_mode
    output_mode = pa.output_mode
    black_path_list = pa.black_path_list

    # target directory
    try:
        target_directory = pa.target_directory(target_mode)#获取目标路径
        logger.info('[CLI] Target : {d}'.format(d=target_directory))

        # static analyse files info
        files, file_count, time_consume = Directory(target_directory, black_path_list).collect_files()
        #确认文件位置，文件数量，用时


        # if not language:
        dt = Detection(target_directory, files)
        main_language = dt.language
        main_framework = dt.framework

        logger.info('[CLI] [STATISTIC] Language: {l} Framework: {f}'.format(l=",".join(main_language), f=main_framework))
        logger.info('[CLI] [STATISTIC] Files: {fc}, Extensions:{ec}, Consume: {tc}'.format(fc=file_count,
                                                                                           ec=len(files),
                                                                                           tc=time_consume))

        if pa.special_rules is not None:#根据特殊规则扫描
            logger.info('[CLI] [SPECIAL-RULE] only scan used by {r}'.format(r=','.join(pa.special_rules)))

        # Pretreatment ast object
        ast_object.init_pre(target_directory, files)
        ast_object.pre_ast_all(main_language)

        # scan
        scan(target_directory=target_directory, a_sid=a_sid, s_sid=s_sid, special_rules=pa.special_rules,
             language=main_language, framework=main_framework, file_count=file_count, extension_count=len(files),
             files=files, secret_name=secret_name)
    except KeyboardInterrupt as e:
        logger.critical("[!] KeyboardInterrupt, exit...")
        exit()
    except PickupException as e:
        result = {
            'code': 1002,
            'msg': 'Repository not exist!'
        }
        Running(s_sid).data(result)
        raise
    except Exception:
        result = {
            'code': 1002,
            'msg': 'Exception'
        }
        Running(s_sid).data(result)
        raise

    # 输出写入文件
    write_to_file(target=target, sid=s_sid, output_format=formatter, filename=output)#formatter默认值为csv
