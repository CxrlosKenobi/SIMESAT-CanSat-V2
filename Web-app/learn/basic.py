# basic.py
import numpy as np
import pandas as pd
import plotly.offline as pyo
import plotly.graph_objs as go
from plotly import tools
'''
#Scatter plot
np.random.seed(42)
random_x = np.random.randint(1,101,100)
random_y = np.random.randint(1,101,150)

data = [go.Scatter(x=random_x,
                    y=random_y,
                    mode='markers',
                    marker=dict(
                        size=12,
                        color='rgb(51,204,153)',
                        symbol='pentagon',
                        line={'width':2}
                    ))]
layout = go.Layout(title='Hello First Plot',
                    xaxis={'title': 'X-axis'},
                    yaxis=dict(title='Y-axis'),
                    hovermode='closest')

fig = go.Figure(data=data, layout=layout)
pyo.plot(fig, filename='scatter.html')


# Line chart
x_values = np.linspace(0,1,100)
y_values = np.random.randn(100)

trace0 = go.Scatter(x=x_values,
                    y=y_values+5,
                    mode='markers',
                    name='markers')
trace1 = go.Scatter(x=x_values,
                    y=y_values,
                    mode='lines',
                    name='mylines')
trace2 = go.Scatter(x=x_values,
                    y=y_values-5,
                    mode='lines+markers',
                    name='mylinesandmarkers')

data = [trace0, trace1, trace2]

layout = go.Layout(title='Line Charts')

fig = go.Figure(data=data, layout=layout)
pyo.plot(fig)


# Line chart part two
df = pd.read_csv('Data/nst-est2017-alldata.csv')
df2 = df[df['DIVISION'] == '1']
df2.set_index('NAME', inplace=True)
list_of_pop_col = [col for col in df2.columns if col.startswith('POP')]
df2 = df2[list_of_pop_col]

data = [go.Scatter(x=df2.columns,
                    y=df2.loc[name],
                    mode='lines',
                    name=name) for name in df2.index]
pyo.plot(data)


# Bar charts
df = pd.read_csv('Data/2018WinterOlympics.csv')

trace1 = go.Bar(x=df['NOC'], y=df['Gold'],
                name='Gold', marker={'color':'#FFD700'})
trace2 = go.Bar(x=df['NOC'], y=df['Silver'],
                name='Silver', marker={'color':'#9EA0A1'})
trace3 = go.Bar(x=df['NOC'], y=df['Bronze'],
                name='Bronze', marker={'color':'#CD7F32'})

data = [trace1, trace2, trace3]
layout = go.Layout(title='Medals', barmode='stack')
fig = go.Figure(data=data, layout=layout)
pyo.plot(fig)


# Heatmaps
#df = pd.read_csv('Data/2010SantaBarbaraCA.csv')
df = pd.read_csv('Data/2010YumaAZ.csv')

data = [go.Heatmap(x=df['DAY'],
                    y=df['LST_TIME'],
                    z=df['T_HR_AVG'].values.tolist(),
                    colorscale='Jet')]
layout = go.Layout(title='SB CA Temps')
fig = go.Figure(data=data, layout=layout)
#pyo.plot(fig)
'''
# Multiple heat maps with subplots
df1 = pd.read_csv('Data/2010SitkaAK.csv')
df2 = pd.read_csv('Data/2010SantaBarbaraCA.csv')
df3 = pd.read_csv('Data/2010YumaAZ.csv')

trace1 = go.Heatmap(x=df1['DAY'],
                    y=df1['LST_TIME'],
                    z=df1['T_HR_AVG'],
                    colorscale='Jet',
                    zmin=5,
                    zmax=40)
trace2 = go.Heatmap(x=df2['DAY'],
                    y=df2['LST_TIME'],
                    z=df2['T_HR_AVG'],
                    colorscale='Jet',
                    zmin=5,
                    zmax=40)
trace3 = go.Heatmap(x=df3['DAY'],
                    y=df3['LST_TIME'],
                    z=df3['T_HR_AVG'],
                    colorscale='Jet',
                    zmin=5,
                    zmax=40)
fig = tools.make_subplots(rows=1,
                        cols=3,
                        subplot_titles=['Sitka AK', 'SB CA', 'Yuma AZ'],
                        shared_yaxes=True)
fig.append_trace(trace1,1,1)
fig.append_trace(trace2,1,2)
fig.append_trace(trace3,1,3)

fig['layout'].update(title='Temps for 3 cities')

pyo.plot(fig)
