from datetime import datetime
from fichier_binaire import charger_scores, sauvegarder_scores

def obtenir_scores():
    return {
        'parties jouées': 0,
        'score total': 0,
        'high score': 0,
        'dernière partie jouée': None
    }

def mettre_a_jour_scores(username, score):
    joueurs = charger_scores()
    if username not in joueurs:
        joueurs[username] = obtenir_scores()
    joueurs[username]['parties jouées'] +=1 
    joueurs[username]['score total'] += score
    if score > joueurs[username]['high score']: 
        joueurs[username]['high score'] = score
    joueurs[username]['dernière partie jouée'] = datetime.now().strftime("%Y-%m-%d %H:%M")
    sauvegarder_scores(joueurs)
    print(f"Scores mis à jour pour {username}: {joueurs[username]}")


