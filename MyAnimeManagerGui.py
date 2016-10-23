#!/usr/bin/python2.7
# -*- coding: utf8 -*- 

# Logging
import logging
log = logging.getLogger()
log.setLevel(logging.DEBUG)


# Librairies standards
import sys
import os
import re
import sqlite3
import pprint
import urllib
from datetime import date, datetime, time, timedelta

sys.path.append("./data/libs")
# Librairies de tierces-parties
import myanimelist
import devtool; devtool.show_stats(sys.argv[0])


# Importation de pyQt
try:
    import PyQt4.QtGui
    import PyQt4.QtCore
    import PyQt4.uic.loadUiType
except:
    log.error("L'application n'arrive pas a trouver pyQt !")
    log.error("Veuillez vous reporter aux notes d'insatallation.")


# Informations sur l'application
__titre__                = "MyAnimeManager"
__version__              = "0.18.%s" % devtool.buildNumber
__auteur__               = "seigneurfuo"
__db_version__           = 5
__dateDeCreation__       = "12/06/2016"
__derniereModification__ = "21/10/2016"


# Création d'un formateur qui va ajouter le temps, le niveau de chaque message quand on écrira un message dans le log
formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(message)s') 


# Les lignes suivantes permettent de rediriger chaque écriture de log sur la console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)
log.addHandler(console_handler)


# Détails
toDo = ["Continuer la fonction de MAJ de la base de donnée pour les prochaines versions",
        "Vider le champ de recherche et MAL lorsque a la fin de l'édition d'un animé",
        "Ajouter des préférences, afin de modifier: l'emplacement de la bdd, l'emplacement des fichiers images",
        "Coder la fenetre directement dans le code - sans utilisation de QtDesign",
        "Ou alors enregistrer le contenu du fichier d'interface dans une docstring dans le code",
        "Renommer les noms des élements génériques. Exemple: Bouton1, bouton2...", 
		"Empécher de remplir les informations d'un animé si il n'a pas d'indentifiant",
		"Les animés avec \":\" dans l'url bloquent sur une erreur 404"]


# Fonctions générale a l'application
def creation_de_la_bdd():
    log.info("Création de la base de donnees")


# Code SQL pour créer la table anime
    curseur.execute(
    """CREATE TABLE anime(
     animeId TEXT PRIMARY KEY NOT NULL,
     animeAjout TEXT,
     animeTitre VARCHAR(100) NOT NULL,
     animeAnnee INT,
     animeStudio VARCHAR(30),
     animeFansub VARCHAR(30),
     animeEtatVisionnage INT,
     animeFavori TEXT,
     animeDateAjout TEXT,
     animeNbVisionnage INT,
     animeNotes TEXT)
     """)



# Code SQL pour créer la table planning
    curseur.execute(
    """
    CREATE TABLE planning (
    planningDate TEXT NOT NULL,
    planningIdentifiantJournalier TEXT,
    planningAnime TEXT,
    planningEpisode TEXT)
    """)

# Code SQL pour créer la table informations


