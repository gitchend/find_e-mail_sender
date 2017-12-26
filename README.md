机器学习课程实验报告

### 山东大学计算机学院



### 题目：判断邮件发送人

- 实现算法：朴素贝叶斯

- 软件环境：python 3.6、mysql 5.0.2

- 成员：

  | 姓名   | 学号   |
  | ---- | ---- |
  |      |      |

  ​





#### 需求及思路分析

​	本实验内容为“通过邮件内容判断邮件发送人”，要完成这个工作，我们首先要明确不同人发送邮件的区别在哪里。显然不同的人有不同的工作、兴趣、社交圈子，而这些内容会或多或少地提现在邮件上。例如：Jack经常给Rose发邮件，邮件中自然就会有“Rose”这一单词，当我们拿到一份未署名的、包含“Rose”的电子邮件，我们就知道这份邮件有一定概率是出自Jack之手。当然名为Rose的人很多，某个Rose并不一定是Jack认识的Rose，所以要在整份邮件中寻找线索，找出最有可能的发送人。我们可以预先通过学习知道Jack以及其他人与某个单词关联的程度，当邮件中出现这个单词时，我们能据此判断邮件属于某个人的概率。

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

#### 代码实现

​	因为实验原始数据太多(1.62 GB)，测试不易，故决定分阶段实现代码，首先实现两个发件人之间的判断，代码稳定之后再进行全部发件人的判断。

###### 实现分析

​	原始数据文件夹结构如图：	![深度截图_dde-file-manager_20171113085351](/home/gitchend/Desktop/深度截图_dde-file-manager_20171113085351.png)

![深度截图_dde-file-manager_20171113085434](/home/gitchend/Desktop/深度截图_dde-file-manager_20171113085434.png)

![深度截图_dde-file-manager_20171113085522](/home/gitchend/Desktop/深度截图_dde-file-manager_20171113085522.png)

即：根目录-某个用户的文件夹-一些随意的文件夹和以正整数命名的邮件文件-以正整数命名的邮件文件。

​	用户文件夹是以“用户名字.用户姓氏开头字母”命名，而其下级文件夹命名随意，所以应当先写好读取并处理一个邮件文件的方法，再递归遍历原始数据文件夹，处理每个文件。而算法所需的类名、特征集需从邮件文件里整理出来。

​	邮件文件如下：

![深度截图_gedit_20171113090256](/home/gitchend/Desktop/深度截图_gedit_20171113090256.png)![深度截图_gedit_20171113090224](/home/gitchend/Desktop/深度截图_gedit_20171113090224.png)

从中我们可以获取到如下信息：

> Mime-Version: 1.0
>
> Content-Type: text/plain; charset=us-ascii

即该邮件遵循MIME协议的1.0版本，Content-Type为text/plain，字符集为us-ascii。通过对MIME协议的了解和对原始文件的充分观察，整理出以下有用信息：

1. MIME协议的邮件头是一组以冒号":"隔开的键值对，每个键值对占一行。
2. 邮件头和正文以第一个空行为界。
3. 邮件头中以“X-From”为键的值，即为发件人昵称。

至此，我们已经了解到解析原始邮件文件的方法，规划出实现过程如下：

- 阶段1:

  1. 编写读取并解析单个邮件文件的程序。
  2. 编写递归遍历某根目录，并读取解析邮件文件的程序。
  3. 准备一个较小(2个发件人)的原始文件集，分为学习集和测试集。
  4. 用2中程序遍历3中学习集。
  5. 在内存中生成各频率表，并维护。
  6. 用2中程序遍历3中测试集。
  7. 在内存中算出获得$P_x$所需的值。
  8. 记录$P_x$，并找出最大$P_x$所对应的$C_x$，比较C‘和$C_x$，并记录正确率。

- 阶段2：

  1. 将所有原始文件分为学习集和测试集。

  2. 遍历学习集。

  3. 将学习集解析出的数据保存到数据库。

  4. 遍历测试集。

  5. 分别从内存和数据库(使用Sql)中算出获得$P_x$所需的值。

  6. 记录$P_x$，并找出最大$P_x$所对应的$C_x$，比较C‘和$C_x$，并记录正确率。

     ![深度截图_选择区域_20171113202251](/home/gitchend/Desktop/深度截图_选择区域_20171113202251.png)

###### 阶段1

1. 编写读取、解析单个文件的程序。

   ```python
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
   		if(line.startswith('X-From')):
   			sender=line[8:].strip()
   			break
   	allLine=''.join(allLine[allLine.index('\r\n')+1:]).lower()
   	allLine=re.compile(r'\d|\s|\r\n|\.|\,|\"|\?|\!').split(allLine)
   	allLine=list(set(allLine))
   	try:
   		allLine.remove('')
   	except Exception,e:
       		print e.message
   	return Fileinfo(sender,allLine)
   ```

   该程序定义了一个类`Fileinfo`和一个方法`dealsingle(filePath)`。`Fileinfo`用来该邮件储存发送人和特征集，`dealsingle(filePath)`功能为：传入一个文件的路径，返回该文件的发送人和特征集，并用`Fileinfo`包装。

   方法`dealsingle(filePath)`做了以下操作：

   1. 打开文件并读取。
   2. 找到以”X-From“开头的行，由此得到sender。
   3. 根据第一个空行切片，去掉文件头，得到正文。
   4. 将所有字符转为小写。
   5. 将正文用各种分割符号正则分割，并转为list
   6. 利用set去重
   7. 返回由该list和sender生成的Fileinfo

   测试代码如下：

   ```python
   a=dealsingle('11.')
   print a.sender
   print a.infolist
   ```

   结果：

   ![深度截图_deepin-terminal_20171113213634](/home/gitchend/Desktop/深度截图_deepin-terminal_20171113213634.png)

2. 编写递归遍历某个文件夹的程序。

   ```python
   #findsender.py

   import os
   import singlefile

   def start(step,dirPath):
   	dirlist=os.listdir(dirPath)
   	for singledir in dirlist:
   		comdir=dirPath+'/'+singledir
   		if(os.path.isfile(comdir)):
   			deal(step,comdir)
   		else:
   			filelist=os.listdir(comdir)
   			for singlefile in filelist:
   				comdir2=comdir+'/'+singlefile
   				if(os.path.isfile(comdir2)):
   					deal(step,comdir2)
   def deal(step,comdir):
   	fileinfo=singlefile.dealsingle(comdir)
   	if step is 0:
   		print comdir+"|"+fileinfo.sender
   	elif step is 1:
   		step1deal(fileinfo)
   	elif step is 2:
   		step2deal(fileinfo)
   ```

   该程序为程序入口。定义一个`start(step,dirPath)`方法：传入阶段（step），阶段为0时为测试；传入dirPath，为需要遍历的根目录。调用`singlefile.dealsingle(comdir)`获得单个邮件文件的信息，step为1或2时分别将邮件信息传入阶段1和阶段2的处理方法。

   测试代码：

   ```python
   start(0,'dickson-s')
   ```

   结果：

   ​