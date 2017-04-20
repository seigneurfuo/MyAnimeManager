#! /usr/bin/env python
# -*- coding: utf8 -*-

# Informations sur l'application
__titre__ = "MyAnimeManager"
__auteur__ = "seigneurfuo"
__dateDeCreation__ = "12/06/2016"
__db_version__ = 6
__version__ = "0.27.89"
__derniereModification__ = "10/04/2017"

# Logging
import logging
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

# Création d'un formateur qui va ajouter le temps, le niveau de chaque message quand on écrira un message dans le log
formatter = logging.Formatter('%(asctime)s : %(lineno)s : %(levelname)s : %(message)s')

# Les lignes suivantes permettent de rediriger chaque écriture de log sur la console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)
log.addHandler(console_handler)

# Importation des librairies
try:
  # Librairies standards
  import sys
  import os
  import re
  import sqlite3
  import urllib
  import argparse
  from distutils.version import LooseVersion
  from datetime import date, datetime, time, timedelta

  # Librairies de tierces-parties
  path = os.path.dirname(os.path.abspath(__file__))
  libsPath = os.path.join(path, "./data/libs")
  sys.path.append(libsPath)

  # Importation de pyQt
  import PyQt4.QtGui
  import PyQt4.QtCore
  import PyQt4.uic


except Exception, erreur:
    log.error("Librairies manquantes !")
    log.error("  %s" %erreur)
    sys.exit()


def creation_de_la_bdd():
    """Fonctions générale a l'application"""

    log.info("Création de la base de donnees")

  # Code SQL pour créer la table anime
    curseur.execute()


def verification_des_dossiers():
    """Fonction qui va créer les dossiers utiles"""
    
    log.info("Verification de l'existance des dossiers ...")

    # Dossier ./data/characters
    if os.path.exists("./data/characters"):
        log.info("  ./data/characters [Ok]")
    else:
        os.makedirs("./data/characters")
        log.info("  Creation de ./data/characters")

    # Dossier ./data/covers
    if os.path.exists("./data/covers"):
        log.info("  ./data/covers [Ok]")
    else:
        os.makedirs("./data/covers")
        log.info("  Creation de ./data/covers")


