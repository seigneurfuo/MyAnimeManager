#! /usr/bin/env python
# -*- coding: utf8 -*-


try:
    # Librairies standards
    import sys
    
    # Importation des autres parties du programme
    sys.path.append("./ressources/core")
    
    import info
    
    import database 
    import utils
    from update import maj_disponible
    
    # Logging
    from log import *
    
    import os
    import re
    import sqlite3
    import urllib
    import argparse
    import webbrowser
    from datetime import date, datetime, timedelta

	# Importation de pyQt
    import PyQt4.QtGui
    import PyQt4.QtCore
    import PyQt4.uic

except Exception, erreur:
    print("Librairies manquantes !")
    print("  %s" %erreur)
    sys.exit()


def creation_de_la_bdd():
    """Fonction de création de tables de la base de données"""
    
    log.info("Création de la base de donnees")

	# Code SQL pour créer la table anime
    curseur.execute(database.CREATE_TABLE_ANIME)

    # Code SQL pour créer la table planning
    curseur.execute(database.CREATE_TABLE_PLANNING)
    
    # Code SQL pour créer la table information
    curseur.execute(database.CREATE_TABLE_INFORMATION)
    curseur.execute("INSERT INTO information VALUES (%s)" %info.__db_version__)
    bdd.commit()
    

