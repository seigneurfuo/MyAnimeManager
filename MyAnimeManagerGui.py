#! /usr/bin/python
# -*- coding: cp1252 -*- 

# Logging
import logging
log = logging.getLogger()
log.setLevel(logging.DEBUG)

# Librairies standards
import sys
sys.path.append("./data/libs")
import os
import sqlite3
import pprint
import re
from datetime import date, datetime, time, timedelta
import json

# Librairies de tierces-parties
import myanimelist
import devtool; devtool.show_stats(sys.argv[0])

# Importation de pyQt
try:
    import PyQt4.QtGui
    import PyQt4.uic.loadUiType
except:
    log.error("L'application n'arrive pas a trouver Qt / pyQt !")

# Informations sur l'application
__titre__                = "MyAnimeManager"
__version__              = "0.10.%s" % devtool.buildNumber
__auteur__               = "seigneurfuo"
__db_version__           = 3
__dateDeCreation__       = "12/06/2016"
__derniereModification__ = "23/07/2016"

# Cr�ation d'un formateur qui va ajouter le temps, le niveau de chaque message quand on �crira un message dans le log
formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s') 

# handler qui va rediriger chaque �criture de log sur la console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)
log.addHandler(console_handler)

# D�tails
toDo = ["Utiliser le titre de l'anim� plutot que son identifiant pour la compl�tion MAL",
        "Continuer la fonction de MAJ de la base de donn�e pour les prochaines versions",
        "Vider le champ de recherche et MAL lorsque a la fin de l'�dition d'un anim�",
        "Ajouter des pr�f�rences, afin de modifier: l'emplacement de la bdd, l'emplacement des fichiers images",
        "Images des anim�s charg�s directement via MAL - possibilit� de mise en cache ?",
        "Coder la fenetre directement dans le code - sans utilisation de QtDesign",
        "Ou alors enregistrer le contenu du fichier d'interface dans une docstring dans le code",
        "Renommer les noms des �lements g�n�riques. Exemple: Bouton1, bouton2..."]

# Fonctions g�n�rale a l'application
def creation_de_la_bdd():
    log.info("Cr�ation de la base de donnees")

# Table anime
    curseur.execute(
"""CREATE TABLE anime(
animeId TEXT PRIMARY KEY NOT NULL,
animeAjout TEXT,
animeTitre VARCHAR(100) NOT NULL,
animeAnnee INT,
animeStudio VARCHAR(20),
animeFansub VARCHAR(20),
animeEtatVisionnage VARCHAR(10),
animeFavori TEXT,
animeDateAjout TEXt,
animeNbVisionnage INT)""")

# Table planning
    curseur.execute(
"""
CREATE TABLE planning (
planningDate TEXT PRIMARY KEY NOT NULL,
planningAnime)""")

# Table informations
    curseur.execute(
"""
CREATE TABLE informations (
    version TEXT)""")

