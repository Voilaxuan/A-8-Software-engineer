from cat import run_codeDector

def staticCodeDetect(inputFile, outputFile, format='xml', ruleId='', secretName=''):
    return run_codeDector(inputFile, outputFile, format, ruleId, secretName)


staticCodeDetect('tests/cloc.php','tests/vul.xml')