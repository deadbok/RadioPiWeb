'''
Read and write extended M3U play lists.

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
from flask import flash


def check_extended_header(filename):
    '''
    Check the header of an M3U file return true if it is an extended M3U file.
    '''
    try:
        with open(filename, 'r') as m3u_file:
            header = m3u_file.readline()
    except EnvironmentError as exception:
        flash(exception.strerror, 'error')
        return(False)

    if header.strip('\n') == PyM3U.header_tag:
        return(True)
    else:
        return(False)


def create_empty(filename):
    '''
    Create an empty extended M3U file.
    '''
    try:
        with open(filename, 'w') as m3u_file:
            m3u_file.write(PyM3U.header_tag + '\n')
    except EnvironmentError as exception:
        flash(exception.strerror, 'error')

    return(True)


class PyM3U(object):
    '''
    Class to handle M3U play lists
    '''
    filename = ''
    '''The filename.'''
    header_tag = '#EXTM3U'
    '''Header tag that identifies an extended M3U file.'''
    info_tag = '#EXTINF:'
    '''Tag to include extended information about a track.'''
    playlist = list()
    '''List of dictionaries for each M3U entry.'''
    def __init__(self, filename):
        '''
        Constructor.
        '''
        self.filename = filename
        self.read()

    def read(self):
        '''
        Read an M3U file. Put the data in a dictionary.

        'runtime' is the runtime in seconds.
        'title' is a human readable text (track name).
        'location' is the path to the media.
        '''
        # Check for header
        if check_extended_header(self.filename):
            with open(self.filename, 'r') as m3u_file:
                self.playlist.clear()
                # Skip the header
                _ = m3u_file.readline()
                # Start at first line after the header
                for line in m3u_file:
                    line = line.strip('\n')
                    if not line == '':
                        if line.startswith(self.info_tag):
                            entry = dict()
                            # remove the extended tag
                            info = line.replace(self.info_tag, '').strip('\n')
                            # Split the rest into time and track info
                            entry['runtime'], _, entry['title'] = info.partition(',')
                        else:
                            # Read the location
                            entry['location'] = line
                            # Append to the list
                            self.playlist.append(entry)

    def write(self):
        '''
        Save the M3U file.
        '''
        with open(self.filename, 'w') as m3u_file:
            # Write header
            m3u_file.write(self.header_tag + '\n')
            # Run through all entries
            for entry in self.playlist:
                # Extended info
                m3u_file.write(self.info_tag
                               + str(entry['runtime'])
                               + ',' + entry['title'] + '\n')
                # Media location
                m3u_file.write(entry['location'] + '\n')

    def add(self, title, runtime, location):
        '''
        Add an entry to the playlist.
        '''
        entry = dict()
        entry['title'] = title
        entry['runtime'] = runtime
        entry['location'] = location
        self.playlist.append(entry)

    def get_index_by_title(self, title):
        '''
        Get the index for an entry from title.
        '''
        i = 0
        for entry in self.playlist:
            if title == entry['title']:
                return(i)
            i += 1
        return(None)

