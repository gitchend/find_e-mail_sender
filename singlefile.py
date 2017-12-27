#singlefile.py

import re

def dealsingle(filePath):
	fileObj = open(filePath)
	try:
	     allLine = fileObj.readlines()
	finally:
	     fileObj.close()
	
	allLine=''.join(allLine[allLine.index('\n')+1:]).lower()
	allLine=re.compile(r'\d|\s|\r\n|\n|\.|\,|\"|\?|\!|\/|\-|\:|\@|\'|\&|\=|\#|\*|\$|\(|\)|\+|\;|\%|\<|\>|\\|\_').split(allLine)
	allLine=list(set(allLine))
	if '' in allLine:
		allLine.remove('')
	return allLine