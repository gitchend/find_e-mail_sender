#learn.py

import os

import singlefile
import global_list

def deal(comdir,singleuser):
	global_list.fileNum+=1
	allLine=singlefile.dealsingle(comdir)
	
	cursor = global_list.db.cursor()
	try:
		cursor.execute("select * from c where c='%s'"%(singleuser))
		data = cursor.fetchall()
		if(data):
			cursor.execute("update c set times=times+1 where c='%s'"%(singleuser))
		else:
			cursor.execute("insert into c(c) values('%s')"%(singleuser))
	except Exception:
		print("illegal user:"+singleuser)
		
	for f in allLine:
		try:
			cursor.execute("select * from cf where c='%s' and f='%s'"%(singleuser,f))
			data = cursor.fetchall()
			if(data):
				cursor.execute("update cf set times=times+1 where c='%s' and f='%s'"%(singleuser,f))
			else:
				cursor.execute("insert into cf(c,f) values('%s','%s')"%(singleuser,f))
		except Exception:
			print("illegal string:"+f)
	global_list.db.commit()
	
def learn(dirPath):
	userlist=os.listdir(dirPath)
	for singleuser in userlist:
		print(singleuser)
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
	
	print(global_list.fileNum)
	global_list.db.close()
		
learn(global_list.mail_dir)











