import subprocess


def installer_bibliotheques_si_besoin(bibliotheques : list[str]):
    """
    Vérifie si les bibliothèques sont installées et les installe si nécessaire.
    bibliotheques: Liste des bibliothèques à installer
    """
    for lib in bibliotheques:
                try:
                    __import__(lib)
                except ImportError:
                    print(f"Installation de la bibliothèque {lib}...")
                    subprocess.check_call(["pip", "install", lib])
                    
# Liste des bibliothèques à installer si elles ne sont pas déjà installées
bibliotheques_a_installer = ["pyxel"]

installer_bibliotheques_si_besoin(bibliotheques_a_installer)


import pyxel
import random
import os
import json
import time
from datetime import datetime




class Particle:
    """
    Classe qui gère les particules
    """
    def __init__(self, x, y, particle_type="gauge") -> None:
        """
        Constructeur de la classe
        -----------------------
        x : coordonnée x de la particule
        y : coordonnée y de la particule
        particle_type : type de particule (gauge ou bird)
        """
        self.x = x
        self.y = y
        if particle_type == "gauge":
            self.vx = random.uniform(-1, 1)
            self.vy = random.uniform(-1, 1)
            self.color = random.choice([7, 9, 10])
        elif particle_type == "bird":
            self.vx = random.uniform(-2, 2)
            self.vy = random.uniform(-2, 2)
            self.color = random.choice([12, 7, 9])
        elif particle_type == "portal":
            self.vx = random.uniform(-1, 1)
            self.vy = random.uniform(-2, 0)
            self.color = random.choice([2, 8])
        self.life = random.randint(10, 20)
        self.type = particle_type




class Save:
    """
    Classe pour la sauvegarde
    """
    def __init__(self, app) -> None:
        """
        Initialisation de la sauvegarde
        """
        self.__save_file = "sauvegarde.json"
        self.__pyxel_egal_caca = app
        self.click_ignore = True


    def sauvegarder(self) -> None:
        """
        Sauvegarde le score
        --------------
        """
        now = datetime.now()
        annee = now.year
        mois = now.month
        jour = now.day
        heure = now.hour
        minute = now.minute
        secondes = now.second

        try:
            with open(self.__save_file, "r") as f:
                saves_json: list[dict[str, int]] = json.load(f)
                partie = max(entry['Partie'] for entry in saves_json if 'Partie' in entry)
        except FileNotFoundError:
            saves_json: list = []  # Si le fichier n'existe pas, commencer avec une liste vide
            partie = 0
        
        # Ajouter les nouvelles données
        saves_json.append({
            "Partie": partie + 1,
            "Date": [jour, mois, annee, [heure, minute, secondes]],
            "Orbes": [self.__pyxel_egal_caca.blue_orb, self.__pyxel_egal_caca.red_orb, self.__pyxel_egal_caca.green_orb],
            "Pos Pos_cam": [[self.__pyxel_egal_caca.x, self.__pyxel_egal_caca.y], [self.__pyxel_egal_caca.camera_x, self.__pyxel_egal_caca.camera_y]],
            "Actual bird": self.__pyxel_egal_caca.actual_bird.to_dict() if hasattr(self.__pyxel_egal_caca.actual_bird, 'to_dict') else str(type(self.__pyxel_egal_caca.actual_bird)),
            "Unlocked": [[item.to_dict() if hasattr(item, 'to_dict') else str(type(item)) for item in self.__pyxel_egal_caca.unlock],
                         [item.to_dict() if hasattr(item, 'to_dict') else str(type(item)) for item in self.__pyxel_egal_caca.unlock_stele]],
            "Bird pos": [[self.__pyxel_egal_caca.blue_bird.x, self.__pyxel_egal_caca.blue_bird.y],
                         [self.__pyxel_egal_caca.red_bird.x, self.__pyxel_egal_caca.red_bird.y],
                         [self.__pyxel_egal_caca.green_bird.x, self.__pyxel_egal_caca.green_bird.y]],
            "Stele pos": [[self.__pyxel_egal_caca.stele.blue_x, self.__pyxel_egal_caca.stele.blue_y],
                          [self.__pyxel_egal_caca.stele.red_x, self.__pyxel_egal_caca.stele.red_y],
                          [self.__pyxel_egal_caca.stele.green_x, self.__pyxel_egal_caca.stele.green_y]],
            "Hommage": [item.to_dict() if hasattr(item, 'to_dict') else str(type(item)) for item in self.__pyxel_egal_caca.hommage],
            "Items": [self.__pyxel_egal_caca.items_blue, self.__pyxel_egal_caca.items_red, 
                      self.__pyxel_egal_caca.items_green]
        })
        # Écrire les données mises à jour dans le fichier
        with open(self.__save_file, "w") as f:
            json.dump(saves_json, f, indent=1)
    

    def show_save(self) -> None:
        """
        Affiche la ou les sauvegarde(s)
        """
        # Draw background panel with original dimensions
        pyxel.rect(30, 20, 196, 216, 5)
        pyxel.rectb(30, 20, 196, 216, 7)
        
        # Draw title
        title_x = 80
        title_y = 60
        for i, letter in enumerate("SAVES"):
            self.__pyxel_egal_caca.draw_letter(letter, title_x + i * 20, title_y, 0.5)

        try:
            with open(self.__save_file, "r") as f:
                saves_json = json.load(f)
                
            # Calculate scroll
            max_visible_saves = 4  # Adjusted for smaller window
            if not hasattr(self, 'scroll_position'):
                self.scroll_position = 0
                
            if pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.KEY_S):
                self.scroll_position = min(len(saves_json) - max_visible_saves, self.scroll_position + 1)
            if pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.KEY_Z):
                self.scroll_position = max(0, self.scroll_position - 1)
                
            # Draw save buttons with scroll
            visible_saves = saves_json[self.scroll_position:self.scroll_position + max_visible_saves]
            for i, save in enumerate(visible_saves):
                button_y = 70 + i * 40
                # Draw button background
                date = save["Date"]
                button_save = {"x": 40, "y": button_y, "w": 176, "h": 30}
                self.__pyxel_egal_caca.draw_button(button_save, f"Save {save['Partie']} - {date[0]}/{date[1]}/{date[2]} a {date[3][0]}h {date[3][1]}min {date[3][2]}s")

                if self.__pyxel_egal_caca.is_button_clicked(button_save):
                                if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and len(visible_saves) == 1:

                                    self.__pyxel_egal_caca.reset()
                                    self.__pyxel_egal_caca.blue_orb = save["Orbes"][0]
                                    self.__pyxel_egal_caca.red_orb = save["Orbes"][1]
                                    self.__pyxel_egal_caca.green_orb = save["Orbes"][2]
                                    self.__pyxel_egal_caca.x, self.__pyxel_egal_caca.y = save["Pos Pos_cam"][0]
                                    self.__pyxel_egal_caca.camera_x, self.__pyxel_egal_caca.camera_y = save["Pos Pos_cam"][1]
                                    self.__pyxel_egal_caca.actual_bird = self.deserialisation(save["Actual bird"])
                                    self.__pyxel_egal_caca.unlock = [self.deserialisation(classe) for classe in save["Unlocked"][0]]
                                    self.__pyxel_egal_caca.unlock_stele = [self.deserialisation(classe) for classe in save["Unlocked"][1]]
                                    self.__pyxel_egal_caca.blue_bird.x = save["Bird pos"][0][0]
                                    self.__pyxel_egal_caca.blue_bird.y = save["Bird pos"][0][1]
                                    self.__pyxel_egal_caca.red_bird.x = save["Bird pos"][1][0]
                                    self.__pyxel_egal_caca.red_bird.y = save["Bird pos"][1][1]
                                    self.__pyxel_egal_caca.green_bird.x = save["Bird pos"][2][0]
                                    self.__pyxel_egal_caca.green_bird.y = save["Bird pos"][2][1]
                                    self.__pyxel_egal_caca.stele.blue_x = save["Stele pos"][0][0]
                                    self.__pyxel_egal_caca.stele.blue_y = save["Stele pos"][0][1]
                                    self.__pyxel_egal_caca.stele.red_x = save["Stele pos"][1][0]
                                    self.__pyxel_egal_caca.stele.red_y = save["Stele pos"][1][1]
                                    self.__pyxel_egal_caca.stele.green_x = save["Stele pos"][2][0]
                                    self.__pyxel_egal_caca.stele.green_y = save["Stele pos"][2][1]
                                    self.__pyxel_egal_caca.hommage = save["Hommage"]
                                    self.__pyxel_egal_caca.items_blue = save["Items"][0]
                                    self.__pyxel_egal_caca.items_red = save["Items"][1]
                                    self.__pyxel_egal_caca.items_green = save["Items"][2]


                                    self.restore_items(save["Items"][0], save["Items"][1], save["Items"][2])
                                    self.__pyxel_egal_caca.mode = "game"

                                elif pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and not self.click_ignore and len(visible_saves) != 1:

                                    self.__pyxel_egal_caca.reset()
                                    self.__pyxel_egal_caca.blue_orb = save["Orbes"][0]
                                    self.__pyxel_egal_caca.red_orb = save["Orbes"][1]
                                    self.__pyxel_egal_caca.green_orb = save["Orbes"][2]
                                    self.__pyxel_egal_caca.x, self.__pyxel_egal_caca.y = save["Pos Pos_cam"][0]
                                    self.__pyxel_egal_caca.camera_x, self.__pyxel_egal_caca.camera_y = save["Pos Pos_cam"][1]
                                    self.__pyxel_egal_caca.actual_bird = self.deserialisation(save["Actual bird"])
                                    self.__pyxel_egal_caca.unlock = [self.deserialisation(classe) for classe in save["Unlocked"][0]]
                                    self.__pyxel_egal_caca.unlock_stele = [self.deserialisation(classe) for classe in save["Unlocked"][1]]
                                    self.__pyxel_egal_caca.blue_bird.x = save["Bird pos"][0][0]
                                    self.__pyxel_egal_caca.blue_bird.y = save["Bird pos"][0][1]
                                    self.__pyxel_egal_caca.red_bird.x = save["Bird pos"][1][0]
                                    self.__pyxel_egal_caca.red_bird.y = save["Bird pos"][1][1]
                                    self.__pyxel_egal_caca.green_bird.x = save["Bird pos"][2][0]
                                    self.__pyxel_egal_caca.green_bird.y = save["Bird pos"][2][1]
                                    self.__pyxel_egal_caca.stele.blue_x = save["Stele pos"][0][0]
                                    self.__pyxel_egal_caca.stele.blue_y = save["Stele pos"][0][1]
                                    self.__pyxel_egal_caca.stele.red_x = save["Stele pos"][1][0]
                                    self.__pyxel_egal_caca.stele.red_y = save["Stele pos"][1][1]
                                    self.__pyxel_egal_caca.stele.green_x = save["Stele pos"][2][0]
                                    self.__pyxel_egal_caca.stele.green_y = save["Stele pos"][2][1]
                                    self.__pyxel_egal_caca.hommage = save["Hommage"]
                                    self.__pyxel_egal_caca.items_blue = save["Items"][0]
                                    self.__pyxel_egal_caca.items_red = save["Items"][1]
                                    self.__pyxel_egal_caca.items_green = save["Items"][2]


                                    self.restore_items(save["Items"][0], save["Items"][1], save["Items"][2])
                                    self.__pyxel_egal_caca.mode = "game"

                                elif pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and self.click_ignore and len(visible_saves) != 1:
                                    self.click_ignore = False
                        
            # Draw scroll indicators if needed
            if self.scroll_position > 0:
                high_button = {"x": 217, "y": 69, "w": 8, "h": 9}
                self.__pyxel_egal_caca.draw_button(high_button, "    ")
                if self.__pyxel_egal_caca.is_button_clicked(high_button):
                                if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                                    self.scroll_position = max(0, self.scroll_position - 1)
                pyxel.tri(
                            220, 70,  # sommet du triangle
                            218, 75,  # coin gauche
                            222, 75,  # coin droit
                            7  # couleur blanche
                        )
            if self.scroll_position + max_visible_saves < len(saves_json):

                high_button = {"x": 217, "y": 212, "w": 8, "h": 9}
                self.__pyxel_egal_caca.draw_button(high_button, "    ")
                if self.__pyxel_egal_caca.is_button_clicked(high_button):
                                if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                                    self.scroll_position = min(len(saves_json) - max_visible_saves, self.scroll_position + 1)
                pyxel.tri(
                            220, 219,  # sommet inversé
                            218, 214,  # coin gauche
                            222, 214,  # coin droit
                            7  # couleur blanche
                        )
            
            # Back button
            back_button = {"x": 140, "y": 30, "w": 80, "h": 20}
            self.__pyxel_egal_caca.draw_button(back_button, "Retour")
            if self.__pyxel_egal_caca.is_button_clicked(back_button):
                if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                    self.__pyxel_egal_caca.mode = "menu"
                
        except:
            pyxel.text(80, 100, "Pas de sauvegarde trouvee", 7)
            pyxel.text(70, 110, "Veuillez effectuer une partie", 7)

            launch_button = {"x": 90, "y": 125, "w": 80, "h": 20}
            self.__pyxel_egal_caca.draw_button(launch_button, "Lancer")
            if self.__pyxel_egal_caca.is_button_clicked(launch_button):
                            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                                self.__pyxel_egal_caca.reset()
                                self.__pyxel_egal_caca.mode = "game"

            back_button = {"x": 90, "y": 200, "w": 80, "h": 20}
            self.__pyxel_egal_caca.draw_button(back_button, "Retour")
            if self.__pyxel_egal_caca.is_button_clicked(back_button):
                if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                    self.__pyxel_egal_caca.mode = "menu"


    def deserialisation(self, classe : str) -> object:
        """
        Récupère l'objet correspondant à la classe passée en paramètre
        ----------------
        classe : classe correspondant à l'oiseau actuel
        """
        if classe == "Bird1":
            return self.__pyxel_egal_caca.blue_bird
        elif classe == "Bird2":
            return self.__pyxel_egal_caca.red_bird
        elif classe == "Bird3":
            return self.__pyxel_egal_caca.green_bird


    def restore_items(self, blue : list[tuple[int, float]], red : list[tuple[int, float]], green : list[tuple[int, float]]) -> None:
        """
        Replace des carrés vides sur les orbes pour reprendre correctement la partie
        ----------------
        blue : liste de coordonnées des orbes bleus déjà récupérées
        red : liste de coordonnées des orbes rouges déjà récupérées
        green : liste de coordonnées des orbes vertes déjà récupérées
        """

        for bleu in blue:
            pyxel.tilemaps[0].pset(bleu[0], bleu[1], (0, 0))

        for rouge in red:
            pyxel.tilemaps[0].pset(rouge[0], rouge[1], (0, 0))

        for vert in green:
            pyxel.tilemaps[0].pset(vert[0], vert[1], (0, 0))




