songza_downloader
=================

A basic cucumber feature to download all the songs from the Songza playlist.
This allows you to kick off an automated song downloader for Songza.  You provide a playlist ID in the features/songza.feature file, run bundle exec cucumber, and sit back.

To get started, read the setup.txt and make sure you have the dependencies.  Then run the following in the project directory:
    bundle install
    bundle exec cucumber

The project is currently configured to use `:selenium` as the default driver, but that can be changed in `/features/support/env.rb`.

