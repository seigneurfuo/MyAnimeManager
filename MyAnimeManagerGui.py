#!/usr/bin/python2.7
# -*- coding: utf8 -*-

# Informations sur l'application
__titre__                = "MyAnimeManager"
__version__              = "0.20.56"
__auteur__               = "seigneurfuo"
__db_version__           = 5
__dateDeCreation__       = "12/06/2016"
__derniereModification__ = "09/11/2016"

# Logging
import logging
log = logging.getLogger()
log.setLevel(logging.DEBUG)


# Librairies standards
import sys
import os
import re
import sqlite3
import urllib
from datetime import date, datetime, time, timedelta

sys.path.append("./data/libs")
# Librairies de tierces-parties
import myanimelist


# Importation de pyQt
try:
    import PyQt4.QtGui
    import PyQt4.QtCore
    import PyQt4.uic.loadUiType
except:
    log.error("L'application n'arrive pas a trouver pyQt !")
    log.error("Veuillez vous reporter aux notes d'insatallation.")


# Création d'un formateur qui va ajouter le temps, le niveau de chaque message quand on écrira un message dans le log
formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(message)s')


# Les lignes suivantes permettent de rediriger chaque écriture de log sur la console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)
log.addHandler(console_handler)


def creation_de_la_bdd():
    """Fonctions générale a l'application"""
	
    log.info("Création de la base de donnees")


# Code SQL pour créer la table anime
    curseur.execute(
    """
    CREATE TABLE anime(
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
    CREATE TABLE planning(
    planningDate TEXT NOT NULL,
    planningIdentifiantJournalier TEXT,
    planningAnime TEXT,
    planningEpisode TEXT)
    """)


# Code SQL pour créer la table informations
    curseur.execute(
    """
    CREATE TABLE information(
    informationVersion)
    """)


# Fonction qui va créer les dossiers utiles
def verification_des_dossiers():
    log.info("Verification de l'existance des dossiers ...")

    # Dossier ./data/characters
    if os.path.exists("./data/characters"):
        log.info("./data/characters - Ok")
    else:
        os.makedirs("./data/characters")
        log.info("Creation de ./data/characters")

    # Dossier ./data/covers
    if os.path.exists("./data/covers"):
        log.info("./data/covers - Ok")
    else:
        os.makedirs("./data/covers")
        log.info("Creation de ./data/covers")


