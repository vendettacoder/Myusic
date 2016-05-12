# -*- coding: utf-8 -*-
"""
Created on Fri Apr  8 01:48:27 2016

@authors: Rohan Kulkarni
          Parth Parekh

@email : rk2845@columbia.edu
         prp2121@columbia.edu
"""
from PyLyrics import *

def getLyrics(songName,artistName):
    try:
        print 'Lyrics Fetched'
        lyrics = PyLyrics.getLyrics(artistName,songName)
        if lyrics:
            with open('./Songs/'+songName.lower().replace(' ','_')+'.txt','w') as f:
                f.write(lyrics.lower())
    except:
        print "No Lyrics fetched"

if __name__ == '__main__':
    getLyrics('Blank Space','Taylor Swift')
