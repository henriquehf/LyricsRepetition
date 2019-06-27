from bs4 import BeautifulSoup as soup
from datetime import date
from datetime import timedelta
import datetime
from funcs import newFile, pegaMusicas, insereMusica
import time
start = time.time()

base_url = 'https://maistocadas.mus.br/'#billboard top 100 url are this followed by a date

today = 2019 #current year
curDate = 1959 #first year to be fetched

filename = "mais_tocadas.csv"
newFile(filename)

while(curDate < today): #future dates arent available
    f = open(filename, "a")
    my_url = base_url + str(curDate) + '/' #builds the url to be used
    print(my_url)
    musicas = pegaMusicas(my_url)
    for musica in musicas:
        position = musica.findAll("span", {"class": "es"})[0].text
        artist = musica.findAll("span", {"class": "mtits"})[0].text
        song = musica.findAll("span", {"class": "marts"})[0].text
        insereMusica(str(curDate), position, artist, song)
        # print(position, artist, song)
    f.close()
    curDate += 1 #gets to next year
    end = time.time()
    print(end - start)