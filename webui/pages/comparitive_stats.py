import dash_html_components as html
import dash_core_components as dcc
from webui.webapp import app
from dash.dependencies import Output, Input, State
from webui import data_pull as dp
import plotly.graph_objs as go
import dash_daq as daq
import json

comparison_page = html.Div([

    html.H3("Select a Clan, Players and the Metrics You want to Plot",
            style={'text-align': 'center',
                   'display': 'inline-block'}),
    dcc.Dropdown(
        id='clan-name',
        placeholder="Select a Clan",
        value='#YUPCJJCR',
        options=dp.get_clan_dropdown_list(),
        style={ 'width': '49%',
                'display': 'block'},
    ),
    html.Div([
        dcc.Dropdown(
            id='player-name',
            placeholder="Select a player to plot",
            options=dp.get_clan_player_dropdown_list(),
            disabled=True,
            multi=True)
    ]),
    dcc.Dropdown(
        id='metric-name',
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
        style={'width': '49%',
                'display': 'block'},
    ),
    html.Br(),
    html.Div([
        daq.BooleanSwitch(
            id='hover-switch',
            label='Hover(On/Off)',
            on=True,
            style={'display': 'flex'}
        ),
        html.Br(),
        dcc.RadioItems(
            id='data-type',
            options=[
                {'label': 'Relative', 'value': 'relative'},
                {'label': 'Absolute', 'value': 'absolute'},
            ],
            value='relative',
            style={'display': 'flex'}
        ),
        html.Br(),

    ], style={'display': 'inline-block'}),
    html.Br(),
    html.Div(id='error-codes',
             style={'color':'red',
                    'font': '16px'}),
    html.Br(),
    html.Div([html.Button('Plot', id='graph-button'),
              # html.Button('Button', id='button-2')
              ],
             style={'display': 'inline'}
             ),
    dcc.Graph(id='comparison-graph'),
    html.Br(),
    html.Div([
        html.Hr(),
        dcc.Link('Back To Index',
                 href='/index',
                 className='NavLinks',
                 style={
                     'width': '49%',
                     'display': 'block'},
                 ),
        html.Br(),
        dcc.Link('Individual Members',
                 href='/member_analytics',
                 className='NavLinks',
                 style={
                     'width': '49%',
                     'display': 'block'},
                 )
    ]),
    html.Div(id='previous-player-name',
             children=None,
             hidden=True)
], className='container')


def get_player_go_dict(player_tag, **kwargs):

    metric = kwargs.get('metric')
    data_type=kwargs.get('data_type')

    hover = kwargs.get('hover')
    hover = 'all' if hover else 'skip'

    if data_type == 'relative':
        df = dp.player_limited_history_start(player_tag, metric=metric, start_time=None, end_time=None)
    else:
        df = dp.get_player_history_df(player_tag, metric=metric)

    player_name = dp.get_player_name(player_tag)

    trace = go.Scatter(
        x=df['created_time'],
        y=df[metric],
        mode='lines',
        name=player_name,
        hoverinfo=hover)

    return trace


# These 3 work for for the player-name dropdown
@app.callback(Output('player-name', 'options'),
              [Input('clan-name', 'value')])
def get_clan_player_list(clan_tag):
    player_options = dp.get_clan_player_dropdown_list(clan_tag)

    print(player_options)

    return player_options


@app.callback(Output('player-name', 'disabled'),
              [Input('clan-name', 'value')])
def enable_metric_list(clan_tag):
    if clan_tag:
        return False

@app.callback(Output('previous-player-name', 'children'),
              [Input('player-name', 'value')])
def store_player_names(player_tag):
    if player_tag:
        return player_tag

@app.callback(Output('player-name', 'value'),
              [Input('clan-name', 'value')],
              [State('previous-player-name', 'children')])
def retain_previous_player_name(clan_tag, player_name):

    if clan_tag and player_name:
        return player_name


@app.callback(
 Output('comparison-graph', 'figure'),
 [Input('graph-button', 'n_clicks')],
 [State('player-name', 'value'),
  State('metric-name', 'value'),
  State('hover-switch', 'on'),
  State('data-type', 'value')])
def update_graph(clicks, member_values, metric_name, hover_switch, data_type):

    if clicks and member_values and metric_name:

        all_traces = []
        for member in member_values:
            trace = get_player_go_dict(member, metric=metric_name, hover=hover_switch, data_type=data_type)
            all_traces.append(trace)

        return {'data': all_traces}
    else:
        return {}

@app.callback(
    Output('error-codes', 'children'),
    [Input('graph-button', 'n_clicks')],
    [State('player-name', 'value'),
     State('metric-name', 'value'),
     State('hover-switch', 'on'),
     State('data-type', 'value')])
def update_graph(clicks, member_values, metric_name, hover_switch, data_type):

    if not member_values and clicks:
        return "Select Atleast One Player "