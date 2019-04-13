import dash_html_components as html
import dash_core_components as dcc
from webui.webapp import app
from dash.dependencies import Output, Input
from webui import data_pull as dp

member_page = html.Div([

    html.Div(children=[
        html.H1(
            children='For Aiur: Member Statistics',
            style={
                'textAlign': 'center',
            }
        )]),

    html.Div(children='Graphs for every measurable stat in the game', style={
        'textAlign': 'center'
    }),
    html.Div([
        dcc.RadioItems(
            id='metric_name',
            options=[
                {'label': 'Trophy Level', 'value': 'current_trophies'},
                {'label': 'Gold Looted', 'value': 'achv_gold_looted'},
                {'label': 'Elixer Looted', 'value': 'achv_elixer_looted'},
                {'label': 'Dark Looted', 'value': 'achv_dark_looted'},
                {'label': 'Donations Given', 'value': 'donations_given'},
                {'label': 'Donations Received', 'value': 'donations_received'},
                {'label': 'Attack Wins', 'value': 'attack_wins'},
                {'label': 'Defense Wins', 'value': 'defense_wins'},
                {'label': 'War Stars', 'value': 'war_stars'},
                {'label': 'King Level', 'value': 'king_level'},
                {'label': 'Queen Level', 'value': 'queen_level'},
                {'label': 'Warden Level', 'value': 'warden_level'}
            ],
            value="current_trophies",
            style={'display': 'flex'}
    )]),
    html.Div([
        dcc.Dropdown(
            id='player_name',
            options=dp.get_clan_player_dropdown_list(),
            placeholder="Select a player to plot",
             ),
    ]),
    dcc.Graph(id='my-graph'),

    html.Div([
        dcc.Link('Back To Index',
                    href='/index',
                    style={
                        'width': '49%'},
                    ),
        dcc.Link('Comparison Between Members',
                 href='/comparison',
                 style={
                     'width': '49%',
                     'display': 'block'},
                 )
              ])
    ], className="container")


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
