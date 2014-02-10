import kivy
from kivy.core.window import Window

kivy.require('1.8.0')

from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.progressbar import ProgressBar
import os
import shutil
import threading
from songStates import SongStates
from stationDownloader import StationDownloader


from stationLoader import StationLoader
from tagLoader import TagLoader
from imageLoader import ImageLoader
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner
from kivy.clock import mainthread
from kivy.properties import ObjectProperty, StringProperty


class DownloaderWrapper(BoxLayout):
    playlist_search_panel = ObjectProperty(None)
    playlist_details = ObjectProperty(None)
    playlist_downloader = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(DownloaderWrapper, self).__init__(**kwargs)
        pass

    def attach_listeners(self):
        self.playlist_search_panel.add_selection_listener(self.station_picked)
        self.playlist_details.add_download_listener(self.download_listener)
        self.playlist_details.add_stop_download_listener(self.stop_download_listener)

    def station_picked(self, station):
        self.playlist_details.load_station_details(station)

    def download_listener(self, station, save_location):
        self.playlist_downloader.begin_download(station, save_location)

    def stop_download_listener(self):
        self.playlist_downloader.stop_download()


class PlaylistDetailsLabel(Label):
    def __init__(self, **kwargs):
        super(PlaylistDetailsLabel, self).__init__(**kwargs)


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
            item = StationListingItem(station, self.layout, self.on_station_select, size=(self.width, 225), text_size=(self.width*.9, 255))
            self.layout.add_widget(item)

    def add_station_selection_listener(self, callback):
        self.callback = callback

    def on_station_select(self, station):
        self.callback(station)


class StationListingItem(Button):
    def __init__(self, station, wrapper, child_click_callback, **kwargs):
        super(StationListingItem, self).__init__(**kwargs)
        self.markup = True
        self.station = station
        self.wrapper = wrapper
        self.text = self._create_text()
        self.callback = child_click_callback

    def on_release(self):
        for child in self.wrapper.children:
            child.background_color = (0, 0, 0, 0)
        self.background_color = (0, .76, .8, 1)
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

    _station = None

    def __init__(self, **kwargs):
        super(PlaylistDetails, self).__init__(**kwargs)

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
        self._station = station
        self._create_layout(station)

    def add_download_listener(self, callback):
        self.download_listener = callback

    def add_stop_download_listener(self, callback):
        self.stop_download_listener = callback

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
        self._popup.dismiss(force=True, animation=False)

    @mainthread
    def add_image(self, image_location):
        self.cover_image.source = image_location

    def download(self):
        if self.download_dir.text is None or self.download_dir.text == "":
            self.download_dir.background_color = (1, .1, .13, 1)
            return
        if self._station is None:
            self.station_text_details.text = "[b][size=20]Please pick a station[/size][/b]"
            return
        else:
            self.download_dir.background_color = (255, 255, 255, 1)
        self.download_listener(self._station, self.download_dir.text)

    def stop_download(self):
        self.stop_download_listener()


class PlaylistDownloader(BoxLayout):
    _current_song = None
    scroll_list = ObjectProperty(None)
    status_container = ObjectProperty(None)
    _progress_bar = None
    _downloader = None

    def __init__(self, **kwargs):
        super(PlaylistDownloader, self).__init__(**kwargs)

    def begin_download(self, station, save_dir):
        self._downloader = StationDownloader(station.id, self.song_status_listener, save_dir)
        if self._progress_bar is None:
            self._progress_bar = ProgressBar(max=4, size_hint=(None, None), width=self.width-20)
            self.add_widget(self._progress_bar)
        self._downloader.start()

    def stop_download(self):
        self.clear_widgets()
        self._downloader.stop()

    @mainthread
    def song_status_listener(self, song, status, isSuccessful):
        if self._current_song == song.id:
            print "Same song, update status"
            self._progress_bar.value += 1
            self._update_existing_status(status, isSuccessful)
        else:
            print "New song, create a status"
            self._progress_bar.value = 0
            self._current_song = song.id
            self._create_new_song_status(song, status, isSuccessful)

    def _update_existing_status(self, status, isSuccessful):
        self._current_status.update_status_led(status, isSuccessful)

    def _create_new_song_status(self, song, status, isSuccessful):
        self._create_status_widget(song, status, isSuccessful)
        self.status_container.add_widget(self._current_status)
        self.scroll_list.scroll_y = 0

    def _create_status_widget(self, song, status, isSuccessful):
        self._current_status = StatusEntry(song, status, isSuccessful, self)


class StatusContainer(BoxLayout):
    def __init__(self, **kwargs):
        super(StatusContainer, self).__init__(**kwargs)


class StatusEntry(BoxLayout):
    status_icon = ObjectProperty(None)
    song_name = ObjectProperty(None)

    def __init__(self, song, status, isSuccessful, parent, **kwargs):
        super(StatusEntry, self).__init__(**kwargs)
        self.size_hint = (None, None)
        self.width = parent.width - 20
        self.id = str(song.id)
        self.song = song
        self.status = status
        self.isSuccessful = isSuccessful
        self._create_status_led()
        self._create_text()
        print "Created status entry..."

    def update_status_led(self, status, isSuccessful):
        self.status = status
        self.isSuccessful = isSuccessful
        self._create_status_led()

    def _create_status_led(self):
        if self.status is not SongStates.FINISHED:
            self.status_icon.source = "assets/status_in_progress.png"
        elif self.status is SongStates.FINISHED and self.isSuccessful:
            self.status_icon.source = "assets/status_success.png"
        else:
            self.status_icon.source = "assets/status_fail.png"

    def _create_text(self):
        label_text = self.song.artist + " - " + self.song.title
        self.song_name.text = label_text


class SongzaDownloader(App):

    def build(self):
        self.title = 'Songza Downloader'
        root = DownloaderWrapper()
        root.attach_listeners()
        return root

if __name__ == '__main__':
    SongzaDownloader().run()