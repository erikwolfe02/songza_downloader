import re

class Song:
    def __init__(self, song_json, album):
        self.song_json = song_json
        
        self.artist = unicode(song_json['song']['artist']['name'])
        self.title = unicode(song_json['song']['title'])
        self.genre = unicode(song_json['song']['genre'])
        self.album = unicode(album)
        self.url = song_json['listen_url']
        self.id = song_json['song']['id']
    
    # Replace any 'special'characters - rethink think this regex (maybe just encode better)
    def replace_special_characters(self, text):
        return re.sub('[^a-zA-Z0-9\n\.]', '-', text)