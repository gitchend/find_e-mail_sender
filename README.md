机器学习课程实验报告

### 山东大学计算机学院



### 题目：判断邮件发送人

- 实现算法：朴素贝叶斯

- 软件环境：python 2.7、mysql 5.0.2

- 成员：

  | 姓名   | 学号   |
  | ---- | ---- |
  |      |      |

  ​





#### 需求及思路分析

​	本实验内容为“通过邮件内容判断邮件发送人”，要完成这个工作，我们首先要明确不同人发送邮件的区别在哪里。显然不同的人有不同的工作、兴趣、社交圈子，而这些内容会或多或少地体现在邮件上。例如：Jack经常给Rose发邮件，邮件中自然就会有“Rose”这一单词，当我们拿到一份未署名的、包含“Rose”的电子邮件，我们就知道这份邮件有一定概率是出自Jack之手。当然名为Rose的人很多，某个Rose并不一定是Jack认识的Rose，所以要在整份邮件中寻找线索，找出最有可能的发送人。我们可以预先通过学习知道Jack以及其他人与某个单词关联的程度，当邮件中出现这个单词时，我们能据此判断邮件属于某个人的概率。

​	找到邮件发送人的行为事实上是一种文本分类，朴素贝叶斯算法通常被用于处理文本分类的问题。



#### 关于朴素贝叶斯算法

###### 贝叶斯定理

​	贝叶斯定理是关于随机事件A和B的条件概率（或边缘概率）的一则定理。其中P(A|B)是在B发生的情况下A发生的可能性。

​	公式：

​		$P(A|B)=\frac{P(B|A)P(A)}{P(B)}$

###### 定理在该情景下的使用

​	在该情景下，我们要做的是对某一份邮件进行归类，即“求某个单词（特征，设为F，下同）出现的时候，发件人（类，设为C，下同）为C的概率”，取概率最大的C，即视为发件人。

​	所以我们要求的是“在F发生的情况下C发生的可能性”，即P(C|F)。根据贝叶斯定理，有：

​		$P(C|F)=\frac{P(F|C)P(C)}{P(F)}$	

​	其中$P(C)$为C的**先验概率(Prior)**，即归类为C的样本在所有样本中所占比例；$P(F)$为**证据(Evidence)**，即特征F出现的概率；$P(F|C)$为**似然(likelihood)**，即如果知道某样本被分类为C类，那么其特征为F的概率。先验概率、证据、似然均可通过对训练集的统计和计算得到。

​	值得注意的是，在同一邮件中，某特征出现的次数并不能代表该特征和发件人的关联程度。例如：Jack在某邮件中和友人聊到Golf，势必会接连使用很多“Golf”这个单词来组织语言，而事实上他只聊到Golf一次；又例如：Jack喜欢使用副词“very”，一篇邮件能用20个“very”，在判断某份带有“very”单词的邮件时，归类为Jack的可能性将会大大提高，这是不符合逻辑的。因此在单个邮件样本中，我们只关心某个特征出现与否，并不关心其出现的次数。

###### 复数特征时的贝叶斯定理

​	对于邮件而言，用来判断发件人的线索显然不止一个，即对于类C，其特征F是复数的。这时贝叶斯定理可扩展如下：

​	$P(C|F_1F_2...F_n)=\frac{P(F_1F_2...F_n|C)P(C)}{P(F_1F_2...F_n)}\\=\frac{P(C)P(F_1|C)P(F_2|CF_1)...P(F_n|CF_1F_2...F_n)}{P(F_1F_2...F_n)}$

###### 关于算法中的朴素概念

​	为了简化计算，朴素贝叶斯算法做出一个假设：“**认为各个特征相互独立**”，即某一特征的出现并不受另一特征的影响。

​	这个假设是不合理的，因为在很多情况下特征之间都是有所联系的。例如：在Jack的邮件中，“Rose”有时和她的姓“Dawson”一起出现，此时的特征“Dawson”显然受特征“Rose”影响。

​	但是在大量应用实践中，该假设对结果影响不大，且简化了运算过程。在此假设的基础上，公式可化简为：

