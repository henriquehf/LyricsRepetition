import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
from datetime import date
from datetime import timedelta
import datetime
import urllib
from urllib.request import urlopen as uReq
from urllib.request import Request, HTTPError
from bs4 import BeautifulSoup as soup
import re
import unidecode

def connect():
	return mysql.connector.connect(host='localhost',
								database='Songs',
								user='root',
								password='root')

def insertSong(week, position, artist, song):
	try:
		connection = connect()

		sql_insert_query = 		'INSERT ignore INTO songss (artist, song) values ("' + artist.replace('"',"'") + '", "' + song.replace('"',"'") + '");'

		cursor = connection.cursor()
		result  = cursor.execute(sql_insert_query)
		# cursor.execute("SELECT id FROM songss where artist = '" + artist + "' and song = '" + song + "' limit 1")
		cursor.execute('SELECT id FROM songss where artist = "' + artist.replace('"',"'") + '" and song = "' + song.replace('"',"'") + '" limit 1')
		myresult = cursor.fetchone()

		# sql_insert_query = 		'INSERT INTO billboard (week, position, song) SELECT * FROM (SELECT "' + week + '", ' + position + ', "' + str(myresult[0]) + '") AS tmp WHERE NOT EXISTS (SELECT id FROM billboard WHERE week = "' + week + '" and position = ' + position + ') LIMIT 1;'
		sql_insert_query = 		'INSERT INTO billboard (week, position, song) values ("' + week + '", ' + position + ', "' + str(myresult[0]) + '");'

		cursor = connection.cursor()
		result  = cursor.execute(sql_insert_query)
		connection.commit()
		print(week, position, artist, song)
		p = 1
	except mysql.connector.Error as error :
		connection.rollback() #rollback if any exception occured
		p = 0
	finally:
		#closing database connection.
		if(connection.is_connected()):
			cursor.close()
			connection.close()
	return p

def insereMusica(year, position, artist, song):
	try:
		connection = connect()

		sql_insert_query = 		'INSERT ignore INTO songss (artist, song) values ("' + artist.replace('"',"'") + '", "' + song.replace('"',"'") + '");'

		cursor = connection.cursor()
		result  = cursor.execute(sql_insert_query)
		# cursor.execute("SELECT id FROM songss where artist = '" + artist + "' and song = '" + song + "' limit 1")
		cursor.execute('SELECT id FROM songss where artist = "' + artist.replace('"',"'") + '" and song = "' + song.replace('"',"'") + '" limit 1')
		myresult = cursor.fetchone()

		# sql_insert_query = 		'INSERT INTO billboard (week, position, song) SELECT * FROM (SELECT "' + week + '", ' + position + ', "' + str(myresult[0]) + '") AS tmp WHERE NOT EXISTS (SELECT id FROM billboard WHERE week = "' + week + '" and position = ' + position + ') LIMIT 1;'
		sql_insert_query = 		'INSERT INTO maistocadas (year, position, song) values ("' + year + '", ' + position + ', "' + str(myresult[0]) + '");'

		cursor = connection.cursor()
		result  = cursor.execute(sql_insert_query)
		connection.commit()
		print(year, position, artist, song)
		p = 1
	except mysql.connector.Error as error :
		connection.rollback() #rollback if any exception occured
		p = 0
	finally:
		#closing database connection.
		if(connection.is_connected()):
			cursor.close()
			connection.close()
	return p

def curWeek():
	connection = connect()
	mycursor = connection.cursor()
	mycursor.execute("SELECT week FROM billboard order by id desc")
	myresult = mycursor.fetchone()
	if(connection.is_connected()):
		mycursor.close()
		connection.close()
	if(myresult): return datetime.datetime.strptime(str(myresult[0]), '%Y-%m-%d').date()+timedelta(weeks = 1)#Returns the week following the last to be inserted on the dataset
	else: #If nothing has been inserted it returns the week of 1959-01-05, chosen as the first of the dataset, and creates a csv file with a header
		newFile("weekly_top_100_songs.csv")
		return datetime.datetime.strptime('1959-01-05', '%Y-%m-%d').date()

def returnSongs():
	connection = connect()
	mycursor = connection.cursor()
	mycursor.execute("select "+
	"songss.id as id, "+
	"songss.artist as artist, "+
	"songss.song as song, "+
	"sum(101-billboard.position) as points "+
	"from billboard "+
	"inner join songss "+
	"on billboard.song = songss.id "+
	"where songss.source is null "+
	"group by billboard.song "+
	"order by sum(101-billboard.position) desc;")
	myresult = mycursor.fetchall()
	#coisas novas
	# mycursor.execute("select count(*) from (select count(*) from songss inner join billboard on songss.id = billboard.song group by songss.id) as b;")
	# totalSongs = mycursor.fetchall()

	if(connection.is_connected()):
		mycursor.close()
		connection.close()
	return myresult

