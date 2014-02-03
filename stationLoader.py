# -*- coding: UTF-8 -*-
# For research purposes only
import urllib2
import json


class StationLoader:
    _stations = []
    _opener = urllib2.build_opener()
    _request_url = "http://songza.com/api/1/station/"

    def __init__(self, stations):
        self.stations = stations
        self.load_stations()

    def load_stations(self):
        for station_id in self.stations:
            station_json = self._get_json(self._request_url + str(station_id))
            self._add_station(station_json)

    def _add_station(self, station_json):
        self._stations.append(Station(station_json))

    def get_stations(self):
        return self._stations

    def _get_json(self, url):
        response = self._opener.open(str(url))
        response_string = str(response.read())
        return json.loads(response_string.encode('utf8'))

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
        self.featured_artist = station_json['featured_artists']