class Main(PyQt4.QtGui.QMainWindow, PyQt4.uic.loadUiType("./data/gui.ui")[0]): # Chargement des interfaces depuis les fichiers
    """Classe de la fenetre principale"""

    def __init__(self, parent=None):
        PyQt4.QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)

        # Variables qui enregistre les modifications (Permet de ne pas afficher la fenetre d'enregistrement si rien n'a été modifié)
        self.modifications = False

        # Gestion des evenements (onglet liste)
        self.table.cellClicked.connect(self.liste_afficher)
        self.table.currentCellChanged.connect(self.liste_afficher)
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

        # Onglet album
        self.testButton.clicked.connect(self.personnages_favoris)
        
        # Onglet outils
        self.pushButton.clicked.connect(self.outils_calcul_temps_calcul)

        # Onglet préférences
        self.pushButton_3.clicked.connect(self.suppression_du_profil)

        # Remplace le numéro de version A propos
        self.label_7.setText("version " + str(__version__))

    # Evenement de fermeture de l'application
        self.closeEvent = self.fermer

        # Fonctions a lancer en premier
        self.liste_rafraichir()
        self.planning_afficher()
        self.animes_vus_afficher()
        self.personnages_favoris()
        

    def liste_rafraichir(self, titreRecherche=False, favorisRecherche=False):
        """La fonction qui efface les entrés (les instructions auraient pus etres contenues dans liste_affiche mais je souhaitais séparer les deux blocs)"""
        
        # Image de l'animé vide
        myPixmap = PyQt4.QtGui.QPixmap("./data/ekHFstR.png")
        image = myPixmap.scaled(self.label_5.size(), )
        self.label_5.setPixmap(image)

        # On vide la liste et les entrées
        self.table.clear()
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
            curseur.execute("SELECT * FROM anime WHERE animeTitre LIKE('%s%s%s') ORDER BY LENGTH(animeId), animeId" %("%", titreRecherche, "%"))

        else :
            # Affichage de la liste normale
            if favorisRecherche == False:
                log.info("Affichage normal de la liste des animes")
                curseur.execute("SELECT * FROM anime ORDER BY LENGTH(animeId), animeId") # Permet de trier les animés de manière croissante et de manière humaine (evite que des identifiants tel que 1000 s'intercalent entre les identfiant 100 / 101

            # Si on veut afficher la liste des favoris
            else:
                log.info("Filtrage de la liste: Afficher les favoris")
                curseur.execute("SELECT * FROM anime WHERE animeFavori = '1' ORDER BY LENGTH(animeId), animeId")


        resultats = curseur.fetchall()
        log.info("Animes: %s" %len(resultats))

        # Remplissage de la liste
        #for anime in resultats:
            #ligne = PyQt4.QtGui.QListWidgetItem(anime["animeTitre"])
            #self.listWidget.addItem(ligne)

        # Définition de la taille du tableau
        nombreLignes = len(resultats)
        self.table.setRowCount(nombreLignes)
        self.table.setColumnCount(2)

        # Définition du titre des colonnes
        titreColonnes = ["Id", "Titre"]
        self.table.setHorizontalHeaderLabels(titreColonnes)

        # Ajout des éléments
        for indice, anime in enumerate(resultats):
            colonne1 = PyQt4.QtGui.QTableWidgetItem(anime["animeId"])
            self.table.setItem(indice, 0, colonne1)

            colonne2 = PyQt4.QtGui.QTableWidgetItem(anime["animeTitre"])
            self.table.setItem(indice, 1, colonne2)


    def liste_recherche(self):
        """Fonction qui permet de rechercher un animé dans la liste grace a son nom"""
        
        recherche = self.rechercheEntry.text()

        # Si le recherche est vide on ne l'active pas
        self.liste_rafraichir(titreRecherche = recherche)

 
    def liste_recherche_vider(self):
        """Fonction qui permet de vider la liste de recherche"""
        
        self.rechercheEntry.setText(str())
        self.liste_rafraichir()


    def liste_recherche_favoris(self):
        """Fonction qui affiche les animés favoris"""
        
        self.liste_rafraichir(favorisRecherche=True)


    def liste_afficher(self):
        """Fonction qui affiche les information pour l'animé sélectionné"""
        
        # Récupère le numéro de ligne actuellement sélectionné dans la liste
        ligneActuelle = int(self.table.currentRow())

        # Si on a bien sélectionné un anime (empèche l'erreur quand la liste est rechargée et que rien n'est sélectionné)
        if ligneActuelle != -1:

            # Le titre de l'animé est contenu dans le deuxième cellule de la colonne (les indices commencent à 0)
            animeTitre = self.table.item(ligneActuelle, 1).text()

            # On cherche les informations dans la base SQL
            curseur.execute("SELECT * FROM anime WHERE animeTitre = '%s'" %animeTitre)

            # Charge les informations récupérées dans la base sql
            ligne = curseur.fetchone() # Permet dene choise que le premier résultat en sql (pour un seul identifiant, on ne peut avoir qu'un seul animé

            # Listes d'entrées
            self.idEntry.setText(str(ligne["animeId"]))
            
            # Affiche le texte si la base ne retourne pas None: Permet d'autrepasser le bug d'encodage UFT8
            if ligne["animeDateAjout"] != None:
                self.ajoutEntry.setText(ligne["animeDateAjout"])
            
            if ligne["animeTitre"] != None:            
                self.titreEntry.setText(ligne["animeTitre"])
            
            if ligne["animeAnnee"] != None: 
                self.anneeEntry.setText(str(ligne["animeAnnee"]))
            
            if ligne["animeStudio"] != None: 
                self.studioEntry.setText(ligne["animeStudio"])
                
            if ligne["animeFansub"] != None: 
                self.fansubEntry.setText(ligne["animeFansub"])
                
            if ligne["animeNotes"] != None: 
                self.notesEntry.setText(ligne["animeNotes"])

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


    def liste_remplir_myanimelist(self):
        """Fonction qui recherche un identifiant ou un titre d'animé sur MAL"""
        
        # Récupère l'identifiant ou le titre entré dans l'entrée MAL
        texte = self.malEntry.text()

        # Si le texte récupéré correspond a un identifiant mal (chiffres uniquement)
        if re.findall("^-?[0-9]+$", texte):
            idMyAnimeList = self.malEntry.text()
            myanimelist.anime(str(idMyAnimeList))

        #else:
            # Sinon, il s'agit d'un titre a rechercher
            #titreMyAnimeList = self.malEntry.text()
            #myanimelist.recherche_titre(str(titreMyAnimeList))

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


    def liste_enregistrer(self):
        """Fonction qui enregistre les données des animés dans la bdd"""
        
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
            animeNotes = self.notesEntry.toPlainText()

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
            information = PyQt4.QtGui.QMessageBox.information(self, "Identifiant invalide", "Veuillez entrer un identifiant composé uniquement de chiffres !", "Continuer")


    def liste_supprimer(self):
        """Fonction qui supprime un anime dans la liste"""
        
        # Récupère le numéro de ligne actuellement sélectionné dans la liste
        ligneActuelle = int(self.table.currentRow())

        # Si on a bien sélectionné un anime (empèche l'erreur quand la liste est rechargée et que rien n'est sélectionné)
        if ligneActuelle != -1:

            # Le titre de l'animé est contenu dans le deuxième cellule de la colonne (les indices commencent à 0)
            animeId= self.table.item(ligneActuelle, 0).text()  
            animeTitre = self.table.item(ligneActuelle, 1).text()          

            # Supression de l'image
            if os.path.exists("./data/covers/%s" %animeId):
                os.remove("./data/covers/%s" %animeId)

            # Supression du champ dans la base SQL
            curseur.execute("DELETE FROM anime WHERE animeTitre = '%s'" %animeTitre)

            # On indique a l'application que quelque chose a été modifié
            self.modifications = True

            # Rafraichi après avoir supprimé
            self.liste_rafraichir()
            self.animes_vus_afficher()


