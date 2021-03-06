# Changements

27/05/2017 - version 0.24.13
- POUR EFFECTUER CETTE MAJ, REMPLACER LE FICHIER update.py PAR CELUI-CI:
- BUGFIX: Une ligne commentée dans le fichier update.py empéchait l'extraction des mise à jour
- Le planning affiche désormais les futurs épisodes à voir.
- BUGFIX: Les fonction relatives au préchargement des onglets (remplissage des liste, des textbox, ...) était désactivé
- Renommage de quelques fonctions dont le nom portait à confusion (fonctions du planning essentiellement)
- BUGFIX: Les prochains épisodes à voir restaient bloqués à 9.
- Ajout et modification de certains icônes de l'interface
- Correction de certaines informations dans ce fichier changelog.md
- Correction d'une erreur UTF8 dans la fenetre de dialoge en cas d'erreur d'identifiant
- Correction d'erreurs UTF8 dans les bulles de notification
- BUGFIX: Le logo de l'application est désormais affiché dans "A propos" (erreur de chemin depuis Qt Designer)
- Modification mineure de l'interface du planning
- Modifications mineures de l'onglet "A propros"
- Création d'un onglet "Aide" qui affichera des images explicatives

19/05/2017 - version 0.24.05
- Réecriture du script de MAJ: la recherche de maj se fait à chaque lancement mais pour metre à jour automatiquement l'application, il faut lancer update.py manuellement
- La page de téléchargement du projet ne s'ouvre plus lors de la détection d'une nouvelle version

18/05/2017 - version 0.23.14
- Les épisodes à voir dans le planning sont automatiquement mis à jour quand le planning est validé

16/05/2017 - version 0.23.13
- Suppression de l'affichage des changements avec Webkit qui est obscelète (Fonctionne désormais sous Manjaro / Archlinux)
- Affiche maintenant la version distante lors d'une recherche de mise à jour

03/05/2017 - version 0.23.11
- BUGFIX: Le fond d'écran des personnages favoris était mal renseigné

02/05/2017 - version 0.23.10
- Modification de la structure des fichiers: Le profil utilisateur est sauvegardé dans ./profile, les ressources sont désormais dans un dossier propre ./ressources
- Déplacement de fonction dans des modules externes (./ressources/core/)
- Les erreurs d'importations sont désormais affichées par print() et non plus par log()
- La base de données passe en version 6 (mise à jour de type de champs)

26/04/2017 - version 0.22.50
- Déplacement des instuctions de log dans un module externe data/libs/log.py
- Modifications mineures de la documentation

21/04/2017 - version 0.22.48
- Ouverture de la page de téléchargement lors de la détection d'une nouvelle version

20/04/2016 - version 0.22.47
- Correction de documentation
- Changement de l'icone de l'application (Merci a Alexandre Vert pour le logo !)

07/12/2016 - version 0.22.46
- Remplacement des boutons radios favoris par une checkbox
- Le path des covers est noté en clair et non plus dans une variable globale
- FEATURE: Dans l'onglet planning, un tableau affiche le dernier episode vu avec le nom de l'animé

