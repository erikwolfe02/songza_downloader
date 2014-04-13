import urllib2
import json
from genre import Genre


class TagLoader:
    _opener = urllib2.build_opener()
    _request_url = "http://songza.com/api/1/gallery/tag/genres"
    _genres = []

    def __init__(self):
        self._populate_genres()

    def get_genres(self):
        return self._genres

    def _populate_genres(self):
        self.genres = self._get_json(self._request_url)

        for x in range(len(self.genres)):
            self._add_to_list(self.genres[x])

    def _get_json(self, url):
        response = self._opener.open(str(url))
        response_string = str(response.read())
        return json.loads(response_string.encode('utf8'))

    def _add_to_list(self, genre_json):
        self._genres.append(Genre(genre_json))
