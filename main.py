import json
import os
import re
import mutagen as mg
from lyricsgenius import Genius


# Getting the lyrics from Genius and saving them to .txt file
def get_lyrics(file_path):
    genius = Genius(f'{get_token()}')
    audio = mg.File(file_path)
    tag_title = audio['title'][0]
    tag_artist = audio['artist'][0]
    song = genius.search_song(title=tag_title, artist=tag_artist)
    song.save_lyrics(filename=file_path,
                     extension='txt',
                     ensure_ascii=False,
                     sanitize=False)


# Text correction: removing unwanted data from .txt file
def clean_lyrics(filename):
    with open(f'{filename}.txt', 'r') as f:
        f4clean = f.read()
    clean = re.sub(r'^.*?(?=\[)|\d.*$', '', f4clean)
    with open(f'{filename}.txt', 'w') as f1:
        f1.write(clean)


# Creating a "lyrics" tag in an audio file and adding lyrics to it from a .txt file
def add_lyrics(file_path):
    audio = mg.File(file_path)
    with open(f'{file_path}.txt', 'r') as f:
        lyrics = f.read()
    audio['lyrics'] = lyrics
    audio.save()


# Creating a config.json with the Genius token and the music directory
def build_config():
    audio_folder = input('Audio folder: ')
    token = input('Genius API token: ')
    config = {
        "token": token,
        "location": audio_folder
    }
    with open('config.json', 'w') as f:
        json.dump(config, f)


# Checking for a config.json
def check_config():
    if os.path.isfile('config.json'):
        return True
    else:
        return False


# Getting music directory from config.json
def get_location():
    with open('config.json', 'r') as f:
        data = json.loads(f.read())
    location = data['location']
    return location


# Getting Genius token from config.json
def get_token():
    with open('config.json', 'r') as f:
        data = json.loads(f.read())
    token = data['token']
    return token


# Main function that run all needed functions
def main():
    for file in os.listdir(get_location()):
        file_path = os.path.abspath(os.path.join(get_location(), file))
        print(file_path)
        get_lyrics(file_path)
        clean_lyrics(file_path)
        add_lyrics(file_path)


if check_config() is True:
    main()
elif check_config() is False:
    q = input('Configuration file not found. Create a new one? (y/n): ')
    if q.lower() == 'y':
        build_config()
        print('The new configuration file has been created. The process will continue')
        main()
    elif q.lower() == 'n':
        raise SystemExit('The process was cancelled')
    else:
        raise SystemExit('Something went wrong...')
    