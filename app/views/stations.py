'''
Everything dealing with stations.

Copyright 2014 Martin Grønholdt

This file is part of RadioPiWeb.

RadioPiWeb is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

RadioPiWeb is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with RadioPiWeb.  If not, see <http://www.gnu.org/licenses/>.
'''
from config import PLAYLIST_DIR
from flask import render_template, request, redirect, url_for, flash
import os.path
from app import app
from app.util.playlists import get_playlists, add_playlist, remove_playlist
from app.util.pym3u import PyM3U


def playlist_filename(playlist):
    '''
    Utility function to get the absolute path of a play list.
    '''
    return(os.path.join(PLAYLIST_DIR, playlist + '.m3u'))


@app.route('/stations')
def station_lists():
    # Get all play lists
    playlists = get_playlists(PLAYLIST_DIR)
    return render_template('stations.html',
                           playlists=playlists,
                           selected='')


@app.route('/stations/<playlist>')
def station_list_selected(playlist):
    # Get all play lists
    playlists = get_playlists(PLAYLIST_DIR)
    return render_template('stations.html',
                           playlists=playlists,
                           selected=playlist)


@app.route('/add_station_list', methods=['POST', 'GET'])
def add_station_list():
    # If data is posted
    if request.method == 'POST':
        # Get the name from the form and process it to strip unwanted
        # naughtiness
        name = os.path.basename(request.form['name'])
        if name == '':
            flash('You must input a name', 'error')
        else:
            # Try to add the new play list
            if add_playlist(PLAYLIST_DIR, name):
                flash('Added "' + name + '"', 'info')
            else:
                flash('Could not add "' + name + '"', 'error')
        # Redirect to station lists list
        return redirect(url_for('station_lists'))
    # Return the form if this is a GET request
    return render_template('addlist.html')


@app.route('/edit_station_list/<playlist>')
def edit_station_list(playlist):
    filename = playlist_filename(playlist)
    # Read the play list
    m3u = PyM3U(filename)
    return render_template('playlist.html',
                           playlist=playlist,
                           m3u=m3u.playlist,
                           selected='')


@app.route('/edit_station_list/<playlist>/<station>')
def edit_station_list_selected(playlist, station):
    filename = playlist_filename(playlist)
    # Read the play list
    m3u = PyM3U(filename)
    return render_template('playlist.html',
                           playlist=playlist,
                           m3u=m3u.playlist,
                           selected=station)


@app.route('/del_station_list/<playlist>')
def del_station_list(playlist):
    # Try to remove the play list
    if remove_playlist(PLAYLIST_DIR, playlist):
        flash('Removed "' + playlist + '"', 'info')
    else:
        flash('Could not remove "' + playlist + '"', 'error')
    return redirect(url_for('station_lists'))


def get_station_data(request):
    '''
    Get the data from the station form and validate them.
    '''
    title = request.form['title']
    location = request.form['url']
    # Check the data
    if title == '':
        flash('You must input a title', 'error')
        return(None, None)
    elif location == '':
        flash('You must input a URL', 'error')
        return(None, None)
    # Return the data if everything checks out.
    return(title, location)


@app.route('/add_station/<playlist>', methods=['GET', 'POST'])
def add_station(playlist):
    # If data is posted
    if request.method == 'POST':
        # Get the data from the form
        title, location = get_station_data(request)
        if not title == None:
            # Everything checks out
            filename = playlist_filename(playlist)
            # Open the play list
            m3u = PyM3U(filename)
            # Add the item
            m3u.add(title, -1, location)
            # Save the play list
            m3u.write()
            flash('Added "' + title + '"', 'info')
        # Redirect to the station list
        return redirect(url_for('edit_station_list', playlist=playlist))
    # Return the form if this is a GET request
    return render_template('station.html',
                           playlist=playlist,
                           action=url_for('add_station', playlist=playlist))


@app.route('/edit_station/<playlist>/<station>', methods=['GET', 'POST'])
def edit_station(playlist, station):
    filename = playlist_filename(playlist)
    # Open play list
    m3u = PyM3U(filename)
    # Get the index of the item
    index = m3u.get_index_by_title(station)
    # If it could not be found
    if index == None:
        flash('Something went wrong, try again.', 'error')
        return redirect(url_for('edit_station_list', playlist=playlist))
    # If data is posted
    if request.method == 'POST':
        # Get the data from the form
        title, location = get_station_data(request)
        if not title == None:
            # Modify the item
            m3u.playlist[index][title] = title
            m3u.playlist[index][location] = location
            # Save the playlist
            m3u.write()
            flash('Changed "' + title + '"', 'info')
        # Redirect to the station list
        return redirect(url_for('edit_station_list', playlist=playlist))
    # Return the form if this is a GET request
    return render_template('station.html',
                           playlist=playlist,
                           action=url_for('edit_station',
                                          playlist=playlist,
                                          station=station),
                           title_value=m3u.playlist[index]['title'],
                           location_value=m3u.playlist[index]['location'])


@app.route('/del_station/<playlist>/<station>')
def del_station(playlist, station):
    filename = playlist_filename(playlist)
    # Open play list
    m3u = PyM3U(filename)
    # Get the index of the item
    index = m3u.get_index_by_title(station)
    # If it could not be found
    if index == None:
        flash('Something went wrong, try again.', 'error')
        return redirect(url_for('edit_station_list', playlist=playlist))
    # Delete the item
    del m3u.playlist[index]
    # Save the file
    m3u.write()
    flash('Deleted "' + station + '"', 'info')
    # Redirect to the station list
    return redirect(url_for('edit_station_list', playlist=playlist))
