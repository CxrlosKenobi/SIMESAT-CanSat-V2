import numpy as np
import pandas as pd
import plotly.offline as pyo
import plotly.graph_objs as go
from plotly import tools

df = pd.read_csv('data1.csv')

df['Temperature(C)'] = df['Temperature(C)'].round(2)
df['Humidity'] = df['Humidity'].round(2)

df[['Time', 'Hour']] = df.Time.str.split(' ', expand=True)
df[['Hour', 'Trash']] = df.Hour.str.split('.', expand=True)

df = df[['Time', 'Hour', 'Temperature(C)', 'Humidity']]
print(df)


'''
data = [go.Heatmap(
            x = df['Temperature(C)'],
            y = df['Time'],
            z = df['Humidity'].values.tolist()
            )]

layout = go.Layout(
            title='Temperatura y humedad en sala de Casa Con-Ciencia en Verano',
            xaxis = {'title':'X-axis'},
            yaxis = {'title':'Y-axis'}
)

fig = go.Figure(
            data = data,
            layout = layout
)

pyo.plot(fig)
'''
