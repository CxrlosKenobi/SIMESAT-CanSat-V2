from mpu9250_jmdev.mpu_9250 import MPU9250
from mpu9250_jmdev.registers import *

from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go
import plotly

from collections import deque
import numpy as np
from time import *
import random
import dash
import os


mpu = MPU9250(
    address_ak=AK8963_ADDRESS,
    address_mpu_master=MPU9050_ADDRESS_68, # In 0x68 Address
    address_mpu_slave=None,
    bus=1,
    gfs=GFS_1000,
    afs=AFS_8G,
    mfs=AK8963_BIT_16,
    mode=AK8963_MODE_C100HZ)
mpu.configure()

def module_data(type):
    accelerometer = mpu.readAccelerometerMaster()
    gyroscope = mpu.readGyroscopeMaster()
    magnetometer = mpu.readMagnetometerMaster()
    temperature = mpu.readTemperatureMaster()

    #Accelerometer sorted values if [0][1][2] are X,Y,Z axis respectively
    xA = round(accelerometer[0], 6)
    yA = round(accelerometer[1], 6)
    zA = round(accelerometer[2], 6)
    outA = [xA, yA, zA]

    #Gyroscope sorted values if [0][1][2] are X,Y,Z axis respectively
    xG = round(gyroscope[0], 6)
    yG = round(gyroscope[1], 6)
    zG = round(gyroscope[2], 6)
    outG = [xG, yG, zG]

    #Magnetometer sorted values if [0][1][2] are X,Y,Z axis respectively
    xM = round(magnetometer[0], 6)
    yM = round(magnetometer[1], 6)
    zM = round(magnetometer[2], 6)
    outM = [xM, yM, zM]

    if type == 'GyroX':
        return xG
    elif type == 'GyroY':
        return yG
    elif type == 'GyroZ':
        return zG

X = deque(maxlen=20)
X.append(module_data(type='GyroX'))

Y = deque(maxlen=20)
Y.append(module_data(type='GyroY'))

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
#server = app.server

app.layout = html.Div(
	[
		dcc.Graph(id = 'live-graph', animate = True),
		dcc.Interval(
			id = 'graph-update',
			interval = 1000,
			n_intervals = 0
		),
	]
)

@app.callback(
	Output('live-graph', 'figure'),
	[ Input('graph-update', 'n_intervals') ]
)

def update_graph_scatter(n):
	X.append(X[-1]+1)
	Y.append(Y[-1]+Y[-1] * random.uniform(-0.1,0.1))

	data = plotly.graph_objs.Scatter(
			x=list(X),
			y=list(Y),
			name='Scatter',
			mode= 'lines+markers'
	)

	return {'data': [data],
			'layout' : go.Layout(xaxis=dict(range=[min(X),max(X)]),yaxis = dict(range = [min(Y),max(Y)]),)}


if __name__ == '__main__':
	app.run_server(debug=True)
