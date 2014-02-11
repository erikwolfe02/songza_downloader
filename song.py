import re


class Song:
    def __init__(self, song_json, album):
        self.song_json = song_json
        
        self.artist = song_json['song']['artist']['name'].encode('utf8')
        self.title = song_json['song']['title'].encode('utf8')
        self.genre = song_json['song']['genre'].encode('utf8')
        self.album = album.encode('utf8')
        self.url = song_json['listen_url']
        self.id = song_json['song']['id']
    
    # Replace any 'special'characters - rethink think this regex (maybe just encode better)
    def replace_special_characters(self, text):
        return re.sub('[^a-zA-Z0-9\n\.]', '-', text)