# Fonctions de l'onglet planning
    def animes_vus_afficher(self):
        """Fonction qui ajoute les animés vus dans la liste des animés vus"""
        
        # On vide la liste des animés
        self.listWidget_3.clear()

        # On éxécute la commande sql qui retourne les animés en cours de visionnage
        curseur.execute("SELECT * FROM anime WHERE animeEtatVisionnage = 1 ORDER BY animeId")
        animes_vus = curseur.fetchall()

        # Remplissage de la liste
        for anime_vu in animes_vus:
            ligne = PyQt4.QtGui.QListWidgetItem(anime_vu["animeTitre"])
            self.listWidget_3.addItem(ligne)


    def planning_animes_vus_inserer(self):
        """Fonction qui ajoute le titre d'un animé en cours de visionnage dans la boite d'entrée du journal"""
        
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
            
        nouveauTexteNettoye = nouveauTexte.replace("\n\n", "\n")

        #Affichage du nouveau titre
        self.planningEntry.setText(nouveauTexteNettoye)


    def planning_afficher(self):
        """Fonction qui affiche les animés vus en fonction de la date sélectionnée sur le calendrier"""        

        # Vide la boite d'entrée
        self.planningEntry.setText(str())

        # Date correspond a la date sur le jour selectionné sur le calendrier
        date = self.planningCalendrier.selectedDate().toPyDate()

        # Recherche dans la base de donnée la liste des animés vu le jour de la date sélectionnée (le tri ce fait en fonction del'indentifiant journalier)
        # La table planningAnime ne contient que l'identifiant de l'animé. Le nom est récupéré grace a une jointure entre la table anime et planning
        curseur.execute("SELECT * FROM planning, anime WHERE planningDate = \"%s\" AND planning.planningAnime = anime.AnimeId ORDER BY LENGTH(planning.planningIdentifiantJournalier), planning.planningIdentifiantJournalier ASC" %date)

        # La ligne du dessous n'est plus vrait avec les identifiants journaliers
        # Pour les résultats trouvés en SQL (1 max car on recherche l'anime en fonction de son titre)
        animes = ""
        for ligne in curseur.fetchall():
            # Ajout les animés dans le label text
            animes = animes + ligne["animeTitre"] + "-Ep " + ligne["planningEpisode"] + "\n"

        # Colle la liste des animés
        self.planningEntry.setText(str(animes))


    def planning_aujourdhui(self):
        """Fonction qui séléctionne la date actuelle sur le calendrier"""
        
        # Demande a Qt la date du jour
        aujourdhui = PyQt4.QtCore.QDate.currentDate ()

        # Affiche le caldendrier à la date du jour
        self.planningCalendrier.setSelectedDate(aujourdhui)


    def planning_enregistrer(self):
        """Fonction qui enregistre le planning dans la bdd"""

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
    def outils_calcul_temps_calcul(self):
        """Fonction qui permet de calculer l'heure de fin d'un visionnage a partir du nombre d'épisodes a voir"""

        # Effacement de la liste
        self.listWidget_2.clear()

        # Récupération du contenu des spinbox
        nombreEpisodes = self.spinBox_2.value()
        dureeEpisode = self.spinBox_3.value()

        # Défini la première plage a partir de maintenant
        plageA = datetime.now()

        for x in range(0, nombreEpisodes):
            plageB = plageA + timedelta(minutes = dureeEpisode)
            heure = "%02d - %02d:%02d -> %02d:%02d" %(x + 1, plageA.hour, plageA.minute, plageB.hour, plageB.minute) # Chaine qui seras affichée
            plage = PyQt4.QtGui.QListWidgetItem(heure) # Création de l'élément
            self.listWidget_2.addItem(plage) #Ajout de l'élément a la liste
            plageA = plageB # Décale la plage


    def telechargement_image(self, url, filename):
        """Fonction qui permet de télécharger des images et de changer le nom du fichier enregistré"""
        
        # Identifiant du numéro de page
        pageId = self.spinboxPageId.value()
        filename = "./data/characters/%s_%s" %(pageId, filename)
        urllib.urlretrieve(url, filename)
        

    def personnages_favoris(self):
        """Fonction qui affiche les personnages préférés"""

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


    def preferences(self):
        """Fonction qui permet de modifier le comportement de l'application en fonction de paramétrages"""

        fname = PyQt4.QtGui.QFileDialog.getOpenFileName(self, 'Open file', 'C:\\')


    def suppression_du_profil(self):
        """Fonction qui supprime toutes les données utilisateurs"""
    
        # Supression des fichiers individuels
        log.warning("Suppression des donnees utilisateur. Action definitive!")
 
        # Avant la supression, une fenetre de confirmation apparait       
        avertissement = PyQt4.QtGui.QMessageBox.question(self, "Suppression des donnees utilisateur", "Etes vous certain de vouloir supprimer vos donnees ?\nCette action est definitive !", "Oui, effacer mes donnees", "Non, ne pas effacer mes donnees")

        # Si on clique sur Oui
        if avertissement == 0:
            log.info("Supression acceptée")

            # Fermeture de la bdd pour pourvoir la supprimer
            log.info("Fermeture de la base de donnees...")
            curseur.close()
            bdd.close()

            log.info("Suppression du fichier: ./data/MyAnimeManager.sqlite3")
            os.remove("./data/MyAnimeManager.sqlite3")

            if os.path.exists("./data/MyAnimeManager.sqlite3-journal"):
                log.info("Suppression du fichier: ./data/MyAnimeManager.sqlite3-journal")
                os.remove("./data/MyAnimeManager.sqlite3-journal")

            # Nettoyage des dossier Characters et Covers
            filelist = [f for f in os.listdir("./data/characters")]
            log.info("Nettoyage du dossier: ./data/characters \t %s elements" %len(filelist))
            for f in filelist:
                log.info("Supression de %s" %f)
                os.remove("./data/characters/%s" %f)

            filelist = [f for f in os.listdir("./data/covers")]
            log.info("Nettoyage du dossier: ./data/covers - %s elements" %len(filelist))
            for f in filelist:
                log.info("Supression de %s" %f)
                os.remove("./data/covers/%s" %f)
            
            # Fin de la suppression des données
            log.info("Nettoyage termine !")
            
            # Fenetre d'information qui demande a relancer l'application
            information = PyQt4.QtGui.QMessageBox.information(self, "Relancer l'application", "L'application va se fermer pour prendre en compte les modifications.\n Vous pouvez la relancer juste apres.", "Fermer")
            

    def fermer(self, event):
        """Ferme le programme et enregistre les modifications apportées à la base de données"""

        # Si des modifications on été apportées, on affiche la fenetre d'enregistrement
        if self.modifications == True:
            # Affiche la fenetre de dialogue
            avertissement = PyQt4.QtGui.QMessageBox.question(self, "Fermeture de l'application", "Voulez-vous sauvegarder les modifications ?", "Oui", "Non")

            if avertissement == 0: # Si on clique sur Oui (Sauvegarder)
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

    # Vérification des dossiers
    verification_des_dossiers()

    # Chemins
    dossier = "./data/covers"

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
        PyQt4.QtGui.QMessageBox.information(Main, "Information", "L'application va créer une base de donnée pour la première utilisation")
        log.info("La bdd n'existe pas ! Creation d'un nouveau profil")
        creation_de_la_bdd()


    # Boucle principale (menu)

    # Titre de la fenetre
    app = PyQt4.QtGui.QApplication(sys.argv)
    fenetrePrincipale = Main(None)
    fenetrePrincipale.show()
    app.exec_()
