import re
import json
import xml.etree.ElementTree as ET

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



def fetchxml():
    '''
    This function will output A JSON format result of the vulnerabilities.
    {
        "s938e2zz1ybo": {
            "extension": "        4    ",
            "file": "        5    ",
            "framework": "        Spring    ",
            "language": "        php    ",
            "push_rules": "        17    ",
            "target_directory": "        C:\\Users\\Lenovo\\Desktop\\Soft_Engi\\project\\CodeauditTool3.0\\tests\\vulnerabilities/    ",
            "trigger_rules": "        13    ",
            "vulnerabilities": {
                "vul": [
                    {
                        "analysis": "            Function-param-controllable        ",
                        "chain": "                    ",
                        "code_content": "            print(\"Hello \" . $cmd);        ",
                        "commit_author": "            JANNEY W        ",
                        "file_path": "            C:\\Users\\Lenovo\\Desktop\\Soft_Engi\\project\\CodeauditTool3.0\\tests\\vulnerabilities/v.php        ",
                        "id": "            1000        ",
                        "language": "            PHP        ",
                        "line_number": "            60        ",
                        "rule_name": "            Reflected XSS        "
                    },
                    ...
                    
                ]
            },
            "target": " tests/vulnerabilities "
        }
    }
    '''
    with open('testdata/vulnerabilities.xml', 'r') as file:
        xml_data = file.read()
    xml_data = re.sub(r'\n', ' ', xml_data)
    xml_data = re.sub(r'\s{2,}', ' ', xml_data)
    root = ET.fromstring(xml_data)
    xml_dict = xml_to_dict(root)

    json_data = json.dumps(xml_dict, indent=4)
    print(json_data)
    return(xml_dict)

#fetchxml()