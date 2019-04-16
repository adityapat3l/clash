import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from webui.webapp import app
from webui.pages import member_stats, comparitive_stats
from webui.components import Header


# overview = html.Div([Header()])

index_page = html.Div(children=[
    html.H1(
        children='Welcome to clashboard',
        style={
            'textAlign': 'center',
             'color': 'darkblue',
            'background-color': 'lightyellow'
        }

    ),
    html.H4(children='Graphs for every available stat in the game',
             style={
            'textAlign': 'center',
             'font': '16px',
             'color': 'grey',
    }),
    html.Div([
    dcc.Link('Member Analytics', href='/member_analytics', className='NavLinks',
             style={
                 'textAlign': 'center',
                'width': '100%',
                'display': 'block'},
             ),
    html.Br(),
    dcc.Link('Comparison Between Members', href='/comparison', className='NavLinks',
             style={
                 'textAlign': 'center',
                 'width': '100%',
                 'display': 'block'},
             ),

    ])
    ], className='index_page')

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
    # html.Div([Header()])
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/member_analytics':
        return member_stats.member_page
    elif pathname == '/comparison':
        return comparitive_stats
    elif pathname == 'index':
        return index_page
    else:
        return index_page


if __name__ == '__main__':
    app.run_server(debug=True, port=5000)
