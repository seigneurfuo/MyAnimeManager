# Changements

27/10/2016 - version 0.20.5
- Ajout d'un système de vérification des dossiers; Crée les dossiers ./data/covers et ./data/characters si il n'existent pas

27/10/2016 - version 0.19.137 
- Correction de bug: Erreur lors du rechargement de la liste: essaye d'afficher des informations alors qu'aucune colonne n'est sélectionnée

27/10/2016 - version 0.19.136 
- Correction de bug: Ajout du code SQL pour la création de la table information

26/10/2016 - version 0.19.134
- Remplacement de la liste par un tableau pour affciher les identifiants et les titres d'animés
- Possibilité de déplacement avec les flèches dans la liste des animés
- Correction de bug: les animés sont désormais triés grâce aux identifants de manière "humaine"
- Possibilité de déplacement avec la touche tab entre les différents éléments
- Adapation du code: Supresion de librairies non-utilisées: pprint

25/09/2016
- Les images de cover sont maintenant lissées.

24/09/2016
- Ajout de 10 pages pour le WaifuBoard

03/08/2016
- Ajout de fonctionalités: Possibilité d'ajouter / supprimer des animés depuis la liste
    
02/08/2016
- Ajout d'une fonction WaifuBoard. Permet d'afficher la liste des ces personages préférés -- Ne se syncronise pas encore avec la base de données
    
27/07/2016
- Mise en place d'un dépot git pour aider a gérer les versions multibranches (ex: tests de fonctionalités)

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
- Il est maintenant possible de revenir sur le jour en cours sur le planning grace a un bouton
- La barre de recherche peut etre vidée grace un bouton

07/07/2016
- Désormais l'application demandera à sauvegarder les données uniquement si quelque chose a été modifié depuis l'ouverture
	 
05/07/2016
- Correction de bug: Les tranches d'heures sont numérotées a partir de 1 désormais,
- Pour rajouter un animé dans l'onglet le journal, il suffit de double cliquer sur celui ci ou de cliquer sur insérer
- Nouvelle fonction: Il est désormais possible de remplire les informations grace a MyAnimelist
				   
04/07/2016
- Depuis l'ongelt planning, il suffit de cliquer dans la liste des animés a voir pour l'ajouter dans le journal
- Correction de bug: Si rien n'a été entré dans la journal, l'ajout d'un animé faisait apparaitre un saut de ligne en première position
- Il est maintenant impossible d'entrer du texte dans la champ ID
				   
03/07/2016
- Dans l'onglet planning, il est désormais possible de voir les animés en cours. Pratique pour savoir ou l'on en est
	 
28/06/2016
- Mise a jour de l'interface
- Ajout d'une fonction de calcul des animés
				   
26/06/2016
- Correction du bug qui empéchait l'enregistrement final (commit de la bdd)
- Ajout d'une fonction planning qui permet d'afficher et de rajouter des animés vus grace a un calendrier
- Ajout d'une table dans la bdd pour la fonction précédente
- Réorganisation légère de l'interface
- Ajout d'informations chargées a partir du code dans l'ongelt \A propos\
				   
19/06/2016
- Changement de l'interface: Passage a une interface a onglet pour acceuillir les futures fonctions
	 
12/06/2016
- Lancement du projet: Utilisation de PyQt car je ne voulais pas utiliser Tkinter
