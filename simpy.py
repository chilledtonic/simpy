'''Simple Last.fm scrobbler for Rockbox`s .log file'''

import os.path
import datetime
from hashlib import md5
import getpass
import pylast


API_KEY = '25486bbdf2ddd3c19c6167b1743570d0'
API_SECRET = 'f8e74958a3dc243574c72421448fd481'

SCRIPTPATH = os.path.dirname(__file__)
ROCKBOX_FILE = os.path.join(SCRIPTPATH, '.scrobbler.log')


def parse_tags():
    '''Parsing information about songs from log file line by line
    and returning result by yield'''

    log_transcription = []
    with open(ROCKBOX_FILE, 'r+') as logfile:
        for line in logfile:
            try:
                log_transcription = {'artist':line.split('\t')[0],
                                     'album':line.split('\t')[1],
                                     'title':line.split('\t')[2],
                                     'timestamp':line.split('\t')[6]}
                yield log_transcription
            except:
                print('Artist or album or something else information needed')


def assignment():
    '''
    '''
    for value in parse_tags():
        artist = value['artist']
        album = value['album']
        title = value['title']
        timestamp = value['timestamp']

        yield artist, album, title, timestamp


def scrobbling(username, password):
    ''' Send information about song and
    scrobble it
    '''
    password_hash = md5(password.encode('utf-8')).hexdigest()
    network = pylast.LastFMNetwork(api_key=API_KEY, api_secret=API_SECRET,
                                   username=username, password_hash=password_hash)
    counter = 0
    for artist, album, title, timestamp in assignment():
        network.scrobble(artist=artist, album=album, title=title, timestamp=timestamp)
        print(artist + ' ' + album + ' ' + title + ' ' +
              datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S'))
        counter = counter + 1


    print('-'*10)
    print('Total tracks scrobbled: ', counter)
    input('Press any key to exit.')


if __name__ == '__main__':
    input_username = input('Login: ')
    input_password = getpass.getpass(prompt='Password: ')
    scrobbling(input_username, input_password)