# Classe de la fenetre principale
class Menu(PyQt4.QtGui.QMainWindow, PyQt4.uic.loadUiType("./data/gui.ui")[0]): # Chargement des interfaces depuis les fichiers
    def __init__(self, parent=None):
        PyQt4.QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)

        # Variables qui enregistre les modifications (Permet de ne pas afficher la fenetre d'enregistrement si rien n'a été modifié)
        self.modifications = False
        
        # Gestion des evenements (onglet liste)
        #self.listWidget.selectionModel().selectionChanged.connect(self.liste_afficher)
        #self.listWidget.selectionModel().currentRowChanged.connect(self.liste_afficher)
        self.listWidget.itemClicked.connect(self.liste_afficher)
        self.boutonEnregistrer.clicked.connect(self.liste_enregistrer)
        self.boutonAnnuler.clicked.connect(self.liste_rafraichir)
        self.boutonCompleter.clicked.connect(self.liste_remplir_myanimelist)
        self.rechercheEntry.textChanged.connect(self.liste_recherche)
        self.rechercheViderBoutton.clicked.connect(self.liste_recherche_vider)
        self.rechercheFavorisBoutton.clicked.connect(self.liste_recherche_favoris)
        
        self.boutonAjouterAnime.clicked.connect(self.liste_rafraichir)
        self.boutonSupprimerAnime.clicked.connect(self.liste_supprimer)

        # Onglet planning
        self.planningCalendrier.clicked.connect(self.planning_afficher)
        self.planningCalendrier.selectionChanged.connect(self.planning_afficher)

        self.boutonPlanningInserer.clicked.connect(self.planning_animes_vus_inserer)
        self.listWidget_3.itemDoubleClicked.connect(self.planning_animes_vus_inserer)
        
        self.boutonPlanningReset.clicked.connect(self.planning_aujourdhui)
        self.boutonPlanningSauvegarder.clicked.connect(self.planning_enregistrer)

        # Onglet outils
        self.testButton.clicked.connect(self.outils_liste_personnages_favoris)
        self.pushButton.clicked.connect(self.outils_calcul_temps_calcul)
        
        # Onglet préférences
        self.pushButton_3.clicked.connect(self.reset)

        # Remplace le numéro de version A propos
        self.label_7.setText("version " + str(__version__))

    # Evenement de fermeture de l'application
        self.closeEvent = self.fermer
        
        # Fonction a lancer en premier
        self.liste_rafraichir()
        self.planning_afficher()
        self.animes_vus_afficher()
        self.outils_liste_personnages_favoris()


    # La fonction qui efface les entrés (les instructions auraient pus etres contenues dans liste_affiche mais je souhaitais séparer les deux blocs)
    def liste_rafraichir(self, titreRecherche=False, favorisRecherche=False):
        # Image de l'animé vide
        myPixmap = PyQt4.QtGui.QPixmap("./data/ekHFstR.png")
        image = myPixmap.scaled(self.label_5.size(), )
        self.label_5.setPixmap(image)

        # On vide la liste et les entrées
        self.listWidget.clear()
        self.idEntry.setText(str())
        self.ajoutEntry.setText(str())
        self.titreEntry.setText(str())
        self.anneeEntry.setText(str())
        self.studioEntry.setText(str())
        self.fansubEntry.setText(str())
        self.malEntry.setText(str())
        self.notesEntry.setText(str())

        # Remise à zéro de la spinbox pour le nombre de visionnages
        self.spinBox.setValue(0)

        # Remise par défault des boutons radio
        self.radiobutton0.setChecked(False)
        self.radiobutton1.setChecked(False)
        self.radiobutton2_2.setChecked(False)
        self.radiobutton2.setChecked(True)
        
        self.favorisNonRadio.setChecked(True)
        
        # Nettoyage du champ MAL
        self.malEntry.setText(str())

        # Si rien n'est rentré dans la barre de recherche:
        if titreRecherche != False and titreRecherche !="" :  
            log.info("Filtrage de la liste: Par correspondance")
            
            # On afiche la liste normale
            curseur.execute("SELECT * FROM anime WHERE animeTitre LIKE('%s%s%s') ORDER BY animeTitre" %("%", titreRecherche, "%"))
                
        else :
            # Si on veut afficher la liste des favoris
            if favorisRecherche == False:
                log.info("Affichage normal de la liste des animes")
                curseur.execute("SELECT * FROM anime ORDER BY animeId")
            
            # Si on veut afficher la liste normale
            else:
                log.info("Filtrage de la liste: Afficher les favoris")
                curseur.execute("SELECT * FROM anime WHERE animeFavori = '1' ORDER BY animeId")
        
            
        resultats = curseur.fetchall()
        log.info("Anime rechargés %s" %len(resultats))
        
        # Remplissage de la liste
        for anime in resultats:
            ligne = PyQt4.QtGui.QListWidgetItem(anime["animeTitre"])
            self.listWidget.addItem(ligne)


    # Fonction qui permet de rechercher un animé dans la liste grace a son nom
    def liste_recherche(self):
        recherche = self.rechercheEntry.text()

        # Si le recherche est vide on ne l'active pas
        self.liste_rafraichir(titreRecherche = recherche)


    # Fonction qui permet de vider la liste de recherche
    def liste_recherche_vider(self):
        self.rechercheEntry.setText(str())
        self.liste_rafraichir()
        
    
    # Fonction qui affiche les animés favoris
    def liste_recherche_favoris(self):
        self.liste_rafraichir(favorisRecherche=True)


    # Fonction qui affiche les information pour l'animé sélectionné
    def liste_afficher(self):
        animeTitre = [str(x.text()) for x in self.listWidget.selectedItems()]
        
        curseur.execute("SELECT * FROM anime WHERE animeTitre = '%s'" %animeTitre[0])

        # Pour les résultats trouvés en SQL (1 max car on recherche l'anime en fonction de son titre)
        for ligne in curseur.fetchall():
            # Listes d'entrées 
            self.idEntry.setText(str(ligne["animeId"]).replace("None", "")) # .replace("None", "")) Permet de ne pas afficher lorsq'une valeur est NULL
            self.ajoutEntry.setText(str(ligne["animeDateAjout"]).replace("None", ""))
            self.titreEntry.setText(str(ligne["animeTitre"]).replace("None", ""))
            self.anneeEntry.setText(str(ligne["animeAnnee"]).replace("None", ""))
            self.studioEntry.setText(str(ligne["animeStudio"]).replace("None", ""))
            self.fansubEntry.setText(str(ligne["animeFansub"]).replace("None", ""))
            self.notesEntry.setText(str(ligne["animeNotes"]).replace("None", ""))

            # Spinbox
            if ligne["animeNbVisionnage"] == None:
                self.spinBox.setValue(0)
            else:
                self.spinBox.setValue(ligne["animeNbVisionnage"])

            # Boutons radios visionnage
            # Animé Terminé
            if ligne["animeEtatVisionnage"] == "0":
                self.radiobutton0.setChecked(True)

            # Animé en cours
            elif ligne["animeEtatVisionnage"] == "1":
                self.radiobutton1.setChecked(True)

            # Animé a voir
            elif ligne["animeEtatVisionnage"] == "2":
                self.radiobutton2_2.setChecked(True)

            # Animé indéfini
            elif ligne["animeEtatVisionnage"] == "3" or ligne["animeEtatVisionnage"] == None:
                self.radiobutton2.setChecked(True)
                
                
            # Boutons radios favori
            if ligne["animeFavori"] == "1":
                self.favorisOuiRadio.setChecked(True)
            else:
                self.favorisNonRadio.setChecked(True)
                

        # Charge et affiche l'image de l'anime
        image = str(ligne["animeId"])
        chemin = os.path.join(dossier, image)
        global listeAfficherImageChemin
        listeAfficherImageChemin = chemin
        
        log.info("Image de couverture: %s" %chemin)

        # Charge et affiche l'image
        myPixmap = PyQt4.QtGui.QPixmap(chemin)
        image = myPixmap.scaled(self.label_5.size(), PyQt4.QtCore.Qt.IgnoreAspectRatio, PyQt4.QtCore.Qt.SmoothTransformation)
        self.label_5.setPixmap(image)


    # Fonction qui recherche un identifiant ou un titre d'animé sur MAL
    def liste_remplir_myanimelist(self):
        # Récupère l'identifiant ou le titre entré dans l'entrée MAL
        texte = self.malEntry.text()
        
        # Si le texte récupéré correspond a un identifiant mal (chiffres uniquement)
        if re.findall("^-?[0-9]+$", texte):
            idMyAnimeList = self.malEntry.text()
            myanimelist.anime(str(idMyAnimeList))
        
        else:
            # Sinon, il s'agit d'un titre a rechercher
            titreMyAnimeList = self.malEntry.text()
            myanimelist.recherche_titre(str(titreMyAnimeList))

        # Remplissage des informations
        self.titreEntry.setText(myanimelist.titre())
        self.anneeEntry.setText(myanimelist.annee())
        self.studioEntry.setText(myanimelist.studio())

        # Téléchargement de l'image d'illustration
        animeId = str(self.idEntry.text())
        myanimelist.telecharger_image(animeId, "./data/covers/")

        # Mise a jour de l'image
        chemin = os.path.join(dossier, animeId)
        log.info("Cover: %s" %chemin)
        
        # Charge et affiche l'image
        myPixmap = PyQt4.QtGui.QPixmap(chemin)
        image = myPixmap.scaled(self.label_5.size(), PyQt4.QtCore.Qt.IgnoreAspectRatio, PyQt4.QtCore.Qt.SmoothTransformation)
        self.label_5.setPixmap(image)


    # Fonction qui enregistre les données des animés dans la bdd
    def liste_enregistrer(self):
        # Entrées (entry)
        animeId = self.idEntry.text()
        
        # Si un identifiant a été rentré
        if animeId != "" or re.findall("^-?[0-9]+$", animeId):
            animeTitre = self.titreEntry.text()
            animeDateAjout = self.ajoutEntry.text()
            animeAnnee = self.anneeEntry.text()
            animeStudio = self.studioEntry.text()
            animeFansub = self.fansubEntry.text()
            animeNbVisionnage = self.spinBox.value()
            animeNotes = str(self.notesEntry.toPlainText()).decode("utf-8") 

            # Etat du visionnage (boutons radio)
            if self.radiobutton0.isChecked(): animeVisionnage = "0"
            elif self.radiobutton1.isChecked(): animeVisionnage = "1"
            elif self.radiobutton2_2.isChecked(): animeVisionnage = "2"
            elif self.radiobutton2.isChecked(): animeVisionnage = "3"
                
            # Animé favoris ?
            if self.favorisNonRadio.isChecked(): 
                animeFavori = "0"
            elif self.favorisOuiRadio.isChecked(): 
                animeFavori = "1"

            # Génération de la command SQL
            curseur.execute("INSERT OR REPLACE INTO anime (animeId, animeDateAjout, animeTitre, animeAnnee, animeStudio, animeFansub, animeEtatVisionnage, animeFavori, animeNbVisionnage, animeNotes) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" %(animeId, animeDateAjout, animeTitre, animeAnnee, animeStudio, animeFansub, animeVisionnage, animeFavori, animeNbVisionnage, animeNotes))

            # On indique a l'application que quelque chose a été modifié
            self.modifications = True
                
            # Rafraichi après avoir enregistré
            self.liste_rafraichir()
            self.animes_vus_afficher()
            
        # Si l'identifiant n'a pas été rempli
        else:
            # Remplacer la fenetre par une version 1 bouton.
            avertissement = PyQt4.QtGui.QMessageBox.information(self, "Message", "Veuillez entrer un identifiant valide !", "Continuer")     

    def liste_supprimer(self):
        animeTitre = [str(x.text()) for x in self.listWidget.selectedItems()]
        
        # Si un élémément a bien été séléctionné dans la liste
        if animeTitre: 
            curseur.execute("DELETE FROM anime WHERE animeTitre = '%s'" %animeTitre[0])

            # On indique a l'application que quelque chose a été modifié
            self.modifications = True
            
            # Rafraichi après avoir supprimé
            self.liste_rafraichir()
            self.animes_vus_afficher()
        

