import re
import unicodedata


class Song:
    def __init__(self, song_json, album):
        self.song_json = song_json
        
        self.artist = self.slugify(song_json['song']['artist']['name'])
        self.title = self.slugify(song_json['song']['title'])
        self.genre = song_json['song']['genre']
        self.album = album
        self.url = song_json['listen_url']
        self.id = song_json['song']['id']

    def slugify(self, value):
        re_slugify = re.compile('[^\w\s-]', re.UNICODE)
        value = unicodedata.normalize('NFKD', value)
        value = unicode(re_slugify.sub('', value).strip())
        value = re.sub('[-\s]+', '-', value)
        return value