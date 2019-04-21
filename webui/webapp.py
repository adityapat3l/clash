import dash
from clashapp import flaskapp as server
from flask_celery import make_celery

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

celery = make_celery(server)
app = dash.Dash(__name__, server=server, external_stylesheets=external_stylesheets)

app.scripts.config.serve_locally = False
app.config.suppress_callback_exceptions = True