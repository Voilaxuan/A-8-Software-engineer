# -*- coding: utf-8 -*-

import sys
import os
import time
import argparse
import logging
import traceback
from .log import log, logger
from . import cli, config
from .cli import get_sid
from .engine import Running

import tkinter as tk
from tkinter import messagebox


try:
    reload(sys)
    sys.setdefaultencoding('utf-8')
except NameError as e:
    pass

def run_codeDector(detectFile, outputFile, format = 'xml', ruleid='', secretName=''):
    logger.debug('[INIT] start scanning...')
    a_sid = get_sid(detectFile, True)  # 用于区分不同的扫描项目

    data = {
        'status': 'running',
        'report': ''
    }
    Running(a_sid).status(data)  # 实例化Running类

    # cli.start(args.target, args.format, args.output, args.special_rules, a_sid, 'php', args.secret_name, args.black_path)
    cli.start(detectFile, format, outputFile, ruleid, a_sid, 'php,', secretName, '')

def main():
    try:
        # fd = os.getcwd()
        t1 = time.time()
        global get_format
        get_format='csv'

        window = tk.Tk()
        window.title('Code audit Tool by J')
        window.geometry('950x550')  # 设置窗口大小

        tk.Label(window, text='Code audit Tool for PHP', font=('Arial', 20)).place(x=500, y=30, anchor='center')
        tk.Label(window,
                 text='help and examples:\n'
                 , font=('Arial', 15)).place(x=50, y=85)
        tk.Label(window,
                 text='This is an automatic static code audit tool for detecting \nvulnerabilities and security risks in PHP.',
                 justify='left',
                 font=('Arial', 13)).place(x=50, y=120)
        tk.Label(window,
                 text='how to scan:'
                 , font=('Arial', 15)).place(x=50, y=185)
        tk.Label(window,
                 text='target: input a file or a folder as your target.\nresult format: chose csv or xml as your result file format.\nspecial rule: input rule id(s).\nsecret name: input names of repaired functions.\nlog name: input the log name to find a log easier.',
                 justify='left',
                 font=('Arial', 13)).place(x=50, y=220)
        tk.Label(window,
                 text='e.g.'
                 , font=('Arial', 15)).place(x=50, y=345)

        tk.Label(window,
                 text='①target: tests/vulnerabilities\n②target: tests/vulnerabilities special rule: 1000\n③target: tests/vulnerabilities secret name: wordpress\n④target: tests/vulnerabilities result name: xml\nlog name: 202004121354',
                 justify='left',
                 font=('Arial', 13)).place(x=50, y=380)

        def start_scan():
            if entry_logname.get():
                log(logging.INFO, entry_logname.get())
            else:
                log(logging.INFO, str(time.time()))

            if entry_targe.get()=='':
                tk.messagebox.showerror(title='Tip',message='The target should not be null.')
            else:

                logger.debug('[INIT] start scanning...')
                a_sid = get_sid(entry_targe.get(), True)  # 用于区分不同的扫描项目

                data = {
                    'status': 'running',
                    'report': ''
                }
                Running(a_sid).status(data)  # 实例化Running类

                # cli.start(args.target, args.format, args.output, args.special_rules, a_sid, 'php', args.secret_name, args.black_path)
                cli.start(entry_targe.get(), get_format, '', entry_ruleid.get(), a_sid, 'php,', entry_secret.get(), '')

                t2 = time.time()
                logger.info('[INIT] Done! Consume Time:{ct}s'.format(ct=t2 - t1))

                # os.chdir(fd)
                tk.messagebox.showinfo(title='Tip', message='scan over\nthe output file in /result\nthe log file in /logs')
                exit()

        def show_format():
            global get_format
            get_format = result_format.get()

        tk.Label(window,
                 text='target (required; php only)'
                 , font=('Arial', 13)).place(x=540, y=80)
        entry_targe = tk.Entry(window, show=None)
        entry_targe.place(x=540, y=110, width=250, height=30)


        tk.Label(window,
                 text='----------------------------------------------------------'
                 , font=('Arial', 13)).place(x=538, y=150)

        tk.Label(window,
                 text='special rule (optional, default:all)'
                 , font=('Arial', 13)).place(x=540, y=180)
        entry_ruleid = tk.Entry(window, show=None)
        entry_ruleid.place(x=540, y=210, width=250, height=30)

        result_format = tk.StringVar()

        tk.Label(window,
                 text='result format (optional, default:csv)'
                 , font=('Arial', 13)).place(x=540, y=260)
        firstchoice = tk.Radiobutton(window, text='save as csv', font=('Arial', 11), variable=result_format,
                                     value='csv', command=show_format)
        firstchoice.place(x=540, y=290)
        secondchoice = tk.Radiobutton(window, text='save as xml', font=('Arial', 11), variable=result_format,
                                      value='xml', command=show_format)
        secondchoice.place(x=700, y=290)


        tk.Label(window,
                 text='secret name (optional, default:null)'
                 , font=('Arial', 13)).place(x=540, y=330)
        entry_secret = tk.Entry(window, show=None)
        entry_secret.place(x=540, y=360, width=250, height=30)

        tk.Label(window,
                 text='log name (optional)'
                 , font=('Arial', 13)).place(x=540, y=410)
        entry_logname = tk.Entry(window, show=None)
        entry_logname.place(x=540, y=440, width=250, height=30)

        scan_button = tk.Button(window, text='scan', width=8, height=1, command=start_scan)
        scan_button.place(x=820, y=110)

        window.mainloop()

    except Exception as e:
        exc_msg = traceback.format_exc()
        logger.warning(exc_msg)


if __name__ == '__main__':
    main()
