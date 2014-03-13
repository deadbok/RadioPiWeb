'''
Routines to handle a directory containing M3U play lists.

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
from os import listdir
import os
from flask import flash
from app.util.pym3u import check_extended_header, create_empty


def get_playlists(directory):
    '''
    Get all M3U files in a directory.
    '''
    try:
        files = listdir(directory)
        playlists = list()
        for file in files:
            root, ext = os.path.splitext(file)
            # If it's an M3U file add it
            if ext.upper() == '.M3U':
                if check_extended_header(os.path.join(directory, file)):
                    playlists.append(os.path.basename(root))
    except EnvironmentError as exception:
        flash(exception.strerror, 'error')
        return(list())

    return(playlists)


def add_playlist(directory, name):
    '''
    Add an empty M3U file to a directory.
    '''
    filename = os.path.join(directory, name + '.m3u')
    return(create_empty(filename))


def remove_playlist(directory, name):
    '''
    Remove an M3U file from a directory.
    '''
    filename = os.path.join(directory, name + '.m3u')
    try:
        os.remove(filename)
    except EnvironmentError as exception:
        flash(exception.strerror, 'error')
        return(False)
    return(True)
