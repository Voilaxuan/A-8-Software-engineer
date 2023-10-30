# -*- coding: utf-8 -*-



class VulnerabilityResult:
    def __init__(self):
        self.id = ''
        self.file_path = None
        self.analysis = ''
        self.chain = ""

        self.rule_name = ''
        self.language = ''
        self.line_number = None
        self.code_content = None
        self.commit_author = 'Unknown'

    def convert_to_dict(self):
        _dict = {}
        _dict.update(self.__dict__)
        return _dict
