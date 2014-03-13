'''

@since 13/03/2014
@author: oblivion
'''
from flask import render_template
from app import app
from app import VERSION


@app.route('/')
def home():
    return render_template('home.html', version=VERSION)
