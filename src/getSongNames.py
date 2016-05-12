# -*- coding: utf-8 -*-
"""
Created on Fri Apr  8 02:34:43 2016

@authors: Rohan Kulkarni
          Parth Parekh

@email  : rk2845@columbia.edu
          prp2121@columbia.edu

"""

import csv
from getSongLyrics import getLyrics

def readSongNames():
    numFiles = 6
    for i in xrange(numFiles+1):
        f = open('../Data/Song'+str(i)+'.csv')
        csv_f = csv.reader(f)
        for row in csv_f:
            songName = row[0]
            artistName = row[1]
            getLyrics(songName,artistName)

if __name__ == '__main__':
    readSongNames()
