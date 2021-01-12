import dash
import dash_html_components as html
import dash_core_components as dcc
# HTML Components
app = dash.Dash()

app.layout = html.Div(['This is the outermost div!',
                        html.Div('This is an inner div!',
                            style={'color':'red', 'border':'2px red solid'}),
                        html.Div(['Another inner div!'],
                            style={'color':'blue', 'border':'3px blue solid'})],
                    style={'color':'green', 'border':'2px green solid'})


if __name__ == '__main__':
    app.run_server()


# Dash core Components
'''
markdown_text = ''
### Dash and Markwon oh yeahh
Dash apps can be written in Markdown.
Dash uses the [CommonMark](http://commomnmark.org/) specification of Markdown. And blah blah blah...
[x]First
[x]Second
[o]Third

app = dash.Dash()

app.layout = html.Div([

            html.Label('Dropdown'),
            dcc.Dropdown(options=[{'label':'New York City',
                                    'value':'NYC'},
                                    {'label':'San Francisco',
                                    'value':'SF'}],
                        value='SF'),
            html.Label('Slider'),
            dcc.Slider(min=-10, max=10, step=0.5, value=0,
                        marks={i: i for i in range(-10, 10)}),
            html.P(html.Label('Some Radio Items')),
            dcc.RadioItems(options=[{'label':'New York City',
                                    'value':'NYC'},
                                    {'label':'San Francisco',
                                    'value':'SF'}],
                            value='SF'),
            html.P(dcc.Markdown(children=markdown_text))
])


if __name__ == '__main__':
    app.run_server()
'''
