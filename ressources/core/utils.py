# coding: utf8
from log import *
import os

def creation_dossier_profil_utilisateur():
    """Fonction qui va créer les dossiers utiles"""
    
    log.info("Verification de l'existence des dossiers utilisateur ...")

    # Dossier ./profile
    if os.path.exists("./profile"):
        log.info("  ./profile [Ok]")
    else:
        os.makedirs("./profile")
        log.info("  Creation de ./profile")


    # Dossier ./profile/characters
    if os.path.exists("./profile/characters"):
        log.info("  ./profile/characters [Ok]")
    else:
        os.makedirs("./profile/characters")
        log.info("  Creation de ./profile/characters")

    # Dossier ./profile/covers
    if os.path.exists("./profile/covers"):
        log.info("  ./profile/covers [Ok]")
    else:
        os.makedirs("./profile/covers")
        log.info("  Creation de ./profile/covers")
