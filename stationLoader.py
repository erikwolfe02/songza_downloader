# -*- coding: UTF-8 -*-
# For research purposes only
import urllib2
import json
import threading
from station import Station


class StationLoader (threading.Thread):
    _stations = []
    _opener = urllib2.build_opener()
    _request_url = "http://songza.com/api/1/station/"

    def __init__(self, stations, callback, threadId="stationLoaderThread"):
        threading.Thread.__init__(self)
        self.thread_id = threadId
        self.stations = stations
        self.callback = callback

    def run(self):
        print "Starting to load Stations..."
        self.load_stations()
        self.callback(self._stations)

    def load_stations(self):
        self._stations = []
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






