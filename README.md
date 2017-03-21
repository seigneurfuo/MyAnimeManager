[French]
# Synopsis
Un petit projet Python et PyQt pour gérer sa collection d'animés.
![alt tag](https://raw.githubusercontent.com/seigneurfuo/MyAnimeManager/master/data/docs/2016-10-27_00-41-12.png)

# Avancement du projet
- A ce jour, une version supportant les saisons ainsi qu'un gestion des épisodes vus est actuellement en developpement.

# Fonctionnalités
- 2 modes de remplissage des informations: manuellement ou automatique grace au informations du site MyAnimeList.net
- Prise de note pour chaque animé
- Un planning intéractif pour organiser les épisodes a voir
- Une liste de vos personnages préférés

# Licenses
Icones venant du projet: http://sourceforge.net/projects/openiconlibrary

# Librairies utilisées
- PyQt: Une librairie utilisée pour créer des interfaces graphiques
- BeautifulSoup: Utilisé par le module myanimelist pour récupérer les informations sur le site web MyAnimeList.net
- Lassie: Utilisé par le module myanimelist pour récupérer les images des différents animés (Sera remplacé par BeautifulSoup)

# Installation

## Windows 32bits / 64bits
- Python 2 (https://www.python.org/ftp/python/2.7.12/python-2.7.12.msi)
- PyQt4 (http://sourceforge.net/projects/pyqt/files/PyQt4/PyQt-4.11.4/PyQt4-4.11.4-gpl-Py2.7-Qt4.8.7-x32.exe)
- BeautifulSoup4 (https://pypi.python.org/pypi/beautifulsoup4)
- Lassie: (https://pypi.python.org/pypi/lassie)

## Ubuntu / Debian / Linux Mint
- sudo apt-get python-qt4
- sudo install python-pip
- sudo pip install beautifulsoup4
- sudo pip install lassie

# A faire
- Ajouter la création des dossiers automatiquement lors du premier démarrage
- Séparer les animés par saison (QTreeView)
- Ajouter un système de tags
- Continuer la fonction de MAJ de la base de donnée pour les prochaines versions
- Vider le champ de recherche et MAL lorsque a la fin de l'édition d'un animé
- Ajouter des préférences, afin de modifier: l'emplacement de la bdd, l'emplacement des fichiers images
- Coder la fenetre directement dans le code - sans utilisation de QtDesign ou alors enregistrer le contenu du fichier d'interface dans une docstring dans le code
- Renommer les noms des élements génériques. Exemple: Bouton1, bouton2...
- Empécher de remplir les informations d'un animé si il n'a pas d'indentifiant
- Les animés avec \":\" dans l'url bloquent sur une erreur 404
