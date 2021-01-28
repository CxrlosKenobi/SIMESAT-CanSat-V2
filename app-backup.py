import SDL_Pi_HDC1080
from mpu9250_jmdev.mpu_9250 import MPU9250
from mpu9250_jmdev.registers import *

from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go
import plotly.io as pio
import plotly

from collections import deque
import datetime as dt
import numpy as np
from time import *
import random
import dash
import sys
import os

####################################
 # Graph container HDC1080 SET-UP #
####################################
sys.path.append('./SDL_Pi_HDC1080_Python3')
hdc1080 = SDL_Pi_HDC1080.SDL_Pi_HDC1080()

X = deque(maxlen=60) # Time
X.append(1)

Y = deque(maxlen=60) # Temperature
Y.append(1)

Z = deque(maxlen=60) # Humidity
Z.append(1)

############################
 # Getting data from GY91 #
############################
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
    xG = round(gyroscope[0], 2)
    yG = round(gyroscope[1], 2)
    zG = round(gyroscope[2], 2)
    outG = [xG, yG, zG]

    #Magnetometer sorted values if [0][1][2] are X,Y,Z axis respectively
    xM = round(magnetometer[0], 6)
    yM = round(magnetometer[1], 6)
    zM = round(magnetometer[2], 6)
    outM = [xM, yM, zM]

    if type == 'xG':
        return xG
    elif type == 'yG':
        return yG
    elif type == 'zG':
        return zG

#################################
 # Graph container GY91 SET-UP #
#################################

Xt = deque(maxlen=30)
Xt.append(np.random.randint(-1,1))

X = deque(maxlen=30)
X.append(module_data(type='GyroX'))
#X.append(np.random.randint(15,20))

Y = deque(maxlen=30)
Y.append(module_data(type='GyroY'))
Y.append(module_data(type='GyroY'))
#Y.append(np.random.randint(35,40))

Z = deque(maxlen=30)
Z.append(module_data(type='GyroZ'))
Z.append(module_data(type='GyroZ'))
#Z.append(np.random.randint(50,60))


#################
 # App set-up #
#################

# 1000 miliseconds = 1 second
GRAPH_INTERVAL = os.environ.get("GRAPH_INTERVAL", 1000)

