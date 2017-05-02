#coding: utf8
import logging
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

# Création d'un formateur qui va ajouter le temps, le niveau de chaque message quand on écrira un message dans le log
formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(message)s')

# Les lignes suivantes permettent de rediriger chaque écriture de log sur la console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)
log.addHandler(console_handler)
