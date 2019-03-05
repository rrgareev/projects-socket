
# coding: utf-8

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
import plotly.offline as offline
from plotly.graph_objs import *

offline.init_notebook_mode()

df_gain = pd.read_csv('GAINGTX.csv')
df_gain.drop(labels='Unnamed: 0', axis=1, inplace=True)
df_gain = df_gain.drop_duplicates('AdapterTime')
df_gain.columns = ['AdapterTime', 'MidPx_gain', 'Spread_gain']

df_hotspot = pd.read_csv('HOTSPOT.csv')
df_hotspot.drop(labels='Unnamed: 0', axis=1, inplace=True)
df_hotspot = df_hotspot.drop_duplicates('AdapterTime')
df_hotspot.columns = ['AdapterTime', 'MidPx_hotspot', 'Spread_hots']

df_deul = pd.read_csv('DEUTSCHE.csv')
df_deul.drop(labels='Unnamed: 0', axis=1, inplace=True)
df_deul = df_deul.drop_duplicates('AdapterTime')
df_deul.columns = ['AdapterTime', 'MidPx_deul', 'Spread_deul']

df_gs = pd.read_csv('GOLDMANSACHS.csv')
df_gs.drop(labels='Unnamed: 0', axis=1, inplace=True)
df_gs = df_gs.drop_duplicates('AdapterTime')
df_gs.columns = ['AdapterTime', 'MidPx_gs', 'Spread_gs']

df_jp = pd.read_csv('JPMORGAN.csv')
df_jp.drop(labels='Unnamed: 0', axis=1, inplace=True)
df_jp = df_jp.drop_duplicates('AdapterTime')
df_jp.columns = ['AdapterTime', 'MidPx_jp', 'Spread_jp']

df = pd.merge(df_gain, df_deul, on='AdapterTime', how='outer', sort=True)
df = pd.merge(df, df_gs, on='AdapterTime', how='outer', sort=True)
df = pd.merge(df, df_jp, on='AdapterTime', how='outer', sort=True)
df = df.fillna(method='ffill')

print(df)


# In[3]:


trace1 = Scatter(x=df['AdapterTime'], y=(df['MidPx_deul'] - df['MidPx_gain']), name='DEUL-GAIN')
trace2 = Scatter(x=df['AdapterTime'], y=(df['MidPx_gs'] - df['MidPx_gain']), name='GS-GAIN')
trace3 = Scatter(x=df['AdapterTime'], y=(df['MidPx_jp'] - df['MidPx_gain']), name='JP-GAIN')
trace4 = Scatter(x=df['AdapterTime'], y=(df['MidPx_hotspot'] - df['MidPx_gain']), name='HS-GAIN')

trace = [trace1, trace2, trace3, trace4]
data = Data(trace)
fig = Figure(data=data)
offline.iplot(fig)


# In[83]:


(df['MidPx_deul'] - df['MidPx_gain']).describe()


# In[89]:


(df['MidPx_gs'] - df['MidPx_gain']).describe()

