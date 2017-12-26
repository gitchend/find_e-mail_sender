#singlefile.py

import re
class Fileinfo:
	sender=0
	infolist=0
	def __init__(self, sender, infolist):
		self.sender=sender
		self.infolist=infolist
	
def dealsingle(filePath):
	fileObj = open(filePath)
	try:
	     allLine = fileObj.readlines()
	finally:
	     fileObj.close()

	for line in allLine:
		if(line.startswith('From')):
			sender=line[8:].strip()
			break
	allLine=''.join(allLine[allLine.index('\r\n')+1:]).lower()
	allLine=re.compile(r'\d|\s|\r\n|\.|\,|\"|\?|\!|\;').split(allLine)
	allLine=list(set(allLine))
	try:
		allLine.remove('')
	except Exception,e:
    		print e.message
	return Fileinfo(sender,allLine)
