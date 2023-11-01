import re
import json
import xml.etree.ElementTree as ET
from cat import run_codeDector
import os
import multiprocessing as mp

def xml_to_dict(element):
    result = {}
    for child in element:
        child_data = xml_to_dict(child)
        if child_data:
            if child.tag in result:
                if not isinstance(result[child.tag], list):
                    result[child.tag] = [result[child.tag]]
                result[child.tag].append(child_data)
            else:
                result[child.tag] = child_data
        else:
            result[child.tag] = child.text
    return result



def codedetect():
    run_codeDector(r'E:\\workspace\\flask_backend\\tests',r'E:\\workspace\\flask_backend\\vul.xml', 'xml', '', '')
    return True

def fetchxml():
    with open(r'E:\\workspace\\flask_backend\\vul.xml', 'r') as file:
            xml_data = file.read()
    xml_data = re.sub(r'\n', ' ', xml_data)
    xml_data = re.sub(r'\s{2,}', ' ', xml_data)
    root = ET.fromstring(xml_data)
    xml_dict = xml_to_dict(root)
    os.remove(r'E:\\workspace\\flask_backend\\vul.xml') 
    json_data = json.dumps(xml_dict, indent=4)
    #print(json_data)   
    return(xml_dict)


