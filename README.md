# LyricsRepetition
There are three folders in this repository.

On the py folder are 7 py files in this. 
fun.py and func.py are the ones containing the main functions used by the other 5 files.
billboard_scraper.py is a web scraper for every weekly hot 100 ranking on billboard from 1959-2019.
maistocadas_scraper.py is a web scraper for every anual top 100 ranking on "Mais Tocadas" from 1959-2019.
lyric_scraper.py is a web scraper for the lyrics of the songs from the billboard rankings.
letra_scraper.py is a web scraper for the lyrics of the songs from the Mais Tocadas rankings,
calc.py calculates the repetitivness and some other metrics from the lyrics that were scraped.

On the db folder are 4 csv files. They contain the data gathered by the web scrapers. The web scrapers saved all the date to a MySQL server, but it was exported to csv so it could be easily added to GitHub.


On the queries folder are two files containing most of the sql queries used to analyse the data from the server. The result from the most important queries can be seen on the fourth chapter of the dissertation.

The dissertation is the TCC.pdf file.
