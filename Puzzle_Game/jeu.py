from moteur import *
import pygame, sys
import random
import os

class Jeu:

    def __init__(self):
        self.lvl = Level()
        self.nom = ""

        self.player = {"Nom": self.nom, "Vie" : 100 , "VieMax" : 100}

        self.monsters = [{"Nom": "Limus", "Vie" : 150, "VieMax" : 150, "attaque" : 7, "Chance" : 80},
                        {"Nom": "Vespa", "Vie" : 200, "VieMax" : 200, "attaque" : 15, "Chance" : 75},
                        {"Nom": "Terram", "Vie" : 300, "VieMax" : 300, "attaque" : 10, "Chance" : 80},
                        {"Nom": "Antarès", "Vie": 350, "VieMax": 350, "attaque": 15, "Chance": 50}]
        
        self.niveaux = [{"Niveau": 1, "Img" : "Images/level1.png", "Hud":"Images/slime.png", "Music": "Music/limus.mp3"},
                        {"Niveau": 2, "Img" : "Images/level2.jpg", "Hud":"Images/waspax.png", "Music": "Music/Foret.mp3"},
                        {"Niveau": 3, "Img" : "Images/level3.jpg", "Hud":"Images/golem.png", "Music": "Music/Cave.mp3"},
                        {"Niveau": 4, "Img": "Images/finalback.png", "Hud": "Images/dragon.png", "Music": "Music/boss-battle.mp3"}]

        self.window = pygame.display.set_mode((1080,720))
        self.mouseX, self.mouseY = pygame.mouse.get_pos()
        self.click = False

        # Sons/Musiques
        if(os.name == 'nt'):
            self.select_button = pygame.mixer.Sound("Music/sound_effect_button.mp3")
        
        # Boucles
        self.run_accueil = True
        self.run_level= False
        self.run_transition = False
        self.run_ecran_histoire = False
        self.run_game = False
        self.run_ecran_nom = False
        self.run_ecran_victoire = False
        self.run_ecran_defaite = False

        # Box
        self.box_idle = pygame.transform.scale(pygame.image.load("Images/red_button11.png"),(380,98))
        self.box_pressed = pygame.transform.scale(pygame.image.load("Images/red_button12.png"),(380, 98))

        self.pixel_font_50 = pygame.font.Font("Autres/prstartk.ttf", 50)
        self.pixel_font_35 = pygame.font.Font("Autres/prstartk.ttf", 35)
        self.pixel_font_25 = pygame.font.Font("Autres/prstartk.ttf", 25)

    def victoire(self):

        # Vérifier que monstres encore vivants
        if self.monsters != []:
            # Si monstre n'a plus de vie, le supprimer ainsi que le niveau en cours
            if self.monsters[0]["Vie"] <= 0:
                del self.monsters[0]
                del self.niveaux[0]
                self.run_game = False

                if self.monsters != []:
                    self.fade()
                    self.run_transition = True
                    self.transition()

        # Si tout les monstres sont morts lancer l'écran de victoire
        elif self.monsters == []:
            self.fade()
            self.run_game = False
            self.run_ecran_victoire = True
            self.ecran_victoire()

    def defaite(self):
        if self.player["Vie"] <= 0:
            self.run_transition = False
            self.fade()
            self.run_ecran_defaite = True
            self.run_game = False
            self.ecran_defaite()
            
    def rejouer(self):
        self.run_ecran_defaite = False
        self.run_game = True
        self.fade()
        self.niveau()
            
    def degats_joueur(self):
        if self.monsters != []:
            hit = len(self.lvl.coord)

            # Vérifier si le monstre a plus ou moins de vie que le hit
            #Si oui on lui retire de sa vie la valeur de hit
            if self.monsters[0]["Vie"] >= hit:
                self.monsters[0]["Vie"] -= hit

            # Si non on lui met sa vie à 0 pour empêcher un bug graphique
            else:
                self.monsters[0]["Vie"] = 0

    def degats_monster(self):
        player_health = self.player["Vie"]

        # Dégâts sur le joueur et vérification que le joueur est vivant
        if (random.randint(0,100) <= self.monsters[0]["Chance"]) and (player_health > 0):

            # Si le joueur a moins de vie que l'attaque du monstre
            if (player_health <= self.monsters[0]["attaque"]):
                self.player["Vie"] = 0
                print(self.player["Vie"])

            # Si le joueur a plus de vie que l'attaque du monstre
            elif (player_health >= self.monsters[0]["attaque"]):
                    self.player["Vie"] -= self.monsters[0]["attaque"]
                    print(self.player["Vie"])

    def afficher_stats(self):
        # Afficher monstre
        print("_______________________________________________")
        for key, value in self.monsters[0].items():
            print(key,":",value)

        # Afficher Joueur
        print("_______________________________________________")
        for key, value in self.player.items():
            print(key,":",value)

    def fade(self):

        # Effet de fondue
        fade = pygame.Surface((1080,720))
        fade.fill((0,0,0))
        for alpha in range(0,150):
            fade.set_alpha(alpha)
            self.window.blit(fade, (0,0))
            pygame.display.update()
            pygame.time.delay(5)

    def niveau(self):

        if self.monsters != []:
            # Marges et taille des cases
            paddingleft = 300
            paddingtop = 150
            blockSize = 60
            
            self.player['Vie'] = self.player['VieMax']

            font = pygame.font.Font("Autres/Engcomica.otf", 50)

            # Les images pour chaques cases et fond de la grille
            fire = pygame.transform.scale((pygame.image.load("Images/Fire.png")),(blockSize,blockSize))
            air = pygame.transform.scale((pygame.image.load("Images/Air.png")),(blockSize,blockSize))
            earth = pygame.transform.scale((pygame.image.load("Images/Earth.png")),(blockSize,blockSize))
            water = pygame.transform.scale((pygame.image.load("Images/Water.png")),(blockSize,blockSize))
            grille = pygame.transform.scale((pygame.image.load("Images/grille.png")),(1090,740))

            # Images du joueur et monstre
            player = pygame.transform.scale((pygame.image.load("Images/hero.png")),(960,540))
            enemy = pygame.transform.scale(pygame.image.load(self.niveaux[0]["Hud"]), (1130,635))

            # Nom ennemi et joeur
            enemy_nom = pygame.transform.scale(font.render(self.monsters[0]["Nom"],True, 'white'), (100,30))
            pseudo = pygame.transform.scale(font.render(self.nom,True, 'white'), (100,30))

            background = pygame.transform.scale(pygame.image.load(self.niveaux[0]["Img"]),(1080,720))

            # Musique
            if(os.name == 'nt'):
                pygame.mixer.music.load(self.niveaux[0]["Music"])
                pygame.mixer.music.play()   
                pygame.mixer.music.set_volume(0.1)

            # Variables pour coordonnées de la souris
            mouseX = None
            mouseY = None
            mouseX2 = None
            mouseY2 = None

            def draw_grid():
                grid = self.lvl.grille

                # Pour chaque valeur associer une image
                for i in range(self.lvl.lignes):
                    for j in range(self.lvl.lignes):
                        # Feu
                        if(grid[i][j] == 1):
                            self.window.blit(fire, ((paddingleft + (j * blockSize)),(paddingtop + (i * blockSize))))

                        # Air
                        if(grid[i][j] == 2):
                            self.window.blit(air,((paddingleft + (j * blockSize)),(paddingtop + (i * blockSize))))

                        # Terre
                        if(grid[i][j] == 3):
                            self.window.blit(earth,((paddingleft + (j * blockSize)),(paddingtop + (i * blockSize))))

                        # Eau
                        if(grid[i][j] == 4):
                            self.window.blit(water,((paddingleft + (j * blockSize)),(paddingtop + (i * blockSize))))

            # Surbrillance/carré autour de la case sélectionnée
            def hilighted():
                # Regarder si c'est la première ou deuxième case qui est séléctionnée
                if ((mouseX != None) and (mouseY != None) and (mouseX2 == None) and (mouseY2 == None)):
                    # Vérifier que la souris est dans la grille
                    if(mouseX >= 0 and mouseX <= self.lvl.lignes) and (mouseY >= 0 and mouseY <= self.lvl.lignes):
                        pygame.draw.rect(self.window,"orange",((paddingleft + (mouseY * blockSize)),(paddingtop + (mouseX * blockSize)),blockSize,blockSize), width = 3, border_radius= 5)

                if ((mouseX2 != None) and (mouseY2 != None) and (mouseX != None) and (mouseY != None)):
                    # Vérifier que la souris est dans la grille
                    if(mouseX2 >= 0 and mouseX2 <= self.lvl.lignes) and (mouseY2 >= 0 and mouseY2 <= self.lvl.lignes):
                        pygame.draw.rect(self.window,"orange",((paddingleft + (mouseY2 * blockSize)),(paddingtop + (mouseX2 * blockSize)),blockSize,blockSize), width = 3, border_radius= 5)

            # Affichage de la barre de hp pour monstres et joueur
            def bar_hp(entite, x):

                health = entite["Vie"]
                max_health = entite["VieMax"]
                color = (0,255,0)

                # Si monstres morts
                if self.monsters == []:
                    pass

                # Vie 100% - 75%
                if (health > (0.75 * max_health)):
                    color = (0,255,0)

                # Vie 75% - 50%
                elif (health <= (0.75 * max_health) and health > (0.5 * max_health)):
                    color = (165,255,0)

                # Vie 50% - 25%
                elif (health <= (0.5 * max_health)) and (health > (0.25 * max_health)):
                    color = (255,255,0)

                # Vie 25% - 0%
                elif (health <= (0.25 * max_health)) and (health >= 0):
                    color = (255,0,0)

                pygame.draw.rect(self.window, color, (x, 80, (140 / max_health)*health, 8))

            # Initialisation de la grille pour chaque niveau
            self.lvl.grille = []
            self.lvl.creation_grille()
            self.lvl.grille_de_debut()
            self.afficher_stats()
            self.lvl.affichage()

            while self.run_game:

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.run_game = False
                        pygame.quit()

                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        # Récuperer la position de la souris
                        pos = pygame.mouse.get_pos()

                        # Si aucune gemme séléctionnée
                        if ((mouseX == None) and (mouseY == None)):

                                # Conversion pos souris en pos dans la grille
                                mouseY = ((pos[0] - (paddingleft)) // blockSize)
                                mouseX = ((pos[1] - paddingtop) // blockSize)

                                # Vérifier que la souris est bien dans la grille, sinon reset
                                if(mouseX < 0 or mouseX > self.lvl.lignes) and (mouseY < 0 or mouseY > self.lvl.lignes):
                                    mouseX = None
                                    mouseY = None

                        # Si une gemme à déjà été séléctionnée
                        elif ((mouseX2 == None) and (mouseY2 == None) and (mouseX != None) and (mouseY != None)):

                                # Conversion pos souris en pos dans la grille
                                mouseY2 = ((pos[0] - (paddingleft)) // blockSize)
                                mouseX2 = ((pos[1] - paddingtop) // blockSize)

                                # Vérifier que la souris est bien dans la grille, sinon reset
                                if(mouseX2 < 0 or mouseX2 > self.lvl.lignes) and (mouseY2 < 0 or mouseY2 > self.lvl.lignes):
                                    mouseX2 = None
                                    mouseY2 = None

                                elif(mouseX2 >= 0 or mouseX2 < self.lvl.lignes) and (mouseY2 >= 0 or mouseY2 < self.lvl.lignes):
                                    # Echange des cases
                                    self.lvl.echange(self.lvl.coor_to_num(mouseX,mouseY),self.lvl.coor_to_num(mouseX2, mouseY2))

                                    # Boucle de destruction des cases et actualisation des stats
                                    while self.lvl.combinaisons():
                                        self.degats_joueur()
                                        self.lvl.destruction()
                                        self.lvl.gravite()

                                    self.degats_monster()
                                    self.afficher_stats()
                                    self.lvl.affichage()

                                    # Reinitialisation des variables
                                    mouseX, mouseY, mouseX2, mouseY2 = None, None, None, None

                    self.victoire()
                
                # Si monstres vivants
                if self.monsters != []:
                    
                    # Afficher les divers éléments
                    self.window.blit(background,(0,0))
                    self.window.blit(grille, (0,0))

                    self.window.blit(player,(-300,-200))
                    self.window.blit(pseudo, (150, 45))
                    self.window.blit(enemy, (325,-245))
                    self.window.blit(enemy_nom, (785, 45))

                    bar_hp(self.player, 150)
                    bar_hp(self.monsters[0], 785)

                    draw_grid()
                    hilighted()
                    pygame.display.update()

                # Si monstres morts 
                else:
                    if(os.name == 'nt'):
                        pygame.mixer.music.unload()
                    self.victoire()
                
                # Si joueur n'a plus de vie
                if self.player["Vie"] <= 0:
                    if(os.name == 'nt'):
                        pygame.mixer.music.unload()
                    self.defaite()
                
            
    def level_selection(self):

        background = pygame.image.load("Images/fe.png")

        boxT = pygame.transform.scale(pygame.image.load("Images/red_button11.png"),(760, 150))
        back = pygame.transform.scale(pygame.image.load("Images/red_sliderRight.png"), (90, 70))

        niveau1 = self.pixel_font_35.render('Niveau 1', True, "white")
        niveau2 = self.pixel_font_35.render('Niveau 2', True, "white")
        niveau3 = self.pixel_font_35.render('Niveau 3', True, "white")
        niveau4 = self.pixel_font_35.render('Niveau 4', True, "white")

        back_texte = pygame.transform.scale(self.pixel_font_35.render("Back", True, 'white'), (50, 30))

        while self.run_level:

            # Récuperer position de la souris
            mouseX, mouseY = pygame.mouse.get_pos()

            self.window.blit(background,(0,0))

            # Créer les zones d'interactions
            rect_niveau1 = pygame.Rect(350, 100, 380, 98)
            rect_niveau2 = pygame.Rect(350, 225, 380, 98)
            rect_niveau3 = pygame.Rect(350, 350, 380, 98)
            rect_niveau4 = pygame.Rect(350, 475, 380, 98)
            rectback = pygame.Rect(0, 0, 90, 70)

            #Niveau 1
            if not rect_niveau1.collidepoint(mouseX, mouseY):
                self.window.blit(self.box_idle, (350, 100))
                self.window.blit(niveau1, (420, 125))
            else:
                self.window.blit(self.box_idle, (350, 110))
                self.window.blit(niveau1, (420, 135))

            #Niveau 2
            if not rect_niveau2.collidepoint(mouseX, mouseY):
                self.window.blit(self.box_idle, (350, 225))
                self.window.blit(niveau2, (420, 250))
            else:
                self.window.blit(self.box_idle, (350, 235))
                self.window.blit(niveau2, (420, 260))

            # Niveau 3
            if not rect_niveau3.collidepoint(mouseX, mouseY):
                self.window.blit(self.box_idle, (350, 350))
                self.window.blit(niveau3, (420, 375))
            else:
                self.window.blit(self.box_idle, (350, 360))
                self.window.blit(niveau3, (420, 385))

             # Niveau 4
            if not rect_niveau4.collidepoint(mouseX, mouseY):
                self.window.blit(self.box_idle, (350, 475))
                self.window.blit(niveau4, (420, 500))
            else:
                self.window.blit(self.box_idle, (350, 485))
                self.window.blit(niveau4, (420, 510))

            # Bouton retour
            if not rectback.collidepoint((mouseX,mouseY)):
                self.window.blit(back, (20, 20))
                self.window.blit(back_texte,(50, 35))
            else:
                self.window.blit(back, (10, 20))
                self.window.blit(back_texte,(40, 35))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Interaction level 1
                    if rect_niveau1.collidepoint((mouseX,mouseY)):

                        # Son de selection bouton
                        if(os.name == 'nt'):
                            self.select_button.play(0, 0, 0)
                       
                        # Evenements
                        self.run_level = False
                        self.fade()
                        self.run_ecran_nom = True
                        self.nom_du_joueur()

                    # Interaction level 2
                    if rect_niveau2.collidepoint((mouseX,mouseY)):

                        # Son de selection bouton
                        if(os.name == 'nt'):
                            self.select_button.play(0, 0, 0)

                        # Evenements
                        self.run_level = False
                        self.fade()
                        del self.monsters[0]
                        del self.niveaux[0]
                        self.run_transition= True
                        self.transition()

                    # Interactions level 3
                    if rect_niveau3.collidepoint((mouseX,mouseY)):

                        # Son de selection bouton
                        if(os.name == 'nt'):
                            self.select_button.play(0, 0, 0)

                        # Evenements
                        self.run_level = False
                        self.fade()
                        del self.monsters[0:2]
                        del self.niveaux[0:2]
                        self.run_transition= True
                        self.transition()

                    # Interaction level 4
                    if rect_niveau4.collidepoint((mouseX,mouseY)):

                        # Son de selection bouton
                        if(os.name == 'nt'):
                            self.select_button.play(0, 0, 0)

                        # Evenements
                        self.run_level = False
                        self.fade()
                        del self.monsters[0:3]
                        del self.niveaux[0:3]
                        self.run_transition = True
                        self.transition()

                    # Interaction bouton retour
                    if rectback.collidepoint((mouseX, mouseY)):
                        # Son de selection bouton
                        if(os.name == 'nt'):
                            self.select_button.play(0, 0, 0)
                            self.select_button.set_volume(0.3)

                        # Evenements
                        self.run_level = False
                        self.run_accueil = True
                        self.accueil()


    def accueil(self):

        background = pygame.image.load("Images/fe.png")
        boxT = pygame.transform.scale(pygame.image.load("Images/red_button11.png"),(760, 150))

        pygame.display.set_caption("Combiner Quest")

        # Différentes écritures
        Titre = self.pixel_font_50.render('COMBINER QUEST', True, "white")
        Jouer = self.pixel_font_35.render('Jouer', True, "white")
        Level= self.pixel_font_35.render('Level', True, "white")
        Quitter = self.pixel_font_35.render('Quitter', True, "white")

        # Musique
        if(os.name == 'nt'):
            pygame.mixer.music.load("Music/music-weeklies-rpg-menu-music.ogg")
            pygame.mixer.music.play()
            pygame.mixer.music.set_volume(0.3)

        while self.run_accueil:

            # Récuperer positions de la souris
            mouseX, mouseY = pygame.mouse.get_pos()

            # Afficher les écritures
            self.window.blit(background,(0,0))
            self.window.blit(boxT, (150, 50))
            self.window.blit(Titre, (185, 90))

            # Zones d'interactions si souris passe sur les boutons
            rect_jouer = pygame.Rect(350, 275, 380, 98)
            rect_level = pygame.Rect(350, 390, 380, 98)
            rect_quitter = pygame.Rect(350, 510, 380, 98)

            # Animations quand souris passe sur les boutons
            # Bouton Jouer
            if not rect_jouer.collidepoint(mouseX, mouseY):
                self.window.blit(self.box_idle, (350, 275))
                self.window.blit(Jouer, (460, 300))
            else:
                self.window.blit(self.box_idle, (350, 285))
                self.window.blit(Jouer, (460, 310))

             #Bouton Level
            if not rect_level.collidepoint(mouseX, mouseY):
                self.window.blit(self.box_idle, (350, 390))
                self.window.blit(Level, (460, 420))
            else:
                self.window.blit(self.box_idle, (350, 400))
                self.window.blit(Level, (460, 430))

            # Bouton Quitter
            if not rect_quitter.collidepoint(mouseX, mouseY):
                self.window.blit(self.box_idle, (350, 510))
                self.window.blit(Quitter, (425, 540))
            else:
                self.window.blit(self.box_idle, (350, 520))
                self.window.blit(Quitter, (425, 550))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                # Evenements lors du clique
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Si clique sur bouton Jouer
                    if rect_jouer.collidepoint((mouseX,mouseY)):

                        # Son de selection des boutons
                        if(os.name == 'nt'):
                            self.select_button.play(0, 0, 0)
                            self.select_button.set_volume(0.3)

                        # Lancer la transition
                        if(os.name == 'nt'):
                            pygame.mixer.music.unload()
                        self.run_accueil = False
                        self.fade()
                        self.run_ecran_nom = True
                        self.nom_du_joueur()

                    # Si clique sur bouton Level
                    if rect_level.collidepoint((mouseX,mouseY)):

                        #son de selection bouton
                        if(os.name == 'nt'):
                            self.select_button.play(0, 0, 0)
                            self.select_button.set_volume(0.3)

                        self.run_accueil = False
                        self.run_level = True
                        self.level_selection()
                        self.fade()

                    # Si clique sur bouton Quitter
                    if rect_quitter.collidepoint((mouseX,mouseY)):
                        sys.exit()

    def transition(self):

        niveau_text = self.pixel_font_50.render("Niveau " + str(self.niveaux[0]["Niveau"]), True, 'white')
        start_time = 0
        clock = pygame.time.Clock()

        while self.run_transition:

            # Incrémenter le compteur de temps
            start_time += 1

            self.window.fill((0,0,0))
            self.window.blit(niveau_text, (350, 250))

            # Si temps est dépassé lancer le niveau
            if start_time > 100:
                self.run_game = True
                self.fade()
                self.run_transition = False
                self.niveau()

            pygame.display.flip()
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

    def nom_du_joueur(self):

        question = self.pixel_font_35.render(('Entrez votre nom'), True, 'white')

        input_name = ""
        emplacement = 530

        while self.run_ecran_nom:

            prenom = self.pixel_font_35.render((str(input_name)), True, 'white')

            self.window.fill((0,0,0))
            self.window.blit(question, (275, 200))
            self.window.blit(prenom, (emplacement,300))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                if event.type == pygame.KEYDOWN:

                    # Taper une lettre
                    if (event.key != pygame.K_BACKSPACE) and (event.key != pygame.K_RETURN) and (len(input_name) <= 10):

                        input_name += str(chr(event.key))
                        # Décalage visuel
                        emplacement -= 17

                    # Effacer lettre
                    elif (event.key == pygame.K_BACKSPACE):

                        input_name = input_name[:-1]
                        emplacement += 17

                    # Enregistre le prénom et lance le niveau
                    elif (event.key == pygame.K_RETURN and input_name != ""):
                        self.nom = input_name
                        self.run_ecran_nom = False
                        self.run_ecran_histoire = True
                        self.histoire()


    def ecran_victoire(self):

        menu = self.pixel_font_35.render('Menu', True, "white")
        quitter = self.pixel_font_35.render('Quitter', True, "white")

        message_victoire1 = pygame.image.load("Images/gagné.png")
        background = pygame.transform.scale(pygame.image.load("Images/victory.jpg"), (1080,720))

        # Son
        if(os.name == 'nt'):
            pygame.mixer.music.load("Music/Victoire.mp3")
            pygame.mixer.music.play()
            pygame.mixer.music.set_volume(0.5)

        while self.run_ecran_victoire:

            # Récuperer positions de la souris
            mouseX, mouseY = pygame.mouse.get_pos()

            self.window.blit(background, (0,0))
            self.window.blit(message_victoire1, (150, 100))

            # Zones d'interactions
            rect_menu = pygame.Rect(350, 400, 380, 98)
            rect_quitter = pygame.Rect(350, 525, 380, 98)

            # Animations boutons
            # Bouton menu
            if not rect_menu.collidepoint(mouseX, mouseY):
                self.window.blit(self.box_idle, (350,400))
                self.window.blit(menu, (465, 425))
            else:
                self.window.blit(self.box_idle, (350,410))
                self.window.blit(menu, (465, 435))

            # Bouton quitter
            if not rect_quitter.collidepoint(mouseX, mouseY):
                self.window.blit(self.box_idle, (350,525))
                self.window.blit(quitter, (435, 550))
            else:
                self.window.blit(self.box_idle, (350,535))
                self.window.blit(quitter, (435, 560))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                # Evenements lors du clique
                if event.type == pygame.MOUSEBUTTONDOWN:

                    # Bouton menu
                    if rect_menu.collidepoint((mouseX,mouseY)):
                        if(os.name == 'nt'):
                            self.select_button.play(0, 0, 0)
                        
                        # Remettre les listes à zero pour rejouer
                        self.monsters = [{"Nom": "Limus", "Vie" : 150, "VieMax" : 150, "attaque" : 7, "Chance" : 80},
                                        {"Nom": "Vespa", "Vie" : 200, "VieMax" : 200, "attaque" : 15, "Chance" : 75},
                                        {"Nom": "Terram", "Vie" : 300, "VieMax" : 300, "attaque" : 10, "Chance" : 80},
                                        {"Nom": "Antarès", "Vie": 350, "VieMax": 350, "attaque": 15, "Chance": 50}]
        
                        self.niveaux = [{"Niveau": 1, "Img" : "Images/level1.png", "Hud":"Images/slime.png", "Music": "Music/limus.mp3"},
                                        {"Niveau": 2, "Img" : "Images/level2.jpg", "Hud":"Images/waspax.png", "Music": "Music/Foret.mp3"},
                                        {"Niveau": 3, "Img" : "Images/level3.jpg", "Hud":"Images/golem.png", "Music": "Music/Cave.mp3"},
                                        {"Niveau": 4, "Img": "Images/finalback.png", "Hud": "Images/dragon.png", "Music": "Music/boss-battle.mp3"}]

                        self.run_accueil = True
                        self.run_ecran_victoire = False
                        self.fade()
                        if(os.name == 'nt'):
                            pygame.mixer.music.unload()
                        self.accueil()

                    # Bouton quitter
                    if rect_quitter.collidepoint((mouseX,mouseY)):
                        if(os.name == 'nt'):
                            self.select_button.play(0, 0, 0)
                        sys.exit()


    def ecran_defaite(self):

        menu = self.pixel_font_35.render('Menu', True, "white")
        rejouer = self.pixel_font_35.render('Rejouer', True, "white")

        message_defaite = pygame.image.load("Images/perdu.png")
        background = pygame.transform.scale(pygame.image.load("Images/mort.jpg"), (1080, 720))

        # Son
        if(os.name == 'nt'):
            pygame.mixer.music.load("Music/death.mp3")
            pygame.mixer.music.play()
            pygame.mixer.music.set_volume(0.5)

        while self.run_ecran_defaite:

            mouseX, mouseY = pygame.mouse.get_pos()

            self.window.blit(background, (0, 0))
            self.window.blit(message_defaite, (-50, 250))

            # Zones d'interactions boutons
            rect_menu = pygame.Rect(350, 400, 380, 98)
            rect_rejouer = pygame.Rect(350, 500, 380, 98)

            # Animations des boutons
            # Bouton menu
            if not rect_menu.collidepoint(mouseX, mouseY):
                self.window.blit(self.box_idle, (350,400))
                self.window.blit(menu, (475, 425))
            else:
                self.window.blit(self.box_idle, (350,410))
                self.window.blit(menu, (475, 435))

            # Bouton Jouer
            if not rect_rejouer.collidepoint(mouseX, mouseY):
                self.window.blit(self.box_idle, (350,520))
                self.window.blit(rejouer, (430, 545))
            else:
                self.window.blit(self.box_idle, (350,530))
                self.window.blit(rejouer, (430, 555))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                # Evenements lors du clique
                if event.type == pygame.MOUSEBUTTONDOWN:

                    # Bouton menu
                    if rect_menu.collidepoint((mouseX,mouseY)):
                        self.monsters = [{"Nom": "Limus", "Vie" : 150, "VieMax" : 150, "attaque" : 7, "Chance" : 80},
                                        {"Nom": "Vespa", "Vie" : 200, "VieMax" : 200, "attaque" : 15, "Chance" : 75},
                                        {"Nom": "Terram", "Vie" : 300, "VieMax" : 300, "attaque" : 10, "Chance" : 80},
                                        {"Nom": "Antarès", "Vie": 350, "VieMax": 350, "attaque": 15, "Chance": 50}]
        
                        self.niveaux = [{"Niveau": 1, "Img" : "Images/level1.png", "Hud":"Images/slime.png", "Music": "Music/limus.mp3"},
                                        {"Niveau": 2, "Img" : "Images/level2.jpg", "Hud":"Images/waspax.png", "Music": "Music/Foret.mp3"},
                                        {"Niveau": 3, "Img" : "Images/level3.jpg", "Hud":"Images/golem.png", "Music": "Music/Cave.mp3"},
                                        {"Niveau": 4, "Img": "Images/finalback.png", "Hud": "Images/dragon.png", "Music": "Music/boss-battle.mp3"}]
                        if(os.name == 'nt'):
                            self.select_button.play(0, 0, 0)
                            pygame.mixer.music.unload()
                        self.run_accueil = True
                        self.run_ecran_victoire = False
                        self.fade()

                        # Remettre les listes à zero pour rejouer
                        
                        self.accueil()
                        
                    # Bouton rejouer
                    if rect_rejouer.collidepoint((mouseX,mouseY)):
                        self.rejouer()

    def histoire(self):

        # Paragraphe histoire
        horde = self.pixel_font_25.render('Une horde de monstre est apparue', True, 'white')
        royaume = self.pixel_font_25.render('dans le royaume Fiore, semant la', True, 'white')
        terreur = self.pixel_font_25.render('terreur parmis les habitants.', True, 'white')
        choisi = self.pixel_font_25.render('Vous avez été choisis noble héro pour ', True, 'white')
        mal = self.pixel_font_25.render('combattre le mal qui ronge ce pays.', True, 'white')
        ennemis = self.pixel_font_25.render('Vainquez tout les ennemis et', True, 'white')
        paix = self.pixel_font_25.render('restaurez la paix !', True, 'white')
        continuer = self.pixel_font_35.render('Continuer', True, 'white')

        monsters = pygame.transform.scale(pygame.image.load("Images/monsters.jpg"), (1080,720))

        # Dessiner un carré avec de la transparence
        def rect_transparent(surface, color, rect):
            shape = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
            pygame.draw.rect(shape, color, shape.get_rect())
            surface.blit(shape, rect)

        while self.run_ecran_histoire:

            # Récuperer positions de la souris
            mouseX, mouseY = pygame.mouse.get_pos()

            self.window.blit(monsters, (0, 0))

            rect_transparent(self.window, (0,0,0,200), (50,40,975,400))

            # Afficher le paragraphe
            self.window.blit(horde, (150, 75))
            self.window.blit(royaume, (150, 125))
            self.window.blit(terreur, (175, 175))
            self.window.blit(choisi, (75,225))
            self.window.blit(mal, (125,275))
            self.window.blit(ennemis, (175,325))
            self.window.blit(paix, (325,375))
            
            rectContinuer = pygame.Rect(300, 550, 380, 98)

            # Animation boutons
            if not rectContinuer.collidepoint(mouseX, mouseY):
                self.window.blit(self.box_idle, (350,525))
                self.window.blit(continuer, (375, 550))
            else:
                self.window.blit(self.box_idle, (350,535))
                self.window.blit(continuer, (375, 560))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                # Evenement clique
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Bouton continuer
                    if rectContinuer.collidepoint((mouseX,mouseY)):
                        if(os.name == 'nt'):
                            self.select_button.play(0, 0, 0)
                        self.fade()
                        self.run_ecran_histoire = False
                        self.run_transition = True
                        self.transition()

pygame.init()

if __name__ == "__main__":
    jeu = Jeu()

    jeu.accueil()
