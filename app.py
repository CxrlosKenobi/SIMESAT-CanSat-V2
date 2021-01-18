from mpu9250_jmdev.mpu_9250 import MPU9250
from mpu9250_jmdev.registers import *
import SDL_Pi_HDC1080

from db.api import get_gy91_data, get_gy91_data_by_id
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

############################
# Graph container 3 SET-UP #
############################
sys.path.append('./SDL_Pi_HDC1080_Python3')
hdc1080 = SDL_Pi_HDC1080.SDL_Pi_HDC1080()

X = deque(maxlen=60) # Time
X.append(1)

Y = deque(maxlen=60) # Temperature
Y.append(1)

Z = deque(maxlen=60) # Humidity
Z.append(1)


############################
# Graph container 2 SET-UP #
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

time = deque(maxlen=50) # Time for X-axis
time.append(1)

GyroscopeX = deque(maxlen=50)
GyroscopeX.append(1)

GyroscopeY = deque(maxlen=50)
GyroscopeY.append(1)

GyroscopeZ = deque(maxlen=50)
GyroscopeZ.append(1)


####################################################################################################
# App set-up
#####################################################################################################

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

# Main layout
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
        		#GY-91 container
        		html.Div(
        			[
        				#GY91
        				html.Div(
        					[
        						html.Div(
        							[html.H6("Live GPS Feed",
        							className='graph__title')]
        						),
                                                        dcc.Graph(
                                                                id = 'live-graph',
                                                                figure = dict(
                                                                	layout = dict(
                                                                        	plot_bgcolor = app_color['graph_bg'],
                                                                                paper_bgcolor = app_color['graph_bg'],
                                                                        ),
                                                                ),
                                                        ),
                                                        dcc.Interval(
                                                                id = 'graph-update'
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
									"Live Conditions Plot",
									className = 'graph__title'
								)
							]
						),
						dcc.Graph(
							id = 'HDC-live', animate = True
						),
						dcc.Interval(
							id = 'HDC-update',
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


if __name__ == '__main__':
    app.run_server(host='192.168.10.37', debug=True)
