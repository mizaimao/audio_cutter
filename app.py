#!/usr/bin/env python3
import os
from textwrap import dedent

import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
import time
import plotly.graph_objs as go
import plotly.figure_factory as ff
from PIL import ImageColor
from dash.dependencies import Input, Output, State

import video_engine as rpd
#from utils.coco_colors import STANDARD_COLORS
import utils.dash_reusable_components as drc

import cutter

DEBUG = True
FRAMERATE = 24.0
WAIT = 3
INSTRUCTION = '''#### Instructions:
 Input a time interval below, followed by a quote in the next line.  
 **Example Input:**    
 01:30-01:34  
 For instance, what is r?  
 **Note: Only two-line inputs are supported currently.**  
'''

record_path = 'data/export.csv'
global df
cell_style=[
    {'if': {'column_id': 'Index'},
        'width': '4%', 'textAlign': 'left'},
    {'if': {'column_id': 'Quotes'},
        'width': '66%', 'textAlign': 'left'},
    {'if': {'column_id': 'Time'},
        'width': '10%'},
    {'if': {'column_id': 'Length'},
        'width': '5%'},
    {'if': {'column_id': 'Submission'},
        'width': '10%'},
    {'if': {'column_id': 'Download'},
        'width': '0%'},
    {'if': {'column_id': 'Source'},
        'width': '5%'},
    ]
CSSSTYLE=[{'selector': '.dash-cell div.dash-cell-value',
        'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'}]

df=pd.read_csv(record_path,sep='\t')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server


# Custom Script for Heroku
if 'DYNO' in os.environ:
    app.scripts.config.serve_locally = False
    app.scripts.append_script({
        'external_url': 'https://cdn.rawgit.com/chriddyp/ca0d8f02a1659981a0ea7f013a378bbd/raw/e79f3f789517deec58f41251f7dbb6bee72c44ab/plotly_ga.js'
    })

app.title = 'R'
app.scripts.config.serve_locally = True
app.config['suppress_callback_exceptions'] = True


def load_data(path):
    data_dict = {
        "root_round": root_round
    }

    if DEBUG:
        print(f'{path} loaded.')
    return data_dict


# Main App
app.layout = html.Div([
    # Banner display
    html.Div([
        html.H2(
            'I want to ask how many people once used R? (Pre-Release)',
            id='title'
        ),
        html.Img(src='http://140.82.4.17/R.gif', style={'width' : '75px','height':'75px'}),
        #html.Img(src="https://www.r-project.org/Rlogo.png",style={'width' : '60px','height':'60px'})
    ],
        className="banner",
    ),

    # Body
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    rpd.my_Player()
                ],
                    id='div-video-player',
                    style={
                        'color': 'rgb(255, 255, 255)',
                        'margin-bottom': '-30px'
                    }
                ),
                html.Div([
                    "Footage Selection:",
                    dcc.Dropdown(
                        options=[
                            {'label': 'Hua Liang: An introduction to R (2012 CBIM Summer School)', 'value': '2012'},
                            {'label': 'Generalized Additive Partial Linear Models with High-dimensional Covariates', 'value': '2011'},
                        ],
                        value='2012',
                        id="dropdown-footage-selection",
                        clearable=False
                    )
                ],),
                html.Div([
                    dcc.Markdown(INSTRUCTION),
                    dcc.Textarea(
                        id='quotearea',
                        placeholder='Enter text...',
                        value='',
                        style={'width': '95%'}
                    ),
                    html.Button('Submit', id='button'),
                    html.Div(id='output-container-button',
                            children='Enter a time interval, and a quote then press submit')
                ],
                    style={'margin': '30px 20px 15px 20px'}  # top right bottom left
                ),
                ],
                className="six columns",
                style={'margin-bottom': '20px'}
            ),
            html.Div([ # Right part of the page
                html.Div(
                    id='html_table',
                    children=dash_table.DataTable(
                        id='record_table',
                        css=CSSSTYLE,
                        columns=[{"name": i, "id": i, 'hidden': True if i == 'Download' else False} for i in df.columns],
                        data=df.to_dict("rows"),
                        style_cell_conditional=cell_style,style_table={'overflowX': 'scroll'},
                    ),
                    style={
                        'margin_top': '60px',
                        'margin_left': '60px',
                    }
                ),
                html.Div([ # Right lower Downloading
                    html.Div(dcc.Markdown('### Download Options') ),
                    html.Div(
                        dcc.Dropdown(
                            id='dl-dropdown',
                            options=[
                            {'label': x, 'value': x} for x in df['Index']
                            ],
                            #multi=True,
                            #searchable=False,
                            placeholder="Select an index to download",
                            value='1'
                        ),
                        style={'width': '70%', 'height':'120%', 'horizontal-align': 'middle',
                            }#'margin': '10px 100px 100px 300px'}  # top right bottom left
                    ),
                    html.P('', id='preview'),
                    html.A('Download', style={'fontSize': '30'} , id='download-link', download="", href="", target="_blank")
                ],
                style={'width': '70%','display': 'inline-block','vertical-align': 'middle', 'horizontal-align': 'middle',
                'margin': '50px 100px 10px 200px'
                    },
                className='row'
                ),
                ],
                className="six columns",
                style={'margin-bottom': '20px'}
            ),
        ],
            className="row"
        ),
    ],
        className="container scalable"
    )
])


