# from bs4 import BeautifulSoup as soup
import datetime
from funcs import returnSongs, getLyric, saveLyrics
import time
start = time.time()

songs = returnSongs()
total = len(songs)
b = 0
worked = 0
tryed = 0
goodUrl = 0
# ten = 0
for song in songs:
    source, url, lyrics = getLyric(song)
    tryed += 1
    if(source != 0): goodUrl += 1
    a = 11
    while(a != 1):
        b = saveLyrics(song[0], source, url, lyrics)
        a -= 1
        if(b == 1):
            a = 1
            worked += 1
    end = time.time()
    print(worked, goodUrl, tryed, total)
    if(goodUrl != 0 and tryed != 0 and total != 0):
        print(str((worked/goodUrl)*100)+'%', str((worked/tryed)*100)+'%', str((tryed/total)*100)+'%', datetime.timedelta(seconds = end-start))
    # ten += 1
    # if(ten==10): break