from mpu9250_jmdev.mpu_9250 import MPU9250
from mpu9250_jmdev.registers import *

from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go
import plotly.io as pio
import plotly
from db.api import get_gy91_data, get_gy91_data_by_id

import datetime as dt
from collections import deque
import numpy as np
from time import *
import random
import dash
import os


####################################################################################################
# App set-up
#####################################################################################################

#1000 miliseconds = 1 second
GRAPH_INTERVAL = os.environ.get("GRAPH_INTERVAL", 850)

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
                    ['''
                        html.Div(
                            [html.H6('2ND GRAPH CONTAINER',
                                    className='graph__title')]
                        ),
                        dcc.Graph(
                            id = 'gps-tracker',
                            animate = True,
                        ),
                        dcc.Interval(
                            id = 'gps-update',
                            interval = int(GRAPH_INTERVAL),
                            n_intervals = 0
                        ),'''
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
            #className='app__content',
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
	mode = 'lines',
    )

    layout = dict(
        plot_bgcolor = app_color['graph_bg'],
        paper_bgcolor = app_color['graph_bg'],
        font = {'color':'#fff'},
        height = 600,
        xaxis = {
            'range':[-5,5],
            'showline':True,
            'zeroline':False,
            'fixedrange':True,
            'tickvals':[-0, 50, 100, 150, 200],
            "ticktext": ["200", "150", "100", "50", "0"],
            'title':'Time Elapses (sec)'
        },
        yaxis = {
            'range': [
                -1,-1
            ],
            'showgrid':True,
            'showline':True,
            'fixedrange':True,
            'zeroline':False,
            "gridcolor": app_color["graph_line"],
        },
    )

    return dict(data=[trace], layout=layout)

'''
    trace0 = go.Scatter(
    			x=list(Xt),
    			y=list(X),
    			name='X',
    			mode= 'lines+markers',
                line={"color": "#FF0000"},
#                hoverinfo='skip'
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

@app.callback(
    Output('counter_text', 'children'),
    [ Input('interval-component', 'n_intervals')]
)
def update_layout_gps(n):
    #something

@app.callback(
    Ourput('gps-tracker', 'figure'),
    [ Input('gps-update', 'n_intervals') ]
)
def gps_tracker_update(n):
    #append varibales for update then the graph
    fig = go.Figure(
        go.Scattermapbox(
            mode = 'markers+lines',
            lon = [],
            lat = [],
            marker = {'size': 10}
        )
    )
    fig.update_layout(
        margin = {'l':0, 't': 0, 'b':0, 'r':0},
        mapbox = {
            'center': {'lon':n, 'lat':n},
            'style' : 'stamen-terrain',
            'center': {'lon':n, 'lat':nn},
            'zoom':1
        }
    )
    return {'data':fig,
        'layout':go.Layout()
        }

app.layout = html.Div([
    dcc.Graph(figure=fig)
])
'''
if __name__ == '__main__':
	app.run_server(debug=True)

