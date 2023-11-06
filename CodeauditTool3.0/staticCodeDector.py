from cat import run_codeDector

def staticCodeDetect(inputFile, outputFile, format='xml', ruleId='', secretName=''):
    return run_codeDector(inputFile, outputFile, format, ruleId, secretName)

if __name__ == '__main__':
    run_codeDector(r'C:\Users\90834\Desktop\A-8-Software-engineer\CodeauditTool3.0\tests\vulnerabilities\java_test.java', r'C:\Users\90834\Desktop\A-8-Software-engineer\CodeauditTool3.0\tests\vulnerabilities\out.xml')