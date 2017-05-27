# coding: utf8

import urllib, os, zipfile, shutil, sys
from distutils.version import LooseVersion


def extraction_maj():
    """ """

    # Extraction du zip
    print "Extraction ..."
    zipfile.ZipFile('./tmp/update.zip').extractall('./tmp/')

    # Copie des fichiers (copie tout les fichiers et dossiers de ./tmp/MyAnimeManager vers le dossier local de l'application
    for path, subdirs, files in os.walk("./tmp/MyAnimeManager-master/"):
        for name in files:
            cheminFichierSrc = os.path.join(path, name)
            cheminFichierDest = cheminFichierSrc.replace("./tmp/MyAnimeManager-master/", "./")
            cheminDossierDest = os.path.dirname(cheminFichierDest)
            
            # Si le chemin n'existe pas, on créer le chemin de fichiers
            if os.path.exists(cheminDossierDest) == False: 
                os.mkdir(cheminDossierDest)
                
            print "%s -> %s" %(cheminFichierSrc, cheminFichierDest)
            shutil.copyfile(cheminFichierSrc, cheminFichierDest)


def telechargement_maj():
    """ """
    
    # Url de la dernière version zippée du projet
    urlZip = "https://codeload.github.com/seigneurfuo/MyAnimeManager/zip/master"
    
    # Telechargement de la mise a jour
    print "Telechargement de la mise a jour ..."
    urllib.urlretrieve(urlZip, "./tmp/update.zip")


def preparation_dossiers():
    """ """

    # Nettoyage des fichiers temporaires (eviter une erreur si le dossier existe déja
    if os.path.exists("./tmp/update.zip"): shutil.rmtree("./tmp/")
    
    # Création du dossier temporaire
    print "Creation du dossier temporaire"
    os.mkdir("./tmp/") 


def maj_disponible(versionLocale=None):
    """ Retourne un booleen qui indique si une version plus récente est disponible en ligne """
    
    # Fichier contenant la dernière version disponible sur github
    urlVersion = "http://raw.githubusercontent.com/seigneurfuo/MyAnimeManager/master/version.txt"
    
    # Recherche de mises à jour
    print("Recherche de mises a jour...")
        
    # Essaye de se connecter en ligne pour trouver la version distante
    try:
        print "  Connection au serveur..."
        
        # Ouverture de l'url
        request = urllib.urlopen(urlVersion)
        
        # Lecture du fichier distant
        data = request.read()
        
        # Récupération de la version distante
        versionDistante = data.replace("\n", "")
        
        # Supression des variables inutiles
        del request, data
    
        # Vérification de la version
        
        # Si le script est lancé indépendemment
        if __name__ == "__main__":
            fichierVersionLocale = open("version.txt", "r")
            data = fichierVersionLocale.read()
        
            # Récupération de la version locale
            sys.path.append("./ressources/core")
    
            versionLocale = data.replace("\n", "")
            
            fichierVersionLocale.close()
        
        print "  Locale: %s" %versionLocale
        print "  Distante: %s" %versionDistante
        
        if LooseVersion(versionLocale) < LooseVersion(versionDistante):
            print "  Une nouvelle mise a jour est disponible: %s" %versionDistante
            return 0
        
        else:
            print "  L'application est a jour"
            return -1
        
    except Exception, error:
        print "  Impossible de contacter le serveur de mise a jour"
        print error
        return 1


if __name__ == "__main__":
    """ Fonction principale de l'application """

    # Si une maj est disponible et que l'argument noupdate n'est pas passé en parametres
    if maj_disponible() == 0:
        preparation_dossiers()
        telechargement_maj()
        extraction_maj()

        print "Vous pouvez maintenant profiter de votre application mise a jour !"
        raw_input()
