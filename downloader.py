# -*- coding: UTF-8 -*-
# For research purposes only
import urllib2
import json
import shutil
import string
import random
import sys
import os
import time
import re
import subprocess
from subprocess import call

class StationDownloader:
    def __trunc__(self):
        return 67

    def __init__(self, station_id):
        try:
            album_id = station_id
            filepath = "C:\Temp"
        except IndexError as e:
            print "Error: script usage should be scriptname.py {album id} {directory to save files}"
            return

        opener = urllib2.build_opener()

        # sessionid is used to provide a unique song on each next request
        opener.addheaders.append(('Cookie', 'sessionid=%s' % str(self.session_id_generator())))

        # Every album has an ID.  Given an id, this will find all the metadata for an album
        url = "http://songza.com/api/1/station/" + str(album_id)
        album_json = self.get_json(url, opener)
        count = album_json['song_count']
        next_song_url = url + "/next"
        album = album_json['name']
        print "Downloading album " + album + "..." 
    
        for x in range(count-1):
            
            song_json = self.get_json(next_song_url, opener)
            artist = song_json['song']['artist']['name']
            title = song_json['song']['title']
            genre = song_json['song']['genre']
            
            the_song = Song(song_json, artist, title, genre, album)
            
            temp_file_path = self.file_path_builder(filepath, the_song)
            if (not self.path_exists(temp_file_path+".mp4")) and (not self.path_exists(temp_file_path+".mp3")):
                trackNumber = str(x  + 1)
                try:
                    print ("Track " + trackNumber + "/" + str(count) + " " + artist + "-" + title).encode('utf8')
                    self.download_file(filepath, the_song)
                except UnicodeEncodeError as e:
                    print "UnicodeEncodeError: " + str(e)
            else:
                # 420 error occurs without a sleep.  Shorter time may work fine
                # don't need if we are converting though  
                time.sleep(2)
        # Clean up mp4s later
    
    def download_file(self, user_filepath, song):
        song_file = urllib2.urlopen(song.song_json['listen_url'])
        self.ensure_dir(self.album_path_builder(user_filepath, song.album))
        # write the file out
        with open(self.file_path_builder(user_filepath, song)+".mp4", 'wb') as dest:
            shutil.copyfileobj(song_file, dest)
            self.convert_file(user_filepath, song)

    def album_path_builder(self, user_filepath, album):
        album = self.replace_special_characters(album)
        return user_filepath + "\\" + album + "\\"
        
    def file_path_builder(self, user_filepath, song):
        return self.album_path_builder(user_filepath, song.album)+ self.replace_special_characters(song.artist) + "-" + self.replace_special_characters(song.title).encode('utf8')

    # replace anything that is not a number or letter with a dash
    def replace_special_characters(self, text):
        return re.sub('[^a-zA-Z0-9\n\.]', '-', text)
        
    def ensure_dir(self, f):
        if not self.path_exists(f):
            os.makedirs(os.path.dirname(f))

    def path_exists(self, f):
        return os.path.exists(f)
            
    def session_id_generator(self, size=18, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
        return ''.join(random.choice(chars) for x in range(size))

    def get_json(self, url, opener):
        response = opener.open(str(url))
        responseString = str(response.read())
        return json.loads(responseString)

    def convert_file(self, user_filepath, song):
        log_file = open('logfile', 'w')
        
        file_path = self.file_path_builder(user_filepath, song)
        filename = self.replace_special_characters(song.artist) +"-"+ self.replace_special_characters(song.title)
        print "-- converting %s.mp4 to %s.mp3 --" % (filename, filename)
        
        call(["mplayer", "-novideo", "-nocorrect-pts", "-ao", "pcm:waveheader", file_path + ".mp4"], stdout=log_file, stderr=subprocess.STDOUT)
        
        call(["lame", "-h", "--vbr-new", "-T", "--add-id3v2", "--ta", song.artist, "--tt", song.title, "--tl", "Songza - " + song.album, "--tg", song.genre, "audiodump.wav", file_path + ".mp3"], stdout=log_file, stderr=subprocess.STDOUT)
        log_file.flush()
        
        os.remove("audiodump.wav")

class Song:
    def __init__(self, song_json, artist, title, genre, album):
        self.song_json = song_json
        self.artist = artist
        self.title = title
        self.genre = genre
        self.album = album
    
if __name__ == "__main__":
    main(sys.argv[1:])