class Main(PyQt4.QtGui.QMainWindow, PyQt4.uic.loadUiType("./ressources/gui.ui")[0]): # Chargement des interfaces depuis les fichiers
    """Classe de la fenetre principale"""

    def __init__(self, parent=None):
        PyQt4.QtGui.QMainWindow.__init__(self, parent)
        
        # Définition de l'interface à charger
        self.setupUi(self)
        
        # Définition du titre
        self.setWindowTitle("%s - %s" %(info.__titre__, info.__version__))

        # Variables qui enregistre les modifications (Permet de ne pas afficher la fenetre d'enregistrement si rien n'a été modifié)
        self.modifications = False

        self.tabWidget.currentChanged.connect(self.chargement_onglet)

        # Gestion des evenements (onglet liste)
        self.table.cellClicked.connect(self.liste_afficher_infos_anime)
        self.table.currentCellChanged.connect(self.liste_afficher_infos_anime)
        self.boutonEnregistrer.clicked.connect(self.liste_enregistrer)
        self.boutonAnnuler.clicked.connect(self.liste_rafraichir)
        self.boutonCompleter.clicked.connect(self.liste_remplir_myanimelist)
        self.rechercheEntry.textChanged.connect(self.liste_recherche)
        self.rechercheViderBoutton.clicked.connect(self.liste_recherche_vider)
        
        self.rechercheLancer.clicked.connect(self.liste_recherche_filtre_liste)

        self.boutonAjouterAnime.clicked.connect(self.liste_rafraichir)
        self.boutonSupprimerAnime.clicked.connect(self.liste_supprimer)

        # Onglet planning
        self.planningCalendrier.clicked.connect(self.planning__afficher)
        self.planningCalendrier.selectionChanged.connect(self.planning__afficher)

        self.boutonPlanningInserer.clicked.connect(self.planning__animes_vus__inserer)
        self.boutonPlanningReset.clicked.connect(self.planning__aujourdhui)
        self.boutonPlanningSauvegarder.clicked.connect(self.planning__enregistrer)
        
        self.animeVuTable.cellDoubleClicked.connect(self.planning__animes_vus__inserer)

        # Onglet album
        self.testButton.clicked.connect(self.personnages_favoris)
        
        # Onglet outils
        self.pushButton.clicked.connect(self.outils__calcul_temps__calcul)

        # Onglet préférences
        self.pushButton_5.clicked.connect(self.exportation_du_profile)
        self.pushButton_3.clicked.connect(self.suppression_du_profile)

        # Remplace le numéro de version A propos
        self.barreDeStatus.showMessage("Version %s" %info.__version__)

        # Evenement de fermeture de l'application
        self.closeEvent = self.fermer
        
        # Icone en zone de notification
        self.tray = PyQt4.QtGui.QSystemTrayIcon(self)
        self.tray.setIcon(PyQt4.QtGui.QIcon("./ressources/icons/icon.png"))
        
        # Création d'un menu contextuel pour le 
        self.tray.menuContextuel = PyQt4.QtGui.QMenu()
    
        # Charge l'icone pour la fermeture
        self.tray.iconeQuitter = PyQt4.QtGui.QIcon("./re/icons/edit-delete-5.ico")
            
        # Créer l'action dans le menu
        self.tray.actionfermer = (PyQt4.QtGui.QAction(self.tray.iconeQuitter, "Quitter", self))
            
        # Evenement de l'action fermer
        self.tray.actionfermer.triggered.connect(self.fermer)
        
        # Ajout de l'action dans le menu
        self.tray.menuContextuel.addAction(self.tray.actionfermer)
        
        # Ajout du menu contextuel
        self.tray.setContextMenu(self.tray.menuContextuel)
        
		# Affichage de l'icone dans la zone de notifications
        self.tray.show()
            
        # Recherche de MAJ
          
        # Si l'argument noupdate est passé en parametres
        if args.noupdate == False:
            # Recherche d'une MAJ
            majDispo = maj_disponible(info.__version__)
            
            # Affichage d'un message si une maj est dispo
            if majDispo == 0:
                self.tray.showMessage(info.__titre__, u"Une mise à jour est disponible. Lancer update.py pour la mettre à jour automatiquement", msecs = 15000)
            
            elif majDispo == -1:
                log.info("Pas de nouvelle maj")
            
            else:
                self.tray.showMessage(info.__titre__, u"Impossible de joindre le serveur de mise à jour", msecs = 10000)
            

        # Définition du premier onglet affiché
        self.tabWidget.setCurrentIndex(0)
        self.chargement_onglet(self)


    def chargement_onglet(self, dump):
        """Fonction déclanchée a chaque fois qu'un onglet est lancé"""
        
        ongletId = self.tabWidget.currentIndex()
        log.info("Id onglet actif: %s" %ongletId)
        
        # Onglet planning
        if ongletId == 0:
            self.planning__afficher()
            self.planning__derniers_episodes_vus__remplir()
        
        # Onglet liste d'animé
        elif ongletId == 1: self.liste_rafraichir()
        
        # Onglet album
        elif ongletId == 2: self.personnages_favoris()


    def liste_rafraichir(self, titreRecherche=False, favorisRecherche=False, AVoirRecherche=False):
        """La fonction qui efface les entrées (les instructions auraient pus etres contenues dans liste_affiche mais je souhaitais séparer les deux blocs)"""
        
        # Image de l'animé vide
        myPixmap = PyQt4.QtGui.QPixmap("./ressources/icons/image-x-generic.png")
        image = myPixmap.scaled(self.label_5.size(), PyQt4.QtCore.Qt.KeepAspectRatio, PyQt4.QtCore.Qt.SmoothTransformation)
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

        # Remise par défault de la comboBoxEtatVisionnage (par défaut sur la position indéfinie)
        self.comboBoxEtatVisionnage.setCurrentIndex(3)

        # Remise à zéro de la checkbox Favoris
        self.checkBoxFavoris.setCheckState(False)

        # Nettoyage du champ MAL
        self.malEntry.setText(str())

        # Si rien n'est rentré dans la barre de recherche:
        if titreRecherche != False and titreRecherche !="" :
            log.info("Filtrage de la liste: Par recherche")

            # On afiche la liste des séries dont le nom contiends le texte entré
            curseur.execute("SELECT * FROM anime WHERE animeTitre LIKE('%s%s%s') ORDER BY LENGTH(animeId), animeId" %("%", titreRecherche, "%"))

        # Si on veut afficher la liste des animés à voir
        elif AVoirRecherche == True:
            log.info("Filtrage de la liste: Afficher les animes a voir")
            curseur.execute("SELECT * FROM anime WHERE animeEtatVisionnage = '2' ORDER BY LENGTH(animeId), animeId")

        # Affichage de la liste normale
        elif favorisRecherche == False:
            log.info("Affichage normal de la liste des animes")
            curseur.execute("SELECT * FROM anime ORDER BY LENGTH(animeId), animeId") # Permet de trier les animés de manière croissante et de manière humaine (evite que des identifiants tel que 1000 s'intercalent entre les identfiant 100 / 101

        # Si on veut afficher la liste des favoris
        else :
            log.info("Filtrage de la liste: Afficher les favoris")
            curseur.execute("SELECT * FROM anime WHERE animeFavori = '1' ORDER BY LENGTH(animeId), animeId")


        resultats = curseur.fetchall()
        log.info("Animes: %s" %len(resultats))
        self.barreDeStatus.showMessage("Animes: %s" %len(resultats))

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


    def liste_recherche_filtre_liste(self):
		"""Fonction, qui en fonction de la valeur du filtre, execute la fonction d'affichage de la liste"""

		if self.comboBoxFiltreRecherche.currentIndex() == 0: 
			self.liste_rafraichir()

		elif self.comboBoxFiltreRecherche.currentIndex() == 1:
			self.liste_rafraichir(favorisRecherche=True)
			
		elif self.comboBoxFiltreRecherche.currentIndex() == 2:
			self.liste_rafraichir(AVoirRecherche=True)


    def liste_afficher_infos_anime(self):
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

            # ComboBoxEtatAnimé
            # Animé Terminé =  0
            # Animé en cours = 1
            # Animé a voir   = 2
            # Animé indéfini = 3
            etatVisionnage = int(ligne["animeEtatVisionnage"])
            self.comboBoxEtatVisionnage.setCurrentIndex(etatVisionnage) 

            # Checkbox favoris
            if ligne["animeFavori"] == "1":
                self.checkBoxFavoris.setCheckState(True)
                
            else:
                self.checkBoxFavoris.setCheckState(False)               


            # Charge et affiche l'image de l'anime
            image = str(ligne["animeId"])
            chemin = os.path.join("./profile/covers", image)
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
        myanimelist.telecharger_image(animeId, "./profile/covers/")

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

            # Etat du visionnage (comboBoxEtatVisionnage)
            animeVisionnage = str(self.comboBoxEtatVisionnage.currentIndex())

            # Animé favoris ?
            self.checkBoxFavoris.checkStateSet()
            if self.checkBoxFavoris.isChecked() == False :
                animeFavori = "0"

            elif self.checkBoxFavoris.isChecked() == True:
                animeFavori = "1"

            # Génération de la command SQL
            curseur.execute("INSERT OR REPLACE INTO anime (animeId, animeDateAjout, animeTitre, animeAnnee, animeStudio, animeFansub, animeEtatVisionnage, animeFavori, animeNbVisionnage, animeNotes) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" %(animeId, animeDateAjout, animeTitre, animeAnnee, animeStudio, animeFansub, animeVisionnage, animeFavori, animeNbVisionnage, animeNotes))

            # On indique a l'application que quelque chose a été modifié
            self.modifications = True

            # Rafraichi après avoir enregistré
            self.liste_rafraichir()
            self.planning__derniers_episodes_vus__remplir()

        # Si l'identifiant n'a pas été rempli
        else:
            # Remplacer la fenetre par une version 1 bouton.
            information = PyQt4.QtGui.QMessageBox.information(self, "Identifiant invalide", u"Veuillez entrer un identifiant composé uniquement de chiffres !", "Continuer")


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
            if os.path.exists("./profile/covers/%s" %animeId):
                os.remove("./profile/covers/%s" %animeId)

            # Supression du champ dans la base SQL
            curseur.execute("DELETE FROM anime WHERE animeTitre = '%s'" %animeTitre)

            # On indique a l'application que quelque chose a été modifié
            self.modifications = True

            # Rafraichi après avoir supprimé
            self.liste_rafraichir()
            self.planning__derniers_episodes_vus__remplir()


