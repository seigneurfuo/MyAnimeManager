# -*- coding: utf8-*-
# Module qui permet de récupérer des infos sur MyAnimelist
# Auteur:                seigneurfuo
# Version:               Beta
# Date de création:      9 Juin 2016
# Dernière modification: 14 Juin 2016

import urllib
import urllib2
import os
import lassie
import re
import pprint
from bs4 import BeautifulSoup

retTitre = None
retAnnee = None
retStudio = None
retSequelle = None
retImageUrl = None

listeTitresAnimes = []
listeAnimesId = []

# En cours
def recherche_titre(animeTitre):
    global listeAnimesId, listeTitresAnimes
    
    baseUrl = "http://myanimelist.net/anime.php?q="
    animeTitreEncode = animeTitre.replace("+"," ")
    url = baseUrl + animeTitreEncode

    html = urllib2.urlopen(url).read()
    soup = BeautifulSoup(html, "html5lib")

    for lien in soup.find_all('a', class_="hoverinfo_trigger fw-b fl-l"):
        lienA = str(lien)
        lienB = lienA.split("href=\"")
        lienC = lienB[1]
        lienD = lienC.split("\"")
        lienE = lienD[0]
        animeUrl = lienE
        animeNomA = animeUrl.split("/")
        animeNom = animeNomA[5]

        animeMyAnimeListIdA = animeUrl.split("/")
        animeMyAnimeListId = animeMyAnimeListIdA[4]

        listeAnimesId.append(animeMyAnimeListId)
        listeTitresAnimes.append(animeNom)

    for _ in range(0, 10):
        print _, ":", listeTitresAnimes[_]
    print "--------------------"

    _ = int(raw_input("Animé a selectionner>"))
    animeMyAnimeListId = listeAnimesId[_]
    print animeMyAnimeListId
    anime(animeMyAnimeListId)

def anime(animeMyAnimeListId):
    try:
        baseUrl = "http://myanimelist.net/anime/" 
        url = baseUrl + str(animeMyAnimeListId)
        html = urllib2.urlopen(url).read()

        global retTitre, retAnnee, retStudio, retSequelle, retImageUrl

        #Titre
        htmlA = html.split("<span itemprop=\"name\">")
        htmlB = htmlA[1]
        htmlC = htmlB.split("</span>")
        retTitre = htmlC[0]

        # Annee
        htmlA = html.split("Aired:</span>")
        htmlB = htmlA[1]
        htmlC = htmlB.split("</div>")
        htmlD = htmlC[0]
        htmlE = htmlD.split(", ")
        htmlF = htmlE[1]
        htmlG = htmlF.split(" to")
        retAnnee = htmlG[0]

        # Studio
        htmlA = html.split("Studios:</span>")
        htmlB = htmlA[1]
        htmlC = htmlB.split("</div>")
        htmlD = htmlC[0]
        htmlE = htmlD.split(">")
        htmlF = htmlE[1]
        htmlG = htmlF.split("<")
        retStudio = htmlG[0]

        # Image
        lassieFetch = lassie.fetch(url)
        retImageUrl = str(lassieFetch["images"][0]["src"])

        del html, htmlA, htmlB, htmlC, htmlD, htmlE, htmlF, htmlG
    except: pass


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
