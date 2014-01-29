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
from subprocess import call

def main(argv):
	try:
		album_id = argv[0]
		filepath = argv[1]
	except IndexError as e:
		print "Error: script usage should be scriptname.py {album id} {directory to save files}"
		return
	
	opener = urllib2.build_opener()
	# sessionid is used to provide a unique song on each next request
	opener.addheaders.append(('Cookie', 'sessionid=%s' % str(session_id_generator())))
	# Every album has an ID.  Given an id, this will find all the metadata for an album
	url = "http://songza.com/api/1/station/" + str(album_id)
	album_json = get_json(url, opener)
	count = album_json['song_count']
	next_song_url = url + "/next"
	album = album_json['name']
	print "Downloading album " + album + "..." 
	
	for x in range(count-1):
		#420 error occurs without a sleep.  Shorter time may work fine
		time.sleep(2)
		song_json = get_json(next_song_url, opener)
		
		artist = song_json['song']['artist']['name']
		title = song_json['song']['title']
		
		if not path_exists(file_path_builder(filepath, album, artist, title)):
			trackNumber = str(x  + 1)
			try:
				print "Track " + trackNumber + "/" + str(count) + " " + artist + "-" + title
			except UnicodeEncodeError as e:
				print "UnicodeEncodeError: " + str(e)
			
			download_file(filepath, artist, title, album, song_json['listen_url'])
		
def download_file(filepath, artist, title, album, songUrl):
	song = urllib2.urlopen(songUrl)
	ensure_dir(album_path_builder(filepath, album))
	# write the file out
	with open(file_path_builder(filepath, album, artist, title), 'wb') as dest:
		shutil.copyfileobj(song, dest)
		#convert_files(album) -- Figure this out

def album_path_builder(filepath, album):
	album = replace_special_characters(album)
	return filepath + "\\" + album + "\\"
	
def file_path_builder(filepath, album, artist, title):
	return album_path_builder(filepath, album)+ replace_special_characters(artist) + "-" + replace_special_characters(title) + ".mp4"

# replace anything that is not a number or letter with a dash
def replace_special_characters(text):
	return re.sub('[^a-zA-Z0-9\n\.]', '-', text)
	
def ensure_dir(f):
    if not path_exists(f):
        os.makedirs(os.path.dirname(f))

def path_exists(f):
	return os.path.exists(f)
		
def session_id_generator(size=18, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
	return ''.join(random.choice(chars) for x in range(size))

def get_json(url, opener):
	response = opener.open(str(url))
	responseString = str(response.read())
	return json.loads(responseString)
	
def convert_files(album):
	album_path = album_path_builder(album)
	files = []
	filelist = [ f for f in os.listdir(album_path) if f.endswith(".mp4") ]
	for path in filelist:
		basename = os.path.basename(path)
		filename = os.path.splitext(basename)[0]
		files.append(filename)

	if len(files) == 0:
		exit("Could not find any files to convert that have not already been converted.")
	 
	for filename in files:
		print "-- converting %s.mp4 to %s.mp3 --" % (filename, filename)
		call(["mplayer", "-novideo", "-nocorrect-pts", "-ao", "pcm:waveheader", album_path + filename + ".mp4"])
		call(["lame", "-h", "-b", "192", "audiodump.wav", album_path + "/" + filename + ".mp3"])
		os.remove("audiodump.wav")
	 
		
if __name__ == "__main__":
	main(sys.argv[1:])










