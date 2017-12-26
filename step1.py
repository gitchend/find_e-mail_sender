#step1.py

import math

def deal(findsender,fileinfo):
	fset=fileinfo.infolist
	sender=fileinfo.sender
	
	if not(findsender.mapOfC.has_key(sender)):
			findsender.mapOfC[sender]=0
	findsender.mapOfC[sender]+=1

	for singleInfo in fset:
		key=sender+'`'+singleInfo
		if not(findsender.mapOfCF.has_key(key)):
			findsender.mapOfCF[key]=1
		findsender.mapOfCF[key]+=1

		
def dealtest(findsender,fileinfo):
	fset=fileinfo.infolist
	sender=fileinfo.sender

	guessSender=''
	guessSenderPc=0
	
	print 'sender:'+sender
	for C in findsender.mapOfC:
		pc=math.log(findsender.mapOfC[C]*1.0/findsender.fileNum)
		sumf=0
		for CF in findsender.mapOfCF:
			if(CF.startswith(C)):
				sumf+=findsender.mapOfCF[CF]
		for CF in findsender.mapOfCF:
			for F in fset:
				if(CF is (C+'`'+F)):
					pc+=math.log(findsender.mapOfCF[CF])
					break
		if(guessSenderPc<pc or guessSenderPc is 0):
			guessSenderPc=pc
			guessSender=C
			print 'most likely:'+C

	print 'sender:'+sender+'  guess:'+guessSender
				
