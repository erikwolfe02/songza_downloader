require 'rubygems'
require 'json'
require 'open-uri'
require 'fileutils'

When /^I visit "([^"]*)"$/ do |url|
  visit(url)
end

Given /^I wait for (\d+) seconds?$/ do |n|
  sleep(n.to_i)
end

When /^I visit playlist "([^"]*)"$/ do |playlist|
  fill_in('q',:with => playlist)
  click_on "#{playlist}"
end

When /^I want to download all the songs in playlist "([^"]*)"$/ do |playlist|
  visit("http://songza.com/api/1/station/#{playlist}?wadl")
  
  element= find("html")
  node = element.native
  page_html = node.text
  json_playlist= JSON.parse(page_html.to_s())
  
  playlist_name = json_playlist["name"]
  playlist_length = json_playlist["song_count"]

  FileUtils.mkpath "#{playlist_name}"  

  $i = 0

  while $i < playlist_length  do
    puts("Getting song #$i" )
    visit("http://songza.com/api/1/station/#{playlist}/next?wadl")
    
    element= find("html")
    node = element.native
    page_html = node.text
    json_song= JSON.parse(page_html.to_s())
  
    url = json_song["listen_url"]
    artist = json_song["song"]["artist"]["name"]
    title = json_song["song"]["title"]
    if(artist != "!!!")
      puts("Downloading song #{artist}-#{title}" )
    
      open("#{playlist_name}/#{artist}-#{title}.mp4", 'wb') do |file|
        file << open("#{url}").read
      end
    end
    sleep(3)
    $i +=1
  end
end

When /^I visit playlist "([^"]*)" JSON$/ do |playlist|
  visit("http://songza.com/api/1/station/#{playlist}/next?wadl")
end

When /^I download the song$/ do 
  element= find("html")
  node = element.native
  page_html = node.text
  json_song= JSON.parse(page_html.to_s())
  
  url = json_song["listen_url"]
  artist = json_song["song"]["artist"]["name"]
  title = json_song["song"]["title"]
  
  open("blah/#{artist}-#{title}.mp4", 'wb') do |file|
    file << open("#{url}").read
  end
 
end

When /^I login with "([^"]*)" and "([^"]*)"$/ do |username, password|
  fill_in('login-username',:with => username)
  fill_in('login-password',:with => password)
  click_on 'Log in'
end
