import pygame
import random #pour les tuyaux
from fichier_binaire import charger_scores
from dictionaire import mettre_a_jour_scores
from fichier_texte import enregistrer_scores_texte

#initialisation de pygame
pygame.init()
pygame.font.init()
pygame.mixer.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Space Cat")
clock = pygame.time.Clock()
font = pygame.font.Font('PressStart2P-Regular.ttf', 30)

#les images
chat_image = pygame.image.load('chat.png')
tuyau_image = pygame.image.load('tuyau.png')
fond_image = pygame.image.load('fond.png')
fond_image = pygame.transform.scale(fond_image, (1280, 720))
accueil_image = pygame.image.load('accueil.png')
accueil_image = pygame.transform.scale(accueil_image, (1280, 720))
bouton_play_image = pygame.image.load('bouton_play.png')
bouton_restart_image = pygame.image.load('bouton_restart.png')

#les variables
score = 0
high_score = 0

#la musique
pygame.mixer.music.load("Vogue.mp3")
pygame.mixer.music.play(-1)

 #class qui permet de créer les boutons
class Bouton(pygame.sprite.Sprite):
  def __init__(self, image, position):
    super().__init__()
    self.image = pygame.transform.scale(image, (700, 500))
    self.rect = self.image.get_rect(center=position)

  #fonction qui permet de savoir si le bouton est cliqué
  def etat_bouton(self):
    return self.rect.collidepoint(pygame.mouse.get_pos())

bouton_play = Bouton(bouton_play_image, (645, 450))
bouton_restart = Bouton(bouton_restart_image, (645, 450))
        
#la page d'accueil
def accueil():
  username = ""
  input_rect = pygame.Rect(0, 0, 450, 50)
  input_rect.center = (645, 600)

  while True:
    screen.blit(accueil_image, (0, 0))
    events = pygame.event.get()
    for event in events:
      if event.type == pygame.QUIT:
          pygame.quit()
          exit()
      if event.type == pygame.KEYDOWN: #on vérifie que nimporte quel bouton est appuyé
        if event.key == pygame.K_BACKSPACE: #on vérifie si le bouton appuyé est la touche retour arrière
          username = username[:-1] #on enlève le dernier caractère de la variable username
        else:
          username += event.unicode #on vérifie quel bouton est appuyé et on l'ajoute à la variable username
      #quand on clique sur le bouton play, on lance le jeu
      if event.type == pygame.MOUSEBUTTONDOWN:
          if bouton_play.etat_bouton() and username.strip(): 
            return username

    pygame.draw.rect(screen, (50, 50, 50), input_rect, 2)
    
    if username == "":
        placeholder = font.render("enter username", True, (180,180,180))
        placeholder_rect = placeholder.get_rect(center=input_rect.center)
        screen.blit(placeholder, placeholder_rect)
    else:
        textsurface = font.render(username, True, (255, 255, 255))
        text_rect = textsurface.get_rect(center=input_rect.center)
        screen.blit(textsurface, text_rect)
    
    screen.blit(bouton_play.image, bouton_play.rect)
  
    pygame.display.flip()
    clock.tick(30)

def restart(score, high_score, username):
    while True:
      screen.blit(accueil_image, (0, 0))
      score_texte = font.render(f"Score: {score}", True, (255, 255, 255))
      screen.blit(score_texte, (15, 600))
      high_score_texte = font.render(f"High Score: {high_score}", True, (255, 255, 255))
      screen.blit(high_score_texte, (15, 650))
      screen.blit(bouton_restart.image, bouton_restart.rect) 
      
      events = pygame.event.get()
      for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        #quand on clique sur le bouton restart, on relance le jeu
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if bouton_restart.etat_bouton():
                main(username)

      pygame.display.flip()
      clock.tick(30)

def afficher_score(score, high_score):
  score_text = font.render(f"Score: {score}", True, (255, 255, 255)) #image du score avec le font
  screen.blit(score_text, (10, 10)) #afficher score sur l'écran screen.blit(image, position)
  highscore_text = font.render(f"High score: {high_score}", True, (255, 255, 255))
  screen.blit(highscore_text, (10, 50))

#les tuyaux
class Tuyau(pygame.sprite.Sprite):
  def __init__(self, x, y, en_haut):
    super().__init__() #initialiser le sprite
    original_image = pygame.transform.scale(tuyau_image, (120, 600))
    if en_haut:    #self.rect rectangle qui definit la position et la taille du tuyau sur l'écran 
      self.image = pygame.transform.flip(original_image, False, True)
      self.rect = self.image.get_rect(topleft=(x, y - 600))
    else:
      self.image = original_image
      self.rect = self.image.get_rect(topleft=(x, y))
    self.vitesse = 4

  def update(self):
    self.rect.x -= self.vitesse #tuyau bouge vers la gauche
    if self.rect.right < 0:
      self.kill() #tuyau disprait quand il sort de l'écran

#le chat
class Chat(pygame.sprite.Sprite):
  def __init__(self):
    super().__init__()
    self.image = pygame.transform.scale_by(chat_image, 3.5)
    self.rect = self.image.get_rect(midleft=(100, 360))
    self.vitesse = 0  

  def update(self):
    touche = pygame.key.get_pressed()
    if touche[pygame.K_SPACE]:
      self.vitesse = -7 #chat monte
    else:
      self.vitesse += 0.3 #chat tombe
    self.rect.y += self.vitesse #mettre à jour la position du chat
    
    if self.rect.top < 0:
      self.rect.top = 0
    if self.rect.bottom > 720: #pour que le chat ne depasse pas l'écran
      self.rect.bottom = 720

  def meurt(self, tuyaux):
    for tuyau in tuyaux:
      if self.rect.colliderect(tuyau.rect):
        return True
    return False

#boucle principale du jeu
def main(username):
  tuyaux = []
  joueur = Chat()
  joueurs = charger_scores()
  high_score = joueurs.get(username, {}).get("high score", 0)
  score = 0

  interval_tuyaux = random.choice([3000, 2000, 4000])
  dernier_tuyau_temps = pygame.time.get_ticks()

  running = True
  while running:
    screen.blit(fond_image, (0, 0))
      
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        exit()

    temps_actuel = pygame.time.get_ticks()
    if temps_actuel - dernier_tuyau_temps > interval_tuyaux:  
      distance_y = random.randint(250, 550)
      tuyau_haut = Tuyau(1300, distance_y - 350, True)
      tuyau_bas = Tuyau(1300, distance_y, False)
      tuyaux.append(tuyau_haut)
      tuyaux.append(tuyau_bas)
      score += 1
      dernier_tuyau_temps = temps_actuel
      interval_tuyaux = random.choice([3000, 2000, 4000]) 
  
    joueur.update()
    for tuyau in tuyaux:
      tuyau.update()
      screen.blit(tuyau.image, tuyau.rect)
    
    if joueur.meurt(tuyaux):
      high_score = max(score, high_score)
      mettre_a_jour_scores(username, score)
      joueurs = charger_scores()
      enregistrer_scores_texte(joueurs)
      print(f"Game Over, Score: {score}, High score: {high_score}")
      restart(score, high_score, username)

    afficher_score(score, high_score)
    screen.blit(joueur.image, joueur.rect)
    pygame.display.flip()
    clock.tick(60)

if __name__ == "__main__":
  username = accueil()
  main(username) 
