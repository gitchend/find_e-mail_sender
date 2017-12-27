#prapare.py

import random
import os
import shutil

import global_list


def deal(comdir,comdir_test):
	fate=random.randint(0,9)
	if(fate<2):
		shutil.copyfile(comdir, comdir_test)
		os.remove(comdir)  
	
def start(dirPath,dirPath_test):
	userlist=os.listdir(dirPath)
	for singleuser in userlist:
		print(singleuser)
		userpath=dirPath+'/'+singleuser
		userpath_test=dirPath_test+'/'+singleuser
		if not(os.path.exists(userpath_test)):
			os.mkdir(userpath_test)
		dirlist=os.listdir(userpath)
		for singledir in dirlist:
			comdir=userpath+'/'+singledir
			comdir_test=userpath_test+'/'+singledir
			if(os.path.isfile(comdir)):
				deal(comdir,comdir_test)
			else:
				if not(os.path.exists(comdir_test)):
					os.mkdir(comdir_test)
				filelist=os.listdir(comdir)
				for singlefilename in filelist:
					comdir2=comdir+'/'+singlefilename
					comdir2_test=comdir_test+'/'+singlefilename
					if(os.path.isfile(comdir2)):
						deal(comdir2,comdir2_test)
						
start(global_list.mail_dir,global_list.mail_dir_test)