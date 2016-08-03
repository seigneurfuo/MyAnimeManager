# -*- coding: cp1252 -*-
# Module pour simplifier les developpement en python
# Auteur: seigneurfuo
# Dernière modification: 2016/07/07

buildNumber = 0

def show_stats(scriptName): # Affiche le nombre de lancement du programme
    import os, pickle
    global buildNumber
    outputFilename = '%s.stats.txt' %scriptName
    isOutputFilenameExists = os.path.isfile(outputFilename)

    if isOutputFilenameExists == False:
        print 'Build\t1'
        buildNumber = 1
        pickle.dump(buildNumber, open(outputFilename, "wb" ))

    else:
        stringBuildNumber = pickle.load(open(outputFilename, "rb"))
        buildNumber = int(stringBuildNumber)
        buildNumber += 1
     
        print 'Build\t%s' %buildNumber
        pickle.dump(buildNumber, open(outputFilename, "wb" ))

dprint_state = False
def dprint(text):# Affiche un texte défini ainsi que la fonction dans laquelle il est éxécuté (utile lors des phases de débogage)
    import inspect
    global dprint_state
    if dprint_state == True:
        parent_fonction = inspect.getouterframes(inspect.currentframe())[1][3]
        print "In", parent_fonction +"(), Value:", text
