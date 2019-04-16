#################################################### TRAIN A MACHINE LEARNING MODEL ####################
import numpy as np
import pandas as pd
from sklearn import preprocessing, cross_validation, neighbors
from sklearn.metrics import precision_score
from sklearn.metrics import f1_score
from sklearn.metrics import average_precision_score
from sklearn.metrics import accuracy_score
column=['time','temp','humidity','relay','rain','green_per','wind','moisture']
df=pd.read_csv(r'/var/www/html/dht.csv',header=None,names=column)
df.drop(['time'],1,inplace=True)
df2=df.mask(df.astype(object).eq('None')).dropna()
X=np.array(df2.drop(['relay'],axis=1))
y=np.array(df2['relay'])
X_train,X_test,y_train,y_test=cross_validation.train_test_split(X,y,test_size=0.1)
print('test'+str(y_test.shape))
print('train'+str(y_train.shape))
clf=neighbors.KNeighborsClassifier()
clf.fit(X_train,y_train)
accuracy=clf.score(X_test,y_test)
example=np.array([36,93,1,96.0,10,400])
arr=example.reshape(1, -1)
predict=clf.predict(X_train)
print(f1_score(y_train, predict, average='binary'))  
#accuracy_score(y_train, predict)
#average_precision_score(y_train,predict)  
#precision_score(y_train, predict, average='macro')