# Data Loading
@app.server.before_first_request
def load_all_footage():
    global data_dict, url_dict
    # Load the dictionary containing all the variables needed for analysis
    url_dict = {
        '2012': 'https://www.youtube.com/watch?v=rd6qNEjJfps&t=564s',
        '2011': 'https://www.youtube.com/watch?v=xeU5gl3w-OE',
    }
    df = pd.read_csv(record_path,sep='\t')

# Footage Selection
@app.callback(Output("div-video-player", "children"),
              [Input('dropdown-footage-selection', 'value'),
               ])
def select_footage(footage):
    url = url_dict[footage]  # Find desired footage
    return [
        rpd.my_Player(id='video-display', url=url, width='100%', height='50vh', controls=True, playing=False, seekTo=0, volume=1)
    ]


# Submission
@app.callback(
    dash.dependencies.Output('output-container-button', 'children'),
    [],
    [dash.dependencies.State('quotearea', 'value'),
    dash.dependencies.State('dropdown-footage-selection','value')],
    [dash.dependencies.Event('button', 'click')])
def update_output(quote, video_input):
    result = 'Invalid input'
    quote = quote.split('\n')
    if len(quote) != 2:
        return result 
    timeinput = quote[0]
    quoteinput = quote[1]

    print(quoteinput,timeinput, video_input)
    result = cutter.cutter(video_input, timeinput, quoteinput)
    return result

# Update table
@app.callback(
    dash.dependencies.Output('html_table', 'children'),
    [],[],
    [dash.dependencies.Event('button', 'click')])
def update_table():
    time.sleep(WAIT)
    global df
    df = pd.read_csv(record_path,sep='\t') 
    return dash_table.DataTable(css=CSSSTYLE,columns=[{"name": i, "id": i, 
        'hidden': True if i == 'Download' else False,
        'align': 'left' if i == 'Quotes' else 'right',
        } for i in df.columns],style_table={'overflowX': 'scroll'},
            data=df.to_dict("rows"),style_cell_conditional=cell_style)


# Update Download
@app.callback(
    dash.dependencies.Output('dl-dropdown', 'options'),
    [],[],
    [dash.dependencies.Event('button', 'click')])
def update_table():
    time.sleep(WAIT+1)
    return [{'label': x, 'value': x} for x in df['Index']]

# Download
@app.callback(
    dash.dependencies.Output('download-link', 'href'),
    [dash.dependencies.Input('dl-dropdown', 'value')])
def update_download_link(audio_index):
    return df.iloc[int(audio_index)-1]['Download']

@app.callback(
    dash.dependencies.Output('preview', 'children'),
    [dash.dependencies.Input('dl-dropdown', 'value')])
def update_download_link(audio_index):
    return df.iloc[int(audio_index)-1]['Quotes']

external_css = [
    "https://cdnjs.cloudflare.com/ajax/libs/normalize/7.0.0/normalize.min.css",  # Normalize the CSS
    "https://fonts.googleapis.com/css?family=Open+Sans|Roboto"  # Fonts
    "https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css",
    "https://cdn.rawgit.com/xhlulu/9a6e89f418ee40d02b637a429a876aa9/raw/base-styles.css",
    "https://cdn.rawgit.com/plotly/dash-object-detection/875fdd6b/custom-styles.css",
    "https://codepen.io/chriddyp/pen/bWLwgP.css",
    "https://codepen.io/chriddyp/pen/brPBPO.css"
    ]
for css in external_css:
    app.css.append_css({"external_url": css})


# Running the server
if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0', port=22222)