# Fonctions de l'onglet planning

    def animes_vus_afficher(self):
        # On vide la liste des animés
        self.listWidget_3.clear()
        
        # On éxécute la commande sql qui retourne les animés en cours de visionnage
        curseur.execute("SELECT * FROM anime WHERE animeEtatVisionnage = 1 ORDER BY animeId")
        animes_vus = curseur.fetchall()
        
        # Remplissage de la liste
        for anime_vu in animes_vus:
            ligne = PyQt4.QtGui.QListWidgetItem(anime_vu["animeTitre"])
            self.listWidget_3.addItem(ligne)


    # Fonction qui ajoute le titre d'un animé en cours de visionnage dans la boite d'entrée du journal
    def planning_animes_vus_inserer(self):
        # Sauvegarde du texte actuel
        ancienTexte = self.planningEntry.toPlainText()
        animeTitre = [str(x.text()) for x in self.listWidget_3.selectedItems()]
        animeTitre = animeTitre[0]
        
        # Si le planning est vide
        if ancienTexte == "":
            nouveauTexte = str(animeTitre + "-Ep ")
        
        # Sinon, on affiche en gardant l'ancien texte
        else:
            nouveauTexte = ancienTexte + "\n" + str(animeTitre + "-Ep ")

        #Affichage du nouveau titre
        self.planningEntry.setText(nouveauTexte)


    # Fonction qui affiche les animés vus en fonction de la date sélectionnée sur le calendrier
    def planning_afficher(self):
        # Vide la boite d'entrée
        self.planningEntry.setText(str())
        
        # Date correspond a la date sur le jour selectionné sur le calendrier
        date = self.planningCalendrier.selectedDate().toPyDate()
        
        # Recherche dans la base de donnée la liste des animés vu le jour de la date sélectionnée (le tri ce fait en fonction del'indentifiant journalier)
        # La table planningAnime ne contient que l'identifiant de l'animé. Le nom est récupéré grace a une jointure entre la table anime et planning
        curseur.execute("SELECT * FROM planning, anime WHERE planningDate = \"%s\" AND planning.planningAnime = anime.AnimeId ORDER BY planningIdentifiantJournalier ASC" %date)

        # La ligne du dessous n'est plus vrait avec les identifiants journaliers
        # Pour les résultats trouvés en SQL (1 max car on recherche l'anime en fonction de son titre)
        animes = ""
        for ligne in curseur.fetchall():
            # Ajout les animés dans le label text
            animes = animes + ligne["animeTitre"] + "-Ep " + ligne["planningEpisode"] + "\n"
        
        # Colle la liste des animés
        self.planningEntry.setText(str(animes))


    # Fonction qui séléctionne la date actuelle sur le calendrier
    def planning_aujourdhui(self):
        # Demande a Qt la date du jour
        aujourdhui = PyQt4.QtCore.QDate.currentDate ()
        
        # Affiche le caldendrier à la date du jour
        self.planningCalendrier.setSelectedDate(aujourdhui)
        

    # Fonction qui enregistre le planning dans la bdd
    def planning_enregistrer(self):
        planningDate = str(self.planningCalendrier.selectedDate().toPyDate())
        planningAnime = str(self.planningEntry.toPlainText())

        # Supprime les entrées du jour dans la base SQL
        curseur.execute("DELETE FROM planning WHERE planningDate = '%s'" %(planningDate))

        # Sépare les lignes (avec le signe \n)
        lignes = planningAnime.split("\n")
        
        # Identifiant de planning journalier, pour identifier chauque entrée dans une journée
        planningIdentifiantJournalier = 0
        
        # Pour chaque ligne dans l'entrée texte
        for ligne in lignes:
            # Si la ligne est vide, on ne fait rien
            if ligne != "":
                # Incrémente le numéro de ligne
                planningIdentifiantJournalier += 1
                
                # Coupe le nom de l'animé et l'épisode en cours
                champs = ligne.split("-Ep ")
                animeTitre = champs[0]
                
                # On récupère l'identifiant correppondant au titre
                curseur.execute("SELECT * FROM anime WHERE animeTitre = '%s'" %(animeTitre))
                for ligne in curseur.fetchall():
                    animeId = ligne["animeId"]
                    
                
                animeEpisode = champs[1]
                
                # Ajoute ou met a jour les entrées dans la table planning.
                curseur.execute("INSERT OR REPLACE INTO planning (planningDate, planningIdentifiantJournalier, planningAnime, planningEpisode) VALUES ('%s', '%s', '%s', '%s')" %(planningDate, planningIdentifiantJournalier, animeId, animeEpisode))
                
    
        # On indique a l'application que quelque chose a été modifié
        self.modifications = True


