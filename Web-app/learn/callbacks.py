import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import pandas as pd
import base64
# 1st Lecture
'''
app = dash.Dash()
app.layout = html.Div([
            dcc.Input(id='my-id', value='Initial Text', type='text'),
            html.Div(id='my-div')
])

@app.callback(Output(component_id='my-div', component_property='children'),
            [Input(component_id='my-id', component_property='value')])
def update_output_div(input_value):
    return f'You entered: {input_value}'

if __name__ == '__main__':
    app.run_server()
'''


# 2nd lecture
'''
df = pd.read_csv('Data/gapminderDataFiveYear.csv')

app = dash.Dash()

year_options = []
for year in df['year'].unique():
    year_options.append({'label':str(year), 'value':year})

app.layout = html.Div([
            dcc.Graph(id='graph'),
            dcc.Dropdown(id='year-picker', options=year_options,
                        value=df['year'].min())
])

@app.callback(Output('graph', 'figure'),
            [Input('year-picker', 'value')])
def update_figure(selected_year):
    # DATA ONLY FOR SELECTED YEAR FROM DROPDOWN MENU
    filtered_df = df[df['year']== selected_year]

    traces = []
    for continent_name in filtered_df['continent'].unique():
        df_by_continent = filtered_df[filtered_df['continent']==continent_name]
        traces.append(go.Scatter(
            x = df_by_continent['gdpPercap'],
            y = df_by_continent['lifeExp'],
            mode ='markers',
            opacity =0.7,
            marker = {'size':15},
            name = continent_name
        ))
    return {'data':traces,
            'layout':go.Layout(title='My Plot',
                                xaxis={'title':'GDP Per Cap', 'type':'log'},
                                yaxis={'title':'Life Expectancy'})}

if __name__ == '__main__':
    app.run_server()
'''

'''
# 3rd Lecture - Multiple Inputs
df = pd.read_csv('Data/mpg.csv')

app = dash.Dash()

# ['mpg, 'hp', ...]
features = df.columns

app.layout = html.Div([
            html.Div([
                dcc.Dropdown(id='xaxis',
                            options=[{'label':i, 'value':i} for i in features],
                            value='displacement')
            ], style={'width':'48%', 'display':'inline-block'}),
            html.Div([
                dcc.Dropdown(id='yaxis',
                            options=[{'label':i, 'value':i} for i in features],
                            value='mpg')
            ],style={'width':'48%', 'display':'inline-block'}),
            dcc.Graph(id='feature-graphic')
], style={'padding':10})

@app.callback(Output('feature-graphic', 'figure'),
            [Input('xaxis', 'value'),
            Input('yaxis', 'value')])
def update_graph(xaxis_name, yaxis_name):
    return {'data':[go.Scatter(x=df[xaxis_name],
                            y=df[yaxis_name],
                                text=df['name'],
                                mode='markers',
                                marker={'size':15,
                                        'opacity':.5,
                                        'line':{'width':.5, 'color':'white'}})
                                ]



    ,'layout':go.Layout(title='My Dashboard for MPG',
                        xaxis={'title':xaxis_name},
                        yaxis={'title':yaxis_name},
                        hovermode='closest')
                        }

if __name__ == '__main__':
    app.run_server()
'''

'''
# 4th Lecture - Multiple Outputs
df = pd.read_csv('Data/wheels.csv')

app = dash.Dash()

def encode_image(image_file):
    encoded = base64.b64encode(open(image_file, 'rb').read())
    return 'data:image/png;base64,{}'.format(encoded.decode())


app.layout = html-Div([
            dcc.RadioItems(id='wheels',
                            options = [{'label':i, 'value':i} for i in df['wheels'].unique()],
                            value=1
                            ),
            html.Div(id='wheels-output'),
            html.Hr(),
            dcc.RadioItems(id='colors',
                            options = [{'label':i, 'value':i} for i in df['color'].unique()],
                            value='blue'
                            ),
            html.Div(id='colors-output'),
            html.Img(id='display-image', src='children', height=300)
], style={'fontFamily':'helvetica', 'fontsize':18})

@app.callback(Output('wheels-output','children'),
            [Input('wheels','value')])
def callback_a(wheels_value):
    return f'You hose {wheels_value}'

@app.callback(Output('colors-output','children'),
            [Input('colors','value')])
def callback_b(colors_value):
    return f'You chose {colors_value}'

@app.callback(Output('display-image', 'src'),
            [Input('wheels','value'),
            Input('colors','value')])
def callback_image(wheel, color):
    path = '/Data/images'
    return encode_image(path+path+df[(df['wheels']==wheel) & (df['color']==color)]['image'].values[0])


if __name__ == '__main__':
    app.run_server()
'''

# Controlling Callbacks with Dash State
app = dash.Dash()
app.layout = html.Div([
            dcc.Input(id='number-in', value=1, style={'fontSize':24}),
            html.Button(id='submit-button',
                        n_clicks=0,
                        children='Submit Here',
                        style={'fontSize':24}),
            html.H1(id='number-out')
])

@app.callback(Output('number-out','children'),
                [Input('submit-button','n_clicks')],
                [State('number-in','value')])
def output(n_clicks, number):
    return '{} was typed in, and button was clicked {} times.'.format(number, n_clicks)


if __name__ == '__main__':
    app.run_server()
