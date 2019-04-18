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
    html.Div([
        html.H2("Select a Chart Type: "),
        dcc.RadioItems(
            id='chart_type',
            options=[
                {'label': 'All History', 'value': 'history'},
                {'label': 'Set Start as 0', 'value': 'limited_start'},
            ],
            value="limited_start",
            style={'display': 'block'},
            className='ChartType'
        )]),
    html.Div([
        html.H2("Select a Metric and Player: "),
        dcc.Dropdown(
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
            # value="current_trophies",
            placeholder="Select a metric to plot",
            # style={'display': 'flex', 'width': '49%'},
            className='MetricType'
                        )]),
    html.Div([
        dcc.Dropdown(
            id='player_name',
            options=dp.get_clan_player_dropdown_list(),
            placeholder="Select a player to plot",
             ),
    ]),
    dcc.Graph(id='my-graph'
              ),


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
        dcc.Link('Comparison Between Members',
                 href='/comparison',
                 className='NavLinks',
                 style={
                     'width': '49%',
                     'display': 'block'},
                 )
              ])
    ], className="container")


@app.callback(Output('my-graph', 'figure'),
              [Input('chart_type', 'value'),
               Input('player_name', 'value'),
               Input('metric_name', 'value')])
def update_graph(chart_type, player_tag, metric_name):

    if not player_tag or not metric_name:
        return {}

    if chart_type == 'history':
        dff = dp.get_player_history_df(player_tag, metric=metric_name)
    else:
        dff = dp.player_limited_history_start(player_tag, metric=metric_name)

    return {
        'data': [{
            'y': dff[metric_name],
            'x': dff.created_time,
            'mode': 'lines',
            'marker': {'size': 12},
            'line': {
                'width': 3,
                'shape': 'spline',
            }
        }]
    }
