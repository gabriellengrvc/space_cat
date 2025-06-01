def enregistrer_scores_texte(scores):
  with open('mon_text.txt', 'w') as fichier:
      for username, score_data in scores.items():
          parties_jouees = score_data['parties jouées']
          score_total = score_data['score total']
          high_score = score_data['high score']
          derniere_partie_jouee = score_data['dernière partie jouée']
          fichier.write(f"{username}: parties jouées={parties_jouees}, score total ={score_total}, high score={high_score}, dernière partie jouée={derniere_partie_jouee}\n")
