from mpu9250_jmdev.mpu_9250 import MPU9250
from mpu9250_jmdev.registers import *

from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go
import plotly.io as pio
import plotly

from collections import deque
import numpy as np
from time import *
import random
import dash
import os


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

# 1000 miliseconds = 1 second
GRAPH_INTERVAL = os.environ.get("GRAPH_INTERVAL", 850)

app = dash.Dash(
	__name__,
	meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)

colors = {'background':'#111111', 'text':'#7FDBFF'}
colors['text']

#server = app.server

app_color = {"graph_bg": "#082255", "graph_line": "#007ACE"}

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
							'This app continually queries csv files and displays live charts of the modules in the OBC at the nano-satellite',
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
        				#GY91 simulation
        				html.Div(
        					[
        						html.Div(
        							[html.H6("GY-91 - simulation",
        							className='graph__title')]
        						),
        						dcc.Graph(
        							id = 'live-graph',
        							animate = True
        						),
        						dcc.Interval(
        							id = 'graph-update',
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
                            [
                                html.H6(
                                    '2ND GRAPH CONTAINER',
                                    className='graph__title'
                                )
                            ]
                        ),
                        dcc.Graph(
                            id = '',
                            animate = True,
                            figure = dict(
                                layout = dict(
                                    plot_bgcolor=app_color["graph_bg"],
                                    paper_bgcolor=app_color["graph_bg"],
                                )
                            )
                        ),
                        dcc.Interval(
                            id = '',
                            interval = int(GRAPH_INTERVAL),
                            n_intervals = 0
                        ),
                    ],
                    className='graph__container first'
                )
            ],
            className='one-third column histogram__direction',
        ),
        # footer
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.P(children=[
                                            '© 2021 Academia de Ciencias SIMES. Todos los derechos reservados. Creado por ',
                                            html.A('Kenobi', href='https://github.com/CxrlosKenobi')
                                            ],
                                            className='app__footer--grey',
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
            ],
            #className='app__content',
        ), # footer's end
	],
	className='app__container',
)

'''
def get_current_time():
    """ Helper function to get the current time in seconds. """

    now = dt.datetime.now()
    total_time = (now.hour * 3600) + (now.minute * 60) + (now.second)
    return total_time
'''

Xt = deque(maxlen=20)
Xt.append(np.random.randint(1,60))

X = deque(maxlen=20)
X.append(np.random.randint(15,20))

Y = deque(maxlen=20)
Y.append(np.random.randint(35,40))

Z = deque(maxlen=20)
Z.append(np.random.randint(50,60))

@app.callback(
	Output('live-graph', 'figure'),
	[ Input('graph-update', 'n_intervals') ]
)

def update_graph_scatter(n):
    Xt.append(Xt[-1]+1)

    X.append(module_data(type='GyroX'))
    Y.append(module_data(type='GyroY'))
    Z.append(module_data(type='GyroZ'))

    '''
    X.append(X[-1] + X[-1] * random.uniform(-0.1, 0.1))
    Y.append(Y[-1] + Y[-1] * random.uniform(-0.1, 0.1))
    Z.append(Z[-1] + Z[-1] * random.uniform(-0.1, 0.1))
    '''
    trace0 = go.Scatter(
    			x=list(Xt),
    			y=list(X),
    			name='X',
    			mode= 'lines+markers',
                line={"color": "#FF0000"}
                )
    trace1 = go.Scatter(
    			x=list(Xt),
    			y=list(Y),
    			name='Y',
    			mode= 'lines+markers',
                line={"color": "#00FF00"}
                )
    trace2 = go.Scatter(
                x=list(Xt),
    			y=list(Z),
    			name='Z',
    			mode= 'lines+markers',
                line={"color": "#FFFF00"}
                )
    data = [trace0, trace1, trace2]
    return {'data': data,
            'layout':go.Layout(
                        xaxis = {
                            'range':[min(Xt), max(Xt)],
                            'title':'X axis',
                            'showline':True,
                        },
                        yaxis = {
                            'range':[min(X),max(Z)],
                            'title':'Y axis',
                            'showgrid':True,
                            "showline": True,
                            "zeroline": False,
                            "gridcolor": app_color["graph_line"]
                        },
                        plot_bgcolor=app_color["graph_bg"],
                        paper_bgcolor=app_color["graph_bg"],
                        font={"color": "#fff"},
                        height=400
					)
			}

if __name__ == '__main__':
	app.run_server(debug=True)
