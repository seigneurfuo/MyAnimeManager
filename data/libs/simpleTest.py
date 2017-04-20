import myanimelist_beautifulsoup
from bs4 import *
import urllib2

myanimelist_beautifulsoup.anime("8425")

print myanimelist_beautifulsoup.titre()
print myanimelist_beautifulsoup.annee()
print myanimelist_beautifulsoup.studio()
print myanimelist_beautifulsoup.image()