class App:
    """
    Classe pour le jeu
    """
    def __init__(self) -> None:
        """
        Initialisation de l'application
        """

        # ============= INIT ================
        self.SCREEN_WIDTH = 256
        self.SCREEN_HEIGHT = 256
        self.map_width = 256 * 8
        self.map_height = 300
        self.save = "sauvegarde.json"
        # ========== END ===================

        # ======================= JEU =========================================
        self.x = 0
        self.y = 0
        self.COLLIDERS = [(5, 0), (4, 1), (5, 1), (6, 0), (6, 1), (7, 0), \
                          (7, 1), (5, 2), (5, 3), (6, 2), (6, 3), (7, 2), (7, 3), (5, 4), \
                          (5, 5), (6, 4), (6, 5), (7, 4), (7, 5), (0, 5)]
        self.special_colliders = [(1, 0)]
        self.mort_colliders = [(0, 3), (1, 3), (2, 3), (3, 3)]
        self.portail_colliders = [(1, 10)]
        self.bird1_frame = 0
        self.bird2_frame = 0
        self.bird3_frame = 0
        self.blue_orb = 0
        self.red_orb = 0
        self.green_orb = 0
        self.camera_x = 0
        self.camera_y = 0
        self.error_message = ""
        self.error_timer = 0
        # ================== END ===========================

        # ============== ANIMATIONS ==========================
        self.flying_bird_pos = [50, 20]
        self.walking_bird1_pos = [150, 64]
        self.walking_bird2_pos = [190, 15]
        self.animation_timer = 0
        self.animation_timer_2 = 0
        self.ajout = 1
        # ==================== END ===========================

        # ==================== MENU ==========================
        self.mode = "menu"
        self.button_start = {"x": 78, "y": 110, "w": 100, "h": 30}
        self.sauvegarde = {"x": 78, "y": 150, "w": 100, "h": 30}
        self.button_quit = {"x": 78, "y": 190, "w": 100, "h": 30}
        # ==================== END ===========================

        # ================= CLASSES ====================
        self.stele = Stele()
        self.save_class = Save(self)
        self.blue_bird = Bird1(self, self.stele)
        self.red_bird = Bird2(self, self.stele)
        self.green_bird = Bird3(self, self.stele)
        self.tombe = Tombe(self)
        self.end = End(self)
        # ================ END ======================

        # ==== VARIABLE DE STOCK POUR LES FENETRES ET LE JEU =======
        self.actual_bird = self.blue_bird
        self.unlock = [self.blue_bird]
        self.unlock_stele = [self.blue_bird]
        self.hommage = []
        self.items_blue = []
        self.items_red = []
        self.items_green = []
        # =============== END =======================
        

        
        pyxel.init(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, "Projet 3")
        pyxel.mouse(True)  # Affiche le curseur de la souris
        pyxel.load("1.pyxres")
        pyxel.run(self.update, self.draw)


    def update_camera(self) -> None:
        """
        Méthode qui gère le mouvement de la caméra (fixe sur les côtés et bouge avec l'oiseau actuel 
        lorsqu'il n'est pas vers les bords de la map)
        """
        player_center_x = self.x + 4
        player_center_y = self.y + 4
        
        # Calculate target camera position
        target_camera_x = player_center_x - self.SCREEN_WIDTH // 2
        target_camera_y = player_center_y - self.SCREEN_HEIGHT // 2
        
        # Update horizontal camera position based on player position
        if player_center_x <= self.SCREEN_WIDTH // 2:
            self.camera_x = 0
        elif player_center_x >= self.map_width - self.SCREEN_WIDTH // 2:
            self.camera_x = self.map_width - self.SCREEN_WIDTH - 8
        else:
            self.camera_x = target_camera_x

        # Update vertical camera position based on player position    
        if player_center_y <= self.SCREEN_HEIGHT // 2:
            self.camera_y = 0
        elif player_center_y >= self.SCREEN_HEIGHT // 2 and player_center_x <= 480:
            self.camera_y = target_camera_y


    def update(self) -> None:
        """
        Méthode qui gère les mises à jour du jeu
        """
        if self.mode == "menu":
            self.animation_timer += 1
            self.animation_timer_2 += 1
            if self.animation_timer > 15:
                self.bird1_frame = 1 - self.bird1_frame  # Toggle between 0 and 1
                self.bird2_frame = 1 - self.bird2_frame  # Toggle between 0 and 1
                self.bird3_frame = 1 - self.bird3_frame  # Toggle between 0 and 1
                self.animation_timer = 0

            if self.animation_timer_2 > 8:
                # Update flying bird position
                self.flying_bird_pos[0] += random.randint(-4, 2)
                self.flying_bird_pos[1] += random.randint(-2, 4)
                self.flying_bird_pos[0] = max(0, min(self.flying_bird_pos[0], 80))
                self.flying_bird_pos[1] = max(0, min(self.flying_bird_pos[1], 45))

                # Update walking birds position
                self.walking_bird1_pos[0] += random.choice([random.randint(-2, 2),random.randint(-2, 2)])
                self.walking_bird2_pos[0] -= random.choice([random.randint(-2, 2),random.randint(-2, 2)])
                self.walking_bird1_pos[0] = max(self.SCREEN_WIDTH - 112, min(self.walking_bird1_pos[0], self.SCREEN_WIDTH - 8))
                self.walking_bird2_pos[0] = max(self.SCREEN_WIDTH - 88, min(self.walking_bird2_pos[0], self.SCREEN_WIDTH - 30))

                self.animation_timer_2 = 0
            
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                if self.is_button_clicked(self.button_start):
                    self.reset()
                    self.mode = "game"
                elif self.is_button_clicked(self.sauvegarde):
                    self.save_class.scroll_position = 0
                    self.save_class.click_ignore = True
                    self.mode = "save"
                elif self.is_button_clicked(self.button_quit):
                    pyxel.quit()
        

        elif self.mode == "save":
            self.animation_timer += 1
            self.animation_timer_2 += 1
            if self.animation_timer > 15:
                self.bird1_frame = 1 - self.bird1_frame  # Toggle between 0 and 1
                self.bird2_frame = 1 - self.bird2_frame  # Toggle between 0 and 1
                self.bird3_frame = 1 - self.bird3_frame  # Toggle between 0 and 1
                self.animation_timer = 0

            if self.animation_timer_2 > 8:
                # Update flying bird position
                self.flying_bird_pos[0] += random.randint(-4, 2)
                self.flying_bird_pos[1] += random.randint(-2, 4)
                self.flying_bird_pos[0] = max(0, min(self.flying_bird_pos[0], 80))
                self.flying_bird_pos[1] = max(0, min(self.flying_bird_pos[1], 45))

                # Update walking birds position
                self.walking_bird1_pos[0] += random.choice([random.randint(-2, 2),random.randint(-2, 2)])
                self.walking_bird2_pos[0] -= random.choice([random.randint(-2, 2),random.randint(-2, 2)])
                self.walking_bird1_pos[0] = max(self.SCREEN_WIDTH - 112, min(self.walking_bird1_pos[0], self.SCREEN_WIDTH - 8))
                self.walking_bird2_pos[0] = max(self.SCREEN_WIDTH - 88, min(self.walking_bird2_pos[0], self.SCREEN_WIDTH - 30))

                self.animation_timer_2 = 0


        elif self.mode == "game":
            self.x = self.actual_bird.x
            self.y = self.actual_bird.y
            self.animation_timer_2 += 1

            if self.animation_timer_2 == 8:  
                self.tombe.hauteur += self.ajout

            if self.tombe.hauteur == 6 or self.tombe.hauteur == 0 and self.ajout == -1:
                self.ajout = -self.ajout
            

            if self.animation_timer_2 > 12:
                self.tombe.frame = (self.tombe.frame + 1) % 2
                self.animation_timer_2 = 0
                

            if pyxel.btn(pyxel.KEY_D) or pyxel.btn(pyxel.KEY_RIGHT):
                self.actual_bird.direction = "droite"
                self.actual_bird.right()
                self.animation_timer += 1
                if self.animation_timer > 15:
                    self.actual_bird.frame = (self.actual_bird.frame + 1) % 2
                    self.animation_timer = 0

            if pyxel.btn(pyxel.KEY_C):
                if self.actual_bird.check_collision_below(self.actual_bird.y):
                    if self.error_timer > 0:
                        self.error_timer = 0
                    self.mode = "bird_select"

            if pyxel.btn(pyxel.KEY_Q) or pyxel.btn(pyxel.KEY_LEFT):
                self.actual_bird.direction = "gauche"
                self.actual_bird.left()
                self.animation_timer += 1
                if self.animation_timer > 15:
                    self.actual_bird.frame = (self.actual_bird.frame + 1) % 2
                    self.animation_timer = 0
                    
            if pyxel.btnp(pyxel.KEY_SPACE):
                self.actual_bird.jump()  # Make the blue bird jump
                pyxel.play(0, 11)

            if pyxel.btnp(pyxel.KEY_P) and self.actual_bird.check_collision_below(self.actual_bird.y):
                self.mode = "place_stele"

            if pyxel.btnp(pyxel.KEY_R) and self.actual_bird.check_collision_below(self.actual_bird.y):
                self.mode = "pause"

            self.actual_bird.update()
            
            self.tombe.check_collision_with_stele(self.actual_bird)  # Appelle la vérification de collision avec la tombe
            self.tombe.check_homage(self.actual_bird)  # Appelle la vérification de l'hommage
            
            self.end.detect(self.blue_orb, self.red_orb, self.green_orb, self.blue_bird, self.red_bird, self.green_bird, self.stele)

            pyxel.camera(self.camera_x, self.camera_y)

            if self.actual_bird.y >= self.SCREEN_HEIGHT + 450:
                self.mode = "mort"


        elif self.mode == "bird_select":
            pyxel.camera(0, 0)
            
            self.animation_timer += 1
            if self.animation_timer > 15:
                self.bird1_frame = 1 - self.bird1_frame  # Toggle between 0 and 1
                self.bird2_frame = 1 - self.bird2_frame  # Toggle between 0 and 1
                self.bird3_frame = 1 - self.bird3_frame  # Toggle between 0 and 1
                self.animation_timer = 0

            # Red bird button
            if self.actual_bird == self.blue_bird:
                if 40 <= pyxel.mouse_x <= 216 and 50 <= pyxel.mouse_y <= 130:
                    if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                        if self.blue_orb >= 6:
                            self.x, self.y = self.stele.tp_red()  # Red bird shrine position
                            self.actual_bird = self.red_bird
                            self.red_bird.goto(self.stele.tp_red())
                            self.mode = "game"
                            if not self.red_bird in self.unlock:
                                self.unlock.append(self.red_bird)
                        else:
                            self.error_message = f"Besoin de {6 - self.blue_orb} orbes bleues en plus !"
                            self.error_timer = 50
                            
                # Green bird button
                if 40 <= pyxel.mouse_x <= 216 and 150 <= pyxel.mouse_y <= 230:
                    if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                        if self.red_orb >= 8:
                            self.x, self.y = self.stele.tp_green()  # Green bird shrine position
                            self.actual_bird = self.green_bird
                            self.green_bird.goto(self.stele.tp_green())
                            self.mode = "game"
                            if not self.green_bird in self.unlock:
                                self.unlock.append(self.green_bird)
                        else:
                            self.error_message = f"Besoin de {8 - self.red_orb} orbes rouges en plus !"
                            self.error_timer = 50
            
            elif self.actual_bird == self.red_bird:

                if 40 <= pyxel.mouse_x <= 216 and 50 <= pyxel.mouse_y <= 130:
                    if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                        self.x, self.y = self.stele.tp_blue()  # Blue bird shrine position
                        self.actual_bird = self.blue_bird
                        self.blue_bird.goto(self.stele.tp_blue())
                        self.mode = "game"
                
                # Green bird button
                if 40 <= pyxel.mouse_x <= 216 and 150 <= pyxel.mouse_y <= 230:
                    if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                        if self.red_orb >= 8:
                            self.x, self.y = self.stele.tp_green()
                            self.actual_bird = self.green_bird
                            self.green_bird.goto(self.stele.tp_green())
                            self.mode = "game"
                            if not self.green_bird in self.unlock:
                                self.unlock.append(self.green_bird)                            
                        else:
                            self.error_message = f"Besoin de {8 - self.red_orb} orbes rouges en plus !"
                            self.error_timer = 50

            elif self.actual_bird == self.green_bird:
                if 40 <= pyxel.mouse_x <= 216 and 50 <= pyxel.mouse_y <= 130:
                    if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                        self.x, self.y = self.stele.tp_red()
                        self.actual_bird = self.red_bird
                        self.red_bird.goto(self.stele.tp_red())
                        self.mode = "game"

                if 40 <= pyxel.mouse_x <= 216 and 150 <= pyxel.mouse_y <= 230:
                    if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                        self.x, self.y = self.stele.tp_blue()
                        self.actual_bird = self.blue_bird
                        self.blue_bird.goto(self.stele.tp_blue())
                        self.mode = "game"    
    
            if pyxel.btnp(pyxel.KEY_R):
                self.mode = "game"


        elif self.mode == "place_stele":
            pyxel.camera(0, 0)
            
            self.animation_timer += 1
            if self.animation_timer > 15:
                self.bird1_frame = 1 - self.bird1_frame  # Toggle between 0 and 1
                self.bird2_frame = 1 - self.bird2_frame  # Toggle between 0 and 1
                self.bird3_frame = 1 - self.bird3_frame  # Toggle between 0 and 1
                self.animation_timer = 0

            if 40 <= pyxel.mouse_x <= 216 and 50 <= pyxel.mouse_y <= 100:
                if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                    self.stele.place_blue(self.actual_bird.x, self.actual_bird.y)
                    self.mode = "game"

                        
            if 40 <= pyxel.mouse_x <= 216 and 110 <= pyxel.mouse_y <= 160:
                if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                    if self.blue_orb >= 10:
                        self.stele.place_red(self.actual_bird.x, self.actual_bird.y)
                        self.mode = "game"
                        if not self.red_bird in self.unlock_stele:
                            self.unlock_stele.append(self.red_bird)
                    else:
                        self.error_message = f"Besoin de {10 - self.blue_orb} orbes bleues en plus !"
                        self.error_timer = 50
            
            if 40 <= pyxel.mouse_x <= 216 and 170 <= pyxel.mouse_y <= 220:
                if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                    if self.red_orb >= 15:
                        self.stele.place_green(self.actual_bird.x, self.actual_bird.y)
                        self.mode = "game"
                        if not self.green_bird in self.unlock_stele:
                            self.unlock_stele.append(self.green_bird)
                    else:
                        self.error_message = f"Besoin de {15 - self.red_orb} orbes rouges en plus !"
                        self.error_timer = 50

            if pyxel.btnp(pyxel.KEY_R):
                self.mode = "game"


        elif self.mode == "mort":
            if pyxel.btn(pyxel.KEY_R):
                self.reset()

        elif self.mode == "pause":
            pyxel.mouse(True)
            pyxel.camera(0, 0)
            

    def draw(self) -> None:
        """
        Méthode qui gère les dessins du jeu
        """
        if self.mode == "menu":
            pyxel.cls(0)
            pyxel.bltm(0, 0, 0, 0, 16, 255 * 8, 255 * 8, None)

           # Draw flying bird
            bird1_x, bird1_y = self.bird1_frame * 8, 16
            pyxel.blt(self.flying_bird_pos[0], self.flying_bird_pos[1], 0, bird1_x, bird1_y, 8, 8, 0)

            # Draw walking birds
            bird2_x, bird2_y = self.bird2_frame * 8, 24
            pyxel.blt(self.walking_bird1_pos[0], self.walking_bird1_pos[1], 0, bird2_x, bird2_y, 8, 8, 0)
            pyxel.blt(self.walking_bird2_pos[0], self.walking_bird2_pos[1], 0, bird2_x + 16, bird2_y, 8, 8, 0)

            # Draw the game title using rectangles
            title_x = (self.SCREEN_WIDTH) // 2
            title_y = 60
            
            # Draw letters using rectangles
            letter_width = 12
            letter_spacing = 8
            start_x = title_x + 70
            
            for i, letter in enumerate("BIRDIES"):
                letter_x = start_x + i * (letter_width + letter_spacing)
                self.draw_letter(letter, letter_x, title_y + 5, 0.5)
                
            # Boutons
            self.draw_button(self.button_start, "Commencer")
            self.draw_button(self.sauvegarde, "Charger une sauvegarde")
            self.draw_button(self.button_quit, "Quitter")


        elif self.mode == "save":
            pyxel.cls(0)
            pyxel.bltm(0, 0, 0, 0, 16, 255 * 8, 255 * 8, None)

           # Draw flying bird
            bird1_x, bird1_y = self.bird1_frame * 8, 16
            pyxel.blt(self.flying_bird_pos[0], self.flying_bird_pos[1], 0, bird1_x, bird1_y, 8, 8, 0)

            # Draw walking birds
            bird2_x, bird2_y = self.bird2_frame * 8, 24
            pyxel.blt(self.walking_bird1_pos[0], self.walking_bird1_pos[1], 0, bird2_x, bird2_y, 8, 8, 0)
            pyxel.blt(self.walking_bird2_pos[0], self.walking_bird2_pos[1], 0, bird2_x + 16, bird2_y, 8, 8, 0)

            self.save_class.show_save()


        elif self.mode == "game":
            pyxel.cls(0)  # Efface l'écran

             # Save current camera position
            camera_pos_x, camera_pos_y = self.x, self.y
            
            # Draw game elements affected by camera
            pyxel.bltm(0, 0, 0, 0, 0, 255 * 8, 255 * 8, None)
            self.stele.blue()
            self.stele.red()
            self.stele.green()
            self.actual_bird.draw()
            self.tombe.check_bird()

            # Reset camera for UI elements
            pyxel.camera(0, 0)

            pyxel.blt(self.SCREEN_WIDTH - 10, 10, 0, 0, 8, 8, 8, 2)
            pyxel.blt(self.SCREEN_WIDTH - 10, 20, 0, 8, 8, 8, 8, 2)
            pyxel.blt(self.SCREEN_WIDTH - 10, 30, 0, 16, 8, 8, 8, 2)
            pyxel.text(self.SCREEN_WIDTH - 15, 12, str(self.blue_orb), 7)
            pyxel.text(self.SCREEN_WIDTH - 15, 22, str(self.red_orb), 7)
            pyxel.text(self.SCREEN_WIDTH - 15, 32, str(self.green_orb), 7)

            pyxel.rect(self.SCREEN_WIDTH - 52, 45, 50, 8, 1)
            la_pipette_jaugee = int((self.actual_bird.teleport_jauge / self.actual_bird.teleport_jauge_max) * 48)
            pyxel.rect(self.SCREEN_WIDTH - 52, 46, la_pipette_jaugee, 6, pyxel.COLOR_GREEN)
            charge_width = int((self.actual_bird.tp_charge / self.actual_bird.tp_max_charge) * 48)
            pyxel.rect(self.SCREEN_WIDTH - 52, 46, charge_width, 6, 9)
            pyxel.rectb(self.SCREEN_WIDTH - 52, 45, 50, 8, 7)

            if self.actual_bird == self.green_bird:
                pyxel.rect(self.SCREEN_WIDTH - 52, 55, 50, 8, 1)
                jauge_val = int((self.green_bird.flight_gauge / self.green_bird.max_flight_gauge) * 48)
                pyxel.rect(self.SCREEN_WIDTH - 52, 56, jauge_val, 6, pyxel.COLOR_LIGHT_BLUE)


            if self.end.show_message:
                pyxel.rect(self.end.pos_rect[0], self.end.pos_rect[1], self.end.taille_rect[0], self.end.taille_rect[1], pyxel.COLOR_BLACK)
                pyxel.text(self.end.pos_rect[0] + 10, self.end.pos_rect[1] + 10, self.end.message, 7)
                if hasattr(self.end, "message_2"):
                    pyxel.rect(self.end.pos_rect[0], self.end.pos_rect[1] + self.end.taille_rect[1], self.end.taille_rect[0], self.end.taille_rect[1] - 10, pyxel.COLOR_BLACK)
                    pyxel.text(self.SCREEN_WIDTH - self.end.taille_rect[0] + self.end.pos_rect[0] + 10, self.end.pos_rect[1] + self.end.taille_rect[1], self.end.message_2, 7)
                self.end.message_timer -= 1
                if self.end.message_timer <= 0:
                    self.end.show_message = False

            if self.tombe.show_message:
                pyxel.rect(self.tombe.pos_rect[0], self.tombe.pos_rect[1], self.tombe.taille_rect[0], self.tombe.taille_rect[1], pyxel.COLOR_BLACK)
                pyxel.text(self.tombe.pos_rect[0] + 10, self.tombe.pos_rect[1] + 10, self.tombe.message, 7)
                
                if hasattr(self.tombe, "message_2") and not self.actual_bird.to_dict() in self.hommage:
                    pyxel.rect(self.tombe.pos_rect[0], self.tombe.pos_rect[1] + self.tombe.taille_rect[1], self.tombe.taille_rect[0], self.tombe.taille_rect[1] - 10, pyxel.COLOR_BLACK)
                    pyxel.text(self.SCREEN_WIDTH - self.tombe.taille_rect[0] + 10, self.tombe.pos_rect[1] + self.tombe.taille_rect[1], self.tombe.message_2, 7)

                if hasattr(self.tombe, "message_2") and self.actual_bird.to_dict() in self.hommage: 
                    pyxel.rect(0, self.tombe.pos_rect[1] + self.tombe.taille_rect[1], 256, self.tombe.taille_rect[1], pyxel.COLOR_BLACK)
                    pyxel.text(10, self.tombe.pos_rect[1] + self.tombe.taille_rect[1] + 10, self.tombe.message_2, 7)

                if hasattr(self.tombe,"message_3"):
                    pyxel.rect(self.tombe.pos_rect3[0], self.tombe.pos_rect[1] + self.tombe.taille_rect[1] * 2, self.tombe.pos_rect3[1], self.tombe.taille_rect[1], pyxel.COLOR_BLACK)
                    pyxel.text(self.tombe.pos_rect3[0] + 10 , self.tombe.pos_rect[1] + self.tombe.taille_rect[1] * 2 + 10, self.tombe.message_3, 7)
                
                self.tombe.message_timer -= 1
                if self.tombe.message_timer <= 0:
                    self.tombe.show_message = False
                    if not self.actual_bird.to_dict() in self.hommage:
                        self.hommage.append(self.actual_bird.to_dict())
            self.actual_bird.draw_particles()
            self.tombe.draw_particles()

            # Restore camera position
            pyxel.camera(camera_pos_x, camera_pos_y)


        elif self.mode == "bird_select":
            pyxel.camera(0, 0)

            if (30 <= pyxel.mouse_x <= 218 and 
                20 <= pyxel.mouse_y <= 228):
                pyxel.mouse(True)
            else:
                pyxel.mouse(False)
                
            if self.error_timer > 0:
                self.error_timer -= 1

            # Background
            pyxel.rect(30, 20, 196, 216, 5)
            pyxel.rectb(30, 20, 196, 216, 7)
            
            # Title
            title_x = 80
            title_y = 55
            for i, letter in enumerate("SELECT BIRD"):
                self.draw_letter(letter, title_x + i * 20, title_y, 0.5)

            if self.actual_bird == self.blue_bird:
                # Red Bird Section
                pyxel.rect(40, 50, 176, 80, 8)
                pyxel.text(50, 60, "Red Bird", 7)
                pyxel.text(130, 60, "Necessaire : 6", 7) if not self.red_bird in self.unlock else None
                pyxel.blt(190, 59, 0, 0, 8, 8, 8, 2) if not self.red_bird in self.unlock else None
                pyxel.blt(50, 80, 0, self.bird2_frame * 8 + 16, 24, 8, 8, 2)  # Red bird sprite
                pyxel.line(40, 100, 216, 100, 7)
                pyxel.text(50, 110, "Fast and agile", 7)
                
                # Green Bird Section
                pyxel.rect(40, 150, 176, 80, 8)
                pyxel.text(50, 160, "Green Bird", 7)
                pyxel.text(130, 160, "Necessaire : 8", 7) if not self.green_bird in self.unlock else None
                pyxel.blt(190, 159, 0, 8, 8, 8, 8, 2) if not self.green_bird in self.unlock else None
                pyxel.blt(50, 180, 0, self.bird3_frame * 8, 24, 8, 8, 2)  # Green bird sprite
                pyxel.line(40, 200, 216, 200, 7)
                pyxel.text(50, 210, "Peut marcher dans les airs pendant", 7)
                pyxel.text(50, 220, "une duree determinee", 7)

            elif self.actual_bird == self.red_bird:
                # Red Bird Section
                pyxel.rect(40, 50, 176, 80, 8)
                pyxel.text(50, 60, "Blue Bird", 7)
                pyxel.blt(50, 80, 0, self.bird2_frame * 8, 16, 8, 8, 2)  # Red bird sprite
                pyxel.line(40, 100, 216, 100, 7)
                pyxel.text(50, 110, "Un oiseau bleu ?", 7)
                
                # Green Bird Section
                pyxel.rect(40, 150, 176, 80, 8)
                pyxel.text(50, 160, "Green Bird", 7)
                pyxel.text(130, 160, "Necessaire : 8", 7) if not self.green_bird in self.unlock else None
                pyxel.blt(190, 159, 0, 0, 8, 8, 8, 2) if not self.green_bird in self.unlock else None
                pyxel.blt(50, 180, 0, self.bird3_frame * 8, 24, 8, 8, 2)  # Green bird sprite
                pyxel.line(40, 200, 216, 200, 7)
                pyxel.text(50, 210, "Peut marcher dans les airs pendant", 7)
                pyxel.text(50, 220, "une duree determinee", 7)

            elif self.actual_bird == self.green_bird:
                # Red Bird Section
                pyxel.rect(40, 50, 176, 80, 8)
                pyxel.text(50, 60, "Red Bird", 7)
                pyxel.blt(50, 80, 0, self.bird2_frame * 8 + 16, 24, 8, 8, 2)  # Red bird sprite
                pyxel.line(40, 100, 216, 100, 7)
                pyxel.text(50, 110, "Fast and agile", 7)
                
                # Green Bird Section
                pyxel.rect(40, 150, 176, 80, 8)
                pyxel.text(50, 160, "Blue Bird", 7)
                pyxel.blt(50, 180, 0, self.bird3_frame * 8, 16, 8, 8, 2)  # Green bird sprite
                pyxel.line(40, 200, 216, 200, 7)
                pyxel.text(50, 210, "Un oiseau bleu ?", 7)

            
            # Error message
            if self.error_timer > 0:
                pyxel.rect(65, 110, 145, 20, pyxel.COLOR_PURPLE)
                pyxel.text(70, 115, self.error_message, 7)        


        elif self.mode == "place_stele":
            pyxel.camera(0, 0)

            if (30 <= pyxel.mouse_x <= 218 and 
                20 <= pyxel.mouse_y <= 228):
                pyxel.mouse(True)
            else:
                pyxel.mouse(False)
                
            if self.error_timer > 0:
                self.error_timer -= 1
    
            # Background
            pyxel.rect(30, 20, 196, 216, 5)
            pyxel.rectb(30, 20, 196, 216, 7)
            
            # Title
            title_x = 80
            title_y = 50
            for i, letter in enumerate("PLACE STELE"):
                self.draw_letter(letter, title_x + i * 20, title_y, 0.5)

            pyxel.rect(40, 50, 176, 50, 8)
            pyxel.text(50, 60, "Blue Stele", 7)
            pyxel.blt(50, 80, 0, 0, 72, 8, 8, 2)  # Red bird stele sprite
            pyxel.blt(150, 80, 0, self.bird1_frame * 8, 16, -8, 8, 2)

            pyxel.rect(40, 110, 176, 50, 8)
            pyxel.text(50, 120, "Red Stele", 7)
            pyxel.text(130, 120, "Necessaire : 10", 7) if not self.red_bird in self.unlock_stele else None
            pyxel.blt(190, 119, 0, 0, 8, 8, 8, 2) if not self.red_bird in self.unlock_stele else None
            pyxel.blt(150, 140, 0, self.bird2_frame * 8 + 16, 24, -8, 8, 2)  # Red bird sprite
            pyxel.blt(50, 140, 0, 8, 64, 8, 8, 2)  # Red bird stele sprite

            pyxel.rect(40, 170, 176, 50, 8)
            pyxel.text(50, 180, "Green Stele", 7)
            pyxel.text(130, 180, "Necessaire : 15", 7) if not self.green_bird in self.unlock_stele else None
            pyxel.blt(190, 179, 0, 8, 8, 8, 8, 2) if not self.green_bird in self.unlock_stele else None
            pyxel.blt(150, 200, 0, self.bird3_frame * 8, 24, -8, 8, 2)  # Green bird sprite
            pyxel.blt(50, 200, 0, 0, 64, 8, 8, 2)  # Red bird stele sprite

            # Error message
            if self.error_timer > 0:
                pyxel.rect(65, 110, 150, 20, pyxel.COLOR_PURPLE)
                pyxel.text(70, 115, self.error_message, 7)  


        elif self.mode == "mort":
            pyxel.cls(0)
            pyxel.camera(0, 0)
            start_x = (self.SCREEN_WIDTH // 2) + 55
            letter_width = 12
            letter_spacing = 8

            for i, letter in enumerate("GAMEOVER"):
                letter_x = start_x + i * (letter_width + letter_spacing)
                self.draw_letter(letter, letter_x, self.SCREEN_WIDTH // 2 + 50, 0.5, pyxel.COLOR_BROWN)

            pyxel.text(self.SCREEN_WIDTH // 2 - 65, self.SCREEN_HEIGHT // 2, "Pressez la touche r pour recommencer", pyxel.COLOR_PEACH)


            if pyxel.btn(pyxel.KEY_R):
                self.mode = "game"

        elif self.mode == "pause" :
            pyxel.camera(0, 0)
            pyxel.cls(0)
            pyxel.text(120, 90, "PAUSE", 7)

            retour_button = {"x": 90, "y": 115, "w": 80, "h": 20}
            self.draw_button(retour_button, "Retour au jeu", pyxel.COLOR_BLACK)
            if self.is_button_clicked(retour_button):
                            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                                self.mode = "game"

            save_button = {"x": 60, "y": 145, "w": 140, "h": 20}
            self.draw_button(save_button, "Sauvegarde et retourner au menu", pyxel.COLOR_BLACK)
            if self.is_button_clicked(save_button):
                            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                                self.save_class.sauvegarder()
                                self.mode = "menu"

            quitter_button = {"x": 90, "y": 175, "w": 80, "h": 20}
            self.draw_button(quitter_button, "Quitter le jeu", pyxel.COLOR_BLACK)
            if self.is_button_clicked(quitter_button):
                            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                                pyxel.quit()


    def draw_letter(self, letter : str, x : int, y : int, scale : int = 1, couleur : bool | int = True) -> None:
        """
        Méthode qui dessine des lettres en grande taille
        -------------------
        letter : lettre à dessiner
        x : position x de la lettre
        y : position y de la lettre
        scale : échelle de la lettre
        couleur : couleur de la lettre
        """
        
        def scaled_rect(x, y, w, h, couleur : bool | int = True) -> None:
            """
            Fonction qui dessine un rectangle pour dessiner les lettres
            -------------------
            x : position x du rectangle
            y : position y du rectangle
            w : largeur du rectangle
            h : hauteur du rectangle
            couleur : couleur du rectangle
            """

            if couleur == True:
                for i in range(h):
                    gradient_col = 7 + int((17 - 7) * i / h)
                    pyxel.rect(x * scale, (y + i) * scale, w * scale, scale, gradient_col)
            else:
                for i in range(h):
                    pyxel.rect(x * scale, (y + i) * scale, w * scale, scale, couleur)
        if letter == 'B':
            scaled_rect(x, y, 4, 30, couleur)
            scaled_rect(x + 4, y, 6, 4, couleur)
            scaled_rect(x + 4, y + 13, 6, 4, couleur)
            scaled_rect(x + 4, y + 26, 6, 4, couleur)
            scaled_rect(x + 10, y + 4, 4, 9, couleur)
            scaled_rect(x + 10, y + 17, 4, 9, couleur)

        elif letter == 'I':
            scaled_rect(x + 4, y, 4, 30, couleur)

        elif letter == 'R':
            scaled_rect(x, y, 4, 30, couleur)
            scaled_rect(x + 4, y, 8, 4, couleur)
            scaled_rect(x + 4, y + 13, 8, 4, couleur)
            scaled_rect(x + 10, y + 4, 4, 9, couleur)
            scaled_rect(x + 4, y + 17, 4, 4, couleur)
            scaled_rect(x + 8, y + 21, 4, 4, couleur)
            scaled_rect(x + 12, y + 24, 4, 5, couleur)

        elif letter == 'D':
            scaled_rect(x, y, 4, 30, couleur)
            scaled_rect(x + 4, y, 8, 4, couleur)
            scaled_rect(x + 4, y + 26, 8, 4, couleur)
            scaled_rect(x + 8, y + 4, 4, 22, couleur)

        elif letter == 'E':
            scaled_rect(x, y, 4, 30, couleur)
            scaled_rect(x + 4, y, 8, 4, couleur)
            scaled_rect(x + 4, y + 13, 8, 4, couleur)
            scaled_rect(x + 4, y + 26, 8, 4, couleur)

        elif letter == 'S':
            scaled_rect(x, y, 12, 4, couleur)
            scaled_rect(x, y + 13, 12, 4, couleur)
            scaled_rect(x, y + 26, 12, 4, couleur)
            scaled_rect(x, y + 4, 4, 9, couleur)
            scaled_rect(x + 8, y + 17, 4, 9, couleur)

        elif letter == 'G':
            scaled_rect(x, y, 4, 30, couleur)
            scaled_rect(x + 4, y, 8, 4, couleur)
            scaled_rect(x + 4, y + 26, 8, 4, couleur)
            scaled_rect(x + 8, y + 13, 4, 13, couleur)

        elif letter == 'A':
            scaled_rect(x, y + 4, 4, 26, couleur)
            scaled_rect(x + 4, y, 8, 4, couleur)
            scaled_rect(x + 4, y + 13, 8, 4, couleur)
            scaled_rect(x + 12, y + 4, 4, 26, couleur)

        elif letter == 'M':
            scaled_rect(x, y, 4, 30, couleur)
            scaled_rect(x + 4, y, 4, 8, couleur)
            scaled_rect(x + 8, y + 8, 4, 8, couleur)
            scaled_rect(x + 12, y, 4, 8, couleur)
            scaled_rect(x + 16, y, 4, 30, couleur)

        elif letter == 'O':
            scaled_rect(x, y, 4, 30, couleur)
            scaled_rect(x + 4, y, 8, 4, couleur)
            scaled_rect(x + 4, y + 26, 8, 4, couleur)
            scaled_rect(x + 12, y, 4, 30, couleur)

        elif letter == 'V':
            scaled_rect(x, y, 4, 20, couleur)
            scaled_rect(x + 4, y + 20, 4, 6, couleur)
            scaled_rect(x + 8, y + 26, 4, 4, couleur)
            scaled_rect(x + 12, y + 20, 4, 6, couleur)
            scaled_rect(x + 16, y, 4, 20, couleur)

        elif letter == 'L':
            scaled_rect(x, y, 4, 30, couleur)
            scaled_rect(x + 4, y + 26, 8, 4, couleur)

        elif letter == 'C':
            scaled_rect(x, y, 4, 30, couleur)
            scaled_rect(x + 4, y, 8, 4, couleur)
            scaled_rect(x + 4, y + 26, 8, 4, couleur)

        elif letter == 'T':
            scaled_rect(x + 4, y, 4, 30, couleur)
            scaled_rect(x, y, 12, 4, couleur)

        elif letter == 'N':
            scaled_rect(x, y, 4, 30, couleur)
            scaled_rect(x + 4, y, 4, 8, couleur)
            scaled_rect(x + 8, y + 8, 4, 8, couleur)
            scaled_rect(x + 12, y + 16, 4, 14, couleur)

        elif letter == 'P':
            scaled_rect(x, y, 4, 30, couleur)
            scaled_rect(x + 4, y, 8, 4, couleur)
            scaled_rect(x + 4, y + 13, 8, 4, couleur)
            scaled_rect(x + 12, y + 4, 4, 9, couleur)


    def draw_button(self, button : dict[str, int | float], text : str, color : int = 5, border_color : int = 7, text_color : int = 7) -> None:
        """
        Méthode qui dessine un bouton
        -------------------
        button : dictionnaire contenant les informations du bouton (coordonnées, taille, etc...)
        text : texte à afficher sur le bouton
        color : couleur du bouton
        border_color : couleur de la bordure du bouton
        text_color : couleur du texte du bouton
        """
        pyxel.rect(button["x"], button["y"], button["w"], button["h"], color)
        pyxel.rectb(button["x"], button["y"], button["w"], button["h"], border_color)
        text_x = button["x"] + (button["w"] - len(text) * 4) // 2
        text_y = button["y"] + (button["h"] - 5) // 2
        pyxel.text(text_x, text_y, text, text_color)

        # Effet de survol
        if self.is_button_clicked(button):
            pyxel.rect(button["x"] + 1, button["y"] + 1, button["w"] - 2, button["h"] - 2, border_color)
            pyxel.rectb(button["x"], button["y"], button["w"], button["h"], text_color)
            pyxel.text(text_x, text_y, text, color)


    def is_button_clicked(self, button : dict[str, int | float]) -> bool :
        """
        Méthode qui vérifie si le bouton est survolé
        -------------------
        button : dictionnaire contenant les informations du bouton (coordonnées, taille, etc...)
        """
        return (button["x"] <= pyxel.mouse_x <= button["x"] + button["w"] and
                button["y"] <= pyxel.mouse_y <= button["y"] + button["h"])


    def reset(self) -> None:
        """
        Méthode qui permet de reset le jeu
        """
        self.blue_bird.reset()
        self.green_bird.reset()
        self.red_bird.reset()
        self.tombe.reset()
        self.end.reset()
        
        while self.items_blue:
            blue = self.items_blue.pop()
            pyxel.tilemaps[0].pset(blue[0], blue[1], (0, 1))

        while self.items_red:
            red = self.items_red.pop()
            pyxel.tilemaps[0].pset(red[0], red[1], (0, 2))  
        
        while self.items_green:
            green = self.items_green.pop()
            pyxel.tilemaps[0].pset(green[0], green[1], (0, 3))
        
        self.x = 0
        self.y = 0
        self.camera_x = 0
        self.camera_y = 0
        self.bird1_frame = 0
        self.bird2_frame = 0
        self.bird3_frame = 0
        self.blue_orb = 0
        self.red_orb = 0
        self.green_orb = 0
        self.error_message = ""
        self.error_timer = 0

        self.animation_timer = 0
        self.animation_timer_2 = 0

        self.actual_bird = self.blue_bird
        self.unlock = [self.blue_bird]
        self.unlock_stele = [self.blue_bird]
        self.hommage = []
        self.items_blue = []
        self.items_red = []
        self.items_green = []




class Bird1:
    """
    Classe de l'oiseau bleu
    """
    def __init__(self, app, stele) -> None:
        """
        Constructeur de la classe Bird1
        -------------------
        app : instance de la classe App
        stele : instance de la classe Stele
        """
        self.x = 10
        self.y = 90
        self.direction = "droite"
        self.velocity_y = 0
        self.bugs_bunny = 0
        self.max_jumps = 3
        self.gravity = 0.1
        self.jump_strength = -2
        self.frame = 0
        self.pyxel_egal_caca = app
        self.def_speed = 2
        self.tp_charge = 0
        self.tp_max_charge = 104
        self.is_charging = False
        self.particles = []
        self.stele = stele
        self.teleport_jauge = 0
        self.teleport_jauge_max = 104
        self.waiting = 0
        
    
    def right(self) -> None:
        """
        Méthode qui permet de faire bouger l'oiseau vers la droite
        """
        new_x = self.x + self.def_speed  # Déplacer le joueur vers la droite
        # Vérifier la collision avec la tuile à droite du joueur
        if self.check_collision_right(new_x):
            # Pas de collision, on peut avancer
            self.x = min(new_x, self.pyxel_egal_caca.map_width - 17)
            self.pyxel_egal_caca.update_camera()
    

    def left(self) -> None:
        """
        Méthode qui permet de faire bouger l'oiseau vers la gauche
        """
        new_x = self.x - self.def_speed  # Déplacer le joueur vers la droite
        # Vérifier la collision avec la tuile à droite du joueur
        if self.check_collision_left(new_x):
            # Pas de collision, on peut avancer
            self.x = max(1, self.x - self.def_speed)
            self.pyxel_egal_caca.update_camera()


    def jump(self) -> None:
        """
        Méthode qui permet de faire sauter l'oiseau
        """
        if self.bugs_bunny < self.max_jumps:
            self.velocity_y = self.jump_strength
            self.bugs_bunny += 1


    def update(self) -> None:
        """
        Méthode qui permet de mettre à jour l'oiseau
        """
        # Apply gravity
        self.velocity_y += self.gravity
        new_y = self.y + self.velocity_y


        if self.check_collision_below(new_y):
            self.y = (new_y // 8) * 8
            self.velocity_y = 0
            self.bugs_bunny = 0
        else:
            if not self.check_collision_above(new_y):
                self.y = new_y


        # Limit falling speed
        if self.velocity_y > 4:
            self.velocity_y = 4

        if pyxel.btn(pyxel.KEY_T):
            if self.teleport_jauge == self.teleport_jauge_max:
                self.is_charging = True
                self.tp_charge = min(self.tp_charge + 2, self.tp_max_charge)
                # Gauge particles
                if random.random() < 0.3:
                    charge_x = self.pyxel_egal_caca.SCREEN_WIDTH - 59 + int((self.tp_charge / self.tp_max_charge) * 48)
                    self.particles.append(Particle(charge_x, 50, "gauge"))
                # Bird particles while charging
                if random.random() < 0.4:
                    self.particles.append(Particle(
                        self.x + random.randint(0, 8),
                        self.y + random.randint(0, 8),
                        "bird"
                    ))
            
            else:
                if self.is_charging and self.tp_charge >= self.tp_max_charge:
                    self.goto(self.stele.tp_blue())
                self.is_charging = False
                self.tp_charge = max(0, self.tp_charge - 1)
                if self.waiting >= 20:
                    self.teleport_jauge = min(self.teleport_jauge + 1, 104)
                    self.waiting = 0
                else:
                    self.waiting += 1

        else:
            if self.is_charging and self.tp_charge >= self.tp_max_charge:
                self.goto(self.stele.tp_blue())
            self.is_charging = False
            self.tp_charge = max(0, self.tp_charge - 1)
            if self.waiting >= 20:
                self.teleport_jauge = min(self.teleport_jauge + 1, 104)
                self.waiting = 0
            else:
                self.waiting += 1
                
        # Update particles
        for particle in self.particles[:]:
            if particle.type == "bird":
                particle.vy += 0.1  # Add gravity to bird particles
            particle.x += particle.vx
            particle.y += particle.vy
            particle.life -= 1
            if particle.life <= 0:
                self.particles.remove(particle)

        self.check_items_collision()


    def draw_particles(self) -> None:
        """
        Méthode qui permet de dessiner les particules
        """
        for particle in self.particles:
            if particle.type == "gauge":
                # Draw gauge particles relative to screen
                screen_x = particle.x
                screen_y = particle.y
            else:
                # Draw bird particles relative to world
                screen_x = particle.x - self.pyxel_egal_caca.camera_x
                screen_y = particle.y - self.pyxel_egal_caca.camera_y
            pyxel.pset(screen_x, screen_y, particle.color)


    def draw(self) -> None:
        """
        Méthode qui permet de dessiner l'oiseau
        """
        if self.direction == "droite":
            pyxel.blt(self.x, self.y, 0, 8 * self.frame, 16, 8, 8, 2)
        else:
            pyxel.blt(self.x, self.y, 0, 8 * self.frame, 16, -8, 8, 2)


    def check_collision_below(self, new_y : int | float) -> bool:
        """
        Vérifie s'il y a une collision sous le joueur en fonction de sa nouvelle position `new_y`.
        --------------
        new_y : position y du zoiseaux
        """
        # On vérifie à deux points : sous le coin gauche et sous le coin droit du joueur
        left_tile = pyxel.tilemaps[0].pget(self.x // 8, (new_y + 6 + self.def_speed) // 8)  # Coin gauche
        right_tile = pyxel.tilemaps[0].pget((self.x + 8) // 8, (new_y + 6 + self.def_speed) // 8)  # Coin droit

        # Si l'une des tuiles en dessous est un obstacle (collide), il y a une collision
        return left_tile in self.pyxel_egal_caca.COLLIDERS or right_tile in self.pyxel_egal_caca.COLLIDERS or left_tile in self.pyxel_egal_caca.special_colliders or right_tile in self.pyxel_egal_caca.special_colliders
    

    def check_collision_right(self, new_x : int) -> bool:
        """
        Vérifie s'il y a une collision à droite du joueur pour le déplacement horizontal.
        --------------
        new_x : position x du zoiseaux
        """
        top_tile = pyxel.tilemaps[0].pget((new_x + 6 + self.def_speed) // 8, self.y // 8)  # Coin supérieur droit
        bottom_tile = pyxel.tilemaps[0].pget((new_x + 6 + self.def_speed) // 8, (self.y + 7) // 8)  # Coin inférieur droit

        # Si l'une des tuiles à droite est un obstacle (collide), il y a une collision
        return top_tile not in self.pyxel_egal_caca.COLLIDERS and bottom_tile not in self.pyxel_egal_caca.COLLIDERS


    def check_collision_left(self, new_x : int) -> bool:
        """
        Vérifie s'il y a une collision à gauche du joueur pour le déplacement horizontal.
        --------------
        new_x : position x du zoiseaux
        """
        top_tile = pyxel.tilemaps[0].pget((new_x + 2 - self.def_speed) // 8, self.y // 8)  # Coin supérieur gauche
        bottom_tile = pyxel.tilemaps[0].pget((new_x + 2 - self.def_speed) // 8, (self.y + 7) // 8)  # Coin inférieur gauche
        # Si l'une des tuiles à gauche est un obstacle (collide), il y a une collision
        return top_tile not in self.pyxel_egal_caca.COLLIDERS and bottom_tile not in self.pyxel_egal_caca.COLLIDERS
    
    
    def check_collision_above(self, new_y : int | float) -> bool:
        """
        Vérifie s'il y a une collision au-dessus du joueur en fonction de sa nouvelle position `new_y`.
        --------------
        new_y : position y du zoiseaux
        """
        # On vérifie à deux points : au-dessus du coin gauche et au-dessus du coin droit du joueur
        left_tile = pyxel.tilemaps[0].pget(self.x // 8, (new_y + 1 - self.def_speed) // 8)  # Coin gauche
        right_tile = pyxel.tilemaps[0].pget((self.x + 7) // 8, (new_y + 1 - self.def_speed) // 8)  # Coin droit

        # Si l'une des tuiles au-dessus est un obstacle (collide), il y a une collision
        return left_tile in self.pyxel_egal_caca.COLLIDERS or right_tile in self.pyxel_egal_caca.COLLIDERS
    

    def check_items_collision(self) -> None:
            """
            Vérifie les collisions avec les items et les efface si nécessaire.
            """
            tile_x = self.x // 8
            tile_y = self.y // 8

            tile = pyxel.tilemaps[0].pget(tile_x, tile_y)

            if tile == (0, 1):
                pyxel.tilemaps[0].pset(tile_x, tile_y, (0, 0))
                self.pyxel_egal_caca.blue_orb += 1
                self.pyxel_egal_caca.items_blue.append((tile_x, tile_y))


    def reset(self) -> None:
        """
        Réinitialise l'oiseau
        """
        self.x = 10
        self.y = 90
        self.direction = "droite"
        self.velocity_y = 0
        self.bugs_bunny = 0
        self.frame = 0
        self.tp_charge = 0
        self.is_charging = False
        self.particles = []
        self.teleport_jauge = 0
        self.waiting = 0


    def get_pos(self) -> tuple[int, int | float] :
        """
        Méthode qui permet de renvoyer les coordonnées de l'oiseau
        """
        return (self.x, self.y)


    def goto(self, tuple_x_y) -> None:
        """
        Méthode qui permet de téléporter l'oiseau
        """
        self.x = tuple_x_y[0]
        self.y = tuple_x_y[1]
        self.teleport_jauge = 0
        self.pyxel_egal_caca.x = tuple_x_y[0]
        self.pyxel_egal_caca.y = tuple_x_y[1]
        self.pyxel_egal_caca.update_camera()


    def set_stele(self) -> None:
        """
        Méthode qui permet de placer la stèle de l'oiseau
        """
        self.stele.place_blue(self.x, self. y)


    def to_dict(self) -> str:
        """
        Méthode qui permet d'ajouter la classe de l'oiseau pour la sauvegarde
        """
        return "Bird1"




class Bird2:
    def __init__(self, app, stele):
        self.x = 0
        self.y = 0
        self.direction = "droite"
        self.velocity_y = 0
        self.bugs_bunny = 0  # Track number of jumps
        self.max_jumps = 3  # Maximum allowed jumps
        self.gravity = 0.1
        self.jump_strength = -2
        self.frame = 0
        self.pyxel_egal_caca = app
        self.def_speed = 2
        self.tp_charge = 0
        self.tp_max_charge = 104
        self.is_charging = False
        self.particles = []
        self.stele = stele
        self.teleport_jauge = 0
        self.teleport_jauge_max = 104
        self.waiting = 0

    def right(self) -> None:
        new_x = self.x + self.def_speed  # Déplacer le joueur vers la droite
        # Vérifier la collision avec la tuile à droite du joueur
        if self.check_collision_right(new_x):
            # Pas de collision, on peut avancer
            self.x = min(new_x, self.pyxel_egal_caca.map_width - 17)
            self.pyxel_egal_caca.update_camera()
    

    def left(self) -> None:
        new_x = self.x - self.def_speed  # Déplacer le joueur vers la droite
        # Vérifier la collision avec la tuile à droite du joueur
        if self.check_collision_left(new_x):
            # Pas de collision, on peut avancer
            self.x = max(1, self.x - self.def_speed)
            self.pyxel_egal_caca.update_camera()


    def jump(self) -> None:
        if self.bugs_bunny < self.max_jumps:
            self.velocity_y = self.jump_strength
            self.bugs_bunny += 1


    def draw(self) -> None:
        if self.direction == "droite":
            pyxel.blt(self.x, self.y, 0, 8 * self.frame + 16, 24, 8, 8, 2)
        else:
            pyxel.blt(self.x, self.y, 0, 8 * self.frame + 16, 24, -8, 8, 2)


    def update(self) -> None:
        # Apply gravity
        self.velocity_y += self.gravity
        new_y = self.y + self.velocity_y


        if self.check_collision_below(new_y):
            self.y = (new_y // 8) * 8
            self.velocity_y = 0
            self.bugs_bunny = 0
        else:
            if not self.check_collision_above(new_y):
                self.y = new_y

        # Limit falling speed
        if self.velocity_y > 4:
            self.velocity_y = 4

        if pyxel.btn(pyxel.KEY_T):
            if self.teleport_jauge == self.teleport_jauge_max:
                self.is_charging = True
                self.tp_charge = min(self.tp_charge + 2, self.tp_max_charge)
                # Gauge particles
                if random.random() < 0.3:
                    charge_x = self.pyxel_egal_caca.SCREEN_WIDTH - 59 + int((self.tp_charge / self.tp_max_charge) * 48)
                    self.particles.append(Particle(charge_x, 50, "gauge"))
                # Bird particles while charging
                if random.random() < 0.4:
                    self.particles.append(Particle(
                        self.x + random.randint(0, 8),
                        self.y + random.randint(0, 8),
                        "bird"
                    ))
            
            else:
                if self.is_charging and self.tp_charge >= self.tp_max_charge:
                    self.goto(self.stele.tp_red())
                self.is_charging = False
                self.tp_charge = max(0, self.tp_charge - 1)
                if self.waiting >= 20:
                    self.teleport_jauge = min(self.teleport_jauge + 1, 104)
                    self.waiting = 0
                else:
                    self.waiting += 1

        else:
            if self.is_charging and self.tp_charge >= self.tp_max_charge:
                self.goto(self.stele.tp_red())
            self.is_charging = False
            self.tp_charge = max(0, self.tp_charge - 1)
            if self.waiting >= 20:
                self.teleport_jauge = min(self.teleport_jauge + 1, 104)
                self.waiting = 0
            else:
                self.waiting += 1
                
        # Update particles
        for particle in self.particles[:]:
            if particle.type == "bird":
                particle.vy += 0.1  # Add gravity to bird particles
            particle.x += particle.vx
            particle.y += particle.vy
            particle.life -= 1
            if particle.life <= 0:
                self.particles.remove(particle)

        self.check_items_collision()


    def check_collision_below(self, new_y : int | float) -> bool :
        """
        Vérifie s'il y a une collision sous le joueur en fonction de sa nouvelle position `new_y`.
        --------------
        new_y : position y du zoiseaux
        """
        # On vérifie à deux points : sous le coin gauche et sous le coin droit du joueur
        left_tile = pyxel.tilemaps[0].pget(self.x // 8, (new_y + 6 + self.def_speed) // 8)  # Coin gauche
        right_tile = pyxel.tilemaps[0].pget((self.x + 8) // 8, (new_y + 6 + self.def_speed) // 8)  # Coin droit

        # Si l'une des tuiles en dessous est un obstacle (collide), il y a une collision
        return left_tile in self.pyxel_egal_caca.COLLIDERS or right_tile in self.pyxel_egal_caca.COLLIDERS or left_tile in self.pyxel_egal_caca.special_colliders or right_tile in self.pyxel_egal_caca.special_colliders
    

    def check_collision_right(self, new_x : int) -> bool:
        """
        Vérifie s'il y a une collision à droite du joueur pour le déplacement horizontal.
        --------------
        new_x : position x du zoiseaux
        """
        top_tile = pyxel.tilemaps[0].pget((new_x + 6 + self.def_speed) // 8, self.y // 8)  # Coin supérieur droit
        bottom_tile = pyxel.tilemaps[0].pget((new_x + 6 + self.def_speed) // 8, (self.y + 7) // 8)  # Coin inférieur droit

        # Si l'une des tuiles à droite est un obstacle (collide), il y a une collision
        return top_tile not in self.pyxel_egal_caca.COLLIDERS and bottom_tile not in self.pyxel_egal_caca.COLLIDERS


    def check_collision_left(self, new_x : int) -> bool:
        """
        Vérifie s'il y a une collision à gauche du joueur pour le déplacement horizontal.
        --------------
        new_x : position x du zoiseaux
        """
        top_tile = pyxel.tilemaps[0].pget((new_x + 2 - self.def_speed) // 8, self.y // 8)  # Coin supérieur gauche
        bottom_tile = pyxel.tilemaps[0].pget((new_x + 2 - self.def_speed) // 8, (self.y + 7) // 8)  # Coin inférieur gauche
        # Si l'une des tuiles à gauche est un obstacle (collide), il y a une collision
        return top_tile not in self.pyxel_egal_caca.COLLIDERS and bottom_tile not in self.pyxel_egal_caca.COLLIDERS
    
    
    def check_collision_above(self, new_y : int | float) -> bool:
        """
        Vérifie s'il y a une collision au-dessus du joueur en fonction de sa nouvelle position `new_y`.
        --------------
        new_y : position y du zoiseaux
        """
        # On vérifie à deux points : au-dessus du coin gauche et au-dessus du coin droit du joueur
        left_tile = pyxel.tilemaps[0].pget(self.x // 8, (new_y + 1 - self.def_speed) // 8)  # Coin gauche
        right_tile = pyxel.tilemaps[0].pget((self.x + 7) // 8, (new_y + 1 - self.def_speed) // 8)  # Coin droit

        # Si l'une des tuiles au-dessus est un obstacle (collide), il y a une collision
        return left_tile in self.pyxel_egal_caca.COLLIDERS or right_tile in self.pyxel_egal_caca.COLLIDERS
    

    def check_items_collision(self) -> None:
        tile_x = self.x // 8
        tile_y = self.y // 8

        tile = pyxel.tilemaps[0].pget(tile_x, tile_y)

        if tile == (1, 1):
            pyxel.tilemaps[0].pset(tile_x, tile_y, (0, 0))
            self.pyxel_egal_caca.red_orb += 1


    def set_stele(self) -> None:
        self.stele.place_red(self.x, self.y)


    def draw_particles(self) -> None:
        for particle in self.particles:
            if particle.type == "gauge":
                # Draw gauge particles relative to screen
                screen_x = particle.x
                screen_y = particle.y
            else:
                # Draw bird particles relative to world
                screen_x = particle.x - self.pyxel_egal_caca.camera_x
                screen_y = particle.y - self.pyxel_egal_caca.camera_y
            pyxel.pset(screen_x, screen_y, particle.color)


    def reset(self) -> None:
        self.x = 0
        self.y = 0
        self.direction = "droite"
        self.velocity_y = 0
        self.bugs_bunny = 0
        self.frame = 0
        self.tp_charge = 0
        self.is_charging = False
        self.particles = []
        self.teleport_jauge = 0
        self.waiting = 0


    def get_pos(self) -> tuple[int, int | float] :
        """
        Méthode qui permet de récupérer les coordonnées de l'oiseau rouge
        """
        return (self.x, self.y)
    

    def goto(self, tuple_x_y) -> None:
        self.x = tuple_x_y[0]
        self.y = tuple_x_y[1]
        self.teleport_jauge = 0
        self.pyxel_egal_caca.x = tuple_x_y[0]
        self.pyxel_egal_caca.y = tuple_x_y[1]
        self.pyxel_egal_caca.update_camera()


    def to_dict(self) -> str:
        """
        Méthode qui permet d'ajouter la classe de l'oiseau pour la sauvegarde
        """
        return "Bird2"




class Bird3:
    def __init__(self, app, stele):
        self.x = 0
        self.y = 0
        self.direction = "droite"
        self.velocity_y = 0
        self.bugs_bunny = 0
        self.max_jumps = 1
        self.gravity = 0.1
        self.jump_strength = -2
        self.frame = 0
        self.pyxel_egal_caca = app
        self.def_speed = 2
        self.flight_gauge = 100
        self.max_flight_gauge = 100
        self.tp_charge = 0
        self.tp_max_charge = 104
        self.is_charging = False
        self.particles = []
        self.particles_teleport = []
        self.stele = stele
        self.teleport_jauge = 0
        self.teleport_jauge_max = 104
        self.waiting = 0
        self.waiting_particles = 0


    def right(self) -> None:
        new_x = self.x + self.def_speed
        if self.check_collision_right(new_x):
            self.x = min(new_x, self.pyxel_egal_caca.map_width - 17)
            self.pyxel_egal_caca.update_camera()


    def left(self) -> None:
        new_x = self.x - self.def_speed
        if self.check_collision_left(new_x):
            self.x = max(1, self.x - self.def_speed)
            self.pyxel_egal_caca.update_camera()


    def jump(self) -> None:
        if self.bugs_bunny < self.max_jumps:
            self.velocity_y = self.jump_strength
            self.bugs_bunny += 1


    def update(self) -> None:
        if pyxel.btn(pyxel.KEY_SPACE) and self.flight_gauge > 0:
            self.velocity_y = -1
            self.flight_gauge = max(0, self.flight_gauge - 1)
            # Add blue particles during flight
            if random.random() < 0.4:
                self.particles.append(Particle(
                    self.x + random.randint(0, 8),
                    self.y + random.randint(4, 8),
                    "bird"
                ))
            if pyxel.btn(pyxel.KEY_RIGHT):
                self.right()
                self.direction = "droite"
            if pyxel.btn(pyxel.KEY_LEFT):
                self.left()
                self.direction = "gauche"
        else:
            self.velocity_y += self.gravity
            if self.waiting >= 20 and not pyxel.btn(pyxel.KEY_SPACE):
                self.flight_gauge = min(self.flight_gauge + 1, self.max_flight_gauge)
                self.waiting = 0
            else:
                self.waiting += 1

        # Update particles
        for particle in self.particles[:]:
            particle.x += particle.vx
            particle.y += particle.vy
            particle.life -= 1
            if particle.life <= 0:
                self.particles.remove(particle)

        new_y = self.y + self.velocity_y

        if self.check_collision_below(new_y):
            self.y = (new_y // 8) * 8
            self.velocity_y = 0
            self.bugs_bunny = 0
        else:
            if not self.check_collision_above(new_y):
                self.y = new_y


        if self.velocity_y > 4:
            self.velocity_y = 4

        if pyxel.btn(pyxel.KEY_T):
            if self.teleport_jauge == self.teleport_jauge_max:
                self.is_charging = True
                self.tp_charge = min(self.tp_charge + 2, self.tp_max_charge)
                # Gauge particles
                if random.random() < 0.3:
                    charge_x = self.pyxel_egal_caca.SCREEN_WIDTH - 59 + int((self.tp_charge / self.tp_max_charge) * 48)
                    self.particles_teleport.append(Particle(charge_x, 50, "gauge"))
                # Bird particles while charging
                if random.random() < 0.4:
                    self.particles_teleport.append(Particle(
                        self.x + random.randint(0, 8),
                        self.y + random.randint(0, 8),
                        "bird"
                    ))
            
            else:
                if self.is_charging and self.tp_charge >= self.tp_max_charge:
                    self.goto(self.stele.tp_green())
                self.is_charging = False
                self.tp_charge = max(0, self.tp_charge - 1)
                if self.waiting_particles >= 20:
                    self.teleport_jauge = min(self.teleport_jauge + 1, 104)
                    self.waiting_particles = 0
                else:
                    self.waiting_particles += 1

        else:
            if self.is_charging and self.tp_charge >= self.tp_max_charge:
                self.goto(self.stele.tp_green())
            self.is_charging = False
            self.tp_charge = max(0, self.tp_charge - 1)
            if self.waiting_particles >= 2:
                self.teleport_jauge = min(self.teleport_jauge + 1, 104)
                self.waiting_particles = 0
            else:
                self.waiting_particles += 1

        # Update particles
        for particle in self.particles_teleport[:]:
            if particle.type == "bird":
                particle.vy += 0.1  # Add gravity to bird particles
            particle.x += particle.vx
            particle.y += particle.vy
            particle.life -= 1
            if particle.life <= 0:
                self.particles_teleport.remove(particle)

        self.check_items_collision()


    def draw(self) -> None:
        if self.direction == "droite":
            pyxel.blt(self.x, self.y, 0, 8 * self.frame, 24, 8, 8, 2)
        else:
            pyxel.blt(self.x, self.y, 0, 8 * self.frame, 24, -8, 8, 2)


    def check_collision_below(self, new_y : int | float) -> bool :
        """
        Vérifie s'il y a une collision sous le joueur en fonction de sa nouvelle position `new_y`.
        --------------
        new_y : position y du zoiseaux
        """
        left_tile = pyxel.tilemaps[0].pget(self.x // 8, (new_y + 6 + self.def_speed) // 8)
        right_tile = pyxel.tilemaps[0].pget((self.x + 8) // 8, (new_y + 6 + self.def_speed) // 8)
        return left_tile in self.pyxel_egal_caca.COLLIDERS or right_tile in self.pyxel_egal_caca.COLLIDERS or left_tile in self.pyxel_egal_caca.special_colliders or right_tile in self.pyxel_egal_caca.special_colliders


    def check_collision_right(self, new_x : int) -> bool:
        """
        Vérifie s'il y a une collision à droite du joueur pour le déplacement horizontal.
        --------------
        new_x : position x du zoiseaux
        """
        top_tile = pyxel.tilemaps[0].pget((new_x + 6 + self.def_speed) // 8, self.y // 8)
        bottom_tile = pyxel.tilemaps[0].pget((new_x + 6 + self.def_speed) // 8, (self.y + 7) // 8)
        return top_tile not in self.pyxel_egal_caca.COLLIDERS and bottom_tile not in self.pyxel_egal_caca.COLLIDERS


    def check_collision_left(self, new_x : int) -> bool:
        """
        Vérifie s'il y a une collision à gauche du joueur pour le déplacement horizontal.
        --------------
        new_x : position x du zoiseaux
        """
        top_tile = pyxel.tilemaps[0].pget((new_x + 2 - self.def_speed) // 8, self.y // 8)
        bottom_tile = pyxel.tilemaps[0].pget((new_x + 2 - self.def_speed) // 8, (self.y + 7) // 8)
        return top_tile not in self.pyxel_egal_caca.COLLIDERS and bottom_tile not in self.pyxel_egal_caca.COLLIDERS


    def check_collision_above(self, new_y : int | float) -> bool:
        """
        Vérifie s'il y a une collision au-dessus du joueur en fonction de sa nouvelle position `new_y`.
        --------------
        new_y : position y du zoiseaux
        """
        left_tile = pyxel.tilemaps[0].pget(self.x // 8, (new_y + 1 - self.def_speed) // 8)
        right_tile = pyxel.tilemaps[0].pget((self.x + 7) // 8, (new_y + 1 - self.def_speed) // 8)
        return left_tile in self.pyxel_egal_caca.COLLIDERS or right_tile in self.pyxel_egal_caca.COLLIDERS


    def reset(self) -> None:
        self.x = 0
        self.y = 0
        self.direction = "droite"
        self.velocity_y = 0
        self.bugs_bunny = 0
        self.frame = 0
        self.flight_gauge = 100
        self.tp_charge = 0
        self.is_charging = False
        self.particles = []
        self.particles_teleport = []
        self.teleport_jauge = 0
        self.waiting = 0
        self.waiting_particles = 0


    def get_pos(self) -> tuple[int, int | float]:
        """
        Méthode qui permet de récupérer les coordonnées de l'oiseau vert
        """
        return (self.x, self.y)


    def goto(self, tuple_x_y) -> None:
        self.x = tuple_x_y[0]
        self.y = tuple_x_y[1]
        self.teleport_jauge = 0
        self.pyxel_egal_caca.x = tuple_x_y[0]
        self.pyxel_egal_caca.y = tuple_x_y[1]
        self.pyxel_egal_caca.update_camera()


    def check_items_collision(self) -> None:
        tile_x = self.x // 8
        tile_y = self.y // 8

        tile = pyxel.tilemaps[0].pget(tile_x, tile_y)

        if tile == (2, 1):
            pyxel.tilemaps[0].pset(tile_x, tile_y, (0, 0))
            self.pyxel_egal_caca.green_orb += 1
            self.pyxel_egal_caca.items_green.append((tile_x, tile_y))


    def draw_particles(self) -> None:
        """
        Méthode qui permet de dessiner les particules
        """
        for particle in self.particles:
            screen_x = particle.x - self.pyxel_egal_caca.camera_x
            screen_y = particle.y - self.pyxel_egal_caca.camera_y
            pyxel.pset(screen_x, screen_y, particle.color)

        for particle in self.particles_teleport:
            if particle.type == "gauge":
                # Draw gauge particles relative to screen
                screen_x = particle.x
                screen_y = particle.y
            else:
                # Draw bird particles relative to world
                screen_x = particle.x - self.pyxel_egal_caca.camera_x
                screen_y = particle.y - self.pyxel_egal_caca.camera_y
            pyxel.pset(screen_x, screen_y, particle.color)


    def to_dict(self) -> str:
        """
        Méthode qui permet d'ajouter la classe de l'oiseau pour la sauvegarde
        """
        return "Bird3"




class Stele:
    """
    Classe pour la gestion des stèles des oiseaux
    """
    def __init__(self) -> None:
        self.blue_x = 3 * 8
        self.blue_y = 14 * 8
        self.red_x = 22 * 8
        self.red_y = 32
        self.green_x = 114 * 8
        self.green_y = 8
    

    def blue(self) -> None:
        pyxel.blt(self.blue_x, self.blue_y, 0, 0, 72, 8, 8, pyxel.COLOR_PURPLE)


    def red(self) -> None:
        pyxel.blt(self.red_x, self.red_y, 0, 8, 64, 8, 8, pyxel.COLOR_PURPLE)


    def green(self) -> None:
        pyxel.blt(self.green_x, self.green_y, 0, 0, 64, 8, 8, pyxel.COLOR_PURPLE)


    def place_blue(self, x, y) -> None:
        self.blue_x = x
        self.blue_y = y


    def place_green(self, x, y) -> None:
        self.green_x = x
        self.green_y = y
    

    def place_red(self, x, y) -> None:
        self.red_x = x
        self.red_y = y


    def tp_blue(self) -> tuple[int, int | float] :
        """
        Méthode qui permet de récupérer les coordonnées de la stèle bleue
        """
        return self.blue_x, self.blue_y
    

    def tp_red(self) -> tuple[int, int | float] :
        """
        Méthode qui permet de récupérer les coordonnées de la stèle rouge
        """
        return self.red_x, self.red_y


    def tp_green(self) -> tuple[int, int | float] :
        """
        Méthode qui permet de récupérer les coordonnées de la stèle verte
        """
        return self.green_x, self.green_y


    def reset(self) -> None:
        """
        Méthode qui réinitialise les attributs de la classe
        """
        self.blue_x = 3 * 8
        self.blue_y = 14 * 8
        self.red_x = 22 * 8
        self.red_y = 32
        self.green_x = 114 * 8
        self.green_y = 8


    def get_stele(self) -> tuple[tuple[int, int | float], tuple[int, int | float], tuple[int, int | float]] :
        """
        Méthode qui permet de récupérer les coordonnées des stèles
        """
        return (self.blue_x, self.blue_y), (self.red_x, self.red_y), (self.green_x, self.green_y)




class Tombe:
    """
    Classe pour la gestion de la tombe
    """
    def __init__(self, app) -> None:
        """
        Constructeur de la classe
        -------------
        app : instance de la classe App
        """
        self.x = 32
        self.y = 47 * 8
        self.width = 8
        self.height = 8
        self.pyxel_egal_caca = app
        self.phrases_hommage = [
                                "Je ne sais pas combien de temps je vais devoir rester ici pour veiller sur cette porte.",
                                "Cette tombe est tout ce qui me reste de mes freres et soeurs...",
                                "Elle risque de blesser mes freres et soeurs si je ne la garde pas.",
                                "Se souvenir, c’est donner un sens à ce que nous avons vecu, merci pour cela.",
                                "Je veille sur ce lieu pour que d'autres n'oublient pas notre histoire.",
                                "Il est parfois difficile de rester ici seul, mais ton hommage me reconforte.",
                                "Chaque hommage me rappelle que je ne suis pas totalement oublie. Mais tout hommage m'eloigne d'eux...",
                                "Rester ici, entre le passe et l’oubli, est moins pesant grâce à toi... Mais je me demande ce qu'ils font ?...",
                                "Je suis la pour proteger, meme si cela signifie rester fige ici pour toujours. (aidez moi a partir...)",
                                "Ton hommage redonne de la vie a notre memoire, merci.",
                                "Je suis le gardien de ce passage, pour que d’autres puissent avancer en paix. (mais je n'arrive plus a tenir)",
                                "Mon existence ici a plus de sens quand on vient me voir. (mais a-t-elle deja eu un sens ? pourquoi je suis comme ça ? je ne suis pas bien...)",
                                "Merci de respecter ce lieu sacre, tout le monde ne le fait pas.",
                                "Restez prudents, je veille ici pour que rien de mal ne survienne. (je peux pas dire que je vais lâcher)",
                                "Ce n'est pas facile de proteger cet endroit, mais ta presence aide. (sans penser a cette autre presence)",
                                "Je veille pour que la tranquillite regne ici, merci de me le rappeler.",
                                "Il n’y a rien de plus precieux que le souvenir que vous m'offrez. (je commence a tout oublier, est-ce donc ça l'au-dela ?...)",
                                "Parfois, la solitude est lourde ici, mais ton hommage adoucit cela. (je souhaite les rejoindre)"
                                ]
        self.frame = 0
        self.hauteur = 0
        self.message_timer = 100
        self.message = ""
        self.pos_rect = (0, 0)
        self.taille_rect = (0, 0)
        self.show_message = False
        self.portail = False
        self.travel_portail = False
        self.particles = []
        

    def check_collision_with_stele(self, bird) -> None:
        """
        Verifie la collision avec la tombe et empeche l'oiseau de passer au travers.
        -----------------
        bird : instance de la classe de l'oiseau actuel
        """
        # Vérifie la collision en fonction de la direction de l'oiseau
        if bird.x < self.x + self.width and bird.x + 8 > self.x and \
        bird.y < self.y + self.height and bird.y + 8 > self.y: # le \ sert à diviser la condition sinon le cobra comprendra que c'est deux instructions distrinctes. il ne se méfie pas assez
            if len(self.pyxel_egal_caca.hommage) != 3: 
                if bird.direction == "droite":
                    bird.x = self.x - 8
                elif bird.direction == "gauche":
                    bird.x = self.x + self.width

            else:
                bird.goto((91*8,14*8))
                self.travel_portail = True
                
        if bird.x >= 92*8 - 2 and bird.y <= 14*8 and self.travel_portail:
            bird.goto(self.pyxel_egal_caca.stele.tp_blue()) if bird == self.pyxel_egal_caca.blue_bird \
                                else bird.goto(self.pyxel_egal_caca.stele.tp_red()) if bird == self.pyxel_egal_caca.red_bird \
                                else bird.goto(self.pyxel_egal_caca.stele.tp_green())
    
    
    def check_homage(self, bird) -> None:
        """
        Vérifie si l'utilisateur appuie sur le 'h' et que l'oiseau est à proximité de la tombe.
        -----------------
        bird : instance de la classe de l'oiseau actuel
        """
        distance_x = abs(bird.x - self.x)
        distance_y = abs(bird.y - self.y)

        # Si l'oiseau est dans une zone de 45 pixels autour de la tombe et que 'h' est appuyé
        if distance_x <= 45 and distance_y <= 45 and pyxel.btnp(pyxel.KEY_H):
            if not bird.to_dict() in self.pyxel_egal_caca.hommage: 
                self.message_timer = 100 
                self.pos_rect = (40, 10)
                self.taille_rect = (190, 30)
                self.message = "Merci de m'avoir rendu hommage, je vais"
                self.message_2 = "bientot pouvoir partir en paix"
                self.show_message = True

            else :
                la_grosse_phrase = self.phrases_hommage[17]

                self.message_timer = 100 
                self.pos_rect = (30, 10)
                self.taille_rect = (200, 30)
                self.message = "Tu m'as deja rendu hommage, merci quand meme."

                if la_grosse_phrase == self.phrases_hommage[0]:
                    self.message_2 = "Je ne sais pas combien de temps je vais devoir rester ici"
                    self.message_3 = "pour veiller sur cette porte."
                    self.pos_rect3 = (60, 140)
                    self.show_message = True
                    self.message_timer = 160
                elif la_grosse_phrase == self.phrases_hommage[1]:
                    self.message_2 = "Cette tombe est tout ce qui me reste de mes freres et"
                    self.message_3 = "soeurs..."
                    self.pos_rect3 = (100, 60)
                    self.show_message = True
                    self.message_timer = 160
                elif la_grosse_phrase == self.phrases_hommage[2]:
                    self.message_2 = "Elle risque de blesser mes freres et soeurs si je ne la "
                    self.message_3 = "garde pas."
                    self.pos_rect3 = (100, 60)
                    self.show_message = True
                    self.message_timer = 160
                elif la_grosse_phrase == self.phrases_hommage[3]:
                    self.message_2 = "Se souvenir, c’est donner un sens à ce que nous avons vecu,"
                    self.message_3 = "merci pour cela."
                    self.pos_rect3 = (90, 80)
                    self.show_message = True
                    self.message_timer = 160
                elif la_grosse_phrase == self.phrases_hommage[4]:
                    self.message_2 = "Je veille sur ce lieu pour que d'autres n'oublient pas notre "
                    self.message_3 = "histoire."
                    self.pos_rect3 = (100, 60)
                    self.show_message = True
                    self.message_timer = 160
                elif la_grosse_phrase == self.phrases_hommage[5]:
                    self.message_2 = "Il est parfois difficile de rester ici seul, mais ton hommage "
                    self.message_3 = "me reconforte."
                    self.pos_rect3 = (90, 80)
                    self.show_message = True
                    self.message_timer = 160
                elif la_grosse_phrase == self.phrases_hommage[6]:
                    self.message_2 = "Chaque hommage me rappelle que je ne suis pas totalement oublie."
                    self.message_3 = "Mais tout hommage m'eloigne d'eux..."
                    self.pos_rect3 = (45, 155)
                    self.show_message = True
                    self.message_timer = 160
                elif la_grosse_phrase == self.phrases_hommage[7]:
                    self.message_2 = "Rester ici, entre le passe et l’oubli, est moins pesant grace"
                    self.message_3 = "à toi... Mais je me demande ce qu'ils font ?..."
                    self.pos_rect3 = (15, 205)
                    self.show_message = True
                    self.message_timer = 160
                elif la_grosse_phrase == self.phrases_hommage[8]:
                    self.message_2 = "Je suis la pour proteger, meme si cela signifie rester fige  "
                    self.message_3 = "ici pour toujours. (aidez moi a partir...)"
                    self.pos_rect3 = (30, 185)
                    self.show_message = True
                    self.message_timer = 160
                elif la_grosse_phrase == self.phrases_hommage[9]:
                    self.message_2 = "   Ton hommage redonne de la vie a notre memoire, merci."
                    self.show_message = True
                    self.message_timer = 160
                elif la_grosse_phrase == self.phrases_hommage[10]:
                    self.message_2 = "la_grosse_phrase"
                    self.message_3 = "garde pas."
                    self.pos_rect3 = (100, 60)
                    self.show_message = True
                    self.message_timer = 160
                elif la_grosse_phrase == self.phrases_hommage[11]:
                    self.message_2 = "la_grosse_phrase"
                    self.message_3 = "garde pas."
                    self.pos_rect3 = (100, 60)
                    self.show_message = True
                    self.message_timer = 160
                elif la_grosse_phrase == self.phrases_hommage[12]:
                    self.message_2 = "la_grosse_phrase"
                    self.message_3 = "garde pas."
                    self.pos_rect3 = (100, 60)
                    self.show_message = True
                    self.message_timer = 160
                elif la_grosse_phrase == self.phrases_hommage[13]:
                    self.message_2 = "la_grosse_phrase"
                    self.message_3 = "garde pas."
                    self.pos_rect3 = (100, 60)
                    self.show_message = True
                    self.message_timer = 160
                elif la_grosse_phrase == self.phrases_hommage[14]:
                    self.message_2 = "la_grosse_phrase"
                    self.message_3 = "garde pas."
                    self.pos_rect3 = (100, 60)
                    self.show_message = True
                    self.message_timer = 160
                elif la_grosse_phrase == self.phrases_hommage[15]:
                    self.message_2 = "la_grosse_phrase"
                    self.message_3 = "garde pas."
                    self.pos_rect3 = (100, 60)
                    self.show_message = True
                    self.message_timer = 160
                elif la_grosse_phrase == self.phrases_hommage[16]:
                    self.message_2 = "la_grosse_phrase"
                    self.message_3 = "garde pas."
                    self.pos_rect3 = (100, 60)
                    self.show_message = True
                    self.message_timer = 160
                elif la_grosse_phrase == self.phrases_hommage[17]:
                    self.message_2 = "Parfois, la solitude est lourde ici, mais ton hommage adoucit cela. (je souhaite les rejoindre)"
                    self.message_3 = "adoucit cela. (je souhaite les rejoindre) pas."
                    self.pos_rect3 = (20, 200)
                    self.show_message = True
                    self.message_timer = 160


    def check_bird(self) -> None:
        """
        Vérifie si tout les oiseaux ont rendu hommage au défunt oiseau
        """
        if len(self.pyxel_egal_caca.hommage) != 3:
            pyxel.blt(4*8, 41*8 + self.hauteur * 2, 0, self.frame * 8 + 16, 64, 8, 8, pyxel.COLOR_PURPLE)
        if len(self.pyxel_egal_caca.hommage) == 3 and not self.portail:
            pyxel.tilemaps[0].pset(4, 47, (3, 9))
            self.portail = True
        
        if self.portail:
            if random.random() < 0.3:
                self.particles.append(Particle(
                    4*8 + random.randint(0, 8),
                    47*8 + random.randint(0, 8),
                    "portal"
                ))
        
        for particle in self.particles[:]:
            particle.x += particle.vx
            particle.y += particle.vy
            particle.life -= 1
            if particle.life <= 0:
                self.particles.remove(particle)       
        

    def draw_particles(self) -> None:
        """
        Dessine les particules du portail
        """
        if self.portail:
            for particle in self.particles:
                screen_x = particle.x - self.pyxel_egal_caca.camera_x
                screen_y = particle.y - self.pyxel_egal_caca.camera_y
                pyxel.pset(screen_x, screen_y, random.choice([2, 8]))


        


    def reset(self) -> None:
        """
        Méthode qui réinitialise les attributs de la classe
        """
        self.frame = 0
        self.hauteur = 0
        self.message_timer = 100
        self.message = ""
        self.show_message = False
        self.portail = False
        self.travel_portail = False
        self.particles = []


 

class End:
    """
    Classe pour la gestion de la fin du jeu
    """
    
    def __init__(self, app) -> None:
        """
        Constructeur de la classe
        -------------
        app : instance de la classe App
        """
        self.blue = 13
        self.red = 21
        self.green = 29
        self.pyxel_egal_caca = app
        self.bx = 247 * 8
        self.by = 13 * 8
        self.rx = 242 * 8
        self.ry = 56    
        self.gx = 252 * 8
        self.gy = 72
        self.message_timer = 100
        self.message = ""
        self.pos_rect = (0, 0)
        self.taille_rect = (0, 0)
        self.show_message = False


    def detect(self, blue, red, green, blue_bird, red_bird, green_bird, stele) -> None:
        """
        Fonction qui détecte si l'utilisateur a bien récuperé toutes les orbes, 
        mis les oiseaux et les steles au bon endroit
        -------------------------
        blue : Nombre d'orbes bleues
        red : Nombre d'orbes rouges
        green : Nombre d'orbes vertes
        blue_bird : Instance de la classe Bird1
        red_bird : Instance de la classe Bird2
        green_bird : Instance de la classe Bird3
        stele : Instance de la classe Stele
        """
        if blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] == self.bx \
        and blue_bird.get_pos()[1] == self.by and red_bird.get_pos()[0] == self.rx and red_bird.get_pos()[1] == self.ry \
        and green_bird.get_pos()[0] == self.gx and green_bird.get_pos()[1] == self.gy and stele.get_stele()[0][0] == self.bx \
        and stele.get_stele()[0][1] == self.by and stele.get_stele()[1][0] == self.rx and stele.get_stele()[1][1] == self.ry \
        and stele.get_stele()[2][0] == self.gx and stele.get_stele()[2][1] == self.gy:
            
            self.pyxel_egal_caca.mode = "win"
            self.pyxel_egal_caca.reset()

        elif blue != self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] == self.bx \
        and blue_bird.get_pos()[1] == self.by and red_bird.get_pos()[0] == self.rx and red_bird.get_pos()[1] == self.ry \
        and green_bird.get_pos()[0] == self.gx and green_bird.get_pos()[1] == self.gy and stele.get_stele()[0][0] == self.bx \
        and stele.get_stele()[0][1] == self.by and stele.get_stele()[1][0] == self.rx and stele.get_stele()[1][1] == self.ry \
        and stele.get_stele()[2][0] == self.gx and stele.get_stele()[2][1] == self.gy:
            
            self.message_timer = 100 
            self.pos_rect = (40, 10)
            self.taille_rect = (190, 30)
            self.message = f"Tu as oublie une orbe bleue ! Mefies-toi !!" if self.blue - blue == 1 else f"Tu as oublie {self.blue-blue} orbes bleues ! Mefies-toi !!"
            self.show_message = True


        elif blue == self.blue and red != self.red and green == self.green and blue_bird.get_pos()[0] == self.bx \
        and blue_bird.get_pos()[1] == self.by and red_bird.get_pos()[0] == self.rx and red_bird.get_pos()[1] == self.ry \
        and green_bird.get_pos()[0] == self.gx and green_bird.get_pos()[1] == self.gy and stele.get_stele()[0][0] == self.bx \
        and stele.get_stele()[0][1] == self.by and stele.get_stele()[1][0] == self.rx and stele.get_stele()[1][1] == self.ry \
        and stele.get_stele()[2][0] == self.gx and stele.get_stele()[2][1] == self.gy:
            
            self.message_timer = 100 
            self.pos_rect = (40, 10)
            self.taille_rect = (190, 30)
            self.message = f"Tu as oublie une orbe rouge ! Mefies-toi !!" if self.red - red == 1 else f"Tu as oublie {self.red-red} orbes rouges ! Mefies-toi !!"
            self.show_message = True


        elif blue == self.blue and red == self.red and green != self.green and blue_bird.get_pos()[0] == self.bx \
        and blue_bird.get_pos()[1] == self.by and red_bird.get_pos()[0] == self.rx and red_bird.get_pos()[1] == self.ry \
        and green_bird.get_pos()[0] == self.gx and green_bird.get_pos()[1] == self.gy and stele.get_stele()[0][0] == self.bx \
        and stele.get_stele()[0][1] == self.by and stele.get_stele()[1][0] == self.rx and stele.get_stele()[1][1] == self.ry \
        and stele.get_stele()[2][0] == self.gx and stele.get_stele()[2][1] == self.gy:
            
            self.message_timer = 100 
            self.pos_rect = (40, 10)
            self.taille_rect = (190, 30)
            self.message = f"Tu as oublie une orbe verte ! Mefies-toi !!" if self.green - green == 1 else f"Tu as oublie {self.green-green} orbes vertes ! Mefies-toi !!"
            self.show_message = True


        elif blue != self.blue and red != self.red and green == self.green and blue_bird.get_pos()[0] == self.bx \
        and blue_bird.get_pos()[1] == self.by and red_bird.get_pos()[0] == self.rx and red_bird.get_pos()[1] == self.ry \
        and green_bird.get_pos()[0] == self.gx and green_bird.get_pos()[1] == self.gy and stele.get_stele()[0][0] == self.bx \
        and stele.get_stele()[0][1] == self.by and stele.get_stele()[1][0] == self.rx and stele.get_stele()[1][1] == self.ry \
        and stele.get_stele()[2][0] == self.gx and stele.get_stele()[2][1] == self.gy:
            
            self.message_timer = 100 
            self.pos_rect = (25, 10)
            self.taille_rect = (210,30)
            self.message = f"Tu as oublie une orbe bleue et une orbe rouge !" if self.blue - blue == 1 and self.red - red == 1 else \
                f"Tu as oublie {self.blue-blue} orbes bleues et une orbe rouge !" if self.blue - blue != 1 and self.red - red == 1 else \
                f"Tu as oublie une orbe bleue et {self.red-red} orbes rouges !" if self.blue - blue == 1 and self.red - red != 1 else \
                f"Tu as oublie {self.blue-blue} orbes bleues et {self.red-red} orbes rouges !"
            self.show_message = True


        elif blue != self.blue and red == self.red and green != self.green and blue_bird.get_pos()[0] == self.bx \
        and blue_bird.get_pos()[1] == self.by and red_bird.get_pos()[0] == self.rx and red_bird.get_pos()[1] == self.ry \
        and green_bird.get_pos()[0] == self.gx and green_bird.get_pos()[1] == self.gy and stele.get_stele()[0][0] == self.bx \
        and stele.get_stele()[0][1] == self.by and stele.get_stele()[1][0] == self.rx and stele.get_stele()[1][1] == self.ry \
        and stele.get_stele()[2][0] == self.gx and stele.get_stele()[2][1] == self.gy:
            
            self.message_timer = 100 
            self.pos_rect = (25, 10)
            self.taille_rect = (210,30)
            self.message = f"Tu as oublie une orbe bleue et une orbe verte !" if self.blue - blue == 1 and self.green - green == 1 else \
                f"Tu as oublie {self.blue-blue} orbes bleues et une orbe verte !" if self.blue - blue != 1 and self.green - green == 1 else \
                f"Tu as oublie une orbe bleue et {self.green-green} orbes vertes !" if self.blue - blue == 1 and self.green - green != 1 else \
                f"Tu as oublie {self.blue-blue} orbes bleues et {self.green-green} orbes vertes !"
            self.show_message = True


        elif blue == self.blue and red != self.red and green != self.green and blue_bird.get_pos()[0] == self.bx \
        and blue_bird.get_pos()[1] == self.by and red_bird.get_pos()[0] == self.rx and red_bird.get_pos()[1] == self.ry \
        and green_bird.get_pos()[0] == self.gx and green_bird.get_pos()[1] == self.gy and stele.get_stele()[0][0] == self.bx \
        and stele.get_stele()[0][1] == self.by and stele.get_stele()[1][0] == self.rx and stele.get_stele()[1][1] == self.ry \
        and stele.get_stele()[2][0] == self.gx and stele.get_stele()[2][1] == self.gy:
            
            self.message_timer = 100 
            self.pos_rect = (25, 10)
            self.taille_rect = (210,30)
            self.message = f"Tu as oublie une orbe rouge et une orbe verte !" if self.red - red == 1 and self.green - green == 1 else \
                f"Tu as oublie {self.red-red} orbes rouges et une orbe verte !" if self.red - red != 1 and self.green - green == 1 else \
                f"Tu as oublie une orbe rouge et {self.green-green} orbes vertes !" if self.red - red == 1 and self.green - green != 1 else \
                f"Tu as oublie {self.red-red} orbes rouges et {self.green-green} orbes vertes !"
            self.show_message = True

        
        elif blue != self.blue and red != self.red and green != self.green and blue_bird.get_pos()[0] == self.bx \
        and blue_bird.get_pos()[1] == self.by and red_bird.get_pos()[0] == self.rx and red_bird.get_pos()[1] == self.ry \
        and green_bird.get_pos()[0] == self.gx and green_bird.get_pos()[1] == self.gy and stele.get_stele()[0][0] == self.bx \
        and stele.get_stele()[0][1] == self.by and stele.get_stele()[1][0] == self.rx and stele.get_stele()[1][1] == self.ry \
        and stele.get_stele()[2][0] == self.gx and stele.get_stele()[2][1] == self.gy:
            
            self.message_timer = 100 
            self.pos_rect = (30, 10)
            self.taille_rect = (200,30)
            self.message = f"Tu as oublie une orbe bleue, une orbe rouge" if self.blue - blue == 1 and self.red - red == 1 and self.green - green == 1 else \
                f"Tu as oublie {self.blue-blue} orbes bleues, une orbe rouge" if self.blue - blue != 1 and self.red - red == 1 and self.green - green == 1 else \
                f"Tu as oublie une orbe bleue, {self.red-red} orbes rouges" if self.blue - blue == 1 and self.red - red != 1 and self.green - green == 1 else \
                f"Tu as oublie une orbe bleue, une orbe rouge" if self.blue - blue == 1 and self.red - red == 1 and self.green - green != 1 else \
                f"Tu as oublie {self.blue-blue} orbes bleues, {self.red-red} orbes rouges"
            self.message_2 = f"et une orbe verte !" if self.blue - blue == 1 and self.red - red == 1 and self.green - green == 1 else \
                f"et une orbe verte !" if self.blue - blue != 1 and self.red - red == 1 and self.green - green == 1 else \
                f"et une orbe verte !" if self.blue - blue == 1 and self.red - red != 1 and self.green - green == 1 else \
                f"{self.green-green} orbes vertes !" if self.blue - blue == 1 and self.red - red == 1 and self.green - green != 1 else \
                f"et {self.green-green} orbes vertes !"
            self.show_message = True

        

        elif blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] != self.bx \
        and blue_bird.get_pos()[1] != self.by and red_bird.get_pos()[0] == self.rx and red_bird.get_pos()[1] == self.ry \
        and green_bird.get_pos()[0] == self.gx and green_bird.get_pos()[1] == self.gy and stele.get_stele()[0][0] == self.bx \
        and stele.get_stele()[0][1] == self.by and stele.get_stele()[1][0] == self.rx and stele.get_stele()[1][1] == self.ry \
        and stele.get_stele()[2][0] == self.gx and stele.get_stele()[2][1] == self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] != self.bx \
        and blue_bird.get_pos()[1] == self.by and red_bird.get_pos()[0] == self.rx and red_bird.get_pos()[1] == self.ry \
        and green_bird.get_pos()[0] == self.gx and green_bird.get_pos()[1] == self.gy and stele.get_stele()[0][0] == self.bx \
        and stele.get_stele()[0][1] == self.by and stele.get_stele()[1][0] == self.rx and stele.get_stele()[1][1] == self.ry \
        and stele.get_stele()[2][0] == self.gx and stele.get_stele()[2][1] == self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] == self.bx \
        and blue_bird.get_pos()[1] != self.by and red_bird.get_pos()[0] == self.rx and red_bird.get_pos()[1] == self.ry \
        and green_bird.get_pos()[0] == self.gx and green_bird.get_pos()[1] == self.gy and stele.get_stele()[0][0] == self.bx \
        and stele.get_stele()[0][1] == self.by and stele.get_stele()[1][0] == self.rx and stele.get_stele()[1][1] == self.ry \
        and stele.get_stele()[2][0] == self.gx and stele.get_stele()[2][1] == self.gy:
            
            self.message_timer = 100 
            self.pos_rect = (40, 10)
            self.taille_rect = (190, 30)
            self.message = f"L'oiseau bleu est mal placee ! Mefies-toi !!"
            self.show_message = True


        elif blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] == self.bx \
        and blue_bird.get_pos()[1] == self.by and red_bird.get_pos()[0] != self.rx and red_bird.get_pos()[1] != self.ry \
        and green_bird.get_pos()[0] == self.gx and green_bird.get_pos()[1] == self.gy and stele.get_stele()[0][0] == self.bx \
        and stele.get_stele()[0][1] == self.by and stele.get_stele()[1][0] == self.rx and stele.get_stele()[1][1] == self.ry \
        and stele.get_stele()[2][0] == self.gx and stele.get_stele()[2][1] == self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] == self.bx \
        and blue_bird.get_pos()[1] == self.by and red_bird.get_pos()[0] != self.rx and red_bird.get_pos()[1] == self.ry \
        and green_bird.get_pos()[0] == self.gx and green_bird.get_pos()[1] == self.gy and stele.get_stele()[0][0] == self.bx \
        and stele.get_stele()[0][1] == self.by and stele.get_stele()[1][0] == self.rx and stele.get_stele()[1][1] == self.ry \
        and stele.get_stele()[2][0] == self.gx and stele.get_stele()[2][1] == self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] == self.bx \
        and blue_bird.get_pos()[1] == self.by and red_bird.get_pos()[0] == self.rx and red_bird.get_pos()[1] != self.ry \
        and green_bird.get_pos()[0] == self.gx and green_bird.get_pos()[1] == self.gy and stele.get_stele()[0][0] == self.bx \
        and stele.get_stele()[0][1] == self.by and stele.get_stele()[1][0] == self.rx and stele.get_stele()[1][1] == self.ry \
        and stele.get_stele()[2][0] == self.gx and stele.get_stele()[2][1] == self.gy:
            
            self.message_timer = 100 
            self.pos_rect = (40, 10)
            self.taille_rect = (190, 30)
            self.message = f"L'oiseau rouge est mal placee ! Mefies-toi !!"
            self.show_message = True

        
        elif blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] == self.bx \
        and blue_bird.get_pos()[1] == self.by and red_bird.get_pos()[0] == self.rx and red_bird.get_pos()[1] == self.ry \
        and green_bird.get_pos()[0] != self.gx and green_bird.get_pos()[1] != self.gy and stele.get_stele()[0][0] == self.bx \
        and stele.get_stele()[0][1] == self.by and stele.get_stele()[1][0] == self.rx and stele.get_stele()[1][1] == self.ry \
        and stele.get_stele()[2][0] == self.gx and stele.get_stele()[2][1] == self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] == self.bx \
        and blue_bird.get_pos()[1] == self.by and red_bird.get_pos()[0] == self.rx and red_bird.get_pos()[1] == self.ry \
        and green_bird.get_pos()[0] != self.gx and green_bird.get_pos()[1] == self.gy and stele.get_stele()[0][0] == self.bx \
        and stele.get_stele()[0][1] == self.by and stele.get_stele()[1][0] == self.rx and stele.get_stele()[1][1] == self.ry \
        and stele.get_stele()[2][0] == self.gx and stele.get_stele()[2][1] == self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] == self.bx \
        and blue_bird.get_pos()[1] == self.by and red_bird.get_pos()[0] == self.rx and red_bird.get_pos()[1] == self.ry \
        and green_bird.get_pos()[0] == self.gx and green_bird.get_pos()[1] != self.gy and stele.get_stele()[0][0] == self.bx \
        and stele.get_stele()[0][1] == self.by and stele.get_stele()[1][0] == self.rx and stele.get_stele()[1][1] == self.ry \
        and stele.get_stele()[2][0] == self.gx and stele.get_stele()[2][1] == self.gy:
            
            self.message_timer = 100 
            self.pos_rect = (40, 10)
            self.taille_rect = (190, 30)
            self.message = f"L'oiseau vert est mal placee ! Mefies-toi !!"
            self.show_message = True


        elif blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] != self.bx \
        and blue_bird.get_pos()[1] != self.by and red_bird.get_pos()[0] != self.rx and red_bird.get_pos()[1] != self.ry \
        and green_bird.get_pos()[0] == self.gx and green_bird.get_pos()[1] == self.gy and stele.get_stele()[0][0] == self.bx \
        and stele.get_stele()[0][1] == self.by and stele.get_stele()[1][0] == self.rx and stele.get_stele()[1][1] == self.ry \
        and stele.get_stele()[2][0] == self.gx and stele.get_stele()[2][1] == self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] != self.bx \
        and blue_bird.get_pos()[1] == self.by and red_bird.get_pos()[0] != self.rx and red_bird.get_pos()[1] == self.ry \
        and green_bird.get_pos()[0] == self.gx and green_bird.get_pos()[1] == self.gy and stele.get_stele()[0][0] == self.bx \
        and stele.get_stele()[0][1] == self.by and stele.get_stele()[1][0] == self.rx and stele.get_stele()[1][1] == self.ry \
        and stele.get_stele()[2][0] == self.gx and stele.get_stele()[2][1] == self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] == self.bx \
        and blue_bird.get_pos()[1] != self.by and red_bird.get_pos()[0] == self.rx and red_bird.get_pos()[1] != self.ry \
        and green_bird.get_pos()[0] == self.gx and green_bird.get_pos()[1] == self.gy and stele.get_stele()[0][0] == self.bx \
        and stele.get_stele()[0][1] == self.by and stele.get_stele()[1][0] == self.rx and stele.get_stele()[1][1] == self.ry \
        and stele.get_stele()[2][0] == self.gx and stele.get_stele()[2][1] == self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] == self.bx \
        and blue_bird.get_pos()[1] != self.by and red_bird.get_pos()[0] != self.rx and red_bird.get_pos()[1] == self.ry \
        and green_bird.get_pos()[0] == self.gx and green_bird.get_pos()[1] == self.gy and stele.get_stele()[0][0] == self.bx \
        and stele.get_stele()[0][1] == self.by and stele.get_stele()[1][0] == self.rx and stele.get_stele()[1][1] == self.ry \
        and stele.get_stele()[2][0] == self.gx and stele.get_stele()[2][1] == self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] != self.bx \
        and blue_bird.get_pos()[1] == self.by and red_bird.get_pos()[0] == self.rx and red_bird.get_pos()[1] != self.ry \
        and green_bird.get_pos()[0] == self.gx and green_bird.get_pos()[1] == self.gy and stele.get_stele()[0][0] == self.bx \
        and stele.get_stele()[0][1] == self.by and stele.get_stele()[1][0] == self.rx and stele.get_stele()[1][1] == self.ry \
        and stele.get_stele()[2][0] == self.gx and stele.get_stele()[2][1] == self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] != self.bx \
        and blue_bird.get_pos()[1] != self.by and red_bird.get_pos()[0] == self.rx and red_bird.get_pos()[1] != self.ry \
        and green_bird.get_pos()[0] == self.gx and green_bird.get_pos()[1] == self.gy and stele.get_stele()[0][0] == self.bx \
        and stele.get_stele()[0][1] == self.by and stele.get_stele()[1][0] == self.rx and stele.get_stele()[1][1] == self.ry \
        and stele.get_stele()[2][0] == self.gx and stele.get_stele()[2][1] == self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] != self.bx \
        and blue_bird.get_pos()[1] != self.by and red_bird.get_pos()[0] != self.rx and red_bird.get_pos()[1] == self.ry \
        and green_bird.get_pos()[0] == self.gx and green_bird.get_pos()[1] == self.gy and stele.get_stele()[0][0] == self.bx \
        and stele.get_stele()[0][1] == self.by and stele.get_stele()[1][0] == self.rx and stele.get_stele()[1][1] == self.ry \
        and stele.get_stele()[2][0] == self.gx and stele.get_stele()[2][1] == self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] != self.bx \
        and blue_bird.get_pos()[1] == self.by and red_bird.get_pos()[0] != self.rx and red_bird.get_pos()[1] != self.ry \
        and green_bird.get_pos()[0] == self.gx and green_bird.get_pos()[1] == self.gy and stele.get_stele()[0][0] == self.bx \
        and stele.get_stele()[0][1] == self.by and stele.get_stele()[1][0] == self.rx and stele.get_stele()[1][1] == self.ry \
        and stele.get_stele()[2][0] == self.gx and stele.get_stele()[2][1] == self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] == self.bx \
        and blue_bird.get_pos()[1] != self.by and red_bird.get_pos()[0] != self.rx and red_bird.get_pos()[1] != self.ry \
        and green_bird.get_pos()[0] == self.gx and green_bird.get_pos()[1] == self.gy and stele.get_stele()[0][0] == self.bx \
        and stele.get_stele()[0][1] == self.by and stele.get_stele()[1][0] == self.rx and stele.get_stele()[1][1] == self.ry \
        and stele.get_stele()[2][0] == self.gx and stele.get_stele()[2][1] == self.gy:
            
            self.message_timer = 100 
            self.pos_rect = (5, 10)
            self.taille_rect = (232, 30)
            self.message = f"L'oiseau bleu et rouge sont mal places ! Mefies-toi !!"
            self.show_message = True


        elif blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] == self.bx \
        and blue_bird.get_pos()[1] == self.by and red_bird.get_pos()[0] != self.rx and red_bird.get_pos()[1] != self.ry \
        and green_bird.get_pos()[0] != self.gx and green_bird.get_pos()[1] != self.gy and stele.get_stele()[0][0] == self.bx \
        and stele.get_stele()[0][1] == self.by and stele.get_stele()[1][0] == self.rx and stele.get_stele()[1][1] == self.ry \
        and stele.get_stele()[2][0] == self.gx and stele.get_stele()[2][1] == self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] == self.bx \
        and blue_bird.get_pos()[1] == self.by and red_bird.get_pos()[0] != self.rx and red_bird.get_pos()[1] == self.ry \
        and green_bird.get_pos()[0] != self.gx and green_bird.get_pos()[1] == self.gy and stele.get_stele()[0][0] == self.bx \
        and stele.get_stele()[0][1] == self.by and stele.get_stele()[1][0] == self.rx and stele.get_stele()[1][1] == self.ry \
        and stele.get_stele()[2][0] == self.gx and stele.get_stele()[2][1] == self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] == self.bx \
        and blue_bird.get_pos()[1] == self.by and red_bird.get_pos()[0] == self.rx and red_bird.get_pos()[1] != self.ry \
        and green_bird.get_pos()[0] == self.gx and green_bird.get_pos()[1] != self.gy and stele.get_stele()[0][0] == self.bx \
        and stele.get_stele()[0][1] == self.by and stele.get_stele()[1][0] == self.rx and stele.get_stele()[1][1] == self.ry \
        and stele.get_stele()[2][0] == self.gx and stele.get_stele()[2][1] == self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] == self.bx \
        and blue_bird.get_pos()[1] == self.by and red_bird.get_pos()[0] != self.rx and red_bird.get_pos()[1] == self.ry \
        and green_bird.get_pos()[0] == self.gx and green_bird.get_pos()[1] != self.gy and stele.get_stele()[0][0] == self.bx \
        and stele.get_stele()[0][1] == self.by and stele.get_stele()[1][0] == self.rx and stele.get_stele()[1][1] == self.ry \
        and stele.get_stele()[2][0] == self.gx and stele.get_stele()[2][1] == self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] == self.bx \
        and blue_bird.get_pos()[1] == self.by and red_bird.get_pos()[0] == self.rx and red_bird.get_pos()[1] != self.ry \
        and green_bird.get_pos()[0] != self.gx and green_bird.get_pos()[1] == self.gy and stele.get_stele()[0][0] == self.bx \
        and stele.get_stele()[0][1] == self.by and stele.get_stele()[1][0] == self.rx and stele.get_stele()[1][1] == self.ry \
        and stele.get_stele()[2][0] == self.gx and stele.get_stele()[2][1] == self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] == self.bx \
        and blue_bird.get_pos()[1] == self.by and red_bird.get_pos()[0] != self.rx and red_bird.get_pos()[1] != self.ry \
        and green_bird.get_pos()[0] != self.gx and green_bird.get_pos()[1] == self.gy and stele.get_stele()[0][0] == self.bx \
        and stele.get_stele()[0][1] == self.by and stele.get_stele()[1][0] == self.rx and stele.get_stele()[1][1] == self.ry \
        and stele.get_stele()[2][0] == self.gx and stele.get_stele()[2][1] == self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] == self.bx \
        and blue_bird.get_pos()[1] == self.by and red_bird.get_pos()[0] != self.rx and red_bird.get_pos()[1] != self.ry \
        and green_bird.get_pos()[0] == self.gx and green_bird.get_pos()[1] != self.gy and stele.get_stele()[0][0] == self.bx \
        and stele.get_stele()[0][1] == self.by and stele.get_stele()[1][0] == self.rx and stele.get_stele()[1][1] == self.ry \
        and stele.get_stele()[2][0] == self.gx and stele.get_stele()[2][1] == self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] == self.bx \
        and blue_bird.get_pos()[1] == self.by and red_bird.get_pos()[0] != self.rx and red_bird.get_pos()[1] == self.ry \
        and green_bird.get_pos()[0] != self.gx and green_bird.get_pos()[1] != self.gy and stele.get_stele()[0][0] == self.bx \
        and stele.get_stele()[0][1] == self.by and stele.get_stele()[1][0] == self.rx and stele.get_stele()[1][1] == self.ry \
        and stele.get_stele()[2][0] == self.gx and stele.get_stele()[2][1] == self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] == self.bx \
        and blue_bird.get_pos()[1] == self.by and red_bird.get_pos()[0] == self.rx and red_bird.get_pos()[1] != self.ry \
        and green_bird.get_pos()[0] != self.gx and green_bird.get_pos()[1] != self.gy and stele.get_stele()[0][0] == self.bx \
        and stele.get_stele()[0][1] == self.by and stele.get_stele()[1][0] == self.rx and stele.get_stele()[1][1] == self.ry \
        and stele.get_stele()[2][0] == self.gx and stele.get_stele()[2][1] == self.gy:
            
            self.message_timer = 100 
            self.pos_rect = (5, 10)
            self.taille_rect = (232, 30)
            self.message = f"L'oiseau rouge et vert sont mal places ! Mefies-toi !!"
            self.show_message = True

        
        elif blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] != self.bx \
        and blue_bird.get_pos()[1] != self.by and red_bird.get_pos()[0] == self.rx and red_bird.get_pos()[1] == self.ry \
        and green_bird.get_pos()[0] != self.gx and green_bird.get_pos()[1] != self.gy and stele.get_stele()[0][0] == self.bx \
        and stele.get_stele()[0][1] == self.by and stele.get_stele()[1][0] == self.rx and stele.get_stele()[1][1] == self.ry \
        and stele.get_stele()[2][0] == self.gx and stele.get_stele()[2][1] == self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] != self.bx \
        and blue_bird.get_pos()[1] == self.by and red_bird.get_pos()[0] == self.rx and red_bird.get_pos()[1] == self.ry \
        and green_bird.get_pos()[0] != self.gx and green_bird.get_pos()[1] == self.gy and stele.get_stele()[0][0] == self.bx \
        and stele.get_stele()[0][1] == self.by and stele.get_stele()[1][0] == self.rx and stele.get_stele()[1][1] == self.ry \
        and stele.get_stele()[2][0] == self.gx and stele.get_stele()[2][1] == self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] == self.bx \
        and blue_bird.get_pos()[1] != self.by and red_bird.get_pos()[0] == self.rx and red_bird.get_pos()[1] == self.ry \
        and green_bird.get_pos()[0] == self.gx and green_bird.get_pos()[1] != self.gy and stele.get_stele()[0][0] == self.bx \
        and stele.get_stele()[0][1] == self.by and stele.get_stele()[1][0] == self.rx and stele.get_stele()[1][1] == self.ry \
        and stele.get_stele()[2][0] == self.gx and stele.get_stele()[2][1] == self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] != self.bx \
        and blue_bird.get_pos()[1] == self.by and red_bird.get_pos()[0] == self.rx and red_bird.get_pos()[1] == self.ry \
        and green_bird.get_pos()[0] == self.gx and green_bird.get_pos()[1] != self.gy and stele.get_stele()[0][0] == self.bx \
        and stele.get_stele()[0][1] == self.by and stele.get_stele()[1][0] == self.rx and stele.get_stele()[1][1] == self.ry \
        and stele.get_stele()[2][0] == self.gx and stele.get_stele()[2][1] == self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] == self.bx \
        and blue_bird.get_pos()[1] != self.by and red_bird.get_pos()[0] == self.rx and red_bird.get_pos()[1] == self.ry \
        and green_bird.get_pos()[0] != self.gx and green_bird.get_pos()[1] == self.gy and stele.get_stele()[0][0] == self.bx \
        and stele.get_stele()[0][1] == self.by and stele.get_stele()[1][0] == self.rx and stele.get_stele()[1][1] == self.ry \
        and stele.get_stele()[2][0] == self.gx and stele.get_stele()[2][1] == self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] != self.bx \
        and blue_bird.get_pos()[1] != self.by and red_bird.get_pos()[0] == self.rx and red_bird.get_pos()[1] == self.ry \
        and green_bird.get_pos()[0] != self.gx and green_bird.get_pos()[1] == self.gy and stele.get_stele()[0][0] == self.bx \
        and stele.get_stele()[0][1] == self.by and stele.get_stele()[1][0] == self.rx and stele.get_stele()[1][1] == self.ry \
        and stele.get_stele()[2][0] == self.gx and stele.get_stele()[2][1] == self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] != self.bx \
        and blue_bird.get_pos()[1] != self.by and red_bird.get_pos()[0] == self.rx and red_bird.get_pos()[1] == self.ry \
        and green_bird.get_pos()[0] == self.gx and green_bird.get_pos()[1] != self.gy and stele.get_stele()[0][0] == self.bx \
        and stele.get_stele()[0][1] == self.by and stele.get_stele()[1][0] == self.rx and stele.get_stele()[1][1] == self.ry \
        and stele.get_stele()[2][0] == self.gx and stele.get_stele()[2][1] == self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] != self.bx \
        and blue_bird.get_pos()[1] == self.by and red_bird.get_pos()[0] == self.rx and red_bird.get_pos()[1] == self.ry \
        and green_bird.get_pos()[0] != self.gx and green_bird.get_pos()[1] != self.gy and stele.get_stele()[0][0] == self.bx \
        and stele.get_stele()[0][1] == self.by and stele.get_stele()[1][0] == self.rx and stele.get_stele()[1][1] == self.ry \
        and stele.get_stele()[2][0] == self.gx and stele.get_stele()[2][1] == self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] == self.bx \
        and blue_bird.get_pos()[1] != self.by and red_bird.get_pos()[0] == self.rx and red_bird.get_pos()[1] == self.ry \
        and green_bird.get_pos()[0] != self.gx and green_bird.get_pos()[1] != self.gy and stele.get_stele()[0][0] == self.bx \
        and stele.get_stele()[0][1] == self.by and stele.get_stele()[1][0] == self.rx and stele.get_stele()[1][1] == self.ry \
        and stele.get_stele()[2][0] == self.gx and stele.get_stele()[2][1] == self.gy:
            
            self.message_timer = 100 
            self.pos_rect = (5, 10)
            self.taille_rect = (232, 30)
            self.message = f"L'oiseau bleu et vert sont mal places ! Mefies-toi !!"
            self.show_message = True


        elif blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] != self.bx \
        and blue_bird.get_pos()[1] != self.by and red_bird.get_pos()[0] != self.rx and red_bird.get_pos()[1] != self.ry \
        and green_bird.get_pos()[0] != self.gx and green_bird.get_pos()[1] != self.gy and stele.get_stele()[0][0] == self.bx \
        and stele.get_stele()[0][1] == self.by and stele.get_stele()[1][0] == self.rx and stele.get_stele()[1][1] == self.ry \
        and stele.get_stele()[2][0] == self.gx and stele.get_stele()[2][1] == self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] != self.bx \
        and blue_bird.get_pos()[1] == self.by and red_bird.get_pos()[0] != self.rx and red_bird.get_pos()[1] == self.ry \
        and green_bird.get_pos()[0] != self.gx and green_bird.get_pos()[1] == self.gy and stele.get_stele()[0][0] == self.bx \
        and stele.get_stele()[0][1] == self.by and stele.get_stele()[1][0] == self.rx and stele.get_stele()[1][1] == self.ry \
        and stele.get_stele()[2][0] == self.gx and stele.get_stele()[2][1] == self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] == self.bx \
        and blue_bird.get_pos()[1] != self.by and red_bird.get_pos()[0] == self.rx and red_bird.get_pos()[1] != self.ry \
        and green_bird.get_pos()[0] == self.gx and green_bird.get_pos()[1] != self.gy and stele.get_stele()[0][0] == self.bx \
        and stele.get_stele()[0][1] == self.by and stele.get_stele()[1][0] == self.rx and stele.get_stele()[1][1] == self.ry \
        and stele.get_stele()[2][0] == self.gx and stele.get_stele()[2][1] == self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] != self.bx \
        and blue_bird.get_pos()[1] == self.by and red_bird.get_pos()[0] != self.rx and red_bird.get_pos()[1] == self.ry \
        and green_bird.get_pos()[0] == self.gx and green_bird.get_pos()[1] != self.gy and stele.get_stele()[0][0] == self.bx \
        and stele.get_stele()[0][1] == self.by and stele.get_stele()[1][0] == self.rx and stele.get_stele()[1][1] == self.ry \
        and stele.get_stele()[2][0] == self.gx and stele.get_stele()[2][1] == self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] == self.bx \
        and blue_bird.get_pos()[1] != self.by and red_bird.get_pos()[0] == self.rx and red_bird.get_pos()[1] != self.ry \
        and green_bird.get_pos()[0] != self.gx and green_bird.get_pos()[1] == self.gy and stele.get_stele()[0][0] == self.bx \
        and stele.get_stele()[0][1] == self.by and stele.get_stele()[1][0] == self.rx and stele.get_stele()[1][1] == self.ry \
        and stele.get_stele()[2][0] == self.gx and stele.get_stele()[2][1] == self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] != self.bx \
        and blue_bird.get_pos()[1] == self.by and red_bird.get_pos()[0] == self.rx and red_bird.get_pos()[1] != self.ry \
        and green_bird.get_pos()[0] == self.gx and green_bird.get_pos()[1] != self.gy and stele.get_stele()[0][0] == self.bx \
        and stele.get_stele()[0][1] == self.by and stele.get_stele()[1][0] == self.rx and stele.get_stele()[1][1] == self.ry \
        and stele.get_stele()[2][0] == self.gx and stele.get_stele()[2][1] == self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] == self.bx \
        and blue_bird.get_pos()[1] != self.by and red_bird.get_pos()[0] != self.rx and red_bird.get_pos()[1] == self.ry \
        and green_bird.get_pos()[0] != self.gx and green_bird.get_pos()[1] == self.gy and stele.get_stele()[0][0] == self.bx \
        and stele.get_stele()[0][1] == self.by and stele.get_stele()[1][0] == self.rx and stele.get_stele()[1][1] == self.ry \
        and stele.get_stele()[2][0] == self.gx and stele.get_stele()[2][1] == self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] != self.bx \
        and blue_bird.get_pos()[1] == self.by and red_bird.get_pos()[0] == self.rx and red_bird.get_pos()[1] != self.ry \
        and green_bird.get_pos()[0] != self.gx and green_bird.get_pos()[1] == self.gy and stele.get_stele()[0][0] == self.bx \
        and stele.get_stele()[0][1] == self.by and stele.get_stele()[1][0] == self.rx and stele.get_stele()[1][1] == self.ry \
        and stele.get_stele()[2][0] == self.gx and stele.get_stele()[2][1] == self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] == self.bx \
        and blue_bird.get_pos()[1] != self.by and red_bird.get_pos()[0] != self.rx and red_bird.get_pos()[1] == self.ry \
        and green_bird.get_pos()[0] == self.gx and green_bird.get_pos()[1] != self.gy and stele.get_stele()[0][0] == self.bx \
        and stele.get_stele()[0][1] == self.by and stele.get_stele()[1][0] == self.rx and stele.get_stele()[1][1] == self.ry \
        and stele.get_stele()[2][0] == self.gx and stele.get_stele()[2][1] == self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] != self.bx \
        and blue_bird.get_pos()[1] != self.by and red_bird.get_pos()[0] != self.rx and red_bird.get_pos()[1] != self.ry \
        and green_bird.get_pos()[0] != self.gx and green_bird.get_pos()[1] == self.gy and stele.get_stele()[0][0] == self.bx \
        and stele.get_stele()[0][1] == self.by and stele.get_stele()[1][0] == self.rx and stele.get_stele()[1][1] == self.ry \
        and stele.get_stele()[2][0] == self.gx and stele.get_stele()[2][1] == self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] != self.bx \
        and blue_bird.get_pos()[1] != self.by and red_bird.get_pos()[0] != self.rx and red_bird.get_pos()[1] != self.ry \
        and green_bird.get_pos()[0] == self.gx and green_bird.get_pos()[1] != self.gy and stele.get_stele()[0][0] == self.bx \
        and stele.get_stele()[0][1] == self.by and stele.get_stele()[1][0] == self.rx and stele.get_stele()[1][1] == self.ry \
        and stele.get_stele()[2][0] == self.gx and stele.get_stele()[2][1] == self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] != self.bx \
        and blue_bird.get_pos()[1] == self.by and red_bird.get_pos()[0] != self.rx and red_bird.get_pos()[1] == self.ry \
        and green_bird.get_pos()[0] != self.gx and green_bird.get_pos()[1] != self.gy and stele.get_stele()[0][0] == self.bx \
        and stele.get_stele()[0][1] == self.by and stele.get_stele()[1][0] == self.rx and stele.get_stele()[1][1] == self.ry \
        and stele.get_stele()[2][0] == self.gx and stele.get_stele()[2][1] == self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] == self.bx \
        and blue_bird.get_pos()[1] != self.by and red_bird.get_pos()[0] == self.rx and red_bird.get_pos()[1] != self.ry \
        and green_bird.get_pos()[0] != self.gx and green_bird.get_pos()[1] != self.gy and stele.get_stele()[0][0] == self.bx \
        and stele.get_stele()[0][1] == self.by and stele.get_stele()[1][0] == self.rx and stele.get_stele()[1][1] == self.ry \
        and stele.get_stele()[2][0] == self.gx and stele.get_stele()[2][1] == self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] != self.bx \
        and blue_bird.get_pos()[1] == self.by and red_bird.get_pos()[0] == self.rx and red_bird.get_pos()[1] != self.ry \
        and green_bird.get_pos()[0] != self.gx and green_bird.get_pos()[1] != self.gy and stele.get_stele()[0][0] == self.bx \
        and stele.get_stele()[0][1] == self.by and stele.get_stele()[1][0] == self.rx and stele.get_stele()[1][1] == self.ry \
        and stele.get_stele()[2][0] == self.gx and stele.get_stele()[2][1] == self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] == self.bx \
        and blue_bird.get_pos()[1] != self.by and red_bird.get_pos()[0] != self.rx and red_bird.get_pos()[1] == self.ry \
        and green_bird.get_pos()[0] != self.gx and green_bird.get_pos()[1] != self.gy and stele.get_stele()[0][0] == self.bx \
        and stele.get_stele()[0][1] == self.by and stele.get_stele()[1][0] == self.rx and stele.get_stele()[1][1] == self.ry \
        and stele.get_stele()[2][0] == self.gx and stele.get_stele()[2][1] == self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] != self.bx \
        and blue_bird.get_pos()[1] != self.by and red_bird.get_pos()[0] != self.rx and red_bird.get_pos()[1] == self.ry \
        and green_bird.get_pos()[0] != self.gx and green_bird.get_pos()[1] == self.gy and stele.get_stele()[0][0] == self.bx \
        and stele.get_stele()[0][1] == self.by and stele.get_stele()[1][0] == self.rx and stele.get_stele()[1][1] == self.ry \
        and stele.get_stele()[2][0] == self.gx and stele.get_stele()[2][1] == self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] != self.bx \
        and blue_bird.get_pos()[1] != self.by and red_bird.get_pos()[0] == self.rx and red_bird.get_pos()[1] != self.ry \
        and green_bird.get_pos()[0] == self.gx and green_bird.get_pos()[1] != self.gy and stele.get_stele()[0][0] == self.bx \
        and stele.get_stele()[0][1] == self.by and stele.get_stele()[1][0] == self.rx and stele.get_stele()[1][1] == self.ry \
        and stele.get_stele()[2][0] == self.gx and stele.get_stele()[2][1] == self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] != self.bx \
        and blue_bird.get_pos()[1] != self.by and red_bird.get_pos()[0] == self.rx and red_bird.get_pos()[1] != self.ry \
        and green_bird.get_pos()[0] != self.gx and green_bird.get_pos()[1] == self.gy and stele.get_stele()[0][0] == self.bx \
        and stele.get_stele()[0][1] == self.by and stele.get_stele()[1][0] == self.rx and stele.get_stele()[1][1] == self.ry \
        and stele.get_stele()[2][0] == self.gx and stele.get_stele()[2][1] == self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] != self.bx \
        and blue_bird.get_pos()[1] != self.by and red_bird.get_pos()[0] != self.rx and red_bird.get_pos()[1] == self.ry \
        and green_bird.get_pos()[0] == self.gx and green_bird.get_pos()[1] != self.gy and stele.get_stele()[0][0] == self.bx \
        and stele.get_stele()[0][1] == self.by and stele.get_stele()[1][0] == self.rx and stele.get_stele()[1][1] == self.ry \
        and stele.get_stele()[2][0] == self.gx and stele.get_stele()[2][1] == self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] != self.bx \
        and blue_bird.get_pos()[1] == self.by and red_bird.get_pos()[0] != self.rx and red_bird.get_pos()[1] != self.ry \
        and green_bird.get_pos()[0] != self.gx and green_bird.get_pos()[1] == self.gy and stele.get_stele()[0][0] == self.bx \
        and stele.get_stele()[0][1] == self.by and stele.get_stele()[1][0] == self.rx and stele.get_stele()[1][1] == self.ry \
        and stele.get_stele()[2][0] == self.gx and stele.get_stele()[2][1] == self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] != self.bx \
        and blue_bird.get_pos()[1] == self.by and red_bird.get_pos()[0] != self.rx and red_bird.get_pos()[1] != self.ry \
        and green_bird.get_pos()[0] == self.gx and green_bird.get_pos()[1] != self.gy and stele.get_stele()[0][0] == self.bx \
        and stele.get_stele()[0][1] == self.by and stele.get_stele()[1][0] == self.rx and stele.get_stele()[1][1] == self.ry \
        and stele.get_stele()[2][0] == self.gx and stele.get_stele()[2][1] == self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] == self.bx \
        and blue_bird.get_pos()[1]!= self.by and red_bird.get_pos()[0] != self.rx and red_bird.get_pos()[1] != self.ry \
        and green_bird.get_pos()[0] != self.gx and green_bird.get_pos()[1] == self.gy and stele.get_stele()[0][0] == self.bx \
        and stele.get_stele()[0][1] == self.by and stele.get_stele()[1][0] == self.rx and stele.get_stele()[1][1] == self.ry \
        and stele.get_stele()[2][0] == self.gx and stele.get_stele()[2][1] == self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] != self.bx \
        and blue_bird.get_pos()[1] == self.by and red_bird.get_pos()[0] != self.rx and red_bird.get_pos()[1] != self.ry \
        and green_bird.get_pos()[0] == self.gx and green_bird.get_pos()[1] != self.gy and stele.get_stele()[0][0] == self.bx \
        and stele.get_stele()[0][1] == self.by and stele.get_stele()[1][0] == self.rx and stele.get_stele()[1][1] == self.ry \
        and stele.get_stele()[2][0] == self.gx and stele.get_stele()[2][1] == self.gy:
            
            self.message_timer = 100 
            self.pos_rect = (30, 10)
            self.taille_rect = (205, 30)
            self.message = f"L'oiseau bleu, rouge et vert sont mal places !"
            self.show_message = True


        elif blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] == self.bx \
        and blue_bird.get_pos()[1] == self.by and red_bird.get_pos()[0] == self.rx and red_bird.get_pos()[1] == self.ry \
        and green_bird.get_pos()[0] == self.gx and green_bird.get_pos()[1] == self.gy and stele.get_stele()[0][0] != self.bx \
        and stele.get_stele()[0][1] != self.by and stele.get_stele()[1][0] == self.rx and stele.get_stele()[1][1] == self.ry \
        and stele.get_stele()[2][0] == self.gx and stele.get_stele()[2][1] == self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] == self.bx \
        and blue_bird.get_pos()[1] == self.by and red_bird.get_pos()[0] == self.rx and red_bird.get_pos()[1] == self.ry \
        and green_bird.get_pos()[0] == self.gx and green_bird.get_pos()[1] == self.gy and stele.get_stele()[0][0] != self.bx \
        and stele.get_stele()[0][1] == self.by and stele.get_stele()[1][0] == self.rx and stele.get_stele()[1][1] == self.ry \
        and stele.get_stele()[2][0] == self.gx and stele.get_stele()[2][1] == self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] == self.bx \
        and blue_bird.get_pos()[1] == self.by and red_bird.get_pos()[0] == self.rx and red_bird.get_pos()[1] == self.ry \
        and green_bird.get_pos()[0] == self.gx and green_bird.get_pos()[1] == self.gy and stele.get_stele()[0][0] == self.bx \
        and stele.get_stele()[0][1] != self.by and stele.get_stele()[1][0] == self.rx and stele.get_stele()[1][1] == self.ry \
        and stele.get_stele()[2][0] == self.gx and stele.get_stele()[2][1] == self.gy:
            
            self.message_timer = 100 
            self.pos_rect = (40, 10)
            self.taille_rect = (190, 30)
            self.message = f"La stele bleue est mal placee ! Mefies-toi !!"
            self.show_message = True


        elif blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] == self.bx \
        and blue_bird.get_pos()[1] == self.by and red_bird.get_pos()[0] == self.rx and red_bird.get_pos()[1] == self.ry \
        and green_bird.get_pos()[0] == self.gx and green_bird.get_pos()[1] == self.gy and stele.get_stele()[0][0] == self.bx \
        and stele.get_stele()[0][1] == self.by and stele.get_stele()[1][0] != self.rx and stele.get_stele()[1][1] != self.ry \
        and stele.get_stele()[2][0] == self.gx and stele.get_stele()[2][1] == self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] == self.bx \
        and blue_bird.get_pos()[1] == self.by and red_bird.get_pos()[0] == self.rx and red_bird.get_pos()[1] == self.ry \
        and green_bird.get_pos()[0] == self.gx and green_bird.get_pos()[1] == self.gy and stele.get_stele()[0][0] == self.bx \
        and stele.get_stele()[0][1] == self.by and stele.get_stele()[1][0] != self.rx and stele.get_stele()[1][1] == self.ry \
        and stele.get_stele()[2][0] == self.gx and stele.get_stele()[2][1] == self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] == self.bx \
        and blue_bird.get_pos()[1] == self.by and red_bird.get_pos()[0] == self.rx and red_bird.get_pos()[1] == self.ry \
        and green_bird.get_pos()[0] == self.gx and green_bird.get_pos()[1] == self.gy and stele.get_stele()[0][0] == self.bx \
        and stele.get_stele()[0][1] == self.by and stele.get_stele()[1][0] == self.rx and stele.get_stele()[1][1] != self.ry \
        and stele.get_stele()[2][0] == self.gx and stele.get_stele()[2][1] == self.gy:
            
            self.message_timer = 100 
            self.pos_rect = (40, 10)
            self.taille_rect = (190, 30)
            self.message = f"La stele rouge est mal placee ! Mefies-toi !!"
            self.show_message = True

        
        elif blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] == self.bx \
        and blue_bird.get_pos()[1] == self.by and red_bird.get_pos()[0] == self.rx and red_bird.get_pos()[1] == self.ry \
        and green_bird.get_pos()[0] == self.gx and green_bird.get_pos()[1] == self.gy and stele.get_stele()[0][0] == self.bx \
        and stele.get_stele()[0][1] == self.by and stele.get_stele()[1][0] == self.rx and stele.get_stele()[1][1] == self.ry \
        and stele.get_stele()[2][0] != self.gx and stele.get_stele()[2][1] != self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] == self.bx \
        and blue_bird.get_pos()[1] == self.by and red_bird.get_pos()[0] == self.rx and red_bird.get_pos()[1] == self.ry \
        and green_bird.get_pos()[0] == self.gx and green_bird.get_pos()[1] == self.gy and stele.get_stele()[0][0] == self.bx \
        and stele.get_stele()[0][1] == self.by and stele.get_stele()[1][0] == self.rx and stele.get_stele()[1][1] == self.ry \
        and stele.get_stele()[2][0] != self.gx and stele.get_stele()[2][1] == self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] == self.bx \
        and blue_bird.get_pos()[1] == self.by and red_bird.get_pos()[0] == self.rx and red_bird.get_pos()[1] == self.ry \
        and green_bird.get_pos()[0] == self.gx and green_bird.get_pos()[1] == self.gy and stele.get_stele()[0][0] == self.bx \
        and stele.get_stele()[0][1] == self.by and stele.get_stele()[1][0] == self.rx and stele.get_stele()[1][1] == self.ry \
        and stele.get_stele()[2][0] == self.gx and stele.get_stele()[2][1]!= self.gy:
            
            self.message_timer = 100 
            self.pos_rect = (40, 10)
            self.taille_rect = (190, 30)
            self.message = f"La stele verte est mal placee ! Mefies-toi !!"
            self.show_message = True


        elif blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] == self.bx \
        and blue_bird.get_pos()[1] == self.by and red_bird.get_pos()[0] == self.rx and red_bird.get_pos()[1] == self.ry \
        and green_bird.get_pos()[0] == self.gx and green_bird.get_pos()[1] == self.gy and stele.get_stele()[0][0] != self.bx \
        and stele.get_stele()[0][1] != self.by and stele.get_stele()[1][0] != self.rx and stele.get_stele()[1][1] != self.ry \
        and stele.get_stele()[2][0] == self.gx and stele.get_stele()[2][1] == self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] == self.bx \
        and blue_bird.get_pos()[1] == self.by and red_bird.get_pos()[0] == self.rx and red_bird.get_pos()[1] == self.ry \
        and green_bird.get_pos()[0] == self.gx and green_bird.get_pos()[1] == self.gy and stele.get_stele()[0][0] != self.bx \
        and stele.get_stele()[0][1] == self.by and stele.get_stele()[1][0] != self.rx and stele.get_stele()[1][1] == self.ry \
        and stele.get_stele()[2][0] == self.gx and stele.get_stele()[2][1] == self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] == self.bx \
        and blue_bird.get_pos()[1] == self.by and red_bird.get_pos()[0] == self.rx and red_bird.get_pos()[1] == self.ry \
        and green_bird.get_pos()[0] == self.gx and green_bird.get_pos()[1] == self.gy and stele.get_stele()[0][0] == self.bx \
        and stele.get_stele()[0][1] != self.by and stele.get_stele()[1][0] == self.rx and stele.get_stele()[1][1] != self.ry \
        and stele.get_stele()[2][0] == self.gx and stele.get_stele()[2][1] == self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] == self.bx \
        and blue_bird.get_pos()[1] == self.by and red_bird.get_pos()[0] == self.rx and red_bird.get_pos()[1] == self.ry \
        and green_bird.get_pos()[0] == self.gx and green_bird.get_pos()[1] == self.gy and stele.get_stele()[0][0] == self.bx \
        and stele.get_stele()[0][1] != self.by and stele.get_stele()[1][0] != self.rx and stele.get_stele()[1][1] == self.ry \
        and stele.get_stele()[2][0] == self.gx and stele.get_stele()[2][1] == self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] == self.bx \
        and blue_bird.get_pos()[1] == self.by and red_bird.get_pos()[0] == self.rx and red_bird.get_pos()[1] == self.ry \
        and green_bird.get_pos()[0] == self.gx and green_bird.get_pos()[1] == self.gy and stele.get_stele()[0][0] != self.bx \
        and stele.get_stele()[0][1] == self.by and stele.get_stele()[1][0] == self.rx and stele.get_stele()[1][1] != self.ry \
        and stele.get_stele()[2][0] == self.gx and stele.get_stele()[2][1] == self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] == self.bx \
        and blue_bird.get_pos()[1] == self.by and red_bird.get_pos()[0] == self.rx and red_bird.get_pos()[1] == self.ry \
        and green_bird.get_pos()[0] == self.gx and green_bird.get_pos()[1] == self.gy and stele.get_stele()[0][0] != self.bx \
        and stele.get_stele()[0][1] != self.by and stele.get_stele()[1][0] == self.rx and stele.get_stele()[1][1] != self.ry \
        and stele.get_stele()[2][0] == self.gx and stele.get_stele()[2][1] == self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] == self.bx \
        and blue_bird.get_pos()[1] == self.by and red_bird.get_pos()[0] == self.rx and red_bird.get_pos()[1] == self.ry \
        and green_bird.get_pos()[0] == self.gx and green_bird.get_pos()[1] == self.gy and stele.get_stele()[0][0] != self.bx \
        and stele.get_stele()[0][1] != self.by and stele.get_stele()[1][0] != self.rx and stele.get_stele()[1][1] == self.ry \
        and stele.get_stele()[2][0] == self.gx and stele.get_stele()[2][1] == self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] == self.bx \
        and blue_bird.get_pos()[1] == self.by and red_bird.get_pos()[0] == self.rx and red_bird.get_pos()[1] == self.ry \
        and green_bird.get_pos()[0] == self.gx and green_bird.get_pos()[1] == self.gy and stele.get_stele()[0][0] != self.bx \
        and stele.get_stele()[0][1] == self.by and stele.get_stele()[1][0] != self.rx and stele.get_stele()[1][1] != self.ry \
        and stele.get_stele()[2][0] == self.gx and stele.get_stele()[2][1] == self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] == self.bx \
        and blue_bird.get_pos()[1] == self.by and red_bird.get_pos()[0] == self.rx and red_bird.get_pos()[1] == self.ry \
        and green_bird.get_pos()[0] == self.gx and green_bird.get_pos()[1] == self.gy and stele.get_stele()[0][0] == self.bx \
        and stele.get_stele()[0][1] != self.by and stele.get_stele()[1][0] != self.rx and stele.get_stele()[1][1] != self.ry \
        and stele.get_stele()[2][0] == self.gx and stele.get_stele()[2][1] == self.gy:
            
            self.message_timer = 100 
            self.pos_rect = (5, 10)
            self.taille_rect = (232, 30)
            self.message = f"La stele bleue et rouge sont mal placees ! Mefies-toi !!"
            self.show_message = True


        elif blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] == self.bx \
        and blue_bird.get_pos()[1] == self.by and red_bird.get_pos()[0] == self.rx and red_bird.get_pos()[1] == self.ry \
        and green_bird.get_pos()[0] == self.gx and green_bird.get_pos()[1] == self.gy and stele.get_stele()[0][0] == self.bx \
        and stele.get_stele()[0][1] == self.by and stele.get_stele()[1][0] != self.rx and stele.get_stele()[1][1] != self.ry \
        and stele.get_stele()[2][0] != self.gx and stele.get_stele()[2][1] != self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] == self.bx \
        and blue_bird.get_pos()[1] == self.by and red_bird.get_pos()[0] == self.rx and red_bird.get_pos()[1] == self.ry \
        and green_bird.get_pos()[0] == self.gx and green_bird.get_pos()[1] == self.gy and stele.get_stele()[0][0] == self.bx \
        and stele.get_stele()[0][1] == self.by and stele.get_stele()[1][0] != self.rx and stele.get_stele()[1][1] == self.ry \
        and stele.get_stele()[2][0] != self.gx and stele.get_stele()[2][1] == self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] == self.bx \
        and blue_bird.get_pos()[1] == self.by and red_bird.get_pos()[0] == self.rx and red_bird.get_pos()[1] == self.ry \
        and green_bird.get_pos()[0] == self.gx and green_bird.get_pos()[1] == self.gy and stele.get_stele()[0][0] == self.bx \
        and stele.get_stele()[0][1] == self.by and stele.get_stele()[1][0] == self.rx and stele.get_stele()[1][1] != self.ry \
        and stele.get_stele()[2][0] == self.gx and stele.get_stele()[2][1] != self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] == self.bx \
        and blue_bird.get_pos()[1] == self.by and red_bird.get_pos()[0] == self.rx and red_bird.get_pos()[1] == self.ry \
        and green_bird.get_pos()[0] == self.gx and green_bird.get_pos()[1] == self.gy and stele.get_stele()[0][0] == self.bx \
        and stele.get_stele()[0][1] == self.by and stele.get_stele()[1][0] != self.rx and stele.get_stele()[1][1] == self.ry \
        and stele.get_stele()[2][0] == self.gx and stele.get_stele()[2][1] != self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] == self.bx \
        and blue_bird.get_pos()[1] == self.by and red_bird.get_pos()[0] == self.rx and red_bird.get_pos()[1] == self.ry \
        and green_bird.get_pos()[0] == self.gx and green_bird.get_pos()[1] == self.gy and stele.get_stele()[0][0] == self.bx \
        and stele.get_stele()[0][1] == self.by and stele.get_stele()[1][0] == self.rx and stele.get_stele()[1][1] != self.ry \
        and stele.get_stele()[2][0] != self.gx and stele.get_stele()[2][1] == self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] == self.bx \
        and blue_bird.get_pos()[1] == self.by and red_bird.get_pos()[0] == self.rx and red_bird.get_pos()[1] == self.ry \
        and green_bird.get_pos()[0] == self.gx and green_bird.get_pos()[1] == self.gy and stele.get_stele()[0][0] == self.bx \
        and stele.get_stele()[0][1] == self.by and stele.get_stele()[1][0] != self.rx and stele.get_stele()[1][1] != self.ry \
        and stele.get_stele()[2][0] != self.gx and stele.get_stele()[2][1] == self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] == self.bx \
        and blue_bird.get_pos()[1] == self.by and red_bird.get_pos()[0] == self.rx and red_bird.get_pos()[1] == self.ry \
        and green_bird.get_pos()[0] == self.gx and green_bird.get_pos()[1] == self.gy and stele.get_stele()[0][0] == self.bx \
        and stele.get_stele()[0][1] == self.by and stele.get_stele()[1][0] != self.rx and stele.get_stele()[1][1] != self.ry \
        and stele.get_stele()[2][0] == self.gx and stele.get_stele()[2][1] != self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] == self.bx \
        and blue_bird.get_pos()[1] == self.by and red_bird.get_pos()[0] == self.rx and red_bird.get_pos()[1] == self.ry \
        and green_bird.get_pos()[0] == self.gx and green_bird.get_pos()[1] == self.gy and stele.get_stele()[0][0] == self.bx \
        and stele.get_stele()[0][1] == self.by and stele.get_stele()[1][0] != self.rx and stele.get_stele()[1][1] == self.ry \
        and stele.get_stele()[2][0] != self.gx and stele.get_stele()[2][1] != self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] == self.bx \
        and blue_bird.get_pos()[1] == self.by and red_bird.get_pos()[0] == self.rx and red_bird.get_pos()[1] == self.ry \
        and green_bird.get_pos()[0] == self.gx and green_bird.get_pos()[1] == self.gy and stele.get_stele()[0][0] == self.bx \
        and stele.get_stele()[0][1] == self.by and stele.get_stele()[1][0] == self.rx and stele.get_stele()[1][1] != self.ry \
        and stele.get_stele()[2][0] != self.gx and stele.get_stele()[2][1] != self.gy:
            
            self.message_timer = 100 
            self.pos_rect = (5, 10)
            self.taille_rect = (232, 30)
            self.message = f"La stele rouge et verte sont mal placees ! Mefies-toi !!"
            self.show_message = True

        
        elif blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] == self.bx \
        and blue_bird.get_pos()[1] == self.by and red_bird.get_pos()[0] == self.rx and red_bird.get_pos()[1] == self.ry \
        and green_bird.get_pos()[0] == self.gx and green_bird.get_pos()[1] == self.gy and stele.get_stele()[0][0] != self.bx \
        and stele.get_stele()[0][1] != self.by and stele.get_stele()[1][0] == self.rx and stele.get_stele()[1][1] == self.ry \
        and stele.get_stele()[2][0] != self.gx and stele.get_stele()[2][1] != self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] == self.bx \
        and blue_bird.get_pos()[1] == self.by and red_bird.get_pos()[0] == self.rx and red_bird.get_pos()[1] == self.ry \
        and green_bird.get_pos()[0] == self.gx and green_bird.get_pos()[1] == self.gy and stele.get_stele()[0][0] != self.bx \
        and stele.get_stele()[0][1] == self.by and stele.get_stele()[1][0] == self.rx and stele.get_stele()[1][1] == self.ry \
        and stele.get_stele()[2][0] != self.gx and stele.get_stele()[2][1] == self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] == self.bx \
        and blue_bird.get_pos()[1] == self.by and red_bird.get_pos()[0] == self.rx and red_bird.get_pos()[1] == self.ry \
        and green_bird.get_pos()[0] == self.gx and green_bird.get_pos()[1] == self.gy and stele.get_stele()[0][0] == self.bx \
        and stele.get_stele()[0][1] != self.by and stele.get_stele()[1][0] == self.rx and stele.get_stele()[1][1] == self.ry \
        and stele.get_stele()[2][0] == self.gx and stele.get_stele()[2][1] != self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] == self.bx \
        and blue_bird.get_pos()[1] == self.by and red_bird.get_pos()[0] == self.rx and red_bird.get_pos()[1] == self.ry \
        and green_bird.get_pos()[0] == self.gx and green_bird.get_pos()[1] == self.gy and stele.get_stele()[0][0] != self.bx \
        and stele.get_stele()[0][1] == self.by and stele.get_stele()[1][0] == self.rx and stele.get_stele()[1][1] == self.ry \
        and stele.get_stele()[2][0] == self.gx and stele.get_stele()[2][1] != self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] == self.bx \
        and blue_bird.get_pos()[1] == self.by and red_bird.get_pos()[0] == self.rx and red_bird.get_pos()[1] == self.ry \
        and green_bird.get_pos()[0] == self.gx and green_bird.get_pos()[1] == self.gy and stele.get_stele()[0][0] == self.bx \
        and stele.get_stele()[0][1] != self.by and stele.get_stele()[1][0] == self.rx and stele.get_stele()[1][1] == self.ry \
        and stele.get_stele()[2][0] != self.gx and stele.get_stele()[2][1] == self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] == self.bx \
        and blue_bird.get_pos()[1] == self.by and red_bird.get_pos()[0] == self.rx and red_bird.get_pos()[1] == self.ry \
        and green_bird.get_pos()[0] == self.gx and green_bird.get_pos()[1] == self.gy and stele.get_stele()[0][0] != self.bx \
        and stele.get_stele()[0][1] != self.by and stele.get_stele()[1][0] == self.rx and stele.get_stele()[1][1] == self.ry \
        and stele.get_stele()[2][0] != self.gx and stele.get_stele()[2][1] == self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] == self.bx \
        and blue_bird.get_pos()[1] == self.by and red_bird.get_pos()[0] == self.rx and red_bird.get_pos()[1] == self.ry \
        and green_bird.get_pos()[0] == self.gx and green_bird.get_pos()[1] == self.gy and stele.get_stele()[0][0] != self.bx \
        and stele.get_stele()[0][1] != self.by and stele.get_stele()[1][0] == self.rx and stele.get_stele()[1][1] == self.ry \
        and stele.get_stele()[2][0] == self.gx and stele.get_stele()[2][1] != self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] == self.bx \
        and blue_bird.get_pos()[1] == self.by and red_bird.get_pos()[0] == self.rx and red_bird.get_pos()[1] == self.ry \
        and green_bird.get_pos()[0] == self.gx and green_bird.get_pos()[1] == self.gy and stele.get_stele()[0][0] != self.bx \
        and stele.get_stele()[0][1] == self.by and stele.get_stele()[1][0] == self.rx and stele.get_stele()[1][1] == self.ry \
        and stele.get_stele()[2][0] != self.gx and stele.get_stele()[2][1] != self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] == self.bx \
        and blue_bird.get_pos()[1] == self.by and red_bird.get_pos()[0] == self.rx and red_bird.get_pos()[1] == self.ry \
        and green_bird.get_pos()[0] == self.gx and green_bird.get_pos()[1] == self.gy and stele.get_stele()[0][0] == self.bx \
        and stele.get_stele()[0][1] != self.by and stele.get_stele()[1][0] == self.rx and stele.get_stele()[1][1] == self.ry \
        and stele.get_stele()[2][0] != self.gx and stele.get_stele()[2][1] != self.gy:
            
            self.message_timer = 100 
            self.pos_rect = (5, 10)
            self.taille_rect = (232, 30)
            self.message = f"La stele bleue et verte sont mal placees ! Mefies-toi !!"
            self.show_message = True


        elif blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] == self.bx \
        and blue_bird.get_pos()[1] == self.by and red_bird.get_pos()[0] == self.rx and red_bird.get_pos()[1] == self.ry \
        and green_bird.get_pos()[0] == self.gx and green_bird.get_pos()[1] == self.gy and stele.get_stele()[0][0] != self.bx \
        and stele.get_stele()[0][1] != self.by and stele.get_stele()[1][0] != self.rx and stele.get_stele()[1][1] != self.ry \
        and stele.get_stele()[2][0] != self.gx and stele.get_stele()[2][1] != self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] == self.bx \
        and blue_bird.get_pos()[1] == self.by and red_bird.get_pos()[0] == self.rx and red_bird.get_pos()[1] == self.ry \
        and green_bird.get_pos()[0] == self.gx and green_bird.get_pos()[1] == self.gy and stele.get_stele()[0][0] != self.bx \
        and stele.get_stele()[0][1] == self.by and stele.get_stele()[1][0] != self.rx and stele.get_stele()[1][1] == self.ry \
        and stele.get_stele()[2][0] != self.gx and stele.get_stele()[2][1] == self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] == self.bx \
        and blue_bird.get_pos()[1] == self.by and red_bird.get_pos()[0] == self.rx and red_bird.get_pos()[1] == self.ry \
        and green_bird.get_pos()[0] == self.gx and green_bird.get_pos()[1] == self.gy and stele.get_stele()[0][0] == self.bx \
        and stele.get_stele()[0][1] != self.by and stele.get_stele()[1][0] == self.rx and stele.get_stele()[1][1] != self.ry \
        and stele.get_stele()[2][0] == self.gx and stele.get_stele()[2][1] != self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] == self.bx \
        and blue_bird.get_pos()[1] == self.by and red_bird.get_pos()[0] == self.rx and red_bird.get_pos()[1] == self.ry \
        and green_bird.get_pos()[0] == self.gx and green_bird.get_pos()[1] == self.gy and stele.get_stele()[0][0] != self.bx \
        and stele.get_stele()[0][1] == self.by and stele.get_stele()[1][0] != self.rx and stele.get_stele()[1][1] == self.ry \
        and stele.get_stele()[2][0] == self.gx and stele.get_stele()[2][1] != self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] == self.bx \
        and blue_bird.get_pos()[1] == self.by and red_bird.get_pos()[0] == self.rx and red_bird.get_pos()[1] == self.ry \
        and green_bird.get_pos()[0] == self.gx and green_bird.get_pos()[1] == self.gy and stele.get_stele()[0][0] == self.bx \
        and stele.get_stele()[0][1] != self.by and stele.get_stele()[1][0] == self.rx and stele.get_stele()[1][1] != self.ry \
        and stele.get_stele()[2][0] != self.gx and stele.get_stele()[2][1] == self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] == self.bx \
        and blue_bird.get_pos()[1] == self.by and red_bird.get_pos()[0] == self.rx and red_bird.get_pos()[1] == self.ry \
        and green_bird.get_pos()[0] == self.gx and green_bird.get_pos()[1] == self.gy and stele.get_stele()[0][0] != self.bx \
        and stele.get_stele()[0][1] == self.by and stele.get_stele()[1][0] == self.rx and stele.get_stele()[1][1] != self.ry \
        and stele.get_stele()[2][0] == self.gx and stele.get_stele()[2][1] != self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] == self.bx \
        and blue_bird.get_pos()[1] == self.by and red_bird.get_pos()[0] == self.rx and red_bird.get_pos()[1] == self.ry \
        and green_bird.get_pos()[0] == self.gx and green_bird.get_pos()[1] == self.gy and stele.get_stele()[0][0] == self.bx \
        and stele.get_stele()[0][1] != self.by and stele.get_stele()[1][0] != self.rx and stele.get_stele()[1][1] == self.ry \
        and stele.get_stele()[2][0] != self.gx and stele.get_stele()[2][1] == self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] == self.bx \
        and blue_bird.get_pos()[1] == self.by and red_bird.get_pos()[0] == self.rx and red_bird.get_pos()[1] == self.ry \
        and green_bird.get_pos()[0] == self.gx and green_bird.get_pos()[1] == self.gy and stele.get_stele()[0][0] != self.bx \
        and stele.get_stele()[0][1] == self.by and stele.get_stele()[1][0] == self.rx and stele.get_stele()[1][1] != self.ry \
        and stele.get_stele()[2][0] != self.gx and stele.get_stele()[2][1] == self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] == self.bx \
        and blue_bird.get_pos()[1] == self.by and red_bird.get_pos()[0] == self.rx and red_bird.get_pos()[1] == self.ry \
        and green_bird.get_pos()[0] == self.gx and green_bird.get_pos()[1] == self.gy and stele.get_stele()[0][0] == self.bx \
        and stele.get_stele()[0][1] != self.by and stele.get_stele()[1][0] != self.rx and stele.get_stele()[1][1] == self.ry \
        and stele.get_stele()[2][0] == self.gx and stele.get_stele()[2][1] != self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] == self.bx \
        and blue_bird.get_pos()[1] == self.by and red_bird.get_pos()[0] == self.rx and red_bird.get_pos()[1] == self.ry \
        and green_bird.get_pos()[0] == self.gx and green_bird.get_pos()[1] == self.gy and stele.get_stele()[0][0] != self.bx \
        and stele.get_stele()[0][1] != self.by and stele.get_stele()[1][0] != self.rx and stele.get_stele()[1][1] != self.ry \
        and stele.get_stele()[2][0] != self.gx and stele.get_stele()[2][1] == self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] == self.bx \
        and blue_bird.get_pos()[1] == self.by and red_bird.get_pos()[0] == self.rx and red_bird.get_pos()[1] == self.ry \
        and green_bird.get_pos()[0] == self.gx and green_bird.get_pos()[1] == self.gy and stele.get_stele()[0][0] != self.bx \
        and stele.get_stele()[0][1] != self.by and stele.get_stele()[1][0] != self.rx and stele.get_stele()[1][1] != self.ry \
        and stele.get_stele()[2][0] == self.gx and stele.get_stele()[2][1] != self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] == self.bx \
        and blue_bird.get_pos()[1] == self.by and red_bird.get_pos()[0] == self.rx and red_bird.get_pos()[1] == self.ry \
        and green_bird.get_pos()[0] == self.gx and green_bird.get_pos()[1] == self.gy and stele.get_stele()[0][0] != self.bx \
        and stele.get_stele()[0][1] == self.by and stele.get_stele()[1][0] != self.rx and stele.get_stele()[1][1] == self.ry \
        and stele.get_stele()[2][0] != self.gx and stele.get_stele()[2][1] != self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] == self.bx \
        and blue_bird.get_pos()[1] == self.by and red_bird.get_pos()[0] == self.rx and red_bird.get_pos()[1] == self.ry \
        and green_bird.get_pos()[0] == self.gx and green_bird.get_pos()[1] == self.gy and stele.get_stele()[0][0] == self.bx \
        and stele.get_stele()[0][1] != self.by and stele.get_stele()[1][0] == self.rx and stele.get_stele()[1][1] != self.ry \
        and stele.get_stele()[2][0] != self.gx and stele.get_stele()[2][1] != self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] == self.bx \
        and blue_bird.get_pos()[1] == self.by and red_bird.get_pos()[0] == self.rx and red_bird.get_pos()[1] == self.ry \
        and green_bird.get_pos()[0] == self.gx and green_bird.get_pos()[1] == self.gy and stele.get_stele()[0][0] != self.bx \
        and stele.get_stele()[0][1] == self.by and stele.get_stele()[1][0] == self.rx and stele.get_stele()[1][1] != self.ry \
        and stele.get_stele()[2][0] != self.gx and stele.get_stele()[2][1] != self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] == self.bx \
        and blue_bird.get_pos()[1] == self.by and red_bird.get_pos()[0] == self.rx and red_bird.get_pos()[1] == self.ry \
        and green_bird.get_pos()[0] == self.gx and green_bird.get_pos()[1] == self.gy and stele.get_stele()[0][0] == self.bx \
        and stele.get_stele()[0][1] != self.by and stele.get_stele()[1][0] != self.rx and stele.get_stele()[1][1] == self.ry \
        and stele.get_stele()[2][0] != self.gx and stele.get_stele()[2][1] != self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] == self.bx \
        and blue_bird.get_pos()[1] == self.by and red_bird.get_pos()[0] == self.rx and red_bird.get_pos()[1] == self.ry \
        and green_bird.get_pos()[0] == self.gx and green_bird.get_pos()[1] == self.gy and stele.get_stele()[0][0] != self.bx \
        and stele.get_stele()[0][1] != self.by and stele.get_stele()[1][0] != self.rx and stele.get_stele()[1][1] == self.ry \
        and stele.get_stele()[2][0] != self.gx and stele.get_stele()[2][1] == self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] == self.bx \
        and blue_bird.get_pos()[1] == self.by and red_bird.get_pos()[0] == self.rx and red_bird.get_pos()[1] == self.ry \
        and green_bird.get_pos()[0] == self.gx and green_bird.get_pos()[1] == self.gy and stele.get_stele()[0][0] != self.bx \
        and stele.get_stele()[0][1] != self.by and stele.get_stele()[1][0] == self.rx and stele.get_stele()[1][1] != self.ry \
        and stele.get_stele()[2][0] == self.gx and stele.get_stele()[2][1] != self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] == self.bx \
        and blue_bird.get_pos()[1] == self.by and red_bird.get_pos()[0] == self.rx and red_bird.get_pos()[1] == self.ry \
        and green_bird.get_pos()[0] == self.gx and green_bird.get_pos()[1] == self.gy and stele.get_stele()[0][0] != self.bx \
        and stele.get_stele()[0][1] != self.by and stele.get_stele()[1][0] == self.rx and stele.get_stele()[1][1] != self.ry \
        and stele.get_stele()[2][0] != self.gx and stele.get_stele()[2][1] == self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] == self.bx \
        and blue_bird.get_pos()[1] == self.by and red_bird.get_pos()[0] == self.rx and red_bird.get_pos()[1] == self.ry \
        and green_bird.get_pos()[0] == self.gx and green_bird.get_pos()[1] == self.gy and stele.get_stele()[0][0] != self.bx \
        and stele.get_stele()[0][1] != self.by and stele.get_stele()[1][0] != self.rx and stele.get_stele()[1][1] == self.ry \
        and stele.get_stele()[2][0] == self.gx and stele.get_stele()[2][1] != self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] == self.bx \
        and blue_bird.get_pos()[1] == self.by and red_bird.get_pos()[0] == self.rx and red_bird.get_pos()[1] == self.ry \
        and green_bird.get_pos()[0] == self.gx and green_bird.get_pos()[1] == self.gy and stele.get_stele()[0][0] != self.bx \
        and stele.get_stele()[0][1] == self.by and stele.get_stele()[1][0] != self.rx and stele.get_stele()[1][1] != self.ry \
        and stele.get_stele()[2][0] != self.gx and stele.get_stele()[2][1] == self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] == self.bx \
        and blue_bird.get_pos()[1] == self.by and red_bird.get_pos()[0] == self.rx and red_bird.get_pos()[1] == self.ry \
        and green_bird.get_pos()[0] == self.gx and green_bird.get_pos()[1] == self.gy and stele.get_stele()[0][0] != self.bx \
        and stele.get_stele()[0][1] == self.by and stele.get_stele()[1][0] != self.rx and stele.get_stele()[1][1] != self.ry \
        and stele.get_stele()[2][0] == self.gx and stele.get_stele()[2][1] != self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] == self.bx \
        and blue_bird.get_pos()[1] == self.by and red_bird.get_pos()[0] == self.rx and red_bird.get_pos()[1] == self.ry \
        and green_bird.get_pos()[0] == self.gx and green_bird.get_pos()[1] == self.gy and stele.get_stele()[0][0] == self.bx \
        and stele.get_stele()[0][1] != self.by and stele.get_stele()[1][0] != self.rx and stele.get_stele()[1][1] != self.ry \
        and stele.get_stele()[2][0] != self.gx and stele.get_stele()[2][1] == self.gy \
        or \
        blue == self.blue and red == self.red and green == self.green and blue_bird.get_pos()[0] == self.bx \
        and blue_bird.get_pos()[1] == self.by and red_bird.get_pos()[0] == self.rx and red_bird.get_pos()[1] == self.ry \
        and green_bird.get_pos()[0] == self.gx and green_bird.get_pos()[1] == self.gy and stele.get_stele()[0][0] != self.bx \
        and stele.get_stele()[0][1] == self.by and stele.get_stele()[1][0] != self.rx and stele.get_stele()[1][1] != self.ry \
        and stele.get_stele()[2][0] == self.gx and stele.get_stele()[2][1] != self.gy:
            
            self.message_timer = 100 
            self.pos_rect = (30, 10)
            self.taille_rect = (205, 30)
            self.message = f"La stele bleue, rouge et verte sont mal placees !"
            self.show_message = True


    def reset(self) -> None:
        """
        Méthode qui réinitialise les attributs de la classe
        """
        self.message_timer = 100
        self.message = ""
        self.show_message = False




if __name__ == "__main__":
    App()