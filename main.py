import kivy
kivy.require('1.8.0')

from downloader import StationDownloader
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.properties import ObjectProperty

class PlaylistDownloader(GridLayout):
    
    station_id = ObjectProperty(None)
    def download(self):
        station_id = self.station_id.text
        print "you -==========" + self.station_id.text
        StationDownloader(station_id)

class Downloader(App):

     def build(self):
         return PlaylistDownloader()

if __name__ == '__main__':
    Downloader().run()