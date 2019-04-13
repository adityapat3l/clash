import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

import flask
import pandas as pd
import time
import os

from webui import data_pull as dp
from clashapp import flaskapp as server

# server.secret_key = os.environ.get('secret_key', 'secret')


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/hello-world-stock.csv')

app = dash.Dash('app', server=server, external_stylesheets=external_stylesheets)

app.scripts.config.serve_locally = False
# dcc._js_dist[0]['external_url'] = 'https://cdn.plot.ly/plotly-basic-latest.min.js'

# colors = {
#     'background': '#111111',
#     'text': '#7FDBFF'
# }

app.layout = html.Div([

    html.H1('Player Stats'),

    html.Div(children=[
        html.H1(
            children='For Aiur: Member Statistics',
            style={
                'textAlign': 'center',
            }
        )]),

        html.Div(children='Graphs for every measurable stat in the game', style={
            'textAlign': 'center',
        }),

    dcc.Dropdown(
        id='metric_name',
        options=[
            {'label': 'Trophy Level', 'value': 'current_trophies'},
            {'label': 'Gold Looted', 'value': 'achv_gold_looted'},
            {'label': 'Elixer Looted', 'value': 'achv_elixer_looted'},
            {'label': 'Dark Looted', 'value': 'achv_dark_looted'},
            {'label': 'Donations Given (This Season)', 'value': 'donations_given'},
            {'label': 'Donations Received (This Season)', 'value': 'donations_received'},
            {'label': 'Attack Wins', 'value': 'attack_wins'},
            {'label': 'Defense Wins', 'value': 'defense_wins'},
            {'label': 'War Stars', 'value': 'war_stars'},
            {'label': 'King Level', 'value': 'king_level'},
            {'label': 'Queen Level', 'value': 'queen_level'},
            {'label': 'Warden Level', 'value': 'warden_level'},
        ],
        clearable=False,
        placeholder="Select a metric",
    ),

    dcc.Dropdown(
        id='player_name',
        options=dp.get_clan_player_dropdown_list(),
        placeholder="Select a player to plot",
    ),
    dcc.Graph(id='my-graph'),

    # China Graph
    dcc.Graph(
        figure=go.Figure(
            data=[
                go.Bar(
                    x=[1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003,
                       2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012],
                    y=[219, 146, 112, 127, 124, 180, 236, 207, 236, 263,
                       350, 430, 474, 526, 488, 537, 500, 439],
                    name='Rest of world',
                    marker=go.bar.Marker(
                        color='rgb(55, 83, 109)'
                    )
                ),
                go.Bar(
                    x=[1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003,
                       2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012],
                    y=[16, 13, 10, 11, 28, 37, 43, 55, 56, 88, 105, 156, 270,
                       299, 340, 403, 549, 499],
                    name='China',
                    marker=go.bar.Marker(
                        color='rgb(26, 118, 255)'
                    )
                )
            ],
            layout=go.Layout(
                title='US Export of Plastic Scrap',
                showlegend=True,
                legend=go.layout.Legend(
                    x=0,
                    y=1.0
                ),
                margin=go.layout.Margin(l=40, r=0, t=40, b=30)
            )
        ),
        style={'height': 300},
        id='my-graph_1'
    )


], className="container")

@server.route('/')
@app.callback(Output('my-graph', 'figure'),
              [Input('player_name', 'value'),
               Input('metric_name', 'value')])

def update_graph(player_tag, metric_name):

    if not player_tag or not metric_name:
        return {}

    dff = dp.get_player_history_df(player_tag, metric=metric_name)

    return {
        'data': [{
            'x': dff[metric_name],
            'y': dff.created_time,
            'line': {
                'width': 3,
                'shape': 'spline'
            }
        }]
    }

# @app.callback(
#     Output(component_id='my-div', component_property='children'),
#     [Input(component_id='my-id', component_property='value')]
# )
# def update_output_div(input_value):
#     return 'You\'ve entered "{}"'.format(input_value)

if __name__ == '__main__':
    app.run_server(debug=True)