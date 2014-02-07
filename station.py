import urllib2


class Station:
    def __init__(self, station_json):
        self.dasherized_name = station_json['dasherized_name'].encode('utf8')
        self.status = station_json['status'].encode('utf8')
        self.name = station_json['name'].encode('utf8')
        self.creator_name = station_json['creator_name'].encode('utf8')
        self.url = station_json['url']
        self.song_count = station_json['song_count']
        self.cover_url = station_json['cover_url']
        self.id = station_json['id']
        self.description = station_json['description'].encode('utf8')
        self.featured_artists = station_json['featured_artists']
        self.featured_artists_string = self._create_artist_string().encode("utf8")

    def _create_artist_string(self):
        artist_list = ""
        for artist in self.featured_artists:
            artist_list = artist_list + artist['name'] + ", "

        return artist_list[:-2]