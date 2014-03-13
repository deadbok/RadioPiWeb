'''
Created on 11/03/2014

@author: oblivion
'''
from config import PLAYLIST_DIR
from flask import render_template, request, redirect, url_for, flash
from os.path import basename
from app import app
from app.util.playlists import get_playlists, add_playlist, remove_playlist


@app.route('/stations')
def station_lists():
    playlists = get_playlists(PLAYLIST_DIR)
    return render_template('stations.html',
                           playlists=playlists,
                           selected='')


@app.route('/stations/<playlist>')
def station_list_selected(playlist):
    playlists = get_playlists(PLAYLIST_DIR)
    return render_template('stations.html',
                           playlists=playlists,
                           selected=playlist,
                           path=playlist)


@app.route('/add_station_list', methods=['POST', 'GET'])
def add_station_list():
    if request.method == 'POST':
        # Get the name from the form and process it to strip unwanted
        # naughtiness
        name = basename(request.form['name'])
        if name == '':
            flash('You must input a name', 'error')
        else:
            if add_playlist(PLAYLIST_DIR, name):
                flash('Added "' + name + '"', 'info')
            else:
                flash('Could not add "' + name + '"', 'error')
        return redirect(url_for('station_lists'))
    # Return the form if this is a GET request
    return render_template('add.html')


@app.route('/edit_station_list/<playlist>')
def edit_station_list(playlist):
    pass


@app.route('/del_station_list/<playlist>')
def del_station_list(playlist):
    if remove_playlist(PLAYLIST_DIR, playlist):
        flash('Removed "' + playlist + '"', 'info')
    else:
        flash('Could not remove "' + playlist + '"', 'error')
    return redirect(url_for('station_lists'))
