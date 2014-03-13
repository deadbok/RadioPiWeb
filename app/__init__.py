from flask import Flask

VERSION = '0.2'

app = Flask(__name__)
app.config.from_object('config')
app.secret_key = 'RadioPiWeb'

from app.views import home
from app.views import stations
