songza_downloader
=================

Python script to download all the songs from a given Songza playlist.

Requires: 

MPlayer - http://www.mplayerhq.hu/design7/dload.html
LAME - http://lame.sourceforge.net/

1. Set environment variables for both MPlayer and your LAME encoder.
2. from your command line in the project diectory, run 'python downloader.py {station_id} {save directory}'

If you go to Songza you can find the station ids by looking at the source for a page with your album on it.  I'll work
on a way to view a list of albums some other time.
