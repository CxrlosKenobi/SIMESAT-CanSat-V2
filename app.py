#!/usr/bin/python
# -*- coding: utf-8 -*-
from mpu9250_jmdev.mpu_9250 import MPU9250
from mpu9250_jmdev.registers import *
import SDL_Pi_HDC1080

from db.api import get_gy91_data, get_gy91_data_by_id
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go
import plotly.io as pio
import plotly
import dash

from collections import deque
import datetime as dt
import numpy as np
from time import *
import random
import sys
import os

####################################
 # Graph container HDC1080 SET-UP #
####################################
sys.path.append('./SDL_Pi_HDC1080_Python3')
hdc1080 = SDL_Pi_HDC1080.SDL_Pi_HDC1080()

############################
# Graph container 3 SET-UP #
############################
X = deque(maxlen=45)  # Time
X.append(1)

Y = deque(maxlen=45)  # Temperature
Y.append(1)

Z = deque(maxlen=45)  # Humidity
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

##  Accelerometer & Gyroscope
mpu.calibrateMPU6500() #  Calibrate sensors
mpu.configure() #  The calibration function rests the sensors, so you need to reconfigure them

abias = mpu.abias # Get the master accelerometer biases
abias_slave = mpu.abias_slave # Get the slave accelerometer biases
gbias = mpu.gbias # Get the master gyroscope biases
gbias_slave = mpu.gbias_slave # Get the slave gyroscope biases


##  Magnetometer
mpu.calibrateAK8963() # Calibrate sensors
mpu.configure() # The calibration function resets the sensors, so you need to reconfigure them

magScale = mpu.magScale # Get magnetometer soft iron distortion
mbias = mpu.mbias # Get magnetometer hard iron distortion

time = deque(maxlen=30)  # Time for X-axis
time.append(1)

GyroscopeX = deque(maxlen=30)
GyroscopeX.append(1)

GyroscopeY = deque(maxlen=30)
GyroscopeY.append(1)

GyroscopeZ = deque(maxlen=30)
GyroscopeZ.append(1)

############################################################
# App set-up
############################################################
colors = {'background':'#111111', 'text':'#7FDBFF'}
colors['text']

# 1000 miliseconds = 1 second
GRAPH_INTERVAL = os.environ.get("GRAPH_INTERVAL", 1000)

FA = "https://use.fontawesome.com/releases/v5.15.1/css/all.css"
PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"

app = dash.Dash(
	__name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP, FA],
	meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)

app.title = "SIMESAT 1 - DRAFT DASHBOARD"