# Classe de la fenetre principale
class Menu(PyQt4.QtGui.QMainWindow, PyQt4.uic.loadUiType("./data/gui.ui")[0]): # Chargement des interfaces depuis les fichiers
    def __init__(self, parent=None):
        PyQt4.QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.setFixedSize(self.frameGeometry().width(), self.frameGeometry().height()) # Bloque le fenetre avec ses dimentions d'origine

        # Variables qui enregistre les modifications (Permet de ne pas afficher la fenetre d'enregistrement si rien n'a �t� modifi�)
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

        # Onglet planning
        self.calendarWidget.clicked.connect(self.planning_afficher)
        self.calendarWidget.selectionChanged.connect(self.planning_afficher)

        self.boutonPlanningInserer.clicked.connect(self.planning_animes_vus_inserer)
        self.listWidget_3.itemDoubleClicked.connect(self.planning_animes_vus_inserer)
        
        self.boutonPlanningReset.clicked.connect(self.planning_aujourdhui)
        self.boutonPlanningSauvegarder.clicked.connect(self.planning_enregistrer)

        # Onglet outils
        self.pushButton.clicked.connect(self.outils_calcul_temps_calcul)
        self.closeEvent = self.fermer

        # Remplace le num�ro de version A propos
        self.label_7.setText("version " + str(__version__))

        # Fonction a lancer en premier
        self.liste_rafraichir()
        self.planning_afficher()
        self.animes_vus_afficher()

    # La fonction qui efface les entr�s (les instructions auraient pus etres contenues dans liste_affiche mais je souhaitais s�parer les deux blocs)
    def liste_rafraichir(self, titreRecherche=False, favorisRecherche=False):
        # Image de l'anim� vide
        myPixmap = PyQt4.QtGui.QPixmap("./data/ekHFstR.png")
        image = myPixmap.scaled(self.label_5.size())
        self.label_5.setPixmap(image)

        # On vide la liste et les entr�es
        self.listWidget.clear()
        self.idEntry.setText(str())
        self.ajoutEntry.setText(str())
        self.titreEntry.setText(str())
        self.anneeEntry.setText(str())
        self.studioEntry.setText(str())
        self.fansubEntry.setText(str())
        self.malEntry.setText(str())

        # Reset spinbox
        self.spinBox.setValue(0)

        # Remise par d�fault des boutons radio
        self.radiobutton0.setChecked(False)
        self.radiobutton1.setChecked(False)
        self.radiobutton2_2.setChecked(False)
        self.radiobutton2.setChecked(True)
        
        self.favorisNonRadio.setChecked(True)

        # Si on recherche un anim�
        if titreRecherche != False and titreRecherche !="" :  
            log.info("Mode recherche textuelle")
            curseur.execute("SELECT * FROM anime WHERE animeTitre LIKE('%s%s%s') ORDER BY animeTitre" %("%", titreRecherche, "%"))
                
        else :
			# Si on veut afficher la liste des favoris
            if favorisRecherche == False:
                log.info("Affichage normal de la liste")
                curseur.execute("SELECT * FROM anime ORDER BY animeId")
            
            # Si on veut afficher la liste normale
            else:
                log.info("Mode favoris recherche")
                curseur.execute("SELECT * FROM anime WHERE animeFavori = '1' ORDER BY animeId")
        
            
        resultats = curseur.fetchall()
        log.info("anime recharg�s %s" %len(resultats))
        
        # Remplissage de la liste
        for anime in resultats:
            ligne = PyQt4.QtGui.QListWidgetItem(anime["animeTitre"])
            self.listWidget.addItem(ligne)


    # Fonction qui permet de rechercher un anim� dans la liste grace a son nom
    def liste_recherche(self):
        recherche = self.rechercheEntry.text()

        # Si le recherche est vid on ne l'active pas
        self.liste_rafraichir(titreRecherche = recherche)


    # Fonction qui permet de vider la liste de recherche
    def liste_recherche_vider(self):
        self.rechercheEntry.setText(str())
        self.liste_rafraichir()
        
    
    # Fonction qui affiche les anim�s favoris
    def liste_recherche_favoris(self):
        self.liste_rafraichir(favorisRecherche=True)


    def liste_afficher(self):
        animeTitre = [str(x.text()) for x in self.listWidget.selectedItems()]
        curseur.execute("SELECT * FROM anime WHERE animeTitre = '%s'" %animeTitre[0])

        # Pour les r�sultats trouv�s en SQL (1 max car on recherche l'anime en fonction de son titre)
        for ligne in curseur.fetchall():
            # Listes d'entr�es 
            self.idEntry.setText(str(ligne["animeId"]).replace("None", "")) # .replace("None", "")) Permet de ne pas afficher lorsq'une valeur est NULL
            self.ajoutEntry.setText(str(ligne["animeDateAjout"]).replace("None", ""))
            self.titreEntry.setText(str(ligne["animeTitre"]).replace("None", ""))
            self.anneeEntry.setText(str(ligne["animeAnnee"]).replace("None", ""))
            self.studioEntry.setText(str(ligne["animeStudio"]).replace("None", ""))
            self.fansubEntry.setText(str(ligne["animeFansub"]).replace("None", ""))

            # Spinbox 
            if ligne["animeNbVisionnage"] == None:
                self.spinBox.setValue(0)
            else:
                self.spinBox.setValue(ligne["animeNbVisionnage"])

            # Boutons radios visionnage
            # Anim� Termin�
            if ligne["animeEtatVisionnage"] == "0":
                self.radiobutton0.setChecked(True)

            # Anim� en cours
            elif ligne["animeEtatVisionnage"] == "1":
                self.radiobutton1.setChecked(True)

            # Anim� a voir
            elif ligne["animeEtatVisionnage"] == "2":
                self.radiobutton2_2.setChecked(True)

            # Anim� ind�fini
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
        
        log.info("Charg�: %s" %chemin)

        # Charge et affiche l'image
        myPixmap = PyQt4.QtGui.QPixmap(chemin)
        image = myPixmap.scaled(self.label_5.size())
        self.label_5.setPixmap(image)


    def liste_remplir_myanimelist(self):
        # R�cup�re l'identifiant entr� dans l'entr�e MAL
        
        # Version avec l'identifiant MAL
        idMyAnimeList = self.malEntry.text()
        myanimelist.anime(idMyAnimeList)

        # Remplissage des informations
        self.titreEntry.setText(myanimelist.titre())
        self.anneeEntry.setText(myanimelist.annee())
        self.studioEntry.setText(myanimelist.studio())

        #t�l�chargement de la cover
        animeId = str(self.idEntry.text())
        myanimelist.telecharger_image(animeId, "./data/covers/")

        # Mise a jour de l'image
        chemin = os.path.join(dossier, animeId)
        log.info("Charg�: %s" %chemin)
        
        # Charge et affiche l'image
        myPixmap = PyQt4.QtGui.QPixmap(chemin)
        image = myPixmap.scaled(self.label_5.size())
        self.label_5.setPixmap(image)


    # Fonction qui enregistre les donn�es des anim�s dans la bdd
    def liste_enregistrer(self):
        # Entr�es (entry)
        animeId = self.idEntry.text()
    
        animeTitre = self.titreEntry.text()
        animeDateAjout = self.ajoutEntry.text()
        animeAnnee = self.anneeEntry.text() 
        animeStudio = self.studioEntry.text()
        animeFansub = self.fansubEntry.text()
        animeNbVisionnage = self.spinBox.value()

        # Etat du visionnage (boutons radio)
        if self.radiobutton0.isChecked(): animeVisionnage = "0"
        elif self.radiobutton1.isChecked(): animeVisionnage = "1"
        elif self.radiobutton2_2.isChecked(): animeVisionnage = "2"
        elif self.radiobutton2.isChecked(): animeVisionnage = "3"
            
        # Anim� favoris ?
        if self.favorisNonRadio.isChecked(): animeFavori = "0"
        elif self.favorisOuiRadio.isChecked(): animeFavori = "1"

        # G�n�ration de la command SQL
        curseur.execute("INSERT OR REPLACE INTO anime (animeId, animeDateAjout, animeTitre, animeAnnee, animeStudio, animeFansub, animeEtatVisionnage, animeFavori, animeNbVisionnage) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" %(animeId, animeDateAjout, animeTitre, animeAnnee, animeStudio, animeFansub, animeVisionnage, animeFavori, animeNbVisionnage))

        # On indique a l'application que quelque chose a �t� modifi�
        self.modifications = True
            
        # Rafraichi apr�s avoir enregistr�
        self.liste_rafraichir()
        self.animes_vus_afficher()
        
        
