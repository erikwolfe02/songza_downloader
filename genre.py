class Genre:
    def __init__(self, genre_json):
        self.name = genre_json['name']
        self.station_ids = genre_json['station_ids']