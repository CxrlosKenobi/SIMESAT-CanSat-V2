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
sys.path.append('./SDL_Pi_HDC1080_Python3')
hdc1080 = SDL_Pi_HDC1080.SDL_Pi_HDC1080()
X = deque(maxlen=30)
X.append(1)
Y = deque(maxlen=30)
Y.append(1)

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
        							[html.H6("Live GPS",
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
                            [html.H6('Live 3D Gyroscope',
                                    className='graph__title')]
                        ),
						dcc.Graph(
							id = 'live-graph2',
							figure = dict(
								layout = dict(
									plot_bgcolor = app_color['graph_bg'],
									paper_bgcolor = app_color['graph_bg'],
									)
							),
						),
						dcc.Interval(
							id = 'graph-update2',
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
							id = 'live-temp', animate = True
						),
						dcc.Interval(
							id = 'temp-update',
							interval = int(GRAPH_INTERVAL),
							n_intervals = 0
						),
					],
					className = 'graph__container second',
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
                                    [	html.Hr(),
                                        html.P(children=[
                                            '© 2021 Academia de Ciencias SIMES. Todos los derechos reservados.'
                                            #Creado por ', html.A('Kenobi', href='https://github.com/CxrlosKenobi')
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
            className='app__content',
        ), # footer's end
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
    total_time = get_current_time()
    df = get_gy91_data(total_time - 200, total_time)

    trace = dict(
        type = 'scatter',
        y = df['yG'],
        line = {'color':'#42C4F7'},
	hoverinfo = 'skip',
	error_y = {
		'type':'data',
		'array':df['yG'],
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
        height = 500,
        xaxis = {
            'range':[-5,5],
            'showline':True,
            'zeroline':False,
            'fixedrange':True,
            'tickvals':[0, 50, 100, 150, 200],
            "ticktext": ["200", "150", "100", "50", "0"],
            'title':'Time Elapsed (sec)'
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


@app.callback(
	Output('live-graph2', 'figure'), [Input('graph-update2', 'n_intervals')]
)
def update_graph_scatter(n):
    total_time = get_current_time()
    df = get_gy91_data(total_time - 200, total_time)

    trace = dict(
        type = 'scatter',
        y = df['yG'],
        line = {'color':'#42C4F7'},
	hoverinfo = 'skip',
	mode = 'lines',
    )

    layout = dict(
        plot_bgcolor = app_color['graph_bg'],
        paper_bgcolor = app_color['graph_bg'],
        font = {'color':'#fff'},
        height = 250,
        autosize = False,
        xaxis = {
            'range':[-5,5],
            'showline':True,
            'zeroline':False,
            'fixedrange':True,
            'tickvals':[0, 50, 100, 150, 200],
            "ticktext": ["200", "150", "100", "50", "0"],
            'title':'Time Elapsed (sec)'
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


@app.callback(Output('live-temp', 'figure'),
              [Input('temp-update', 'n_intervals')])
def update_graph_scatter(input_data):
    X.append(X[-1]+1)
    Y.append(round(hdc1080.readTemperature(), 2))
    data = go.Scatter(
                x = list(X),
                y = list(Y),
                name = 'Scatter',
                mode = 'lines+markers',
                line = {'color':'#42C4F7'},
            )
    layout = go.Layout(
                plot_bgcolor = app_color['graph_bg'],
                paper_bgcolor = app_color['graph_bg'],
                font = {'color':'#fff'},
                height = 250,
                autosize = True,
                xaxis = dict(
                        range = [min(X), max(X)],
                        showline = True,
                        zeroline = False,
                        fixedrange = True,
                        tickvals = [0, 50, 100, 150, 200],
                        ticktext = ['200', '150', '100', '50', '0'],
                        title = 'Time elapsed (sec)'
                ),
                yaxis = dict(
                            range = [min(Y)- .5, max(Y)+ .5],
                            showgrid = True,
                            showline = True,
                            fixedrange = True,
                            zeroline = False,
                            gridcolor = app_color['graph_line']
                        ),
            )

    return {'data': [data], 'layout' : layout}


if __name__ == '__main__':
    app.run_server(host='192.168.10.37', debug=True)

