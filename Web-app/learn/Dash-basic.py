import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import numpy as np
import os
os.system('clear')

# Lecture 1
# Dash creates the Flask app for you
app = dash.Dash()

colors = {'background':'#111111', 'text':'#7FDBFF'}
colors['text']

app.layout = html.Div(children=[
            html.H1('Hello Dash!', style={'textAlign':'center',
                                            'color':colors['text']}),
            html.Div('Dash: Web Dashboards with Python'),
            dcc.Graph(id='example',
                    figure={'data':[
                    {'x':[1,2,3], 'y':[4,1,2],'type':'bar','name':'SF'},
                    {'x':[1,2,3], 'y':[2,4,5],'type':'bar','name':'NYC'}
                    ],
                            'layout':{
                            'plot_bgcolor':colors['background'],
                            'paper_bgcolor':colors['background'],
                            'font':{'color':colors['text']},
                            'title':'BAR PLOTS!'
                            }})
], style={'backgroundColor':colors['background']}
)
if __name__ == '__main__':
    app.run_server()


# 2nd lecture
app = dash.Dash()

# Creating DATA
np.random.seed(42)
random_x = np.random.randint(1,101,100)
random_y = np.random.randint(1,101,100)

app.layout = html.Div([dcc.Graph(id='scatterplot',
                        figure = {'data':[
                            go.Scatter(
                                x=random_x,
                                y=random_y,
                                mode='markers',
                                marker={
                                    'size':12,
                                    'color':'rgb(51,204,153)',
                                    'line':{'width':2}
                                }
                            )],
                        'layout':go.Layout(title='My Scatterplot',
                                            xaxis = {'title':'Some X title'})}
                        ),
                        dcc.Graph(id='scatterplot2',
                        figure = {'data':[
                            go.Scatter(
                                x=random_x,
                                y=random_y,
                                mode='markers',
                                marker={
                                    'size':12,
                                    'color':'rgb(200,204,53)',
                                    'line':{'width':2}
                                }
                            )],
                        'layout':go.Layout(title='Second plot',
                                            xaxis = {'title':'Some X title'})}
                        )
                        ])
if __name__ == '__main__':
    app.run_server()
