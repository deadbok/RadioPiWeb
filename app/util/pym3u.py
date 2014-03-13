'''
Read and write extended M3U play lists.
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

    if header.strip('\n') == pym3u.header_tag:
        return(True)
    else:
        return(False)


def create_empty(filename):
    '''
    Create an empty extended M3U file.
    '''
    try:
        with open(filename, 'w') as m3u_file:
            m3u_file.write(pym3u.header_tag + '\n')
    except EnvironmentError as exception:
        flash(exception.strerror, 'error')

    return(True)


class pym3u(object):
    '''
    Class to handle M3U play lists
    '''
    m3u_file = None
    '''M3U file.'''
    header_tag = '#EXTM3U'
    '''Header tag that identifies an extended M3U file.'''
    info_tag = '#EXTINF:'
    '''Tag to include extended information about a track.'''
    m3u_data = None
    '''List of the lines in the M3U file.'''
    playlist = list()
    '''List of dictionaries for each M3U entry.'''
    def __init__(self, filename):
        '''
        Constructor.
        '''
        self.m3u_file = open(filename)
        self.m3u_data = self.m3u_file.readlines()
        if self.check_header():
            self.read()

    def check_header(self):
        '''
        Check for the correct header.
        '''
        if self.m3u_data[0] == self.header_tag:
            return(True)
        return(False)

    def read(self):
        '''
        Read an M3U file. Put the data in a dictionary.

        'runtime' is the runtime in seconds.
        'title' is a human readable text (track name).
        'location' is the path to the media.
        '''
        # Start at first line after the header
        line = 1
        while (line < len(self.m3u_data)):
            entry = dict()
            # remove the extended tag
            info = self.m3u_data[line].replace(self.info_tag, '')
            # Split the rest into time and track info
            entry['runtime'], _, entry['title'] = info.partition(',')
            # next line
            line += 1
            entry['location'] = self.m3u_data[line]
            # Append to the list
            self.playlist.append(entry)