​	$P(C|F_1F_2...F_n)=\frac{P(F_1F_2...F_n|C)P(C)}{P(F_1F_2...F_n)}\\=\frac{P(C)P(F_1|C)P(F_2|CF_1)...P(F_n|CF_1F_2...F_{n-1})}{P(F_1F_2...F_n)}\\≈\frac{P(C)P(F_1|C)P(F_2|C)...P(F_n|C)}{P(F_1F_2...F_n)}$



#### 实现过程

​	主要过程为：对于每个类C以及每个特征F，通过学习求得$P(F_n|C) $、$P(C) $以及$P(F_1F_2...F_n)$，用化简后的公式算出$P(C|F_1F_2...F_n)$，然后找出其中P最大的C，即为该样本所属的类。据此，实现过程如下：

1. (对每个发件人)将样本集合理划分为80%的学习集和20%的测试集。

2. 处理学习集中的原始邮件，对于其中每一个样本：

   1. 提取出该样本所属的类C(发件人)。
   2. 删除邮件头，将邮件内容按单词分割，生成一个不重复的特征集D。

3. 进行步骤2时，记录样本容量n，根据特征集D和类C维护如下两个动态表：

   1. 类-特征频率表(表1)

      | C     | F     | times     |
      | ----- | ----- | --------- |
      | $C_x$ | $F_y$ | $i_{x,y}$ |

      其中$i_{x,y}$为特征$F_y$在类$C_x$的特征集中出现的次数。

   2. 类频率表(表2)

      | C     | times |
      | ----- | ----- |
      | $C_x$ | $j_x$ |

      其中$j_x$为$C_x$出现次数。

4. 对于测试集中的每一个样本，用和步骤2一样的方法处理，提取类C‘，生成特征集E。

5. 利用特征集E和步骤3中的表求出需要的值。

   ​	因为最终目的是比较各个$P(C|F_1F_2...F_n)$的大小，对于同一学习集中的所有类$C$，$P(F_1F_2...F_n)$显然是相同的，可以简化不算，故对于每个类$C_x$，只需要计算以下值：

   1. $P(C_x) =\frac{j_x}{n}$
   2. $P(F_y|C_x) =\frac{i_{x,y}}{\sum\limits_{m = 0}^{max(y)}{i_{x,m}}}\ (F_y\in E)$

   据此算出$P_x=P(C)P(F_1|C)P(F_2|C)...P(F_n|C)$，其中$P_x$为可以代表$P(C|F_1F_2...F_n)$的数。

6. 记录$P_x$，并找出最大$P_x$所对应的$C_x$，即为算法所判断的发件人。

   ​

#### 代码实现

