import kivy
kivy.require('1.8.0')

from stationDownloader import StationDownloader
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.graphics import Color, Rectangle
from kivy.core.image import Image as CoreImage
from kivy.core.window import Window

class DownloaderWrapper(BoxLayout):
    def __init__(self, **kwargs):
        super(DownloaderWrapper, self).__init__(**kwargs)
        pass

class PlaylistSearcher(BoxLayout):
    station_id = ObjectProperty(None)
    station_list = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super(PlaylistSearcher, self).__init__(**kwargs)
        
    def download(self):
        print "PlaylistSearcher go!"
        print "Station: " + self.station_id.text
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