# Fonctions de l'onglet outils
    # Fonction qui permet de calculer l'heure de fin d'un visionnage a partir du nombre d'épisodes a voir
    def outils_calcul_temps_calcul(self):
        # Effacement de la liste
        self.listWidget_2.clear()

        # Récupération du contenu des spinbox
        nombreEpisodes = self.spinBox_2.value()
        dureeEpisode = self.spinBox_3.value()
        
        plageA = datetime.now()

        for x in range(0, nombreEpisodes):
            plageB = plageA + timedelta(minutes = dureeEpisode)
            heure = "%02d - %02d:%02d -> %02d:%02d" %(x + 1, plageA.hour, plageA.minute, plageB.hour, plageB.minute) # Chaine qui seras affichée
            plage = PyQt4.QtGui.QListWidgetItem(heure) # Création de l'élément
            self.listWidget_2.addItem(plage) #Ajout de l'élément a la liste
            plageA = plageB # Décale la plage


    # Fonction qui permet de télécharger des images et de changer le nom du fichier enregistré
    def telechargement_image(self, url, filename):
        # Identifiant du numéro de page
        pageId = self.spinboxPageId.value()
        filename = "./data/characters/%s_%s" %(pageId, filename)
        urllib.urlretrieve(url, filename)


    # Fonction qui affiche les personnages préférés
    def outils_liste_personnages_favoris(self):
        waifuEntry = {1:self.waifu001Entry,
                      2:self.waifu002Entry,
                      3:self.waifu003Entry,
                      4:self.waifu004Entry,
                      5:self.waifu005Entry,
                      6:self.waifu006Entry,
                      7:self.waifu007Entry,
                      8:self.waifu008Entry,
                      9:self.waifu009Entry,
                      10:self.waifu010Entry}
                      
        waifu = {1:self.waifu001,
                 2:self.waifu002,
                 3:self.waifu003,
                 4:self.waifu004,
                 5:self.waifu005,
                 6:self.waifu006,
                 7:self.waifu007,
                 8:self.waifu008,
                 9:self.waifu009,
                 10:self.waifu010}
        
        # Rajouter la sauvegarde dans la base de données
        for imageId in range(1, 11): 
            # Lit l'url depuis l'entrée texte
            url = str(waifuEntry[imageId].text())
            
            # Si l'url n'est pas vide
            if url != "": 
                # On télécharge l'image
                self.telechargement_image(url, imageId) 

            try:
                # Identifiant du numéro de la page affichée
                pageId = self.spinboxPageId.value()
                # Charge l'image téléchargée
                pixmap = PyQt4.QtGui.QPixmap("./data/characters/%s_%s" %(pageId, imageId))

                # Si la case de déformation n'est pas cochée
                if self.deformerCheckBox.isChecked() == False:
                   # Redimentionne l'image a la taille du rectangle - lissage des images et garde l'aspect ratio
                    image = pixmap.scaled(waifu[imageId].size(), PyQt4.QtCore.Qt.KeepAspectRatio, PyQt4.QtCore.Qt.SmoothTransformation)
                
                # Sinon, on affiche l'image dans tout le carré
                else:
                    image = pixmap.scaled(waifu[imageId].size(), PyQt4.QtCore.Qt.IgnoreAspectRatio, PyQt4.QtCore.Qt.SmoothTransformation)
                
                # Applique l'image
                waifu[imageId].setPixmap(image)
                
                # Centre l'image
                waifu[imageId].setAlignment(PyQt4.QtCore.Qt.AlignCenter)
            
            except Exception, e: 
                log.error(e)
                
        # Fond de la page
        # Lit l'url depuis l'entrée texte
        url = str(self.waifuWallpaperEntry.text())
        
        if url != "": self.telechargement_image(url, "wallpaper")
        # Charge l'image téléchargée
        pixmap = PyQt4.QtGui.QPixmap("./data/characters/wallpaper")
        
        # Application de l'image (avec aspect ratio et lissage)
        image = pixmap.scaled(self.waifuWallpaper.size(), PyQt4.QtCore.Qt.IgnoreAspectRatio, PyQt4.QtCore.Qt.SmoothTransformation)
        self.waifuWallpaper.setPixmap(image)
     

    # Fonction qui permet de modifier le comportement de l'application en fonction de paramétrages
    def preferences(self):
        fname = PyQt4.QtGui.QFileDialog.getOpenFileName(self, 'Open file', 'C:\\')


    # Fonction qui supprime toutes les données utilisateurs
    def reset(self):
        # Supression des fichiers individuels
        log.warning("Suppression des donnes utilisateur. Action irrecuperable!")
        log.info("Suppression du fichier: MyAnimeManagerGui.py.stats.txt")
        
        if os.path.exists("MyAnimeManagerGui.py.stats.txt"):
			os.remove("MyAnimeManagerGui.py.stats.txt")
        
        # Fermeture de la bdd pour pourvoir la supprimer
        curseur.close()
        bdd.close()
        log.info("Fermeture de la base de donnees...")
        
        log.info("Suppression du fichier: ./data/MyAnimeManager.sqlite3")
        os.remove("./data/MyAnimeManager.sqlite3")
        
        if os.path.exists("./data/MyAnimeManager.sqlite3-journal"):
			log.info("Suppression du fichier: ./data/MyAnimeManager.sqlite3-journal")
			os.remove("./data/MyAnimeManager.sqlite3-journal")
        
        # Nettoyage des dossier Characters et Covers
        filelist = [f for f in os.listdir("./data/characters")]
        for f in filelist:
            os.remove("./data/characters/%s" %f)
        log.info("Nettoyage du dossier: ./data/characters \t %s elements" %len(filelist))
            
        filelist = [f for f in os.listdir("./data/covers")]
        for f in filelist:
            os.remove("./data/covers/%s" %f)  
        log.info("Nettoyage du dossier: ./data/covers - %s elements" %len(filelist)) 
        log.info("Nettoyage termine !")  


    # Ferme le programme et enregistre les modifications apportées à la base de données
    def fermer(self, event):
        # Si des modifications on été apportées, on affiche la fenetre d'enregistrement
        if self.modifications == True:
            # Affiche la fenetre de dialogue
            avertissement = PyQt4.QtGui.QMessageBox.question(self, "Fermeture de l'application", "Voulez-vous sauvegarder les modifications ?", "Oui", "Non")

            if avertissement  == 0: # Si on clique sur Oui (Sauvegarder)
                bdd.commit() # Enregistre les modifications dans la bdd (il est ansi possible de fermer le programme pour ne pas enregistrer les nouvelles données
                log.info("Modifications sauvegardées")
                
            else:
				# Annule tout les changements depuis le dernier enregistrement
				bdd.rollback()

        # Affichage du nombre de notifications
        log.info("Nombre de changement dans la base: %s" %bdd.total_changes)

        # On ferme proprement la bdd
        curseur.close()
        bdd.close()
        log.info("Bdd fermée")

        # Et on ferme le programme
        log.info("Fermeture du programme")
        sys.exit()

        