​	因为实验[原始数据](http://www.cs.cmu.edu/~enron/enron_mail_20150507.tar.gz)太多(1.62 GB)，直接在内存中测试不易，故决定利用数据库存贮学习结果，进行测试。

###### 实现分析

​	原始数据文件夹结构如图：

```

maildir
  ├─allen-p
  │  ├─all_documents
  │  │	├─1
  │  │	├─2
  │  │	└─...
  │  │
  │  ├─contacts
  │  └─...
  │
  ├─...
  │
  └─zufferli-j
     └─...
```

即：根目录-某个用户的文件夹-一些随意的文件夹和以正整数命名的邮件文件-以正整数命名的邮件文件。

​	用户文件夹是以“用户名字.用户姓氏开头字母”命名，而其下级文件夹命名随意，所以应当先写好读取并处理一个邮件文件的方法，再递归遍历原始数据文件夹，处理每个文件。而算法所需的类名、特征集需从邮件文件里整理出来。

​	邮件文件样例如下：

```
Message-ID: <31429551.1075855374433.JavaMail.evans@thyme>
Date: Fri, 28 Dec 2001 17:19:45 -0800 (PST)
From: arsystem@mailman.enron.com
To: k..allen@enron.com
Subject: Your Approval is Overdue: Access Request for matt.smith@enron.com
Mime-Version: 1.0
Content-Type: text/plain; charset=us-ascii
Content-Transfer-Encoding: 7bit
X-From: ARSystem <ARSystem@mailman.enron.com>@ENRON
X-To: Allen, Phillip K. </O=ENRON/OU=NA/CN=RECIPIENTS/CN=PALLEN>
X-cc: 
X-bcc: 
X-Folder: \Phillip_Allen_Jan2002_1\Allen, Phillip K.\Deleted Items
X-Origin: Allen-P
X-FileName: pallen (Non-Privileged).pst

This request has been pending your approval for  58 days.  Please click http://itcapps.corp.enron.com/srrs/auth/emailLink.asp?ID=000000000067320&Page=Approval to review and act upon this request.
Request ID          : 000000000067320
Request Create Date : 10/11/01 10:24:53 AM
Requested For       : matt.smith@enron.com
Resource Name       : Risk Acceptance Forms Local Admin Rights - Permanent
Resource Type       : Applications
```

从中我们可以获取到如下信息：

> Mime-Version: 1.0
>
> Content-Type: text/plain; charset=us-ascii

即该邮件遵循MIME协议的1.0版本，Content-Type为text/plain，字符集为us-ascii。通过对MIME协议的了解和对原始文件的充分观察，整理出以下有用信息：

1. MIME协议的邮件头是一组以冒号":"隔开的键值对，每个键值对占一行。
2. 邮件头和正文以第一个空行为界。
3. 邮件头中以“X-From”为键的值，即为发件人昵称；以“From”为键的值，即为发件人邮箱账号。根据观察，同一用户可以有不同格式甚至完全不同的昵称和账号，故选用文件夹名作为用户名。

至此，我们已经了解到解析原始邮件文件的方法，规划出实现过程如下：

1. 将所有原始文件分为学习集和测试集。
2. 遍历学习集。
3. 将学习集解析出的数据保存到数据库。
4. 遍历测试集。
5. 分别从内存和数据库(使用Sql)中算出获得$P_x$所需的值。
6. 记录$P_x$，并找出最大$P_x$所对应的$C_x$，比较C‘和$C_x$，并记录正确率。

###### 具体代码

1. 将所有原始文件分为学习集和测试集。

   ```python
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
   ```

   该程序遍历了原本的数据文件，并复制所有文件夹。对于其中每个文件，生成随机数，有20%几率复制该文件到测试文件夹，并删除原来的文件。

2. 读取、解析单个文件的程序。

   ```python
   #singlefile.py

   import re

   def dealsingle(filePath):
   	fileObj = open(filePath)
   	try:
   	     allLine = fileObj.readlines()
   	finally:
   	     fileObj.close()
   	
   	allLine=''.join(allLine[allLine.index('\n')+1:]).lower()
   	allLine=re.compile(r'\d|\s|\r\n|\n|\.|\,|\"|\?|\!|\/|\-|\:|\@|\'|\&|\=|\#|\*|\$|\(|\)|\+|\;|\%|\<|\>').split(allLine)
   	allLine=list(set(allLine))
   	if '' in allLine:
   		allLine.remove('')
   	return allLine
   ```

   该程序定义了一个方法`dealsingle(filePath)`。该方法做了以下操作：

   1. 打开文件并读取。
   2. 根据第一个空行切片，去掉文件头，得到正文。
   3. 将所有字符转为小写。
   4. 将正文用各种分割符号正则分割，并转为list
   5. 利用set去重
   6. 返回特征集

3. 学习

   ```python
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
   ```

   递归遍历每个文件，对于每个用户的所有文件，用`singlefile.dealsingle(filePath)`提取出文件中的结果集，将读入的类和特征集存入数据库。如果数据库中已有该数据（C,F或C）则让出现次数(times)增1，若无则创建。

   3.测试

   ```python
   #test.py

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
   		print(str(global_list.fileNum)+':sender:'+singleuser+'  guess:'+sender_mostlike+"  --matching")
   		global_list.fileNum_correct+=1
   	else:
   		print(str(global_list.fileNum)+':sender:'+singleuser+'  guess:'+sender_mostlike+"  --mismatching")
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
   ```

   根据算法进行测试。因为PC在测试过程中是一直要使用的，所以预先全部读入内存中。将某个类中某个特征出现的次数(CF)从数据库读出，按需存入内存，这样既不会开始运行程序时太慢，也不会以较慢的均匀速度运行，而是会越来越快。

   对于PFC连乘，因为PFC是很多小数，小数连乘可能造成下溢出，所以讲所有PFC取对数相加。为防止数学错误(log(0))，对于某个类没有出现过的某个特征（PFC=0），当做这个特征出现过一个极小数次(0.00000001次)。

   4.全局变量

   ```python
   #global_list.py

   import MySQLdb

   mail_dir='C:/Users/Administrator/Desktop/ml_mail/maildir'
   mail_dir_test='C:/Users/Administrator/Desktop/ml_mail/maildir_test'

   db = MySQLdb.connect("localhost","root","","findsender")

   fileNum=0
   fileNum_correct=0
   fileNum_incorrect=0

   pcmap={}
   sumcmap={}
   sumfcmap={}
   sumcfmap={}
   ```

   一些文件路径、数据库的配置信息，以及一些需要全局记录的变量。

#### 运行测试

速度稳定后平均每秒可测试3条记录。测试集中共98,774个文件，全部测试完需要9.146小时。由于时间太长，故每次随机选取约200个文件进行测试，多次测试取平均值。取到每个文件的概率约为0.2%。

改进后的代码如下：

```python
#test_sub.py

import os
import math
import random
from decimal import *

import singlefile
import global_list

def deal(comdir,singleuser):
	fate=random.randint(0,999)
	if(fate>=2):
		return
		
	global_list.fileNum+=1
	allLine=singlefile.dealsingle(comdir)
	
	PCsumPFClog_max=0
	sender_mostlike=""
	
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
			PCsumPFClog_max=PCsumPFClog
			sender_mostlike=user_guess
	
	isMatched=(singleuser==sender_mostlike)
	if(singleuser==sender_mostlike):
		print(str(global_list.fileNum)+':sender:'+singleuser+'  guess:'+sender_mostlike+"  --matching")
		global_list.fileNum_correct+=1
	else:
		print(str(global_list.fileNum)+':sender:'+singleuser+'  guess:'+sender_mostlike+"  --mismatching")
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
	
	rate=global_list.fileNum_correct/(1.0*global_list.fileNum)
	print('total:'+str(global_list.fileNum))
	print('matching:'+str(global_list.fileNum_correct)+'   mismatching:'+str(global_list.fileNum_incorrect))
	print('correct rate:'+str(rate))
	global_list.fileNum=global_list.fileNum_correct=global_list.fileNum_incorrect=0
	return rate

	
getPC()
rate_array={};
for i in range(5):
	rate_array[i]=test(global_list.mail_dir_test)
print("\ntest times:"+str(len(rate_array)))
sum_rate=0.0
rate_str="rate: "
for i in range(len(rate_array)):
	rate_str+=(str(round(rate_array[i],2))+" ")
	sum_rate+=rate_array[i]
print(rate_str+"\naverage rate:"+str(round(sum_rate/len(rate_array),2)))
global_list.db.close()

```

运行结果(略)：

```
1:sender:allen-p  guess:allen-p  --matching
2:sender:arnold-j  guess:arnold-j  --matching
3:sender:arnold-j  guess:whalley-l  --mismatching
4:sender:arnold-j  guess:arnold-j  --matching
5:sender:bass-e  guess:farmer-d  --mismatching
...
187:sender:watson-k  guess:scott-s  --mismatching
188:sender:whalley-g  guess:whalley-l  --mismatching
189:sender:whalley-l  guess:beck-s  --mismatching
190:sender:whalley-l  guess:beck-s  --mismatching
191:sender:williams-j  guess:williams-j  --matching
192:sender:williams-w3  guess:meyers-a  --mismatching
193:sender:ybarbo-p  guess:watson-k  --mismatching
194:sender:zipper-a  guess:zipper-a  --matching
total:194
matching:113   mismatching:81
correct rate:0.582474226804
1:sender:allen-p  guess:allen-p  --matching
2:sender:arnold-j  guess:arnold-j  --matching
3:sender:arnold-j  guess:maggi-m  --mismatching
4:sender:arnold-j  guess:arnold-j  --matching
5:sender:arnold-j  guess:dasovich-j  --mismatching
...
197:sender:williams-j  guess:giron-d  --mismatching
198:sender:williams-w3  guess:williams-w3  --matching
199:sender:wolfe-j  guess:scott-s  --mismatching
200:sender:ybarbo-p  guess:ybarbo-p  --matching
total:200
matching:119   mismatching:81
correct rate:0.595

...

test times:5
rate: 0.58 0.59 0.58 0.57 0.64
average rate:0.59
```

总共进行了5次测试，每次约200个文件，平均识别率为59%左右。

