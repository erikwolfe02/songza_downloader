import kivy

kivy.require('1.8.0')

from stationLoader import StationLoader
from tagLoader import TagLoader
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.properties import ObjectProperty
from kivy.uix.dropdown import DropDown


class DownloaderWrapper(BoxLayout):
    playlist_search_panel = ObjectProperty(None)
    playlist_details = ObjectProperty(None)
    playlist_downloader = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(DownloaderWrapper, self).__init__(**kwargs)
        pass


class GenreSpinner(Spinner):
    genres = None

    def __init__(self, **kwargs):
        super(GenreSpinner, self).__init__(**kwargs)
        self.values = map(str, self._load_genres())

    def _load_genres(self):
        loader = TagLoader()
        self.genres = loader.get_genres()
        return self.genres

    def get_genre(self, genre):
        return next((x for x in self.genres if x.name == genre), None)


class PlaylistSearchPanel(BoxLayout):
    station_info = None

    genre_list = ObjectProperty(None)
    station_list = ObjectProperty(None)
    drop_down_button = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(PlaylistSearchPanel, self).__init__(**kwargs)

    def download(self):
        print "PlaylistSearcher go!"
        # print "Station: " + self.station_id.text
        #station_id = self.station_id.text
        #print "you -==========" + self.station_id.text
        #StationDownloader(station_id)
        #StationDownloader("1390998")

    def genre_picked(self, genre):
        chosen_genre = self.genre_list.get_genre(genre)
        print "========1"
        if chosen_genre is not None:
            print "========2"
            stationLoader = StationLoader(chosen_genre.station_ids)
            station_info = stationLoader.get_stations()
            print "========3"
            self.station_list.update_list(station_info)

class PlaylistDetails(BoxLayout):

    def __init__(self, **kwargs):
        super(PlaylistDetails, self).__init__(**kwargs)
        
    def download(self):
        print "PlaylistDetails go!"
        #station_id = self.station_id.text
        #print "you -==========" + self.station_id.text
        #StationDownloader(station_id)
        #StationDownloader("1390998")


class PlaylistDownloader(BoxLayout):

    def __init__(self, **kwargs):
        super(PlaylistDownloader, self).__init__(**kwargs)
        
    def download(self):
        print "PlaylistDownloader go!"
        #station_id = self.station_id.text
        #print "you -==========" + self.station_id.text
        #StationDownloader(station_id)
        #StationDownloader("1390998")   


class StationList(ScrollView):
    layout = None
    collection = None
    def __init__(self, **kwargs):
        super(StationList, self).__init__(**kwargs)

        self.layout = GridLayout(cols=1, size_hint=(None, None))
        self.layout.bind(minimum_height=self.layout.setter('height'))
        self.add_widget(self.layout)

    def update_list(self, collection):
        print "About to update"
        if collection == self.collection:
            return
        else:
            print "Clearing..."
            self.layout.clear_widgets()
            self.collection = collection

        print "========4"

        for station in collection:
            btn = StationListingItem(text=str(station.name))
            self.layout.add_widget(btn)


class StationListingItem(Button):
    def __init__(self, **kwargs):
        super(StationListingItem, self).__init__(**kwargs)


class SongzaDownloader(App):

    def build(self):
        root =  DownloaderWrapper()
        return root

if __name__ == '__main__':
    SongzaDownloader().run()