# Fonctions de l'onglet planning

    def animes_vus_afficher(self):
        # On vide la liste des anim�s
        self.listWidget_3.clear()
		
        # On �x�cute la commande sql qui retourne les anim�s en cours de visionnage
        curseur.execute("SELECT * FROM anime WHERE animeEtatVisionnage = 1 ORDER BY animeId")
        animes_vus = curseur.fetchall()
        
        # Remplissage de la liste
        for anime_vu in animes_vus:
            ligne = PyQt4.QtGui.QListWidgetItem(anime_vu["animeTitre"])
            self.listWidget_3.addItem(ligne)


    # Fonction qui ajoute le titre d'un anim� en cours de visionnage dans la boite d'entr�e du journal
    def planning_animes_vus_inserer(self):
        # Sauvegarde du texte actuel
        ancienTexte = self.planningEntry.toPlainText()
        animeTitre = [str(x.text()) for x in self.listWidget_3.selectedItems()]
        
        # Si la boite de texte est vide
        if ancienTexte == "":
            nouveauTexte = str(animeTitre[0])
        #�Si le boite de texte comporte une ligne vide au dessus
        elif ancienTexte[-2:] == "\n\n":
            nouveauTexte = ancienTexte[:-1] + str(animeTitre[0])
        # Sinon, on affiche en gardant l'ancien texte
        else:
            nouveauTexte = ancienTexte + "\n" + str(animeTitre[0])

        #Affichage du nouveau titre
        self.planningEntry.setText(nouveauTexte)
		

    # Fonction qui affiche les anim�s vus en fonction de la date s�lectionn�e sur le calendrier
    def planning_afficher(self):
        # Vide la boite d'entr�e
        self.planningEntry.setText(str())
        date = self.calendarWidget.selectedDate().toPyDate()
        curseur.execute("SELECT * FROM planning WHERE planningDate = '%s'" %date)

        # Pour les r�sultats trouv�s en SQL (1 max car on recherche l'anime en fonction de son titre)
        for ligne in curseur.fetchall():
            #Listes d'entr�es 
            self.planningEntry.setText(str(ligne["planningAnime"]))


    # Fonction qui s�l�ctionne la date actuelle sur le calendrier
    def planning_aujourdhui(self):
        aujourdhui = PyQt4.QtCore.QDate.currentDate ()
        self.calendarWidget.setSelectedDate(aujourdhui)
        

    # Fonction qui enregistre le planning dans la bdd
    def planning_enregistrer(self):
        planningDate = str(self.calendarWidget.selectedDate().toPyDate())
        planningAnime = str(self.planningEntry.toPlainText())

        curseur.execute("INSERT OR REPLACE INTO planning (planningDate, planningAnime) VALUES ('%s', '%s')" %(planningDate, planningAnime))

        # On indique a l'application que quelque chose a �t� modifi�
        self.modifications = True


