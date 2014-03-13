'''
Created on 11/03/2014

@author: oblivion
'''
from config import PLAYLIST_DIR
from flask import render_template, request, redirect, url_for, flash
import os.path
from app import app
from app.util.playlists import get_playlists, add_playlist, remove_playlist
from app.util.pym3u import PyM3U


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
                           selected=playlist)


@app.route('/add_station_list', methods=['POST', 'GET'])
def add_station_list():
    if request.method == 'POST':
        # Get the name from the form and process it to strip unwanted
        # naughtiness
        name = os.path.basename(request.form['name'])
        if name == '':
            flash('You must input a name', 'error')
        else:
            if add_playlist(PLAYLIST_DIR, name):
                flash('Added "' + name + '"', 'info')
            else:
                flash('Could not add "' + name + '"', 'error')
        return redirect(url_for('station_lists'))
    # Return the form if this is a GET request
    return render_template('addlist.html')


@app.route('/edit_station_list/<playlist>')
def edit_station_list(playlist):
    filename = os.path.join(PLAYLIST_DIR, playlist + '.m3u')
    m3u = PyM3U(filename)
    return render_template('playlist.html',
                           playlist=playlist,
                           m3u=m3u.playlist,
                           selected='')


@app.route('/edit_station_list/<playlist>/<station>')
def edit_station_list_selected(playlist, station):
    filename = os.path.join(PLAYLIST_DIR, playlist + '.m3u')
    m3u = PyM3U(filename)
    return render_template('playlist.html',
                           playlist=playlist,
                           m3u=m3u.playlist,
                           selected=station)


@app.route('/del_station_list/<playlist>')
def del_station_list(playlist):
    if remove_playlist(PLAYLIST_DIR, playlist):
        flash('Removed "' + playlist + '"', 'info')
    else:
        flash('Could not remove "' + playlist + '"', 'error')
    return redirect(url_for('station_lists'))


@app.route('/add_station/<playlist>', methods=['GET', 'POST'])
def add_station(playlist):
    if request.method == 'POST':
        # Get the name from the form and process it to strip unwanted
        # naughtiness
        title = request.form['title']
        location = request.form['url']
        if title == '':
            flash('You must input a title', 'error')
        elif location == '':
            flash('You must input a URL', 'error')
        else:
            filename = os.path.join(PLAYLIST_DIR, playlist + '.m3u')
            m3u = PyM3U(filename)
            m3u.add(title, -1, location)
            m3u.write()
            flash('Added "' + title + '"', 'info')
        return redirect(url_for('edit_station_list', playlist=playlist))
    # Return the form if this is a GET request
    return render_template('station.html',
                           playlist=playlist)


@app.route('/edit_station/<playlist>/<station>')
def edit_station(playlist, station):
    filename = os.path.join(PLAYLIST_DIR, playlist + '.m3u')
    m3u = PyM3U(filename)
    return render_template('station.html',
                           playlist=playlist)


@app.route('/del_station/<playlist>/<station>')
def del_station(playlist, station):
    filename = os.path.join(PLAYLIST_DIR, playlist + '.m3u')
    m3u = PyM3U(filename)
    return render_template('playlist.html',
                           playlist=playlist,
                           m3u=m3u.playlist,
                           selected=station)
