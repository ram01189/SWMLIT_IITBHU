import numpy as np
import pandas as pd
from sklearn import preprocessing, cross_validation, neighbors
from sklearn.neighbors import KNeighborsRegressor
import csv
column = ['time','temp','humidity','relay','rain','green_per','wind','moisture']
df=pd.read_csv(r'/var/www/html/dht.csv',header=None,names=column)
df.drop(['time'],1,inplace=True)
df2=df.mask(df.astype(object).eq('None')).dropna()
X = np.array(df2.drop(['relay'],1))
Y = np.array(df2['relay'])
X_train,X_test,y_train,y_test=cross_validation.train_test_split(X,Y,test_size=0.1,random_state =7)
clf = KNeighborsRegressor(metric='manhattan')
clf.fit(X_train,y_train)
accuracy=clf.score(X_test,y_test)
print(accuracy)

