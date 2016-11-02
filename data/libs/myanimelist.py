# -*- coding: utf8-*-
# Module qui permet de récupérer des infos sur MyAnimelist.net
# Auteur:                seigneurfuo
# Version:               0.8.5-Beta
# Date de création:      9 Juin 2016
# Dernière modification: 02 Novembre 2016

# Importation des librairies
import urllib
import urllib2
import os
import lassie
import re
from bs4 import BeautifulSoup

retTitre = None
retAnnee = None
retStudio = None
retSequelle = None
retImageUrl = None

listeTitresAnimes = []
listeAnimesId = []


#def recherche_titre(animeTitre):
    #global listeAnimesId, listeTitresAnimes
    
    #baseUrl = "http://myanimelist.net/anime.php?q="
    #animeTitreEncode = animeTitre.replace("+"," ")
    #url = baseUrl + animeTitreEncode

    #html = urllib2.urlopen(url).read()
    #soup = BeautifulSoup(html, "html5lib")

    #for lien in soup.find_all('a[class="hoverinfo_trigger fw-b fl-l"]'):
        

        #listeAnimesId.append(animeMyAnimeListId)
        #listeTitresAnimes.append(animeNom)

    #for _ in range(0, 10):
        #print _, ":", listeTitresAnimes[_]
    #print "--------------------"

    #_ = int(raw_input("Animé a selectionner>"))
    #animeMyAnimeListId = listeAnimesId[_]
    #print animeMyAnimeListId
    #anime(animeMyAnimeListId)


def anime(animeMyAnimeListId):
    try:
        baseUrl = "http://myanimelist.net/anime/" 
        url = baseUrl + str(animeMyAnimeListId)
        html = urllib2.urlopen(url).read()
        soup = BeautifulSoup(html, "html5lib")
        
        global retTitre, retAnnee, retStudio, retSequelle, retImageUrl

        # Titre
        resultats = soup.select('h1 span[itemprop="name"]') #class="header-right"
        retTitre = resultats[0].getText()

        # Annee
        resultats = soup.select('div[class="js-scrollfix-bottom"] div a') #class="header-right"
        retAnnee = resultats[10].getText().split(" ")[1]

        # Studio
        resultats = soup.select('div[class="js-scrollfix-bottom"] div a')
        retStudio = resultats[18].get("title")

        # Image
        resultats = soup.select('div[class="js-scrollfix-bottom"] div a img')
        retImageUrl = resultats[0].get("src")

        del resultats
    except Exception, e:
        print e


def titre():
    return retTitre


def annee():
    return retAnnee


def studio():
    return retStudio


def image():
    return retImageUrl


def telecharger_image(animeId, emplacement):
    filename = os.path.join(emplacement, str(animeId))
    urllib.urlretrieve(retImageUrl, filename)