def returnMusicas():
	connection = connect()
	mycursor = connection.cursor()
	mycursor.execute("select "+
	"songss.id as id, "+
	"songss.artist as artist, "+
	"songss.song as song "+
	"from maistocadas "+
	"inner join songss "+
	"on maistocadas.song = songss.id "+
	"where songss.source is null "+
	"group by songss.id "+
	"order by songss.id desc;")
	myresult = mycursor.fetchall()
	#coisas novas
	# mycursor.execute("select count(*) from (select count(*) from songss inner join billboard on songss.id = billboard.song group by songss.id) as b;")
	# totalSongs = mycursor.fetchall()

	if(connection.is_connected()):
		mycursor.close()
		connection.close()
	return myresult

def get_url_data(url = ""):#places some header information on the urlopen so the targeted website believes its a person and not a machine acessing it
    try:
        request = Request(url, headers = {'User-Agent' :\
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36"})
        response = uReq(request)
        return response
    except HTTPError:
        return None

def getSoupData(my_url):
	try:
		uClient = get_url_data(my_url)
		if(uClient):
			page_url = uClient.read()
			uClient.close()
			return soup(page_url, "html.parser")
		else: return None
	except HTTPError:
		return None

def getSongs(my_url):#gets the data from the given url and returns a list with all div items with a chart-list-item class (the elements with the top 100 information)
	page_soup = getSoupData(my_url)
	return page_soup.findAll("div", {"class": "chart-list-item"})

def pegaMusicas(my_url):#gets the data from the given url and returns a list with all div items with a chart-list-item class (the elements with the top 100 information)
	page_soup = getSoupData(my_url)
	return page_soup.findAll("li", {"class": "line"})

def newFile(name):
	f = open(name, "w")
	header = "week, position, artist, song\n"
	f.write(header)
	f.close()

def getMetroLyricsFromSoup(soup):
	lyric = []
	l = soup.findAll("div", {"class": "js-lyric-text"})
	if(len(l) != 0):
		v = l[0].findAll("p", {"class": "verse"})
		for verse in v:
			lyric.append(verse.text)
		lyrics = "".join(lyric)
		return lyrics
	else: return None

def getSongLyricsFromSoup(soup):
	lyrics = soup.findAll("p", {"id": "songLyricsDiv"})
	if(len(lyrics) != 0): return(lyrics[0].text)
	else: return None

def getVagalumeLyricsFromSoup(soup):
	lyrics = soup.findAll("div", {"id": "lyrics"})
	if(len(lyrics) != 0):
		for br in lyrics[0].find_all("br"):
			br.replace_with("\n")
		return lyrics[0].text
	else: return None

def getLyric(song):
	artist = re.split(" featuring | feat | feat. | with | duet | and ", song[1].lower())
	char = artist[0].replace("the ", "")
	metroURL = "http://metrolyrics.com/" + re.sub('[^\w\s]+', '', song[2]).replace(" ", "-").lower() + "-lyrics-" + re.sub('[^\w\s]+', '', artist[0]).replace(" ", "-") + ".html"
	# print(metroURL)
	metroURL = unidecode.unidecode(metroURL)
	songL = 0
	vagaL = 0
	noL = 0
	source = 0
	# print(metroURL)
	soup = getSoupData(metroURL)
	if(soup):
		# print(metroURL)
		lyrics = getMetroLyricsFromSoup(soup)
		if(lyrics):
			source = 1
			url = metroURL
		else: songL = 1
	else: songL = 1
	if(songL == 1):
		songURL = "http://songlyrics.com/" + re.sub('[^\w\s]+', '', artist[0]).replace(" ", "-") + "/" + re.sub('[^\w\s]+', '', song[2]).replace(" ", "-").lower()  + "-lyrics"
		# print(songURL)
		songURL = unidecode.unidecode(songURL)
		soup = getSoupData(songURL)
		if(soup):
			# print(songURL)
			lyrics = getSongLyricsFromSoup(soup)
			if(lyrics):
				source = 2
				url = songURL
			else: vagaL = 1
		else: vagaL = 1
		if(vagaL == 1):
			# modeURL = "http://www.lyricsmode.com/lyrics/" + char + "/" + re.sub('[^\w\s]+', '', artist[0]).replace(" ", "-") + "/" + re.sub('[^\w\s]+', '', song[2]).replace(" ", "-").lower() + ".html"
			# print(modeURL)
			# soup = getSoupData(modeURL)
			vagaURL = "https://www.vagalume.com.br/" + re.sub('[^\w\s]+', '', artist[0]).replace(" ", "-") + "/" + re.sub('[^\w\s]+', '', song[2]).replace(" ", "-").lower() + ".html"
			vagaURL = unidecode.unidecode(vagaURL)
			# print(vagaURL)
			soup = getSoupData(vagaURL)
			if(soup):
				# print(vagaURL)
				lyrics = getVagalumeLyricsFromSoup(soup)
				if(lyrics):
					source = 3
					url = vagaURL
				else: noL = 1
			else: noL = 1
			if(noL == 1):
				source = 0
				lyrics = None
				url = None
	return source, url, lyrics


def pegaLetra(song):
	artist = re.split(" featuring | feat | feat. | with | duet | and ", song[1].lower())
	char = artist[0].replace("the ", "")
	aux = artist[0].split()
	artistt = " ".join(aux)
	aux = song[2].split()
	songg = " ".join(aux)
	# while(artist[0] == " "):
	# 	artist[0] = artist[0][1:]
	# while(artist[0] == " "):
		# song[2] = song[2][1:]
	vagaURL = "https://www.vagalume.com.br/" + re.sub('[^\w\s]+', '', artistt).replace(" ", "-") + "/" + re.sub('[^\w\s]+', '', songg).replace(" ", "-").lower() + ".html"
	vagaURL = unidecode.unidecode(vagaURL)
	#print(vagaURL)
	songL = 0
	vagaL = 0
	noL = 0
	source = 0
	# print(metroURL)
	soup = getSoupData(vagaURL)
	if(soup):
		# print(metroURL)
		lyrics = getVagalumeLyricsFromSoup(soup)
		if(lyrics):
			source = 3
			url = vagaURL
		else: songL = 1
	else: 
		source = 0
		lyrics = None
		url = None
	return source, url, lyrics

def saveLyrics(idd, source, url, lyrics):
	# print(lyrics)
	try:
		connection = connect()
		cursor = connection.cursor()
		if(source != 0 and isinstance(lyrics, str)):
			# escapedLyrics = connection._cmysql.escape_string(lyrics)
			p = 1
			info = (str(url), source, lyrics, idd)
			result  = cursor.execute("update songss set link = %s, source = %s, text = %s where id = %s;", info)
			# result  = cursor.execute(sql_update_query)
		else:
			p = 0
			sql_update_query = 		"update songss set source = 0 where id = " + str(idd) + ";"
			result  = cursor.execute(sql_update_query)
		connection.commit()
	except mysql.connector.Error as error :
		connection.rollback() #rollback if any exception occured
		p = 0
	finally:
		#closing database connection.
		if(connection.is_connected()):
			cursor.close()
			connection.close()
	return p

def returnSongIDs():
	connection = connect()
	mycursor = connection.cursor()
	mycursor.execute("select "+
	"songss.id as id "+
	"from songss "+
	"where songss.text is not null and songss.rep is null;")
	myresult = mycursor.fetchall()
	if(connection.is_connected()):
		mycursor.close()
		connection.close()
	return myresult

def returnLyrics(idd):
	connection = connect()
	info = (idd)
	mycursor = connection.cursor()
	mycursor.execute("select "+
	"songss.text as lyrics "+
	"from songss "+
	"where songss.id = %s;", idd)
	myresult = mycursor.fetchall()
	if(connection.is_connected()):
		mycursor.close()
		connection.close()
	return myresult[0][0]

def saveCalcs(idd, rep, size, equal, hw, dictionary):
	# print(idd, rep, size, equal, hw)
	p1 = saveToSongss(idd, rep, size, equal, hw)
	p2 = saveToDictionary(idd, dictionary)
	return p1, p2

def saveToSongss(idd, rep, size, equal, hw):
	try:
		connection = connect()
		cursor = connection.cursor()
		info = (size, equal, rep, hw, idd)
		# print(info)
		result  = cursor.execute("update songss set effective_size = %s, comp_dec_equal = %s, rep = %s, hard_words = %s where id = %s;", info)
		# info = (str(url), source, lyrics, idd)
		# result  = cursor.execute("update songss set link = %s, source = %s, text = %s where id = %s;", info)
		connection.commit()
		p = 1
	except mysql.connector.Error as error :
		connection.rollback() #rollback if any exception occured
		p = 0
	finally:
		#closing database connection.
		if(connection.is_connected()):
			cursor.close()
			connection.close()
	return p

def saveToDictionary(idd, dictionary):
	try:
		connection = connect()
		cursor = connection.cursor()
		for word in dictionary:
			info = (idd, word[0], word[1])
			result  = cursor.execute("INSERT ignore INTO dictionary (song, word, amount) values (%s, %s, %s);", info)
			#sql_insert_query = 		'INSERT ignore INTO dictionary (song, word, amount) values (%s, %s, %s);'
		connection.commit()
		p = 1
	except mysql.connector.Error as error :
		connection.rollback() #rollback if any exception occured
		p = 0
	finally:
		#closing database connection.
		if(connection.is_connected()):
			cursor.close()
			connection.close()
	return p

# accented_string = ''
# accented_string = accented_string + 'Muaua'
# # accented_string is of type 'unicode'
# unaccented_string = unidecode.unidecode(accented_string)
# print(accented_string, unaccented_string)