class Main(PyQt4.QtGui.QMainWindow, PyQt4.uic.loadUiType("./data/gui.ui")[0]): # Chargement des interfaces depuis les fichiers
    """Classe de la fenetre principale"""

    def __init__(self, parent=None):
        PyQt4.QtGui.QMainWindow.__init__(self, parent)
        
        # Définition de l'interface à charger
        self.setupUi(self)
        
        # Définition du titre
        self.setWindowTitle("%s - %s" %(__titre__, __version__))

        # Variables qui enregistre les modifications (Permet de ne pas afficher la fenetre d'enregistrement si rien n'a été modifié)
        self.modifications = False

        # Initialisation des evenements
        self.__init__evenements()
        
        # Chargement du systray
        self.__init__systray()
        
        # Si l'argument noupdate est passé en parametres, on ne met pas a jour
        if args.noupdate == False:
            # Lance la recherche de MAJ
            self.recherche_mise_a_jour()
            
        # Définition du premier onglet affiché
        self.tabWidget.setCurrentIndex(0)
           
        # Chargement des fonctions
        self.chargement_onglet(self) # Inutile car il est appelé lorsque l'onglet actif est changé.


    def __init__evenements(self):
        """Fonction qui contiends toutes les evenements liées aux boutons / widgets"""
        
        # Au changement d'onglet
        self.tabWidget.currentChanged.connect(self.chargement_onglet)
        
        # ----- Onglet liste -----
        
        # Evenements du tableau seriesTable

        self.seriesTable.cellClicked.connect(self.onglet_liste__liste_serie__changement_selection)
        self.seriesTable.currentCellChanged.connect(self.onglet_liste__liste_serie__changement_selection)

        # Evenements du tableau serieSaisonsTable      
        self.serieSaisonsTable.cellClicked.connect(self.onglet_liste__liste_saison__changement_selection)
        self.serieSaisonsTable.currentCellChanged.connect(self.onglet_liste__liste_saison__changement_selection)

        # Bouton de nouvelle série
        self.boutonAjouterSerie.clicked.connect(self.onglet_liste__rafraichir)

		# Bouton de sauvegarde de la série éditée
        self.boutonEnregistrer.clicked.connect(self.onglet_liste__enregistrer)
        
        # Bouton de supression de série
        self.boutonSupprimerSerie.clicked.connect(self.onglet_liste__supprimer_serie)
        

        # ----- Onglet planning -----
        self.planningCalendrier.clicked.connect(self.onglet_planning__planning__changement_selection)
        self.planningCalendrier.selectionChanged.connect(self.onglet_planning__planning__changement_selection)

        self.boutonPlanningInserer.clicked.connect(self.onglet_planning__liste_animes_vus__ligne__inserer)
        self.animeEnCoursTable.cellDoubleClicked.connect(self.onglet_planning__liste_animes_vus__ligne__inserer)
        
        self.boutonPlanningReset.clicked.connect(self.onglet_planning__calendrier__aujourdhui)

        self.supprimerElementPlanningBouton.clicked.connect(self.onglet_planning__liste_animes_vus__ligne__supprimer)
        
        self.boutonPlanningSauvegarder.clicked.connect(self.onglet_planning__enregistrer)
        

        # ----- Onglet album -----
        self.testButton.clicked.connect(self.personnages_favoris)
        
        
        # ----- Onglet outils -----
        self.pushButton.clicked.connect(self.outils_calcul_temps_calcul)


        # ----- Onglet préférences -----
        self.pushButton_5.clicked.connect(self.exportation_du_profil)
        self.pushButton_3.clicked.connect(self.suppression_du_profil)


        # Remplace le numéro de version
        self.barreDeStatus.showMessage("Version %s" %__version__)

        # Evenement de fermeture de l'application
        self.closeEvent = self.fermer
        
        
    def __init__systray(self):
        """Fonction qui contiends le code du systray"""
        
        # Icone en zone de notification
        self.tray = PyQt4.QtGui.QSystemTrayIcon(self)
        self.tray.setIcon(PyQt4.QtGui.QIcon("./data/icons/icon.png"))
        
        # Création d'un menu contextuel pour le 
        self.tray.menuContextuel = PyQt4.QtGui.QMenu()
    
        # Charge l'icone pour la fermeture
        self.tray.iconeQuitter = PyQt4.QtGui.QIcon("./data/icons/edit-delete-5.ico")

        # Créer l'action dans le menu
        self.tray.actionfermer = (PyQt4.QtGui.QAction(self.tray.iconeQuitter, "Quitter", self))
     
        # Evenement de l'action fermer
        self.tray.actionfermer.triggered.connect(self.fermer)
        
        # Ajout de l'action dans le menu
        self.tray.menuContextuel.addAction(self.tray.actionfermer)
        
        # Ajout du menu contextuel en clic droit
        self.tray.setContextMenu(self.tray.menuContextuel)
        
    # Affichage de l'icone dans la zone de notifications
        self.tray.show()


    def _init__variables(self):
        """Initialisation des variables qui serons utilisées par plusieurs fonctions"""
        ongletListeSerieInfo = ""
        ongletListeSaisonInfo = ""


    def util__serie_id(self, serieTitre):
        """Renvoi le titre de la série associée à l'indentifiant donné"""

        curseur.execute("""
                        SELECT serieId
                        FROM serie
                        WHERE serieTitre = \"%s\"
                        """ %serieTitre)
                       
        return curseur.fetchone()[0]
        
        
    def util__serie_existe(self, serieId):
        """Renvoi le titre de la série associée à l'indentifiant donné"""

        curseur.execute("""
                        SELECT serieId
                        FROM serie
                        WHERE serieId = \"%s\"
                        """ %serieId)
                       
        return curseur.fetchone()[0]


    def recherche_mise_a_jour(self):
        """Fontion de vérification de mise a jour""" 
        
        log.info("Recherche de mises a jour...")
         
        # Téléchargement du fichier contenant la dernière version disponible sur github
        url = "https://raw.githubusercontent.com/seigneurfuo/MyAnimeManager/master/version.txt"
        
        try:
            log.info("  Connection au serveur de mise a jour")
            request = urllib.urlopen(url)
            data = request.read()
            versionRecente = data.replace("\n", "")
            
            # Supression des variables inutiles
            del request, data
        
            # Vérification de la version
            if LooseVersion(__version__) < LooseVersion(versionRecente):
                log.info("  Une nouvelle mise a jour est disponible")
                self.tray.showMessage(__titre__, "Une mise a jour est disponible", msecs = 10000)
            
            else:
                log.info("  L'application est a jour")
                return True
        
        except:
            log.info("  Impossible de contacter le serveur de mise a jour")
            self.tray.showMessage(__titre__, "Impossible de verifier la version en ligne", msecs = 10000)


    def chargement_onglet(self, dump):
        """Fonction déclanché a chaque fois qu'un onglet est chargé"""
        
        ongletId = self.tabWidget.currentIndex()
        log.info("Id onglet actif: %s" %ongletId)
        
        # Onglet planning
        if ongletId == 0:
            self.onglet_planning__liste_animes_en_cours__remplir()
            self.onglet_planning__liste_animes_vus__remplir()
        
        # Onglet liste d'animé
        elif ongletId == 1: self.onglet_liste__liste_serie__remplir()
        
        # Onglet album
        elif ongletId == 2: self.personnages_favoris()


    def onglet_liste__liste_serie__remplir(self):
        """Génére la liste qui contiends touts les séries disponibles"""
        
        curseur.execute("SELECT * FROM serie ORDER BY LENGTH(serieId) ASC") # Permet de trier les animés de manière croissante et de manière humaine (evite que des identifiants tel que 1000 s'intercalent entre les identfiant 100 / 101
        listeDesSeries = curseur.fetchall()
        
        # Définition du titre des colonnes
        colonnes = ["Id", "Episode"]
        
        # Définition de la taille du tableau
        nombreColonnes = len(colonnes)
        nombreLignes = len(listeDesSeries)

        self.seriesTable.setHorizontalHeaderLabels(colonnes)
        self.seriesTable.setColumnCount(nombreColonnes)
        self.seriesTable.setRowCount(nombreLignes)

        # Ajout des éléments
        for indice, serie in enumerate(listeDesSeries):
            planningIdentifiantSaison = str(serie["serieId"])
            colonne1 = PyQt4.QtGui.QTableWidgetItem(planningIdentifiantSaison)
            self.seriesTable.setItem(indice, 0, colonne1)
            
            planningEpisodeId = str(serie["serieTitre"])
            colonne2 = PyQt4.QtGui.QTableWidgetItem(planningEpisodeId)
            self.seriesTable.setItem(indice, 1, colonne2)


    def onglet_liste__infos_serie__effacer(self):
        """La fonction qui efface les entrés (les instructions auraient pus etres contenues dans liste_affiche mais je souhaitais séparer les deux blocs)"""

        # On vide la liste les entrées
        self.serieIdEntry.setText(str())
        self.serieTitreEntry.setText(str())

  
    def onglet_liste__infos_serie__remplir(self):
        """Cette fonction permet de remplir l'identifiant et le titre de l'animé lorsque celui-ci est sélectionné et qu'aucunne saison ne l'est"""
        
        listeSerieLigneActuelle = int(self.seriesTable.currentRow())
        
        # Si on a bien sélectionné un anime (empèche l'erreur quand la liste est rechargée et que rien n'est sélectionné)
        if listeSerieLigneActuelle != -1:
            serieId = self.seriesTable.item(listeSerieLigneActuelle, 0).text()
            serieTitre = self.seriesTable.item(listeSerieLigneActuelle, 1).text()
            
            # Remplissage des informations
            self.serieIdEntry.setText(serieId)
            self.serieTitreEntry.setText(serieTitre)
            
            curseur.execute("SELECT serieFavori FROM serie WHERE serieId='%s'" %serieId)
            favoris = curseur.fetchall()
            for ligne in favoris:
				if ligne["serieFavori"] == 1 :
					self.serieFavoriCheckBox.setChecked(True)

            
    def onglet_liste__liste_saison__remplir(self):
        """Genere la liste qui contiendra les saisons pour l'anime selectionné"""
        
        listeSerieLigneActuelle = int(self.seriesTable.currentRow())

        # Si on a bien sélectionné un anime (empèche l'erreur quand la liste est rechargée et que rien n'est sélectionné)
        if listeSerieLigneActuelle != -1:
            serieId = self.seriesTable.item(listeSerieLigneActuelle, 0).text()
            serieTitre = self.seriesTable.item(listeSerieLigneActuelle, 1).text()
            
            curseur.execute("SELECT * FROM saison, serie WHERE saisonSerieId = serieId AND saisonSerieId = %s ORDER BY saisonId ASC" %serieId) # Permet de trier les animés de manière croissante et de manière humaine (evite que des identifiants tel que 1000 s'intercalent entre les identfiant 100 / 101
            listeDesSaisons = curseur.fetchall()
            
            # Définition de la taille du tableau
            nombreColonnes = 2
            nombreLignes = len(listeDesSaisons)

            self.serieSaisonsTable.setColumnCount(nombreColonnes)
            self.serieSaisonsTable.setRowCount(nombreLignes)

            # Ajout des éléments
            for indice, serie in enumerate(listeDesSaisons):
                saisonId = str(serie["saisonId"])
                colonne1 = PyQt4.QtGui.QTableWidgetItem(saisonId)
                self.serieSaisonsTable.setItem(indice, 0, colonne1)
                
                saisonTitre = str(serie["saisonTitre"])
                
                # Si le titre n'est pas défini, on utilise celui de la série
                if saisonTitre == "" or saisonTitre == "None": saisonTitre = serieTitre

                colonne2 = PyQt4.QtGui.QTableWidgetItem(saisonTitre)
                self.serieSaisonsTable.setItem(indice, 1, colonne2)  


    def onglet_liste__infos_saison__remplir(self):
        """Fonction qui affiche les information pour l'animé sélectionné"""
        
        # Récupère le numéro de ligne actuellement sélectionné dans la liste
        listeSerieLigneActuelle = int(self.seriesTable.currentRow())
        listeSaisonsLigneActuelle = int(self.serieSaisonsTable.currentRow())

        # Si on a bien sélectionné un anime (empèche l'erreur quand la liste est rechargée et que rien n'est sélectionné)
        if listeSaisonsLigneActuelle != -1:
            # Le titre de l'animé est contenu dans la premiere cellule de la colonne (les indices commencent à 0)
            serieId = self.seriesTable.item(listeSerieLigneActuelle, 0).text()
            serieTitre = self.seriesTable.item(listeSerieLigneActuelle, 1).text()
            saisonId = self.serieSaisonsTable.item(listeSaisonsLigneActuelle, 0).text()
            saisonTitre = self.serieSaisonsTable.item(listeSaisonsLigneActuelle, 1).text()

            # On cherche les informations dans la base SQL
            curseur.execute("""SELECT * FROM serie, saison
                               WHERE saisonSerieId = serieId 
                               AND saisonId = '%s' 
                               AND serieId = '%s'""" 
                               %(saisonId, serieId)
                           )

            # Charge les informations récupérées dans la base sql
            resultats = curseur.fetchone() # Permet de ne choisir que le premier résultat en sql (pour un seul identifiant, on ne peut avoir qu'un seul animé

            saisonAnnee = str(resultats["saisonAnnee"])
            saisonStudio = resultats["saisonStudio"]
            saisonFansub = resultats["saisonFansub"]
            saisonDateAjout = str(resultats["saisonDateAjout"])
            saisonEpisodesNombre = str(resultats["saisonEpisodesNombre"])
            saisonVisionnageEtat = str(resultats["saisonVisionnageEtat"])
            saisonVisionnageNombre = str(resultats["saisonVisionnageNombre"])
            saisonCommentaires = resultats["saisonCommentaires"]
            
            # Application des valeurs
            self.saisonIdEntry.setText(saisonId)
            self.saisonTitreEntry.setText(saisonTitre)

            # Affiche le texte si la base ne retourne pas None: Permet d'autrepasser le bug d'encodage UFT8
            
            # Entrée saisonAnnee
            if saisonAnnee != "None": 
                self.saisonAnneeEntry.setText(str(saisonAnnee))

            # Entrée saisonStudio
            if saisonStudio != None: 
                self.saisonStudioEntry.setText(saisonStudio)
                     
            # Entrée saisonFansub
            if saisonFansub != None: 
                self.saisonFansubEntry.setText(saisonFansub)
            
            # Entrée saisonDateAjout
            if saisonDateAjout != "None":
                self.saisonDateAjoutEntry.setText(saisonDateAjout)

            # Entrée saisonEpisodesNombre
            if saisonEpisodesNombre != "None":
                self.saisonEpisodesNombreSpinBox.setValue(int(saisonEpisodesNombre))
             
            # Entrée saisonVisionnageEtat
            if saisonVisionnageEtat != "None": 
                # Animé Terminé =  0
                # Animé en cours = 1
                # Animé a voir   = 2
                # Animé indéfini = 3
                self.saisonVisionnageEtatComboBox.setCurrentIndex(int(saisonVisionnageEtat))

            # Entrée saisonVisionnageNombre
            if saisonVisionnageNombre != "None":
                self.saisonVisionnageNombreSpinBox.setValue(int(saisonVisionnageNombre))
            

            #if ligne["animeNotes"] != None: 
                #self.notesEntry.setText(ligne["animeNotes"])


            # Charge et affiche l'image de l'anime
            image = str(serieId)
            chemin = os.path.join("./data/covers", image)

            log.info("Image de couverture: %s" %chemin)

            # Charge et affiche l'image
            myPixmap = PyQt4.QtGui.QPixmap(chemin)
            image = myPixmap.scaled(self.label_5.size(), PyQt4.QtCore.Qt.IgnoreAspectRatio, PyQt4.QtCore.Qt.SmoothTransformation)
            self.label_5.setPixmap(image)
            
        
    def onglet_liste__infos_saison__effacer(self):
        """Fonction qui supprime les informations pour une saison"""
        
        # Vide les valeurs pour les champs
        self.saisonIdEntry.setText(str())
        self.saisonTitreEntry.setText(str())
        self.saisonAnneeEntry.setText(str())
        self.saisonStudioEntry.setText(str())
        self.saisonDateAjoutEntry.setText(str())
        self.saisonEpisodesNombreSpinBox.setValue(0)
        self.saisonVisionnageNombreSpinBox.setValue(0)
        
        # Image de l'animé vide
        myPixmap = PyQt4.QtGui.QPixmap("./data/icons/image-x-generic.png")
        image = myPixmap.scaled(self.label_5.size(), PyQt4.QtCore.Qt.KeepAspectRatio, PyQt4.QtCore.Qt.SmoothTransformation)
        self.label_5.setPixmap(image)
    
    
    def onglet_liste__liste_serie__changement_selection(self):
		"""Fonctions qui serons appelées lors du changement de sélection dans la liste série"""
        
		self.onglet_liste__infos_saison__effacer()
		self.onglet_liste__liste_saison__effacer()
		self.onglet_liste__infos_serie__effacer()
        
		self.onglet_liste__infos_serie__remplir()
		self.onglet_liste__liste_saison__remplir()

    
    def onglet_liste__liste_saison__changement_selection(self):
        """Fonction appellée lors du changement de selection dans un élement de la liste saison"""
        
        self.onglet_liste__infos_saison__effacer() # Efface les informations sur la série
        self.onglet_liste__infos_saison__remplir() # Remplissage des informations


    def onglet_liste__liste_serie__effacer(self):
        """Fonction qui vide les entrées de la liste des séries"""
        
        self.seriesTable.clear()
        

    def onglet_liste__liste_saison__effacer(self):
        """Fonction qui vide les entrées de la liste des saisons"""
        
        self.serieSaisonsTable.clear()


    def onglet_liste__rafraichir(self):
        """Fonction qui nettoie et affiche remplir la liste des animes avec les nouvelles valeurs"""
        
        # Efface
        self.onglet_liste__infos_serie__effacer()
        self.onglet_liste__liste_saison__effacer()
        self.onglet_liste__liste_serie__effacer()
        
        # Recharge
        self.onglet_liste__liste_serie__remplir()
        
        
    def onglet_liste__annuler(self):
        """Efface uniquement les information sur la série et la saison sélectionnée, evite de recharger toute la liste des animés puisque rien n'a été enregistré"""
        
        # Efface uniquement les élement a ne plus afficher
        self.onglet_liste__infos_serie__effacer()
        self.onglet_liste__liste_saison__effacer()


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


    def onglet_liste__enregistrer(self):
        """Fonction qui enregistre les données des animés dans la bdd"""
		# ----- Série ------

        # Si un identifiant valide a été rentré
        #if serieId != "" or re.findall("^-?[0-9]+$", serieId):
        listeSaisonLigneActuelle = int(self.serieSaisonsTable.currentRow())

        serieTitre = self.serieTitreEntry.text()

        # Animé favoris ?
        boolToDec = {True:"1", False:"0"}
        serieFavoriCheckboxState = self.serieFavoriCheckBox.isChecked()
        serieFavori = boolToDec[serieFavoriCheckboxState]

        # Génération de la commande SQL pour modifier les informations de la série
        log.info("Enregistrement des infos de la série")
        
        print util__serie_existe()
        
        if 
        curseur.execute("INSERT INTO serie (serieId, serieTitre, serieFavori) VALUES ('%s', '%s', '%s') WHERE serieId" %(serieId, serieTitre, serieFavori))

        
        else:
        

        # ----- Saison ------
        saisonId = self.saisonIdEntry.text()
        saisonTitre = self.saisonTitreEntry.text()
        saisonAnnee = self.saisonAnneeEntry.text()
        saisonStudio = self.saisonStudioEntry.text()
        saisonFansub = self.saisonFansubEntry.text()
        saisonDateAjout = self.saisonDateAjoutEntry.text()
        saisonEpisodesNombre = str(self.saisonEpisodesNombreSpinBox.value())
        saisonVisionnageEtat = str(self.saisonVisionnageEtatComboBox.currentIndex())
        saisonVisionnageNombre = str(self.saisonVisionnageNombreSpinBox.value())	

        # Génération de la commande SQL pour modifier les informations de la saison
        log.info("Enregistrement des infos de la saison")
        curseur.execute("INSERT OR REPLACE INTO saison (saisonId, saisonSerieId, saisonTitre, saisonAnnee, saisonStudio, saisonFansub, saisonEpisodesNombre, saisonVisionnageEtat, saisonVisionnageNombre, saisonDateAjout) VALUES ('%s, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" %(saisonId, serieId, saisonTitre, saisonAnnee, saisonStudio, saisonFansub, saisonEpisodesNombre, saisonVisionnageEtat, saisonVisionnageNombre, saisonDateAjout))

        # On indique a l'application que quelque chose a été modifié
        self.modifications = True

        # Rafraichi après avoir enregistré
        self.onglet_liste__rafraichir()

    # Si l'identifiant n'a pas été rempli
        #else:
            # Remplacer la fenetre par une version 1 bouton.
            information = PyQt4.QtGui.QMessageBox.information(self, "Identifiant invalide", "Veuillez entrer un identifiant comportant uniquement de chiffres !", "Continuer")