# Fonction principale
if __name__ == "__main__":
    log.info("Version: %s" %__version__)
    # Chemins
    dossier = "./data/covers"
    #dossier = config["coverPath"]

    # Nom de la base de donnée
    nomBdd = "./data/MyAnimeManager.sqlite3"
    bddVierge = False

    # Recherche si le fichier de la base de donnée existe déja
    if not os.path.exists(nomBdd):
        bddVierge = True

    # On se connecte à la bdd (si elle n'existe pas elle sera créer mais restera vide)
    bdd = sqlite3.connect(nomBdd)
    bdd.row_factory = sqlite3.Row # Accès facile aux colonnes (Par leur nom et nom par leur emplacement)
    curseur = bdd.cursor()

    # Si la base de donnée est vierge, on utilise la fonction creation_de_la_bdd()
    if bddVierge == True: 
        #PyQt4.QtGui.QMessageBox.information(Menu, "Information", "L'application va créer une base de donnée pour la première utilisation")
        log.info("La bdd n'existe pas ! Creation d'un nouveau profil")
        creation_de_la_bdd()
        
        

    # Boucle principale (menu)
  
    # Titre de la fenetre
    app = PyQt4.QtGui.QApplication(sys.argv)
    fenetreMenu = Menu(None)
    fenetreMenu.show()
    app.exec_()
