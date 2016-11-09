# Changements

09/11/2016 - version 0.20.56
- BUGFIX: Dans le planning, une insertion ne supprimais pas les sauts de lignes en trop.

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