06/12/2016 - version 0.22.31
- Suppression des entrées urllib2 dans le code
- BUGFIX: Utilisation de urllib, (urllib 2 était utilisé (future migration ?)

04/12/2016 - version 0.22.30
- BUGFIX: Urllib.retrieve car urllib2.retrieve n'existe pas
- Affichage de la version dans la barre de status dans l'onglet à propos
- Ajout d'un visonneur web pour afficher le changelog

03/12/2016 - version 0.22.24
- BUGFIX: Importation de PyQt4.uic.loadUiType au lieux de PyQt4.uic
- Identation dans les logs pour certaines sous fonctions
- Remplacement des boutons radios pour l'état du visionnage par une liste déroulante
- Ajout d'une liste déroulante pour la liste des filtres
- L'onglet par défaut est le premier, peut importe celui selectionné dans la fichier gui.ui
- Affiche une cover par défault lorsque aucun animé n'est sélectionné
- Affichage d'un log error et fermeture de l'application en cas de librairie manquantes
- BUGFIX: Les boutons radio favoris ne s'activaient plus

23/11/2016 - version 0.21.75
- BUGFIX: Sélection simple dans la liste des animés
- Amélioration de la fonction de parsage des arguments, utilisation de la librairie argparse
- Modification de l'ordenancement des fonctions dans le code (nottement le system tray et la recherche de mise a jour qui sont maintenant des enfants de la fenetre principale
- BUGFIX: L'icone reste dans le systray meme une fois l'application fermée. Utilisation de la fonction pour quitter l'application pyQt: PyQt4.QtCore.QCoreApplication.exit(0)

18/11/2016 - version 0.21.20
- Ajout de bulle de notification si une version plus récente est disponible ou en cas d'erreur de connection
- BUGFIX: L'application propose des mises à jours alors que l'application l'est déja. Utilisation de la librairie distutils
- BUGFIX: L'application se ferme si il n'arrive pas à contacter le serveur de mises a jour
- Ajout d'une icon pour la zone de notification
- Ajout d'un menu contextuel dans la zone de notification
- Ajout d'une fonction pour quitter l'application (clic droit sur l'icone en zone de notification)
- Possibilité de démarrer l'application sans activer la recherche de mise a jour (option -noupdates)

17/11/2016 - version 0.20.85
- Utilisation du widget statusbar à la place d'un label pour la barre de status
- Création d'une fonction de recherche de mise a jour. Pour le moment, le message de MAJ est uniquement notifié dans les logs.

14/11/2016
- Renommage de la fonction animes_vus_afficher en planning_animes_vus_afficher
- L'insertion des animés dans le planning passe le focus sur la zone de texte
- Ajout d'une barre de status pour les informations diverses

13/11/2016 - version 0.20.80
- Renommage de la fonction liste_afficher en liste_afficher_infos_anim
- FEATURE: Ajout d'une fonction pour afficher les animés a voir"

09/11/2016 - version 0.20.65
- BUGFIX: Dans le planning, une insertion ne supprimais pas les sauts de lignes en trop.
- BUGFIX: Désormais, les onglets sont chargés uniquement lorsqu'ils sont visibles. Évite de charger / rafraîchir tout les onglets à la fois
- Ajout de log pour la fonction l'onglet Album

07/11/2016 - version 0.20.55
- BUGFIX: Il est désormais possible d'écrire des textes en UFT8 !
- BUGFIX: La bdd ne parse plus NONE, quand la chaîne ne contiens rien

02/11/2016 - version 0.20.43
- BUGFIX: Suppression des images des animés uniquement ci celle-ci existe
- Portage du module myanimelist lassie vers Beautifulsoup
- Renommage de la fonction "reset" en "suppression_du_profil"
- Suppression des doubles saut de ligne automatique dans le planning des animés
- La fonction de recherche d’animé par titre est en réécriture - elle est gelée pour le moment

31/10/2016 - version 0.20.25
- Modification de la fonction qui supprime les animés de la base: Supprime désormais les images de images
- Correction de bug: impossible de supprimer l'animé dans la liste

28/10/2016 - version 0.20.15
- Documentation des fonctions
- Ajout d'une confirmation lors de la suppression des données
- Ajout de plus de log pour la fonction reset

27/10/2016 - version 0.20.5
- Ajout d'un système de vérification des dossiers; Crée les dossiers ./data/covers et ./data/characters si il n'existent pas

27/10/2016 - version 0.19.137 
- Correction de bug: Erreur lors du rechargement de la liste: essaye d'afficher des informations alors qu'aucune colonne n'est sélectionnée

27/10/2016 - version 0.19.136 
- Correction de bug: Ajout du code SQL pour la création de la table information

26/10/2016 - version 0.19.134
- Remplacement de la liste par un tableau pour afficher les identifiants et les titres d'animés
- Possibilité de déplacement avec les flèches dans la liste des animés
- Correction de bug: les animés sont désormais triés grâce aux identifiants de manière "humaine"
- Possibilité de déplacement avec la touche tab entre les différents éléments
- Adapation du code: Suppression de librairies non-utilisées: pprint

25/09/2016
- Les images de cover sont maintenant lissées.

24/09/2016
- Ajout de 10 pages pour le WaifuBoard

03/08/2016
- Ajout de fonctionnalités: Possibilité d'ajouter / supprimer des animés depuis la liste
    
02/08/2016
- Ajout d'une fonction WaifuBoard. Permet d'afficher la liste des ses personnages préférés -- Ne se synchronise pas encore avec la base de données
    
27/07/2016
- Mise en place d'un dépot git pour aider a gérer les versions multi branches (ex: tests de fonctionnalités)

25/07/2016
- Modification du module MAL: Il télécharge désormais les affiches des animés automatiquement

24/07/2016
- Lors du remplissage des informations par MyanimeList, la cover de l'animé est téléchargée
	
23/07/2016
- Ajout d'icones sur les boutons et les onglets
- Ajout d'un bouton qui permet d'afficher ses animés préférés d'un seul clic

20/07/2016
- Correction du bug de texte dans l'entrée MAL
- Ajout d'une entrée Ajouté le dans les informations des animés

09/07/2016
- Ajout d'une barre de recherche pour parcourir les animés
- Il est maintenant possible de revenir sur le jour en cours sur le planning grâce a un bouton
- La barre de recherche peut être vidée grâce un bouton

07/07/2016
- Désormais l'application demandera à sauvegarder les données uniquement si quelque chose a été modifié depuis l'ouverture
 
05/07/2016
- Correction de bug: Les tranches d'heures sont numérotées a partir de 1 désormais,
- Pour rajouter un animé dans l'onglet le journal, il suffit de double cliquer sur celui ci ou de cliquer sur insérer
- Nouvelle fonction: Il est désormais possible de remplir les informations grâce a MyAnimelist

04/07/2016
- Depuis l’onglet planning, il suffit de cliquer dans la liste des animés a voir pour l'ajouter dans le journal
- Correction de bug: Si rien n'a été entré dans la journal, l'ajout d'un animé faisait apparaître un saut de ligne en première position
- Il est maintenant impossible d'entrer du texte dans la champ ID

03/07/2016
- Dans l'onglet planning, il est désormais possible de voir les animés en cours. Pratique pour savoir ou l'on en est
	 
28/06/2016
- Mise a jour de l'interface
- Ajout d'une fonction de calcul des animés

26/06/2016
- Correction du bug qui empêchait l'enregistrement final (commit de la bdd)
- Ajout d'une fonction planning qui permet d'afficher et de rajouter des animés vus grâce a un calendrier
- Ajout d'une table dans la base de données pour la fonction précédente
- Réorganisation légère de l'interface
- Ajout d'informations chargées a partir du code dans l’onglet « A propos »
 
19/06/2016
- Changement de l'interface: Passage a une interface a onglet pour accueillir les futures fonctions

12/06/2016
- Lancement du projet: Utilisation de PyQt car je ne voulais pas utiliser Tkinter