# Fonctions de l'onglet outils
    # Fonction qui permet de calculer l'heure de fin d'un visionnage a partir du nombre d'�pisodes a voir
    def outils_calcul_temps_calcul(self):
        # Effacement de la liste
        self.listWidget_2.clear()

        # R�cup�ration du contenu des spinbox
        nombreEpisodes = self.spinBox_2.value()
        dureeEpisode = self.spinBox_3.value()
        
        plageA = datetime.now()

        for x in range(0, nombreEpisodes):
            plageB = plageA + timedelta(minutes = dureeEpisode)
            heure = "%02d - %02d:%02d -> %02d:%02d" %(x + 1, plageA.hour, plageA.minute, plageB.hour, plageB.minute) # Chaine qui seras affich�e
            plage = PyQt4.QtGui.QListWidgetItem(heure) # Cr�ation de l'�l�ment
            self.listWidget_2.addItem(plage) #Ajout de l'�l�ment a la liste
            plageA = plageB # D�cale la plage


    # Fonction qui permet de modifier le comportement de l'application en fonction de param�trages
    def preferences_(self):
        fname = PyQt4.QtGui.QFileDialog.getOpenFileName(self, 'Open file', 'C:\\')


    # Ferme le programme et enregistre les modifications apport�es � la base de donn�es
    def fermer(self, event):
        
        # Si des modifications on �t� apport�es, on affiche la fenetre d'enregistrement
        if self.modifications == True:
            # Affiche la fenetre de dialogue
            avertissement = PyQt4.QtGui.QMessageBox.question(self, 'Message', "Voulez-vous sauvegarder les modifications ?", "Oui", "Non")

            if avertissement  == 0: # Si on clique sur Oui (Sauvegarder)
                bdd.commit() # Enregistre les modifications dans la bdd (il est ansi possible de fermer le programme pour ne pas enregistrer les nouvelles donn�es
                log.info("Modifications sauvegard�es")

        # On ferme proprement la bdd
        curseur.close()
        bdd.close()
        log.info("Bdd ferm�e")

        # Et on ferme le programme
        log.info("Fermeture du programme")
        sys.exit()

        
# Fonction principale
if __name__ == "__main__":
    # Chemins
    dossier = "N:\Temp [Auto]\python.MyAnimeManager\data\covers"
    #dossier = config["coverPath"]

    # Nom de la base de donn�e
    nomBdd = "./data/MyAnimeManager.sqlite3"
    bddVierge = False

    # Recherche si le fichier de la base de donn�e existe d�ja
    if not os.path.exists(nomBdd):
        bddVierge = True

    # On se connecte � la bdd (si elle n'existe pas elle sera cr�er mais restera vide)
    bdd = sqlite3.connect(nomBdd)
    bdd.row_factory = sqlite3.Row # Acc�s facile aux colonnes (Par leur nom et nom par leur emplacement)
    curseur = bdd.cursor()

    # Si la base de donn�e est vierge, on utilise la fonction creation_de_la_bdd()
    if bddVierge == True: 
        #PyQt4.QtGui.QMessageBox.information(Menu, "Information", "L'application va cr�er une base de donn�e pour la premi�re utilisation")
        creation_de_la_bdd()

    # Boucle principale (menu)
  
    # Titre de la fenetre
    app = PyQt4.QtGui.QApplication(sys.argv)
    fenetreMenu = Menu(None)
    fenetreMenu.show()
    app.exec_()
