import json
import os
import re
import glob
import mutagen as mg
from lyricsgenius import Genius

EXTENSION = 'txt'


# Getting the lyrics from Genius and saving them to .txt file
def get_lyrics(file_path=None, extension=EXTENSION):
    genius = Genius(f'{get_token()}')
    audio = mg.File(file_path)
    tag_title = audio['title'][0]
    tag_artist = audio['artist'][0]
    song = genius.search_song(title=tag_title, artist=tag_artist)
    if song != None:
        song.save_lyrics(filename=file_path,
                     extension=extension,
                     sanitize=False)
    else:
        return None
        
# Text correction: removing unwanted data from .txt file
def clean_lyrics(file_path, extension=EXTENSION):
    with open(f'{file_path}.{extension}', 'r', encoding='utf-8') as f:
        f4clean = f.read()
    clean = re.sub(r'^.*?(?=\[)|\d.*$', '', f4clean)
    with open(f'{file_path}.{extension}', 'w', encoding='utf-8') as f1:
        f1.write(clean)


# Creating a "lyrics" tag in an audio file and adding lyrics to it from a .txt file
def add_lyrics(file_path, extension=EXTENSION):
    audio = mg.File(file_path)
    for f in glob.iglob(f'{get_location()}/*.{extension}'):
        with open(f, 'r', encoding='utf-8') as f:
            lyrics = f.read()
    audio['lyrics'] = lyrics
    audio.save()


# Creating a config.json with the Genius token and the music directory
def build_cfg():
    audio_folder = input('Audio folder: ')
    token = input('Genius API token: ')
    config = {"token": token, "location": audio_folder}
    with open('config.json', 'w') as f:
        json.dump(config, f)


# Checking for a config.json
def check_cfg():
    if os.path.isfile('config.json'):
        return True
    else:
        return False


# Getting music directory from config.json
def get_location():
    with open('config.json', 'r') as f:
        data = json.load(f)
    return data['location']


# Getting Genius token from config.json
def get_token():
    with open('config.json', 'r') as f:
        data = json.load(f)
    return data['token']


# Main function that run all needed functions
def main():
    q = input('Search lyrics OR add existed texts to songs? [1/2]: ')
    if q == '1':
        if not check_cfg():
            q1 = input('Configuration file not found. Create a new one? (y/n): ')
            if q1.lower() == 'y':
                build_cfg()
                print('The new configuration file has been created. The process will continue.')
            elif q1.lower() == 'n':
                raise SystemExit('The process was cancelled.')

        q2 = input('Add saved lyrics to audio file? (y/n): ')
        for file in glob.iglob(f'{get_location()}/*.*'):
            file_path = os.path.join(get_location(), file)
            if get_lyrics(file_path) != None:
                clean_lyrics(file_path)
        if q2.lower() == 'y':
            add_lyrics(file_path)
    elif q == '2':
        for file in glob.iglob(f'{get_location()}/*.*'):
            file_path = os.path.join(get_location(), file)
            add_lyrics(file_path)


if __name__ == "__main__":
    main()
    
