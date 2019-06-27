import datetime
from funcs import returnSongIDs, returnLyrics, saveCalcs
from fun import repetCalculator
import time
start = time.time()

ids = returnSongIDs()
#songs = returnMusicas()
total = len(ids)
b = 0
worked1 = 0
worked2 = 0
tryed = 0
# ten = 0
for idd in ids:
    #print(song)
    lyric = returnLyrics(idd)
    # print(lyric)
    rep, size, equal, hw, dictionary = repetCalculator(lyric)
    #print(rep, size, equal)
    # print(rep, size, equal, hw)
    # print(idd[0], rep, size, equal, hw)
    p1, p2 = saveCalcs(idd[0], rep, size, equal, hw, dictionary)
    #print(dictionary)
    worked1 += p1
    worked2 += p2
    tryed += 1
    # tryed += 1
    # if(source != 0): goodUrl += 1
    # a = 11
    # while(a != 1):
    #     b = saveLyrics(song[0], source, url, lyrics)
    #     a -= 1
    #     if(b == 1):
    #         a = 1
    #         worked += 1
    end = time.time()
    print(worked1, worked2, tryed, total, datetime.timedelta(seconds = end-start))
    # if(goodUrl != 0 and tryed != 0 and total != 0):
    #     print(str((worked/goodUrl)*100)+'%', str((worked/tryed)*100)+'%', str((tryed/total)*100)+'%', datetime.timedelta(seconds = end-start))
    # ten += 1
    # if(ten==10): break