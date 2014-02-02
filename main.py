import kivy
kivy.require('1.8.0')

from stationDownloader import StationDownloader
from stationLoader import StationLoader
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.uix.dropdown import DropDown

class DownloaderWrapper(BoxLayout):
    def __init__(self, **kwargs):
        super(DownloaderWrapper, self).__init__(**kwargs)
        pass

class ListDropDown(DropDown):
    def __init__(self, **kwargs):
        super(ListDropDown, self).__init__(**kwargs)
        loader = StationLoader()
        genres = loader.get_genres()
        for genre in genres:
            btn = Button(text=genre.name, size_hint_y=None, height=20)
            btn.bind(on_release=lambda btn: self.select(btn.text))
            self.add_widget(btn)

    def select(self, data):
        print "Clicked " + data

class PlaylistSearcher(BoxLayout):
    list_type = ObjectProperty(None)
    station_list = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super(PlaylistSearcher, self).__init__(**kwargs)
        
    def download(self):
        print "PlaylistSearcher go!"
        # print "Station: " + self.station_id.text
        #station_id = self.station_id.text
        #print "you -==========" + self.station_id.text
        #StationDownloader(station_id)
        #StationDownloader("1390998")
       
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
    def __init__(self, **kwargs):
        super(StationList, self).__init__(**kwargs)
        print "I was made...."
        
        layout = GridLayout(cols=1, size_hint=(None, None))
                
        layout.bind(minimum_height=layout.setter('height'))
        
        for i in range(30):
            btn = StationListingItem(text=str(i))
            layout.add_widget(btn)
        self.add_widget(layout)
 
class StationListingItem(Button):
    def __init__(self, **kwargs):
        super(StationListingItem, self).__init__(**kwargs)
        
class SongzaDownloader(App):

    def build(self):
        root =  DownloaderWrapper()
        return root

if __name__ == '__main__':
    SongzaDownloader().run()