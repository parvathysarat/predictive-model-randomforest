# -*- coding: ut8 -*-
import glob,struct,os
import pandas as pd
import numpy as np
names=["Timestamp","Customer ID","Host","Log file","Log sequence no.","Entry type","Entry identifier","User,if","Reporting IP/host","Source IP,if","Source port,if","Destination IP, if","Destination Port, if","Text field1","Text field2","Text field3","Numeric field1","Numeric field2"]
path=r'C:\\Users\\A\\Desktop\\data'
all_files=glob.glob(os.path.join(path,"*.csv"))
df_each=(pd.read_csv(f,header=None) for f in all_files)
result=pd.concat(df_each)
result.columns=names

#deleting unwanted columns
result.drop(result.columns[[1,2,3,5,7,8,17]],axis=1,inplace=True)
#arranging so that what needs to be predicted is at the end
arranged=result.iloc[:, np.r_[0:7,8:11,7]]
#checking I haven't dropped any columns while indexing
len(arranged.columns)==len(result.columns)

#converting all strings to numeric
arranged["Entry identifier"]=arranged['Entry identifier'].map({'_000':0, '_001':1,'_002':2})
arranged['Text field3']= arranged['Text field3'].map({'UDP':1, 'TCP':2, '47':3})
arranged["Text field2"]=arranged["Text field2"].map({"eth0": 0, "tun0": 1,"lo":2})
features=arranged.columns[:10] # 10columns

#factorizing column to be predicted, saving it in label
y,label = pd.factorize(arranged["Text field1"])
 
#direct method to convert IP address to int in Python 3
import ipaddress
arranged["Destination IP, if"]=arranged["Destination IP, if"].map(lambda x:  int(ipaddress.IPv4Address(x)))

from sklearn.ensemble import RandomForestClassifier
clf=RandomForestClassifier(n_jobs=2)
clf.fit(arranged[features],y)

#import test file
test=pd.read_csv("test.csv",names=names)
test.drop(test.columns[[1,2,3,5,7,8,17]],axis=1,inplace=True)
arranged_test=test.iloc[:, np.r_[0:7,8:11,7]]
(arranged.columns==arranged_test.columns).sum() #11. Arranged correctly

#converting all strings
arranged_test["Entry identifier"]=arranged_test['Entry identifier'].map({'_000':0, '_001':1,'_002':2})
arranged_test['Text field3']= arranged_test['Text field3'].map({'UDP':1, 'TCP':2, '47':3})
arranged_test["Text field2"]=arranged_test["Text field2"].map({"eth0": 0, "tun0": 1,"lo":2})
arranged_test["Destination IP, if"]=arranged_test["Destination IP, if"].map(lambda x:  int(ipaddress.IPv4Address(x)))

pred=clf.predict(arranged_test[features])
pred_label=label[pred]

#normalize=True yields fraction of correct answers
#normalize=False yields no. of correct answers
accuracy=accuracy_score(arranged_test["Text field1"],pred_label,normalize=True)
print (accuracy)

#running
#test=pd.read_csv("test.csv",names=names)
#exec(open("temp.py").read())
#0.906253546703