'''
Configuration for RadioPi web interface.
'''
import os


basedir = os.path.abspath(os.path.dirname(__file__))

# PLAYLIST_DIR should point to a directory containing M3U files.
PLAYLIST_DIR = '/var/lib/mpd/playlists'
