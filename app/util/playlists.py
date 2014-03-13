'''
Routines to handle a directory containing M3U play lists.
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