# Fonctions de l'onglet planning
    def onglet_planning__liste_animes_en_cours__remplir(self):
        """Fonction qui ajoute les animés en cours dans la liste des animes en cours"""
        
        # On vide la liste des animés
        self.animeEnCoursTable.clear()

        # On éxécute la commande sql qui retourne: les animés en cours de visionnage qui avec leur épisode vu le plus récent
        curseur.execute("""
                        SELECT *
                        FROM serie, saison
                        WHERE saisonSerieId = serieId
                        AND saisonVisionnageEtat = 1
                        AND saisonEpisodesNombreVus < saisonEpisodesNombre
                        """)

        animesEnCours = curseur.fetchall()

        # Définition de la taille du tableau
        nombreLignes = len(animesEnCours)
        self.animeEnCoursTable.setRowCount(nombreLignes)
        self.animeEnCoursTable.setColumnCount(3)

        # Définition du titre des colonnes
        titreColonnes = ["Titre", "Saison", "Episode"]
        self.animeEnCoursTable.setHorizontalHeaderLabels(titreColonnes)

        # Ajout des éléments
        for indice, serie in enumerate(animesEnCours):
            
            colonne1 = PyQt4.QtGui.QTableWidgetItem(str(serie["serieTitre"]))
            self.animeEnCoursTable.setItem(indice, 0, colonne1)
            
            colonne2 = PyQt4.QtGui.QTableWidgetItem(str(serie["saisonId"]))
            self.animeEnCoursTable.setItem(indice, 1, colonne2)
            
            episodeAVoirId = int(serie["saisonEpisodesNombreVus"]) +1
            
            # On rajoute +1 au nombre d'épisodes vus pour proposer le suivant qui lui, n'a pas été vu
            colonne3 = PyQt4.QtGui.QTableWidgetItem(str(episodeAVoirId))
            self.animeEnCoursTable.setItem(indice, 2, colonne3)
            



    def onglet_liste__supprimer_serie(self):
        """Fonction qui permet de supprimer une série de la base de données"""
        
        log.info("Supression d'un série !")
        
        # Récupèration du numéro de ligne actuellement sélectionné dans la liste
        listeSerieLigneActuelle = int(self.seriesTable.currentRow())

        log.info(listeSerieLigneActuelle)

        # Si on a bien sélectionné une série (empèche l'erreur quand la liste est rechargée et que rien n'est sélectionné)
        if listeSerieLigneActuelle != -1:
            # Le titre de l'animé est contenu dans la premiere cellule de la colonne (les indices commencent à 0)
            serieId = self.seriesTable.item(listeSerieLigneActuelle, 0).text()

            log.info("Supression de la serie ayant pour id: %s" %serieId)

            # Suppression des saisons associées
            curseur.execute("DELETE FROM Saison WHERE saisonSerieId = %s" %serieId)

            # Supression de la série
            curseur.execute("DELETE FROM serie WHERE serieId = %s" %serieId)
            
            # On informe le programme que des chose ont été modifiés
            self.modifications = True
            
            # Rafraichissement de l'onglet liste
            self.onglet_liste__rafraichir()
        

    def onglet_planning__planning__changement_selection(self):
        """Fonction appelée lors du changement de la date"""
        
        # On vide la liste des animés vus
        self.animeVuTable.clear()
        self.onglet_planning__liste_animes_vus__remplir()


    def onglet_planning__liste_animes_vus__ligne__inserer(self):
        """Action qui insere un anime dans la liste des animes vus"""
        
        ligneSelectionnee = self.animeEnCoursTable.currentRow()
        
        # Si la ligne n'est pas vide
        if ligneSelectionnee != -1:
   
            # Récupère le nombre de lignes dans animeVuTable pour insérer de nouveaux épisodes à la suite
            nombreLignesAnimeEnCoursTable = int(self.animeVuTable.rowCount())
            
            self.animeVuTable.insertRow(nombreLignesAnimeEnCoursTable)
            
            # Récupération des variables
            serieTitre = str(self.animeEnCoursTable.item(ligneSelectionnee, 0).text())
            planningSaisonId = self.animeEnCoursTable.item(ligneSelectionnee, 1).text()
            planningEpisodeId = self.animeEnCoursTable.item(ligneSelectionnee, 2).text()
            
            # Remplissage des colonnes SerieId
            colonne1 = PyQt4.QtGui.QTableWidgetItem(str(serieTitre))
            self.animeVuTable.setItem(nombreLignesAnimeEnCoursTable, 0, colonne1)
            
            # Remplissage des colonnes SaisonId
            colonne2 = PyQt4.QtGui.QTableWidgetItem(planningSaisonId)
            self.animeVuTable.setItem(nombreLignesAnimeEnCoursTable, 1, colonne2)

            # Remplissage des colonnes EpisodeId
            colonne3 = PyQt4.QtGui.QTableWidgetItem(str(planningEpisodeId))
            self.animeVuTable.setItem(nombreLignesAnimeEnCoursTable, 2, colonne3)
            

    def onglet_planning__liste_animes_vus__ligne__supprimer(self):
        ligneSelectionnee = self.animeVuTable.currentRow()
        
        # Si la ligne n'est pas vide
        if ligneSelectionnee != -1:
        
            # Suppression dans la base de données
            dateSelectionnee = self.planningCalendrier.selectedDate().toPyDate()
            
            serieTitre = self.animeVuTable.item(ligneSelectionnee, 0).text()
            saisonId = self.animeVuTable.item(ligneSelectionnee, 1).text()
            planningEpisodeId = self.animeVuTable.item(ligneSelectionnee, 2).text()
            
            serieId = self.util__serie_id(serieTitre)
            
            commandeSQL = """
                      DELETE FROM planning
                      WHERE planningSerieId = %s
                      AND planningSaisonId = %s
                      AND planningEpisodeId = %s
                      AND planningDate = '%s'
                     """ %(serieId, saisonId, planningEpisodeId, dateSelectionnee)
            
            
            log.info(commandeSQL)
            curseur.execute(commandeSQL)
            
            # Supprime la ligne actuelle dans la table
            self.animeVuTable.removeRow(ligneSelectionnee)
            
            # Décrémentation du nombre d'épisodes vus 
            curseur.execute("UPDATE saison SET saisonEpisodesNombreVus = saisonEpisodesNombreVus-1 WHERE saisonId=%s" %saisonId)

            self.modifications = True

        
    def onglet_planning__enregistrer(self):
        """Fonction qui enregistre le planning pour la date donnée"""    
        
        log.info("Enregistrement du planning")
        
        # Récupère le nombre de lignes du tableau AnimeVus
        nombreLignes = self.animeVuTable.rowCount()
        
        # Pour chaque élément, on va créer son entrée dans la table
        for idLigne in range(0, nombreLignes):

            # Récuparation des variables depuis le texte de la liste
            serieTitre = self.animeVuTable.item(idLigne, 0).text()
            saisonId = self.animeVuTable.item(idLigne, 1).text()
            episodeId = self.animeVuTable.item(idLigne, 2).text()

            # On recupère l'identifiant correspondant au titre de l'anime
            serieId = self.util__serie_id(serieTitre)

            # Récupération de la date depuis le calendrier
            planningDate = str(self.planningCalendrier.selectedDate().toPyDate())
            
            # Suppression de tout les épisodes (permet de'outrepasser le bug des "épisodes en double
            curseur.execute("DELETE FROM planning WHERE planningDate = '%s' AND planningSerieId = %s AND planningSaisonId = '%s' AND planningEpisodeId = '%s'" %(planningDate, serieId, saisonId, episodeId))
            
            # Enregistrement de l'episode vu dans la table planning
            curseur.execute("INSERT INTO planning (planningDate, planningSerieId, planningSaisonId, planningEpisodeId) VALUES ('%s', %s, %s, %s)" %(planningDate, serieId, saisonId, episodeId))
            
            # Incrementation du nombre d'épisodes vus 
            curseur.execute("UPDATE saison SET saisonEpisodesNombreVus = saisonEpisodesNombreVus+1 WHERE saisonId=%s" %saisonId)
            
            self.modifications = True


    def onglet_planning__liste_animes_vus__remplir(self):
        """Rempli la liste des animés vus en fonction de la date séléctionnée dans le calendrier"""
        
        dateSelectionnee = self.planningCalendrier.selectedDate().toPyDate()
        
        # On éxécute la commande sql qui retourne: les animés en cours de visionnage qui avec leur épisode vu le plus récent
        curseur.execute("""
                        SELECT *
                        FROM serie, saison, planning
                        WHERE saisonSerieId = serieId
                        AND planningSerieId = serieId
                        AND planningSerieId = saisonSerieId
                        AND planningSaisonId = saisonId
                        AND planningDate = '%s'
                        """
                        %dateSelectionnee)

        animesVus = curseur.fetchall()

        # Définition de la taille du tableau
        nombreLignes = len(animesVus)
        self.animeVuTable.setRowCount(nombreLignes)
        self.animeVuTable.setColumnCount(3)

        # Définition du titre des colonnes
        titreColonnes = ["Titre", "Saison", "Episode"]
        self.animeVuTable.setHorizontalHeaderLabels(titreColonnes)

        # Ajout des éléments
        for indice, serie in enumerate(animesVus):
            
            colonne1 = PyQt4.QtGui.QTableWidgetItem(str(serie["serieTitre"]))
            self.animeVuTable.setItem(indice, 0, colonne1)
            
            colonne2 = PyQt4.QtGui.QTableWidgetItem(str(serie["saisonId"]))
            self.animeVuTable.setItem(indice, 1, colonne2)
            
            colonne3 = PyQt4.QtGui.QTableWidgetItem(str(serie["planningEpisodeId"]))
            self.animeVuTable.setItem(indice, 2, colonne3)


    def onglet_planning__calendrier__aujourdhui(self):
        """Fonction qui séléctionne la date actuelle sur le calendrier"""
        
        # Demande à Qt la date du jour
        aujourdhui = PyQt4.QtCore.QDate.currentDate ()

        # Affiche le caldendrier à la date du jour
        self.planningCalendrier.setSelectedDate(aujourdhui)


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
                
                log.info("Image chargee: ./data/characters/%s_%s" %(pageId, imageId))

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

    
    def importation_du_profil(self):
        """Fonction qui permet d'importer un profil"""
        
        cheminDeSauvegarde = PyQt4.QtGui.QFileDialog(self)


    def exportation_du_profil(self):
        """Fonction qui permet d'exporter un profil"""

        cheminDeSauvegarde = PyQt4.QtGui.QFileDialog(self)


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


# Fonction principale
if __name__ == "__main__":
    log.info("Version: %s" %__version__)
    
    # Parsage des arguments
    argParser = argparse.ArgumentParser()
    argParser.add_argument("-noupdate", action="store_true", default=False)
    argParser.add_argument("-nocheckdirectories", action="store_true", default=False)
    args = argParser.parse_args()
    
    if args.nocheckdirectories == False:
        # Vérification des dossiers
        verification_des_dossiers()

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
        log.info("La bdd n'existe pas ! Creation d'un nouveau profil")
        creation_de_la_bdd()

    # Définition de l'application pyQt
    app = PyQt4.QtGui.QApplication(sys.argv)     
    
    # Création de la fenetre principale
    fenetrePrincipale = Main(None)
    fenetrePrincipale.show()
 
    # Lancement de la boucle de l'application pyQt   
    app.exec_()