# Fonctions de l'onglet planning
    def planning__derniers_episodes_vus__remplir(self):
        """Fonction qui ajoute les animés vus dans la liste des animés vus"""
        
        # On vide la liste des animés
        self.animeVuTable.clear()

        # On éxécute la commande sql qui retourne: les animés en cours de visionnage qui avec leur épisode vu le plus récent
        curseur.execute("""
                        SELECT anime.animeTitre, planning.planningEpisode AS planningEpisode
                        FROM anime, planning
                        WHERE planning.planningAnime = anime.animeId
                        AND anime.animeEtatVisionnage = 1
                        GROUP BY anime.animeTitre
                        ORDER BY anime.animeId ASC""")
        animesVus = curseur.fetchall()

        # Définition de la taille du tableau
        nombreLignes = len(animesVus)
        self.animeVuTable.setRowCount(nombreLignes)
        self.animeVuTable.setColumnCount(2)

        # Définition du titre des colonnes
        titreColonnes = ["Ep.", "Anime"]
        self.animeVuTable.setHorizontalHeaderLabels(titreColonnes)

        # Ajout des éléments
        for indice, anime in enumerate(animesVus):
            colonne1 = PyQt4.QtGui.QTableWidgetItem(str(int(anime["planningEpisode"]) + 1) )
            self.animeVuTable.setItem(indice, 0, colonne1)

            colonne2 = PyQt4.QtGui.QTableWidgetItem(anime["animeTitre"])
            self.animeVuTable.setItem(indice, 1, colonne2)
            

    def planning__animes_vus__inserer(self):
        """Fonction qui ajoute le titre d'un animé en cours de visionnage dans la boite d'entrée du journal"""

        
        # Sauvegarde du texte actuel
        ancienTexte = self.planningEntry.toPlainText()
        
        # Récupère le numéro de ligne actuellement sélectionné dans la liste
        ligneActuelle = int(self.animeVuTable.currentRow())

        # Si on a bien sélectionné un anime (empèche l'erreur quand la liste est rechargée et que rien n'est sélectionné)
        if ligneActuelle != -1:

            # Le titre de l'animé est contenu dans le deuxième cellule de la colonne (les indices commencent à 0)
            animeTitre = self.animeVuTable.item(ligneActuelle, 1).text()
            planningEpisodeAVoirSuivant = int(self.animeVuTable.item(ligneActuelle, 0).text()) + 1

            # Si le planning est vide
            if ancienTexte == "":
                nouveauTexte = str(animeTitre + "-Ep %s" %planningEpisodeAVoirSuivant)

            # Sinon, on affiche en gardant l'ancien texte
            else:
                nouveauTexte = ancienTexte + "\n" + str(animeTitre + "-Ep %s" %planningEpisodeAVoirSuivant)
                
            nouveauTexteNettoye = nouveauTexte.replace("\n\n", "\n")

            #Affichage du nouveau titre
            self.planningEntry.setText(nouveauTexteNettoye)
            
            # Mise du focus sur la zone de texte
            self.planningEntry.setFocus()


    def planning__afficher(self):
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


    def planning__aujourdhui(self):
        """Fonction qui séléctionne la date actuelle sur le calendrier"""
        
        # Demande a Qt la date du jour
        aujourdhui = PyQt4.QtCore.QDate.currentDate ()

        # Affiche le caldendrier à la date du jour
        self.planningCalendrier.setSelectedDate(aujourdhui)


    def planning__enregistrer(self):
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
        
        # On rafraichi la liste des animés dans le planining pour prendre en compte les nouveaux épisodes vus
        self.planning__derniers_episodes_vus__remplir()


