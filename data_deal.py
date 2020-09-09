import pandas as pd
import numpy as np
from pyecharts.charts import Bar
import seaborn as sns
#读取文件
data = pd.read_csv(r"C:\Users\54127\Desktop\同程旅游end.csv",encoding='utf-8')
data.head()


# In[2]:


#type(data['start'])
data.dtypes


# In[156]:


#划分出日期一列，名为date
a=[0 for x in range(len(data['start']))]
for i in range(len(data['start'])):
    a[i]=data['start'][i][:10]
data['date']=a
#data.head()


# In[3]:


#将时间字符串改为datetime类型
data['start']=pd.to_datetime(data['start'])
data['end']=pd.to_datetime(data['end'])


# In[173]:


type(data.start.dt.time)


# In[186]:


#划分时间段
from datetime import date
time1 = datetime.strptime('00:00','%H:%M').time()
time2 = datetime.strptime('04:00','%H:%M').time()
time3 = datetime.strptime('08:00','%H:%M').time()
time4 = datetime.strptime('12:00','%H:%M').time()
time5 = datetime.strptime('16:00','%H:%M').time()
time6 = datetime.strptime('20:00','%H:%M').time()
time7 = datetime.strptime('23:59','%H:%M').time()
df1=data[(data.start.dt.time >= time1)&(data.start.dt.time < time2)]
df2=data[(data.start.dt.time >= time2)&(data.start.dt.time < time3)]
df3=data[(data.start.dt.time >= time3)&(data.start.dt.time < time4)]
df4=data[(data.start.dt.time >= time4)&(data.start.dt.time < time5)]
df5=data[(data.start.dt.time >= time5)&(data.start.dt.time < time6)]
df6=data[(data.start.dt.time >= time6)&(data.start.dt.time < time7)]
#按索引遍历
a=[0 for x in range(len(data['start']))]
for i in df1.index:
    a[i]=1
for i in df2.index:
    a[i]=2
for i in df3.index:
    a[i]=3
for i in df4.index:
    a[i]=4
for i in df5.index:
    a[i]=5
for i in df6.index:
    a[i]=6
#print(df1.index[0])
data['timeId']=a
data.head()


# In[187]:


#保存文件
data.to_csv(r"C:\Users\54127\Desktop\同程旅游end.csv",index=0)


# In[147]:


data = data.sort_values(by = 'start')
df = data[(data['departurename']=="上海") & (data['arrivename']=="北京")].head(300)
data.head(115)


# In[ ]:


#折线范围图
fig=sns.relplot(x="timeId", y="price", data=data,
            hue="flightcompany", #style="品号", 
            col="date", col_wrap=1,
            markers=True,dashes=False,# 添加标记，禁止虚线
            kind="line",
            height=7,aspect=1.75)


# In[122]:


import matplotlib.pyplot as plt
import seaborn as sns
#折线
x = df['start']
y1 = df['price']
 
#(data['flightcompany']=='东方航空')&
fig=sns.relplot(x="start", y="price", data=df,
            hue="flightcompany", #style="flightcompany", 
            col="date", 
            markers=True,dashes=False,# 添加标记，禁止虚线
            kind="line",col_wrap=1,
            height=7,aspect=1.75)


# In[70]:


data[(data['departurename']=="上海") & (data['arrivename']=="北京")].head(20)


# In[35]:


data[(data['flightcompany']=='东方航空')&(data['departurename']=="上海") & (data['arrivename']=="北京")]

