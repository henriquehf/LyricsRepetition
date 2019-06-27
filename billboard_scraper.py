from bs4 import BeautifulSoup as soup
from datetime import date
from datetime import timedelta
import datetime
from funcs import curWeek, getSongs, insertSong
import time
start = time.time()

base_url = 'https://www.billboard.com/charts/hot-100/'#billboard top 100 url are this followed by a date

today = date.today() #today
curDate = curWeek() #first week to be fetched
delta = timedelta(weeks = 1) #to facilitate getting the next week to be fetched

filename = "weekly_top_100_songs.csv"

while(curDate + delta < today): #future dates arent available
    f = open(filename, "a")
    my_url = base_url + str(curDate) #builds the url to be used
    print(my_url)
    p = 0
    mydivs = getSongs(my_url) #gets all song data from the url
    for div in mydivs: #writes the songs data to the database and to a csv file
        f.write(str(curDate) + ',' + str(div['data-rank']) + ',' + "\"" + str(div['data-artist']) + "\"" + ',' + "\"" + str(div['data-title']) + "\"" + '\n')
        a = 11
        while(a != 1):
            b = insertSong(str(curDate), str(div['data-rank']), str(div['data-artist']), str(div['data-title']))
            a -= 1
            if(b == 1):
                a = 1
                p += 1
        # print(curDate, div['data-rank'], div['data-artist'], div['data-title'])
    f.close()
    curDate += delta #gets to next weel
    end = time.time()
    print(p, end - start)
