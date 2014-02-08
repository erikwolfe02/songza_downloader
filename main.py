import kivy
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
import os
import shutil
import threading

kivy.require('1.8.0')

from stationLoader import StationLoader
from tagLoader import TagLoader
from imageLoader import ImageLoader
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner
from kivy.clock import mainthread
from kivy.properties import ObjectProperty


class DownloaderWrapper(BoxLayout):
    playlist_search_panel = ObjectProperty(None)
    playlist_details = ObjectProperty(None)
    playlist_downloader = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(DownloaderWrapper, self).__init__(**kwargs)
        pass

    def attach_listeners(self):
        self.playlist_search_panel.add_selection_listener(self.station_picked)

    def station_picked(self, station):
        self.playlist_details.load_station_details(station)


class PlaylistDetailsLabel(Label):
    def __init__(self, **kwargs):
        super(PlaylistDetailsLabel, self).__init__(**kwargs)


class DownloadButton(Button):
    def __init__(self, **kwargs):
        super(DownloadButton, self).__init__(**kwargs)


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
    current_genre_from_list = None

    genre_list = ObjectProperty(None)
    station_list = ObjectProperty(None)
    drop_down_button = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(PlaylistSearchPanel, self).__init__(**kwargs)
        self.register_event_type('on_station_select')

    def genre_picked(self, selected_genre):
        if self.current_genre_from_list == selected_genre:
            return
        file_manipulation_thread = threading.Thread(target=self.remove_album_images)
        file_manipulation_thread.start()
        self.genre = selected_genre
        chosen_genre = self.genre_list.get_genre(self.genre)

        self.station_list.add_station_selection_listener(self.on_station_select)

        if chosen_genre is not None:
            self.stationLoader = StationLoader(chosen_genre.station_ids, self.add_stations)
            self.stationLoader.start()

    def add_selection_listener(self, callback):
        self.parent_selection_listener = callback

    def on_station_select(self, station):
        self.parent_selection_listener(station)

    def remove_album_images(self):
        shutil.rmtree("temp")
        os.mkdir("temp")

    @mainthread
    def add_stations(self, stations):
        self.station_list.update_list(stations)

class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

class PlaylistDetails(GridLayout):
    cover_image = ObjectProperty(None)
    station_text_details = ObjectProperty(None)
    download_button = ObjectProperty(None)
    download_dir = ObjectProperty(None)
    # file_chooser = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(PlaylistDetails, self).__init__(**kwargs)
        self.cols = 1
        self.size_hint = (None, None)
        self.width = 225
        self.padding = (20, 20)

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content, size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, path, filename):
        self.download_dir.text = path
        self.dismiss_popup()

    def cancel(self):
        self.dismiss_popup()

    def load_station_details(self, station):
        self._create_layout(station)

    def _create_layout(self, station):
        self._download_album_art(station)
        details_string = ""
        details_string += "[b]Song Count:[/b] " + str(station.song_count)+"\n\n"
        details_string += "[b]Created By:[/b] " + station.creator_name + "\n\n"
        details_string += "[b]Featured Artists:[/b] \n"
        details_string += station.featured_artists_string
        self.station_text_details.text = str(details_string)

    def _download_album_art(self, station):
        image_loader = ImageLoader(station.cover_url, station.dasherized_name, self.add_image)
        image_loader.start()

    def dismiss_popup(self):
        self._popup.dismiss()
        self.remove_widget(self._popup)

    @mainthread
    def add_image(self, image_location):
        print "About to set the image"
        print image_location
        self.cover_image.source = image_location

    # def download(self):
    #     print "PlaylistDetails go!"
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
        if collection == self.collection:
            return

        self.collection = collection
        self.layout.clear_widgets()
        for station in collection:
            item = StationListingItem(station, self.on_station_select)
            self.layout.add_widget(item)

    def add_station_selection_listener(self, callback):
        self.callback = callback

    def on_station_select(self, station):
        self.callback(station)


class StationListingItem(Button):
    def __init__(self, station, child_click_callback, **kwargs):
        super(StationListingItem, self).__init__(**kwargs)
        self.markup = True
        self.station = station
        self.text = self._create_text()
        self.callback = child_click_callback

    def on_release(self):
        self.callback(self.station)

    def _create_text(self):
        label_text = "[size=16][b]"+str(self.station.name)+"[/b][/size]"
        label_text = label_text + "\n\n[size=12]"+self._build_description(self.station.description)+"[/size]"
        label_text = label_text + "\n\n[size=9]" + self.station.featured_artists_string+"[/size]"
        return label_text

    def _build_description(self, description):
        if len(description) > 160:
            description = description[:160]
            index_of_last_space = description.rfind(" ")
            description = description[:index_of_last_space]
            return description + "..."
        return description


class SongzaDownloader(App):

    def build(self):
        root = DownloaderWrapper()
        root.attach_listeners()
        return root

if __name__ == '__main__':
    SongzaDownloader().run()