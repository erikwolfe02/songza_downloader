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
import atexit
import subprocess
from song import Song

class StationDownloader:
    _opener = urllib2.build_opener()
    _request_url = "http://songza.com/api/1/station/"
    _session_url = None
    _log_file = open('logfile', 'w')
    _downloaded_count = 0
    
    def __init__(self, station_id, filepath = "C:\Temp"):
        self._user_path = filepath
        self._session_url = self._request_url + str(station_id)
        
        # sessionid is used to provide a unique song on each "next" request.
        self._create_session_id()

        # Every album has an ID.  Given an id, this will find all the metadata for an album
        self.album_json = self._get_json(self._session_url)
        
        self._song_count = self.album_json['song_count']
        self.album_name = self.album_json['dasherized_name']
        
        print "Downloading album " + self.album_name + "..." 

        self._ensure_dir_exists(self._album_path_builder(self.album_name))
        
        for current_song in range(self._song_count):
            the_song = Song(self._get_next_song(), self.album_name)
            path_to_song = self._file_path_builder(the_song)

            if (self._path_does_not_exist(path_to_song)):
                self._process_next_track(the_song, path_to_song, current_song)
            else:
                # 420 error occurs without a sleep.  Shorter time may work fine,
                # don't need if we are converting though  
                time.sleep(2)

        print "Download complete!"
        print "Downloaded " + str(self._downloaded_count) + " from " + self.album_name
        
    def _process_next_track(self, the_song, path_to_song, current_song):
        try:
            print "Track " + str(current_song + 1) + "/" + str(self._song_count) + " " + the_song.artist + "-" + the_song.title
            the_file_name = path_to_song + ".mp4"
            self._download_file(the_song, the_file_name)
            self._convert_file(the_song, path_to_song)
            os.remove(the_file_name)
            
            self._log_file.flush()
            
            self._downloaded_count += 1
        except UnicodeEncodeError as e:
            print "UnicodeEncodeError: " + str(e)
            
    def _path_does_not_exist(self, path):
        return (not self._path_exists(path + ".mp4")) and (not self._path_exists(path + ".mp3"))
    
    def _download_file(self, song, the_song_file):
        song_from_site = urllib2.urlopen(song.url)
        with open(the_song_file, 'wb') as dest:
            shutil.copyfileobj(song_from_site, dest)

    def _album_path_builder(self, album):
        return self._user_path + "\\" + album + "\\"
        
    def _file_path_builder(self, song):
        return self._album_path_builder(song.album) + song.artist + "-" + song.title

    def _ensure_dir_exists(self, f):
        if not self._path_exists(f):
            os.makedirs(os.path.dirname(f))

    def _path_exists(self, f):
        return os.path.exists(f)
            
    def _session_id_generator(self, size=18, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
        return ''.join(random.choice(chars) for x in range(size))

    def _get_json(self, url):
        response = self._opener.open(str(url))
        response_string = str(response.read())
        return json.loads(response_string.encode('utf8'))

    def _convert_file(self, song, file_path):
        filename = song.artist +"-"+ song.title
        print "-- converting %s.mp4 to %s.mp3 --" % (filename, filename)
        
        self._convert_to_wav_for_lame(file_path)
        self._convert_to_mp3_with_lame(song, file_path)

    def _convert_to_wav_for_lame(self, file_path):
        subprocess.call([os.path.normpath("./tools/mplayer.exe"), "-novideo", "-msglevel",  "all=-1", "-nocorrect-pts", "-ao", "pcm:waveheader", file_path + ".mp4"], stdout=self._log_file, stderr=subprocess.STDOUT)
    
    def _convert_to_mp3_with_lame(self, song, file_path):
        subprocess.call([os.path.normpath("./tools/lame.exe"), "-h", "-S", "--vbr-new", "-T", "--add-id3v2", "--ta", song.artist, "--tt", song.title, "--tl", "Songza - " + song.album, "--tg", song.genre, "audiodump.wav", file_path + ".mp3"], stdout=self._log_file, stderr=subprocess.STDOUT)
        
        self._remove_temp_file()
        
    def _create_session_id(self):
        self._opener.addheaders.append(('Cookie', 'sessionid=%s' % str(self._session_id_generator())))
    
    def _get_next_song(self):
        return self._get_json(self._session_url + "/next")

    @atexit.register
    def _remove_temp_file(self):
        os.remove("audiodump.wav")



