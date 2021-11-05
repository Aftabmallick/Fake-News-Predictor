import pandas as pd 
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import  classification_report
import re
import string
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import GradientBoostingClassifier

df_fake = pd.read_csv("Fake.csv")
df_true =pd.read_csv("True.csv")
df_fake.head()
df_true.head()
df_fake["class"]=0
df_true["class"]=1
df_fake.shape,df_true.shape
df_fake_manual_testing =df_fake.tail(10)
for i in range(23480,23470,-1):
    df_fake.drop([i],axis=0,inplace=True)
df_true_manual_testing =df_true.tail(10)   
for i in range(21416,21406,-1):
    df_true.drop([i],axis=0,inplace=True)
    
df_manual_testing = pd.concat([df_fake_manual_testing,df_true_manual_testing],axis=0)
df_manual_testing.to_csv("manual_test.csv")
df_merge =pd.concat([df_fake,df_true],axis=0)
df_merge.head()
df=df_merge.drop(["title","subject","date"],axis=1)
df.head()
df=df.sample(frac=1)
df.head()
df.isnull().sum()
def word_drop(text):
    text=text.lower()
    text=re.sub('\[.*?\]','',text)
    text=re.sub("\\W"," ",text)
    text=re.sub('https?://\S+|www\.\S+','',text)
    text=re.sub('<.*?>+','',text)
    text=re.sub('[%s]'% re.escape(string.punctuation),'',text)
    text=re.sub('\n','',text)
    text=re.sub('\w*\d\w*','',text)
    return text
df["text"]=df["text"].apply(word_drop)
df.head()
x=df["text"]
y=df["class"]
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=.25)
vectorization=TfidfVectorizer()
xv_train=vectorization.fit_transform(x_train)
xv_test=vectorization.transform(x_test)
LR=LogisticRegression()
LR.fit(xv_train,y_train)
LR.score(xv_test,y_test)
pred_LR=LR.predict(xv_test)
print(classification_report(y_test,pred_LR))
DT = DecisionTreeClassifier()
DT.fit(xv_train, y_train)
DT.score(xv_test,y_test)
pred_DT = DT.predict(xv_test)
print(classification_report(y_test,pred_DT))

GBC=GradientBoostingClassifier(random_state=0)
GBC.fit(xv_train,y_train)
GBC.score(xv_test,y_test)
pred_GBC= GBC.predict(xv_test)

print(classification_report(y_test,pred_GBC))
RFC = RandomForestClassifier(random_state=0)
RFC.fit(xv_train,y_train)
RFC.score(xv_test,y_test)
pred_RFC= RFC.predict(xv_test)
print(classification_report(y_test,pred_RFC))

def output_lable(n):
    if n == 0:
        return "Fake News"
    elif n == 1:
        return "Not A Fake News"
    
def manual_testing(news):
    testing_news = {"text":[news]}
    new_def_test = pd.DataFrame(testing_news)
    new_def_test["text"] = new_def_test["text"].apply(word_drop) 
    new_x_test = new_def_test["text"]
    new_xv_test = vectorization.transform(new_x_test)
    pred_LR = LR.predict(new_xv_test)
    pred_DT = DT.predict(new_xv_test)
    pred_GBC = GBC.predict(new_xv_test)
    pred_RFC = RFC.predict(new_xv_test)

    return print("\n\nLR Prediction: {} \nDT Prediction: {} \nGBC Prediction: {} \nRFC Prediction: {}".format(output_lable(pred_LR[0]),output_lable(pred_DT[0]), output_lable(pred_GBC[0]),output_lable(pred_RFC[0]))) 


news = str(input())
manual_testing(news)