# Fonctions de l'onglet outils
    def outils__calcul_temps__calcul(self):
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


    def telechargement_image_personnage(self, url, filename):
        """Fonction qui permet de télécharger des images et de changer le nom du fichier enregistré"""
        
        # Identifiant du numéro de page
        pageId = self.spinboxPageId.value()
        filename = "./profile/characters/%s_%s" %(pageId, filename)
        urllib.urlretrieve(url, filename)
        
        
    def telechargement_image_wallpaper(self, url):
        """Fonction qui permet de télécharger des images et de changer le nom du fichier enregistré"""
        
        # Identifiant du numéro de page
        pageId = self.spinboxPageId.value()
        filename = "./profile/characters/wallpaper"
        urllib.urlretrieve(url, filename)
        

    def personnages_favoris(self):
        """Fonction qui affiche les personnages préférés"""

        waifu = {
                    1:[self.waifu001Entry, self.waifu001],
                    2:[self.waifu002Entry, self.waifu002],
                    3:[self.waifu003Entry, self.waifu003],
                    4:[self.waifu004Entry, self.waifu004],
                    5:[self.waifu005Entry, self.waifu005],
                    6:[self.waifu006Entry, self.waifu006],
                    7:[self.waifu007Entry, self.waifu007],
                    8:[self.waifu008Entry, self.waifu008],
                    9:[self.waifu009Entry, self.waifu009],
                    10:[self.waifu010Entry, self.waifu010]}

        # Pour chaque champ texte
        for imageId in range(1, 11):
            # Lit l'url depuis l'entrée texte
            url = str(waifu[imageId][0].text())

            # Si l'url n'est pas vide
            if url != "":
                # On télécharge l'image
                self.telechargement_image_personnage(url, imageId)

            try:
                # Identifiant du numéro de la page affichée
                pageId = self.spinboxPageId.value()
                
                # Charge l'image téléchargée
                pixmap = PyQt4.QtGui.QPixmap("./profile/characters/%s_%s" %(pageId, imageId))
                
                log.info("Image chargee: ./profile/characters/%s_%s" %(pageId, imageId))

                # Si la case de déformation n'est pas cochée
                if self.deformerCheckBox.isChecked() == False:
                   
                   # Redimentionne l'image a la taille du rectangle - lissage des images et garde l'aspect ratio
                    image = pixmap.scaled(waifu[imageId][1].size(), PyQt4.QtCore.Qt.KeepAspectRatio, PyQt4.QtCore.Qt.SmoothTransformation)

                # Sinon, on affiche l'image dans tout le carré
                else:
                    image = pixmap.scaled(waifu[imageId][1].size(), PyQt4.QtCore.Qt.IgnoreAspectRatio, PyQt4.QtCore.Qt.SmoothTransformation)

                # Applique l'image
                waifu[imageId][1].setPixmap(image)

                # Centre l'image
                waifu[imageId][1].setAlignment(PyQt4.QtCore.Qt.AlignCenter)

            except Exception, e:
                log.error(e)

        # Fond de la page
        # Lit l'url depuis l'entrée texte
        url = str(self.waifuWallpaperEntry.text())

        if url != "": self.telechargement_image_wallpaper(url)
        
        # Charge l'image téléchargée
        pixmap = PyQt4.QtGui.QPixmap("./profile/characters/wallpaper")

        # Application de l'image (avec aspect ratio et lissage)
        image = pixmap.scaled(self.waifuWallpaper.size(), PyQt4.QtCore.Qt.IgnoreAspectRatio, PyQt4.QtCore.Qt.SmoothTransformation)
        self.waifuWallpaper.setPixmap(image)

    
    def importation_du_profile(self):
        """Fonction qui permet d'importer un profile"""
        
        pass


    def exportation_du_profile(self):
        """Fonction qui permet d'exporter un profile"""

        cheminDeSauvegarde = PyQt4.QtGui.QFileDialog(self)


    def suppression_du_profile(self):
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

            log.info("Suppression du fichier: ./profile/MyAnimeManager.sqlite3")
            os.remove("./profile/MyAnimeManager.sqlite3")

            if os.path.exists("./profile/MyAnimeManager.sqlite3-journal"):
                log.info("Suppression du fichier: ./profile/MyAnimeManager.sqlite3-journal")
                os.remove("./profile/MyAnimeManager.sqlite3-journal")

            # Nettoyage des dossier Characters et Covers
            filelist = [f for f in os.listdir("./profile/characters")]
            log.info("Nettoyage du dossier: ./profile/characters \t %s elements" %len(filelist))
            for f in filelist:
                log.info("Supression de %s" %f)
                os.remove("./profile/characters/%s" %f)

            filelist = [f for f in os.listdir("./profile/covers")]
            log.info("Nettoyage du dossier: ./profile/covers - %s elements" %len(filelist))
            for f in filelist:
                log.info("Supression de %s" %f)
                os.remove("./profile/covers/%s" %f)
            
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

            elif avertissement == 1: # Si on clique sur Quitter sans sauvegarder
                # Annule tout les changements depuis le dernier enregistrement
                log.info("Modifications annulee")
                bdd.rollback()

        # Affichage du nombre de notifications
        log.info("Nombre de changement dans la base: %s" %bdd.total_changes)

        # On ferme proprement la bdd
        curseur.close()
        bdd.close()
        log.info("Bdd fermée")

        # Et on ferme le programme
        log.info("Fermeture du programme")
        PyQt4.QtCore.QCoreApplication.exit(0)

if __name__ == "__main__":
    """ Fonction principale de l'application """
    # Fonction principale
    log.info("Version: %s" %info.__version__)
    
    # Parsage des arguments
    argParser = argparse.ArgumentParser()
    argParser.add_argument("-noupdate", action="store_true", default=False)
    args = argParser.parse_args()

    # Création du dossier utilisateur
    utils.creation_dossier_profil_utilisateur()

    # Nom de la base de donnée
    nomBdd = "./profile/MyAnimeManager.sqlite3"
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
        log.info("La bdd n'existe pas ! Creation d'un nouveau profile")
        creation_de_la_bdd()
        
    # Récupération de la version de la base de données
    curseur.execute("SELECT * FROM information")

    bddInformations = curseur.fetchone()
    bddVersion = int(bddInformations["version"])


    # MAJ de la base de données
    if bddVersion == 5 or bddVersion == None:
        log.info("MAJ de la base de donnees")
        sys.exit()
        exit()

    # Définition de l'application pyQt
    app = PyQt4.QtGui.QApplication(sys.argv)     

    # Création de la fenetre principale
    fenetrePrincipale = Main(None)
    fenetrePrincipale.show()

    # Lancement de la boucle de l'application pyQt   
    app.exec_()
