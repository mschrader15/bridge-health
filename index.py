import dash_bootstrap_components as dbc
import dash
import pathlib
import os

# app.config.suppress_callback_exceptions = True
APP_PATH = str(pathlib.Path(__file__).parent.resolve())


class Paths(object):
    BRIDGE_EXCEL = os.path.join(APP_PATH, 'setup_data', 'bridges.xlsx')


class Config(object):
    SERVER_NAME = 'tcp:hanson-bridge-monitor.database.windows.net'
    DATABASE_NAME = 'Hanson-Bridge-Monitor'
    DATABASE_USERNAME = 'mcschrader'
    DATABASE_PASSWORD = 'br1dge-health'
    MAPBOX_KEY = "pk.eyJ1IjoibWF4LXNjaHJhZGVyIiwiYSI6ImNrOHQxZ2s3bDAwdXQzbG81NjZpZm96bDEifQ.etUi4OK4ozzaP_P8foZn_A"
    OPENWEATHER_KEY = "f0ba75a422b9742251ae12ae17c0e027"

    # CSRF_ENABLED = True
    # SECRET_KEY = os.environ.get('SECRET_KEY') or "77tgFCdrEEdv77554##@3"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(APP_PATH, 'db', 'database.db')

    STATUS_COLOR_DICT = {'Ok': 'green', 'Monitor': 'yellow', 'Alert': 'red'}
    PLOT_COLORS = ["#849E68", "#59C3C3", "#F9ADA0"]
    PLOT_LAYOUT = dict(
        autosize=True,
        #automargin=True,
        margin=dict(l=30, r=30, b=20, t=40),
        hovermode="closest",
        plot_bgcolor="#F9F9F9",
        paper_bgcolor="#F9F9F9",
        legend=dict(font=dict(size=10), orientation="h"))
    # SQLALCHEMY_TRACK_MODIFICATIONS = False
    # LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    # MAIL_SERVER = os.environ.get('MAIL_SERVER')
    # MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    # MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    # MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    # MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    # ADMINS = [os.environ.get('ADMIN_EMAIL'), os.environ.get('ADMIN_PASSWORD')]
    # MS_TRANSLATOR_KEY = os.environ.get('MS_TRANSLATOR_KEY')
    # ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')
    # REDIS_URL = os.environ.get('REDIS_URL') or 'redis://'


config = Config()
paths = Paths()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', dbc.themes.BOOTSTRAP]
app = dash.Dash(__name__,  # external_stylesheets=external_stylesheets,
                meta_tags=[{"name": "viewport", "content": "width=device-width"}])
server = app.server