app = dash.Dash(
	__name__,
	meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
app.title = "SIMESAT 1 - DRAFT DASHBOARD"

colors = {'background':'#111111', 'text':'#7FDBFF'}
colors['text']

server = app.server

app_color = {"graph_bg": "#082255", "graph_line": "#007ACE"}


#####################################################################
# Main layout
#####################################################################
app.layout = html.Div(
	[
		#header
		html.Div(
			[
				html.Div(
					[
						html.H4('🛰️ SIMESAT 1 - DRAFT DASHBOARD',
						className='app__header__title'
						),
						html.P(
							'This app continually queries a SQL database and displays live charts',
							className='app__header__title--grey',
						),
					],
					className='app__header__desc'
				),
				html.Div(
					[
						html.Img(
							src=app.get_asset_url('SIMES_white.png'),
							className='app__menu__img',
						)
					],
					className='app__header__logo',
				),
			],
			className='app__header',
		),
        html.Div(
            [
        		# Container 1
        		html.Div(
        			[
        				#GY91
        				html.Div(
        					[
        						html.Div(
        							[html.H6("Live Conditions Plot",
        							className='graph__title')]
        						),
                                dcc.Graph(
                                        id = 'HDC-live',
                                        figure = dict(
                                        	layout = dict(
                                                	plot_bgcolor = app_color['graph_bg'],
                                                        paper_bgcolor = app_color['graph_bg'],
                                                ),
                                        ),
                                ),
                                dcc.Interval(
                                        id = 'HDC-update',
			                            interval = int(GRAPH_INTERVAL),
			                            n_intervals = 0
                                ),
        					],
        				),
        			],
                className="two-thirds column wind__speed__container",
    			#className='app__content'
                ),
            ],
        ),
        # Second column container
        html.Div(
            [   # Second graph
                html.Div(
                    [
                        html.Div(
                            [html.H6('Live 2D Gyroscope',
                                    className='graph__title')]
                        ),
						dcc.Graph(
							id = 'Gyroscope-live', animate = True
                        ),
                        dcc.Interval(
                            id = 'Gyroscope-update',
                            interval = int(GRAPH_INTERVAL),
                            n_intervals = 0
                        ),
                    ],
                    className='graph__container first',
                ),
				# Third container
				html.Div(
					[
						html.Div(
							[
								html.H6(
									"Live GPS Feed",
									className = 'graph__title'
								)
							]
						),
						dcc.Graph(
							id = 'live-graph', animate = True
						),
						dcc.Interval(
							id = 'graph-update',
							interval = int(GRAPH_INTERVAL),
							n_intervals = 0
						),
					],
					className = 'graph__container second',
				)
            ],
            className='one-third column histogram__direction',
        ),
	],
	className='app__container',
)

def get_current_time():
    """ Helper function to get the current time in seconds. """

    now = dt.datetime.now()
    total_time = (now.hour * 3600) + (now.minute * 60) + (now.second)
    return total_time


#######################
# HDC1080 - live feed #
#######################
@app.callback(
	Output('HDC-live', 'figure'), [Input('HDC-update', 'n_intervals')]
)
def update_graph_scatter(n):
    X.append(X[-1]+1)
    Y.append(round(hdc1080.readTemperature(), 2))
    Z.append(round(hdc1080.readHumidity(), 2))

    minV = [min(Y), min(Z)]
    maxV = [max(Y), max(Z)]
    trace0 = go.Scatter( # Temperature
                x = list(X),
                y = list(Y),
                name = 'Temperature (C)',
                mode = 'lines',
                line = {'color':'#42C4F7'},
            )
    trace1 = go.Scatter( # Humidity
                x = list(time),
                y = list(Z),
                name = 'Humidity (%)',
                mode = 'lines',
                line = {'color':'#51E751'},
            )

    layout = go.Layout(
                plot_bgcolor = app_color['graph_bg'],
                paper_bgcolor = app_color['graph_bg'],
                font = {'color':'#fff'},
                height = 250,
                autosize = True,
                showlegend = False,
                xaxis = dict(
                        range = [min(X)- 1.5, max(X)+ 1.5],
                        showline = True,
                        zeroline = False,
                        fixedrange = True,
                        title = 'Time elapsed (sec)'
                ),
                yaxis = dict(
                            range = [min(minV)- 1.5, max(maxV)+ 1.5],
                            showgrid = True,
                            showline = True,
                            fixedrange = True,
                            zeroline = False,
                            gridcolor = app_color['graph_line']
                        ),
            )

    return {'data': [trace0, trace1], 'layout' : layout}

#####################
# Graph container 2 #
#####################
@app.callback(Output('Gyroscope-live', 'figure'),
              [Input('Gyroscope-update', 'n_intervals')])
def update_graph_scatter(input_data):
    time.append(X[-1]+1)
    GyroscopeX.append(round( mpu.readGyroscopeMaster()[0] , 4))
    GyroscopeY.append(round( mpu.readGyroscopeMaster()[1] , 4))
    GyroscopeZ.append(round( mpu.readGyroscopeMaster()[2] , 4))

    minV = [min(GyroscopeX), min(GyroscopeY), min(GyroscopeZ)]
    maxV = [max(GyroscopeX), max(GyroscopeY), max(GyroscopeZ)]

    GyroX = go.Scatter( # Gyroscope X-axis
                x = list(time),
                y = list(GyroscopeX),
                name = 'X-Gyroscope',
                mode = 'lines',
                line = {'color':'#A50EFF'},
            )
    GyroY = go.Scatter( # Gyroscope Y-axis
                x = list(time),
                y = list(GyroscopeY),
                name = 'Y-Gyroscope',
                mode = 'lines',
                line = {'color':'#FF2C00'},
            )
    GyroZ = go.Scatter( # Gyroscope Z-axis
                x = list(time),
                y = list(GyroscopeZ),
                name = 'Z-Gyroscope',
                mode = 'lines',
                line = {'color':'#FF0082'},
            )

    layout = go.Layout(
                plot_bgcolor = app_color['graph_bg'],
                paper_bgcolor = app_color['graph_bg'],
                font = {'color':'#fff'},
                height = 250,
                autosize = True,
                showlegend = False,
                xaxis = dict(
                        range = [min(X)- 1.5, max(X)+ 1.5],
                        showline = True,
                        zeroline = False,
                        fixedrange = True,
                        title = 'Time elapsed (sec)'
                ),
                yaxis = dict(
                            range = [min(minV)- 1.5, max(maxV)+ 1.5],
                            showgrid = True,
                            showline = True,
                            fixedrange = True,
                            zeroline = False,
                            gridcolor = app_color['graph_line']
                        ),
            )

    return {'data': [GyroX, GyroY, GyroZ], 'layout' : layout}

#####################
# Graph container 3 #
#####################
@app.callback(
	Output('live-graph', 'figure'), [Input('graph-update', 'n_intervals')]
)
def update_graph_scatter(n):

    trace = dict(
        type = 'scatter',
        line = {'color':'#42C4F7'},
	hoverinfo = 'skip',
	error_y = {
		'type':'data',
		'thickness':1.5,
		'width':2,
		'color':'#B4E8FC',
	},
	mode = 'lines',
    )

    layout = dict(
        plot_bgcolor = app_color['graph_bg'],
        paper_bgcolor = app_color['graph_bg'],
        font = {'color':'#fff'},
        height = 570,
        xaxis = {
            'range':[-5,5],
            'showline':True,
            'zeroline':False,
            'fixedrange':True,
            'title':'X axis'
        },
        yaxis = {
            'range': [
                -5,5
            ],
            'showgrid':True,
            'showline':True,
            'fixedrange':True,
            'zeroline':False,
            "gridcolor": app_color["graph_line"],
        },
    )

    return dict(data=[trace], layout=layout)


if __name__ == '__main__':
    app.run_server(host='192.168.10.37', debug=True)

