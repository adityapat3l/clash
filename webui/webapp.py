import dash
from clashapp import flaskapp as server

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, server=server, external_stylesheets=external_stylesheets)

app.scripts.config.serve_locally = False
app.config.suppress_callback_exceptions = True