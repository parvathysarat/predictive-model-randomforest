import glob,struct,os
import pandas as pd
import numpy as np

#names of the columns
names=["Timestamp","Customer ID","Host","Log file","Log sequence no.","Entry type","Entry identifier","User,if","Reporting IP/host","Source IP,if","Source port,if","Destination IP, if","Destination Port, if","Text field1","Text field2","Text field3","Numeric field1","Numeric field2"]

# defining path to the dataset folder
path=r'C:/Users/PARVATHY SARAT/Desktop/FIREWALL'

#accessing all CSV files (datasets or Firewall logs) in the folder
all_files=glob.glob(os.path.join(path,"*.csv"))

df_each=(pd.read_csv(f,header=None) for f in all_files)

#concatenating all the CSV files in the folder
result=pd.concat(df_each)
result.columns=names

arranged=result.iloc[:,[12,13]]
# ensuring 'arranged' is not a copy of the original 'result' dataset as 
# it can lead to errors with certain functions and make it difficult
# to work with
arranged.is_copy=False

# Removing all the rows for which Output = "AUDIT" as
# they are redundant
arranged=arranged[arranged["Text field1"]!="AUDIT"]
arranged=arranged[arranged["Text field1"]!="AUDIT INVALID"]

features=arranged.columns[0] 
arranged=arranged.dropna(axis=0)

train=np.array(arranged[features])
train=train.reshape(-1,1)

#factorizing column to be predicted, saving it in 'label'
y,label = pd.factorize(arranged["Text field1"])
 
from sklearn.ensemble import RandomForestClassifier
clf=RandomForestClassifier()

#fitting the Random Forest Classification model to the training data
clf.fit(train,y)

#import test file
test=pd.read_csv("file:///C:/Users/PARVATHY SARAT/Desktop/test.csv",names=names)

arranged_test=test.iloc[:,[12,13]]

# Applying same changes as to the training set
# Removing redundant rows
arranged_test=arranged_test[arranged_test["Text field1"]!="AUDIT"]
arranged_test=arranged_test[arranged_test["Text field1"]!="AUDIT INVALID"]

test=np.array(arranged_test[features])
test=test.reshape(-1,1)

# Using the model to predict the Output (ie. fraud or not) on the test datset
pred=clf.predict(test)
pred_label=label[pred]

from sklearn.metrics import accuracy_score

#normalize=True yields fraction of correct answers
#normalize=False yields no. of correct answers

accuracy=accuracy_score(arranged_test["Text field1"],pred_label,normalize=True)
print (accuracy)

# 1.0