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