'''
Routines to handle a directory containing M3U play lists.
'''
from os import listdir
import os
from flask import flash


def get_playlists(directory):
    '''
    Get all M3U files in a directory.
    '''
    files = listdir(directory)
    playlists = list()
    for file in files:
        root, ext = os.path.splitext(file)
        # If it's an M3U file
        if ext.upper() == '.M3U':
            playlists.append(os.path.basename(root))
    return(playlists)


def add_playlist(directory, name):
    '''
    Add an empty M3U file to a directory.
    '''
    filename = os.path.join(directory, name + '.m3u')
    try:
        open(filename, 'a').close()
    except IOError as exception:
        flash(exception.strerror, 'error')
        return(False)
    return(True)


def remove_playlist(directory, name):
    '''
    Remove an M3U file from a directory.
    '''
    filename = os.path.join(directory, name + '.m3u')
    try:
        os.remove(filename)
    except IOError as exception:
        flash(exception.strerror, 'error')
        return(False)
    return(True)
