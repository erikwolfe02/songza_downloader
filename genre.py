class Genre:
    def __init__(self, genre_json):
        self.name = genre_json['name']
        self.station_ids = genre_json['station_ids']

    def __str__(self):
        print "Remove this crap...."
        if len(self.name) > 18:
            new_string = ""
            separator = "\n"
            list_string = list(self.name)
            i = 0
            for character in list_string:
                if i < 18:
                    new_string += character
                    i += 1
                else:
                    if character == ' ':
                        new_string += separator
                        i = 0
                    else:
                        new_string += character
                        i += 1
            return new_string

        return self.name