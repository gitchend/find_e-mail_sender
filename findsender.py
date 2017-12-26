#findsender.py

import os
import singlefile
import step1



class mainclass:
	fileNum=0;
	fileNumTest=0
	mapOfC={}
	mapOfCF={}

	def deal(self,step,comdir):
		fileinfo=singlefile.dealsingle(comdir)
		self.fileNum+=1
		if step is 0:
			print comdir+"|"+fileinfo.sender
		elif step is 1:
			step1.deal(self,fileinfo)
		elif step is 2:
			step2.deal(self,fileinfo)

	def learn(self,step,dirPath):
		userlist=os.listdir(dirPath)
		for singleuser in userlist:
			userpath=dirPath+'/'+singleuser
			dirlist=os.listdir(userpath)
			for singledir in dirlist:
				comdir=userpath+'/'+singledir
				if(os.path.isfile(comdir)):
					self.deal(step,comdir)
				else:
					filelist=os.listdir(comdir)
					for singlefile in filelist:
						comdir2=comdir+'/'+singlefile
						if(os.path.isfile(comdir2)):
							self.deal(step,comdir2)

	def dealtest(self,step,comdir):
		fileinfo=singlefile.dealsingle(comdir)
		self.fileNumTest+=1
		if step is 0:
			print comdir+"|"+fileinfo.sender
		elif step is 1:
			step1.dealtest(self,fileinfo)
		elif step is 2:
			step2.dealtest(self,fileinfo)

	def test(self,step,dirPath):
		userlist=os.listdir(dirPath)
		for singleuser in userlist:
			userpath=dirPath+'/'+singleuser
			dirlist=os.listdir(userpath)
			for singledir in dirlist:
				comdir=userpath+'/'+singledir
				if(os.path.isfile(comdir)):
					self.dealtest(step,comdir)
				else:
					filelist=os.listdir(comdir)
					for singlefile in filelist:
						comdir2=comdir+'/'+singlefile
						if(os.path.isfile(comdir2)):
							self.dealtest(step,comdir2)

	def start(self,step,dirPath,dirPathTest):
		self.learn(step,dirPath)
		self.test(step,dirPathTest)
		print self.fileNum
		print self.fileNumTest
		

mainclass().start(1,'maildirsub','maildirsub-test')











