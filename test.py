import os
import math
from decimal import *

import singlefile
import global_list

def deal(comdir,singleuser):
	global_list.fileNum+=1
	allLine=singlefile.dealsingle(comdir)
	
	PCsumPFClog_max=0
	sender_mostlike=""
	
	
	print(singleuser)
				
	cursor = global_list.db.cursor()
	for user_guess in global_list.pcmap:
		sumPFClog=0
		sumc=global_list.sumfcmap[user_guess]
		
		for f in allLine:
			key=user_guess+":"+f
			sumf=0
			if(global_list.sumcfmap.has_key(key)):
				sumf=global_list.sumcfmap[key]
			else:
				cursor.execute("select times from cf where c='%s' and f='%s'"%(user_guess,f))
				data = cursor.fetchall()
				if data:
					sumf=data[0][0]
					if not sumf:
						sumf=Decimal(0.00000001)
				else:
					sumf=Decimal(0.00000001)
				global_list.sumcfmap[key]=sumf
			sumPFClog+=math.log(sumf/(sumc*Decimal(1.0)))
		PCsumPFClog=sumPFClog+math.log(global_list.pcmap[user_guess])
		if(PCsumPFClog>PCsumPFClog_max or PCsumPFClog_max==0):
			print("--guess:"+user_guess)
			PCsumPFClog_max=PCsumPFClog
			sender_mostlike=user_guess
	
	isMatched=(singleuser==sender_mostlike)
	if(singleuser==sender_mostlike):
		print('###sender:'+singleuser+'  guess:'+sender_mostlike+"  --matching")
		global_list.fileNum_correct+=1
	else:
		print('###sender:'+singleuser+'  guess:'+sender_mostlike+"  --mismatching")
		global_list.fileNum_incorrect+=1
	
		
def	getPC():
	getcontext().prec = 5
	cursor = global_list.db.cursor()
	cursor.execute("select sum(times) from c")
	data = cursor.fetchall()
	n=data[0][0]
	
	cursor.execute("select * from c")
	data = cursor.fetchall()
	for row in data:
		global_list.pcmap[row[0]]=row[1]/(n*Decimal(1.0))
	
	cursor.execute("select * from fc");
	data = cursor.fetchall()
	for row in data:
		global_list.sumfcmap[row[0]]=row[1]
	
def test(dirPath):
	getPC()
	userlist=os.listdir(dirPath)
	for singleuser in userlist:
		userpath=dirPath+'/'+singleuser
		dirlist=os.listdir(userpath)
		for singledir in dirlist:
			comdir=userpath+'/'+singledir
			if(os.path.isfile(comdir)):
				deal(comdir,singleuser)
			else:
				filelist=os.listdir(comdir)
				for singlefilename in filelist:
					comdir2=comdir+'/'+singlefilename
					if(os.path.isfile(comdir2)):
						deal(comdir2,singleuser)
	
	global_list.db.close()
	print('total:'+global_list.fileNum)
	print('matching:'+global_list.fileNum_correct+'   mismatching:'+global_list.fileNum_incorrect)
	print('correct rate:'+global_list.fileNum_correct/(1.0*global_list.fileNum))

	
test(global_list.mail_dir_test)











