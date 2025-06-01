import pickle

def charger_scores():
    try:
        with open('mon_binaire.bin','rb') as fichier: # avec le with, pas utile de fermer le fichier
            mon_depickler = pickle.Unpickler(fichier)
            joueurs = mon_depickler.load()
        return joueurs 
    except (FileNotFoundError, EOFError):
        return {}

def sauvegarder_scores(joueurs):
    with open('mon_binaire.bin','wb') as fichier:
        mon_pickler = pickle.Pickler(fichier)
        mon_pickler.dump(joueurs)



