from cat import run_codeDector

def staticCodeDetect(inputFile, outputFile, format='xml', ruleId='', secretName=''):
    return run_codeDector(inputFile, outputFile, format, ruleId, secretName)