sidebar = html.Div(
    [
        html.Div(
            [
                #  width: 3rem ensures the logo is the exact width of the collapsed sidebar (acounting for padding)
                html.Img(src=PLOTLY_LOGO, style={"width":"3rem"}),
                html.H2("Sidebar"),
            ],
            className="sidebar-header",
        ),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink(
                    [html.I(className="fas fa-home mr-2"),
                    html.Span("Home")],
                    href="/",
                    active="exact",
                ),
                dbc.NavLink(
                    [
                        html.I(className="fas fa-calendar-alt mr-2"),
                        html.Span("Demostration"),
                    ],
                    href="/demo",
                    active="exact",
                ),
                dbc.NavLink(
                    [
                        html.I(className="fas fa-envelope-open-text mr-2"),
                        html.Span("Messages"),
                    ],
                    href="/messages",
                    active="exact",
                ),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    className="sidebar",
)

content = html.Div(id="page-content", className="content")

#server = app.server

app_color = {"graph_bg": "#082255", "graph_line": "#007ACE"}

############################################################
# App layout
############################################################
homeDir = html.Div(
    [
        # Header
        html.Div(
            [
                html.Div(
                    [html.H4(
                        '🛰️ SIMESAT 1 - DRAFT DASHBOARD',
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
                    [html.Img(
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
            [  # First container
                html.Div(
                    [  # Container
                        html.Div(
                            [html.Div(
                                [html.H6("Live Conditions Plot",
                                         className='graph__title')]
                            ),
                                dcc.Graph(
                                id='HDC-live',  # ID
                                figure=dict(
                                    layout=dict(
                                                plot_bgcolor=app_color['graph_bg'],
                                                paper_bgcolor=app_color['graph_bg'],
                                    ),
                                ),
                            ),
                                dcc.Interval(
                                id='HDC-update',  # ID
                                interval=int(GRAPH_INTERVAL),
                                n_intervals=0
                            ),
                            ],
                        ),
                    ],
                    className="two-thirds column wind__speed__container",
                    # className='app__content'
                ),
            ],
        ),
        # Second column container
        html.Div(
            [  # Second graph & container
                html.Div(
                    [html.Div(
                        [html.H6('Live 2D Gyroscope',
                                 className='graph__title')
                         ]
                    ),
                        dcc.Graph(
                        id='Gyroscope-live',  # ID
                        figure=dict(
                            layout=dict(
                                plot_bgcolor=app_color['graph_bg'],
                                paper_bgcolor=app_color['graph_bg'],
                            ),
                        ),
                    ),
                        dcc.Interval(
                        id='Gyroscope-update',  # ID
                        interval=int(GRAPH_INTERVAL),
                        n_intervals=0
                    ),
                    ],
                    className='graph__container first',
                ),
                # Third graph & container
                html.Div(
                    [html.Div(
                        [html.H6(
                            "Live GPS Feed",
                            className='graph__title'
                        )
                        ]
                    ),
                        dcc.Graph(
                        id='live-graph',  # ID
                        figure=dict(
                            layout=dict(
                                plot_bgcolor=app_color['graph_bg'],
                                paper_bgcolor=app_color['graph_bg'],
                            ),
                        ),
                    ),
                        dcc.Interval(
                        id='graph-update',  # ID
                        interval=int(GRAPH_INTERVAL),
                        n_intervals=0
                    ),
                    ],
                    className='graph__container second',
                ),
            ],
            className='one-third column histogram__direction',
        ),
    ],
    className='app__container',
)


app.layout = html.Div(
    [dcc.Location(id="url"), sidebar, content]
)
#  Set the content according to the current pathname
@app.callback(Output("page-content", "children"), Input("url", "pathname"))
def render_page_content(pathname):
    if pathname == "/":
        return homeDir
    elif pathname == "/demo":
        return html.P("Here are our demostration with random data!")
    elif pathname == "/calendar":
        return html.P("This is your calendar... not much in the diary...")

    #  If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
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
    X.append(X[-1] + 1)
    #  Y.append(np.random.randint(20, 25) * random.uniform(-1, 1))
    #  Z.append(np.random.randint(25, 30) * random.uniform(-1, 1))

    #  X.append(X[-1]+1)
    Y.append(round(hdc1080.readTemperature(), 2))
    Z.append(round(hdc1080.readHumidity(), 2))

    minV = [min(Y), min(Z)]
    maxV = [max(Y), max(Z)]

    # Temperature
    trace0 = go.Scatter(
        x=list(X),
        y=list(Y),
        name='Temperature (C)',
        mode='lines',
        line={'color': '#FF8300', 'width': 2.5}
    )

    # Humidity
    trace1 = go.Scatter(
        x=list(time),
        y=list(Z),
        name='Humidity (%)',
        mode='lines',
        line={'color': '#51E751', 'width': 2.5}
    )

    layout = go.Layout(
        plot_bgcolor=app_color['graph_bg'],
        paper_bgcolor=app_color['graph_bg'],
        font={'color': '#fff'},
        height=570,
        autosize=True,
        showlegend=False,
        xaxis=dict(
            range=[min(X) - 1.5, max(X) + 1.5],
            showline=True,
            zeroline=False,
            fixedrange=True,
            title='Time elapsed (sec)'
        ),
        yaxis=dict(
            range=[min(minV) - 1.5, max(maxV) + 1.5],
            showgrid=True,
            showline=True,
            fixedrange=True,
            zeroline=False,
            gridcolor=app_color['graph_line']
        ),
    )

    return {'data': [trace0, trace1], 'layout': layout}


#####################
# Graph container 2 #
#####################
@app.callback(Output('Gyroscope-live', 'figure'),
              [Input('Gyroscope-update', 'n_intervals')])
def update_graph_scatter(input_data):
    time.append(X[-1] + 1)
#    GyroscopeX.append(np.random.randint(-5, 1) * random.uniform(-1, 1))
#    GyroscopeY.append(np.random.randint(-1, 10) * random.uniform(-1, 1))
#    GyroscopeZ.append(np.random.randint(-1, 5) * random.uniform(-1, 1))

    GyroscopeX.append(round( mpu.readGyroscopeMaster()[0] , 4))
    GyroscopeY.append(round( mpu.readGyroscopeMaster()[1] , 4))
    GyroscopeZ.append(round( mpu.readGyroscopeMaster()[2] , 4))

    minV = [min(GyroscopeX), min(GyroscopeY), min(GyroscopeZ)]
    maxV = [max(GyroscopeX), max(GyroscopeY), max(GyroscopeZ)]

#  Gyroscope X-axis
    GyroX = go.Scatter(
        x=list(time),
        y=list(GyroscopeX),
        name='X-Gyroscope',
        mode='lines',
        line={'color': '#A50EFF'},
    )
# Gyroscope Y-axis
    GyroY = go.Scatter(
        x=list(time),
        y=list(GyroscopeY),
        name='Y-Gyroscope',
        mode='lines',
        line={'color': '#FF2C00'},
    )
# Gyroscope Z-axis
    GyroZ = go.Scatter(
        x=list(time),
        y=list(GyroscopeZ),
        name='Z-Gyroscope',
        mode='lines',
        line={'color': '#FF0082'},
    )

    layout = go.Layout(
        plot_bgcolor=app_color['graph_bg'],
        paper_bgcolor=app_color['graph_bg'],
        font={'color': '#fff'},
        height=250,
        autosize=True,
        showlegend=False,
        xaxis=dict(
            range=[min(X) - 1.5, max(X) + 1.5],
            showline=True,
            zeroline=False,
            fixedrange=True,
            title='Time elapsed (sec)'
        ),
        yaxis=dict(
            range=[min(minV) - 1.5, max(maxV) + 1.5],
            showgrid=True,
            showline=True,
            fixedrange=True,
            zeroline=False,
            gridcolor=app_color['graph_line']
        ),
    )

    return {'data': [GyroX, GyroY, GyroZ], 'layout': layout}


#####################
# Graph container 3 #
#####################
@app.callback( Output('live-graph', 'figure'), [Input('graph-update', 'n_intervals')]
)
def update_graph_scatter(n):
    trace = dict(
        type='scatter',
        line={'color': '#42C4F7'},
        hoverinfo='skip',
        mode='lines',
        error_y={
            'type': 'data',
            'thickness': 1.5,
            'width': 2,
            'color': '#B4E8FC',
        },
    )

    layout = dict(
        plot_bgcolor=app_color['graph_bg'],
        paper_bgcolor=app_color['graph_bg'],
        font={'color': '#fff'},
        height=250,
        xaxis={
            'range': [-5, 5],
            'showline': True,
            'zeroline': False,
            'fixedrange': True,
            'title': 'X axis'
        },
        yaxis={
            'range': [-5, 5],
            'showgrid': True,
            'showline': True,
            'fixedrange': True,
            'zeroline': False,
            'gridcolor': app_color["graph_line"],
        },
    )

    return dict(data=[trace], layout=layout)


if __name__ == '__main__':
    app.run_server(host='192.168.10.37', debug=True)
