    # coding:utf-8

"""######################################
#####                               #####
#####          projet ISN           #####
#####                               #####
#####################################"""


# imporatation des differents module
import pygame
import time
from pygame.locals import *
from tkinter import *
from threading import *
from random import *
import trifusion

class personnage :
#definition de la classe personnage

    def __init__(self,img):
        #methode qui ce lance au moment de la création de l'objet
        self.para ={"CDTir":0.8, "moveX": 1, "VJump":-9, "projV": 5, "degat":1 }
        self.image = img
        self.imageBlank = [pygame.image.load("img/persoBlank2.gif").convert_alpha(),pygame.image.load("img/persoBlank1.gif").convert_alpha()]
        self.listeActiveImage = self.image
        self.pos = self.image[0].get_rect()
        self.hp = 3
        self.anim = 0
        self.tir =[]
        self.D1 = 0
        self.v = 0
        self.cdtir = True
        self.invincible = False
        self.ceDeplace = False
        self.tirimage=pygame.image.load("img/tir.png").convert()

    def sautF(self):
        # methode qui gère la gravité/saut du personnage
        global continuer, piege, g, score
        while continuer == 1:
            if self.pos.collidelist(piege) != -1:   # si le personnage et sur un piège il perd 1 pv
                Thread(target = personnage.pv, args=(self,1)).start()
            self.nopS = self.pos                    #enregistrement de la position pré-déplacement
            self.v = self.v +g*0.020                #calcule ça nouvelle vittesse (v)
            self.pos=self.pos.move(0,self.v)        #déplace le personnage en fonction de ça vitesse calculé précédament
            if self.pos.collidelist(wall) != -1:    #verifie si il est dans un mur à ca nouvelle position
                if self.v > 0: self.jumping = False     #si il retombe (v>0) et qu'il touche un mur alors il peut resauté a nouveau
                self.pos = self.nopS                    #on redonne les coos d'origine
                self.v = 0                         #on lui attribut une vitesse de 0
            elif self.pos.collidelist(wallOnlyUp) != -1 and self.v > 0:
                self.jumping = False
                self.pos = self.nopS
                self.v = 0
            else:
                self.jumping = True
                if self.pos.top > 680:                  #si il est trops bas
                    score[self.name] = score[self.name]+1 #il perds
                    continuer = 0
            time.sleep(0.006)                       #on met un delai de 3 ms

    def CDTir(self):
        # méthode qui force un delai entre deux tir
        time.sleep(self.para["CDTir"])
        self.cdtir= True

    def evenement(self):
        global continuer, tir, murbonus,pos_bonus
        while continuer ==1:
            touche_presser = pygame.key.get_pressed()         #enregistre dans une liste toute les touches préssées
            # on sauvegarde les positions initiale du joeur
            self.nop = self.pos
            #on fait les action corespondant aux touches pressées
            if flag[self.tag] >= 1:
                Thread(target = personnage.pv, args=(self,flag[self.tag],)).start()
            if touche_presser[self.touche[0]]:
                if self.jumping == False:
                    self.v = self.para["VJump"]
            if touche_presser[self.touche[1]]:
                self.pos = self.pos.move(-self.para["moveX"],0)
                self.D1=0
                self.ceDeplace = True
            if touche_presser[self.touche[2]]:
                self.pos = self.pos.move(self.para["moveX"],0)
                self.D1=1
                self.ceDeplace = True
            if touche_presser[self.touche[3]]:
                self.saut = 0
            if touche_presser[self.touche[4]] and self.cdtir == True:
                self.cdtir = False
                self.D2 = self.D1
                self.tir.append(projectile(self))
                Thread(target = self.CDTir, args=()).start()

            if self.pos.collidelist(wall) != -1:
                self.pos = self.nop
            if self.pos.collidelist(wallOnlyUp) != -1 and self.v > 0:
                self.pos = self.nop
            if self.pos.collidelist(pos_bonus) != -1 and murbonus== -1 :
                Thread(target = self.get_bonus, args=()).start()
                murbonus = 15
            time.sleep(0.001)

    def get_bonus(self):
        global type_bonus
        if type_bonus==1:
            self.tirimage=pygame.image.load("img/tir2.png").convert()
            self.para["degat"] = 2
            time.sleep(5)
            if continuer ==1 :
                self.tirimage=pygame.image.load("img/tir.png").convert()
                self.para["degat"] = 1
        if type_bonus == 2:
            self.para["moveX"] = 2
            time.sleep(6)
            if continuer ==1:
                self.para["moveX"] = 1
        if type_bonus ==3:
            self.para["CDTir"]=0.3
            time.sleep(4)
            self.para["CDTir"]=0.8
        if type_bonus ==4:
            self.para["VJump"]=-13
            time.sleep(6)
            self.para["VJump"]=-9


    def pv(self, degat):
        # méthode qui gère la perte de pv/hp
        global continuer, flag, score
        if self.invincible: flag[self.tag] = False
        else:
            self.invincible = True
            Thread(target = personnage.CDInvincible, args=(self,)).start()
            self.hp = self.hp-degat
            if self.hp <= 0:
                continuer = 0
                score[self.name] = score[self.name]+1
            flag[self.tag] = False

    def CDInvincible(self):
        # méthdode qui gère la periode d'invulabilité après avoir pris des dégats
        for i in range(0,13):
            time.sleep(0.05)
            self.listeActiveImage = self.imageBlank + self.imageBlank
            time.sleep(0.05)
            self.listeActiveImage = self.image
        self.invincible = False

    def animation(self):
        # methode gerant lanimation de déplacement du personnage
        global continuer
        while continuer ==1:
            if self.ceDeplace == True :
                self.ceDeplace = False
                self.anim = 2
                time.sleep(0.25)
                self.anim = 0
            time.sleep(0.25)





class projectile:
# on definit la classe projectile

    def __init__(self,joueur):
        # ce lance à la creation de l'objet
        self.para = dict(joueur.para)
        self.image = joueur.tirimage
        self.pos = self.image.get_rect()
        self.pos.left = joueur.pos.left
        self.pos.top = joueur.pos.top
        self.direction = joueur.D2
        time.sleep(0.005)
        Thread(target = projectile.déplacement, args=(self,joueur,)).start()

    def déplacement(self,joueur):
        # methode qui déplace le projectile
        global continuer, aSupr, flag
        while continuer ==1:
            if self.direction==0:                   # déplace le projectile en fonction de ça direction
                self.pos=self.pos.move(-self.para["projV"],0)
            elif self.direction==1:
                self.pos=self.pos.move(self.para["projV"],0)
            if self.pos.collidelist(wall) != -1:       # on verifie si il se trouve dans un mure
                joueur.tir.remove(self)                      # si oui on suprime le tir
                return
            if self.pos.collidelist([J1.pos,J2.pos]) != -1 and self.pos.collidelist([J1.pos,J2.pos]) != joueur.tag :   # puis on verifie si le tir touche l'adversaire
                flag[self.pos.collidelist([J1.pos,J2.pos])] = self.para["degat"]
                joueur.tir.remove(self)
                return
            if self.pos.left > 2000 or self.pos.left < -60:     # si le projectile sort de l'écran, on le suprime
                joueur.tir.remove(self)
                return
            time.sleep(0.001)


def GIF():
    # procédure qui fait clignoté les personnage TEST
    while continuer == 1:
        for l in range(0,2):
            time.sleep(0.05)
            J2.imageActive = J2.image[l]
            J1.imageActive = J1.image[l]
            time.sleep(0.05)

def jeu(name1,name2, choixmap):
    # procédure principale du programme
    global continuer, Jcolision, fond, J1, J2, fenetre, wall, wallOnlyUp, piege, g, flag, playing, tir, murbonus, pos_bonus, score
    pygame.display.init()
    continuer = 1
    murbonus = 20
    g = 9.81 - 0.1
    flag = [False,False]


    #définit la fenètre
    fenetre = pygame.display.set_mode((1080, 680))

    #charge le fond
    fond = pygame.image.load("img/background.jpg").convert()
    fenetre.blit(fond, (0,0))

    #charge les images des mur dans une liste
    mur = []
    mur.append(pygame.image.load("img/0.png").convert_alpha())
    mur.append(pygame.image.load("img/mur_bois.png").convert_alpha())
    mur.append(pygame.image.load("img/mur_brick.png").convert_alpha())
    mur.append(pygame.image.load("img/mur_pierre.png").convert_alpha())
    mur.append(pygame.image.load("img/mur_planche.png").convert_alpha())
    mur.append(pygame.image.load("img/2.png").convert_alpha())
    mur.append(pygame.image.load("img/3.png").convert_alpha())
    mur.append(pygame.image.load("img/4.png").convert_alpha())
    murbonus_avc_image=pygame.image.load("img/5.png").convert_alpha()

    vie = []
    vie.append(pygame.image.load("img/vie1.png").convert_alpha())
    vie.append(pygame.image.load("img/vie2.png").convert_alpha())
    vie.append(pygame.image.load("img/vie3.png").convert_alpha())

    # creation des deux objet J1 et J2 de classe personnage
    J1 = personnage([pygame.image.load("img/perso22.gif").convert_alpha(), pygame.image.load("img/perso21.gif").convert_alpha(), pygame.image.load("img/perso22C.gif").convert_alpha(), pygame.image.load("img/perso21C.gif").convert_alpha()])
    J1.name = name1
    J1.tag = 0
    J1.pos = J1.pos.move(40,40)
    J1.nopS = J1.pos
    J1.touche = [K_w, K_a, K_d, K_s, K_c]

    J2 = personnage([pygame.image.load("img/perso2.gif").convert_alpha(),pygame.image.load("img/perso1.gif").convert_alpha(),pygame.image.load("img/perso2C.gif").convert_alpha(),pygame.image.load("img/perso1C.gif").convert_alpha()])
    J2.name = name2
    J2.tag = 1
    J2.pos = J2.pos.move(1000,40)
    J2.nopS = J2.pos
    J2.touche = [K_UP, K_LEFT, K_RIGHT, K_DOWN, K_m]

    J1.enemyName = J2.name
    J2.enemyName = J1.name

    # charge l'image du projéctile


    #importation de la carte
    listeF = open("liste.txt","r")
    liste = listeF.readlines()
    listeF.close()
    rand = randrange(0,len(liste))
##    maptxt=open("save/"+liste[rand][:-1]+".txt","r")
##    maptxt=open("save/"+input("map à charger")+".txt","r")
    maptxt=open("save/"+choixmap+".txt","r")
    Map=maptxt.readlines()
    maptxt.close()

    # transformation de la liste en une matrice
    for i in range (0,16):
        Map[i] = Map[i].split("|") # Map[ligne][collone]

    # place à l'aide de la matrice les blocs
    wall = []
    wallOnlyUp = []
    piege = []
    wallbonus = []
    haveBonus = False
    for i in range (0,27):              #collone
        for j in range (0,16):          #ligne
            if int(Map[j][i]) == 1:
                wall.append(pygame.Rect(i*40,j*40,40,40))
                fenetre.blit(mur[int(Map[j][i])], (i*40,j*40))
            elif int(Map[j][i]) == 2:
                wall.append(pygame.Rect(i*40,j*40,40,40))
                fenetre.blit(mur[int(Map[j][i])], (i*40,j*40))
            elif int(Map[j][i]) == 3:
                wall.append(pygame.Rect(i*40,j*40,40,40))
                fenetre.blit(mur[int(Map[j][i])], (i*40,j*40))
            elif int(Map[j][i]) == 4:
                wall.append(pygame.Rect(i*40,j*40,40,40))
                fenetre.blit(mur[int(Map[j][i])], (i*40,j*40))
            elif int(Map[j][i]) == 5:
                wallOnlyUp.append(pygame.Rect(i*40,j*40,40,10))
                fenetre.blit(mur[int(Map[j][i])], (i*40,j*40))
            elif int(Map[j][i]) == 6 :
                piege.append(pygame.Rect(i*40,(j*40)+35,40,5))
                fenetre.blit(mur[int(Map[j][i])], (i*40,j*40))
            elif int(Map[j][i]) == 7 :
                pos_bonus=[pygame.Rect(i*40,j*40,40,40)]
                fenetre.blit(mur[int(Map[j][i])], (i*40,j*40))
                haveBonus = True

    def apparition_bonus():
        global type_bonus, pos_bonus
        global murbonus
        global continuer
        while continuer==1:
            time.sleep(0.5)
            if murbonus>=1:murbonus = murbonus-1
            else:
                type_bonus=randrange(1,5)
                murbonus = -1


    pygame.display.flip()
    ecran = pygame.display.get_surface().copy()     # prend une capture d'écran du fond avec les bloc placé

    pygame.key.set_repeat(1,650)        # paramètre le delais entre chaque répétition de touche

    # lance les fonction en // du programme

    if haveBonus: Thread(target = apparition_bonus, args=()).start()
    else:
        pos_bonus=[pygame.Rect(-10,-40,1,1)]
        murbonus = 1
    Thread(target = personnage.sautF, args=(J1,)).start()
    Thread(target = personnage.sautF, args=(J2,)).start()
    Thread(target = personnage.evenement, args=(J1,)).start()
    Thread(target = personnage.evenement, args=(J2,)).start()
    Thread(target = personnage.animation, args=(J1,)).start()
    Thread(target = personnage.animation, args=(J2,)).start()

##    Thread(target = GIF, args=()).start()

    # boucle de recoloage et de fermeture de la fenètre
    while continuer== 1:
        time.sleep(0.002)


        for event in pygame.event.get():

            if event.type == QUIT:          #si l'évenement est la fermeture de la fenètre alors on fini la partit
                continuer = 0
                score["stop"] = 1

    	# on recolle les image à leur bonne position
        fenetre.blit(ecran,(0,0))
        if murbonus == -1 :
            fenetre.blit(murbonus_avc_image,pos_bonus[0])
        fenetre.blit(vie[J1.hp-1],(40,10))
        fenetre.blit(vie[J2.hp-1],(1000,10))
        fenetre.blit(J1.listeActiveImage[J1.D1 + J1.anim], J1.pos)
        fenetre.blit(J2.listeActiveImage[J2.D1 + J2.anim], J2.pos)
        for k in J1.tir:
            fenetre.blit(k.image,k.pos)
        for k in J2.tir:
            fenetre.blit(k.image,k.pos)

        # on rafraichie la fenètre
        pygame.display.flip()

    time.sleep(0.3)
    pygame.display.quit()
    time.sleep(0.8)

def maping():
    #outil de création de carte
    pygame.init()
    continuer = 1
    selected_type = 1

    #définit la fenètre
    fenetre = pygame.display.set_mode((1080, 680))

    #charge le fond
    fond = pygame.image.load("img/background.jpg").convert()
    fenetre.blit(fond, (0,0))

    #charge les images des mur dans une liste
    mur = []
    mur.append(pygame.image.load("img/0b.png").convert_alpha())
    mur.append(pygame.image.load("img/mur_bois.png").convert_alpha())
    mur.append(pygame.image.load("img/mur_brick.png").convert_alpha())
    mur.append(pygame.image.load("img/mur_pierre.png").convert_alpha())
    mur.append(pygame.image.load("img/mur_planche.png").convert_alpha())
    mur.append(pygame.image.load("img/2.png").convert_alpha())
    mur.append(pygame.image.load("img/3.png").convert_alpha())
    mur.append(pygame.image.load("img/4.png").convert_alpha())

    murbonus_avc_image=pygame.image.load("img/5.png").convert_alpha()

    #importation de la carte
    listeF = open("liste.txt","r")
    liste = listeF.readlines()
    listeF.close()
    rand = randrange(0,len(liste))
##    maptxt=open("save/"+liste[rand][:-1]+".txt","r")
    maptxt=open("save/"+input("map à charger")+".txt","r")
##    maptxt=open("save/test3.txt","r")
    Map=maptxt.readlines()
    maptxt.close()

    # transformation du fichier texte en une matrice
    for i in range (0,16):
        Map[i] = Map[i].split("|") # Map[ligne][collone]

    # place à l'aide de la matrice les blocs
    wall = []
    piege = []
    wallbonus = []
    for i in range (0,27):              #collone
        for j in range (0,16):          #ligne
            if int(Map[j][i]) == 1:
                wall.append(pygame.Rect(i*40,j*40,40,40))
                fenetre.blit(mur[int(Map[j][i])], (i*40,j*40))
            elif int(Map[j][i]) == 2:
                wall.append(pygame.Rect(i*40,j*40,40,40))
                fenetre.blit(mur[int(Map[j][i])], (i*40,j*40))
            elif int(Map[j][i]) == 3:
                wall.append(pygame.Rect(i*40,j*40,40,40))
                fenetre.blit(mur[int(Map[j][i])], (i*40,j*40))
            elif int(Map[j][i]) == 4:
                wall.append(pygame.Rect(i*40,j*40,40,40))
                fenetre.blit(mur[int(Map[j][i])], (i*40,j*40))
            elif int(Map[j][i]) == 5:
                wall.append(pygame.Rect(i*40,j*40,40,10))
                fenetre.blit(mur[int(Map[j][i])], (i*40,j*40))
            elif int(Map[j][i]) == 6 :
                piege.append(pygame.Rect(i*40,(j*40)+35,40,5))
                fenetre.blit(mur[int(Map[j][i])], (i*40,j*40))
            elif int(Map[j][i]) == 7 :
                pos_bonus=[pygame.Rect(i*40,j*40,40,40)]
                fenetre.blit(mur[int(Map[j][i])], (i*40,j*40))


    pygame.key.set_repeat(1,650)        # paramètre le delais entre chaque répétition de touche

    # boucle de gestion des évenements et recolage
    while continuer== 1:
        for event in pygame.event.get():   #On parcours les evenement reçu
            if event.type == QUIT:     #Si l'evenement est la fermeture de la fenètre
                continuer = 0    #On ferme la fenètre
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    xevent = event.pos[0]//40               #on regarde dans quelle case la personne clique
                    yevent = event.pos[1]//40
                    if xevent >= 0 and xevent <= 26 and yevent >=0 and yevent <=15: #on vérifie qu'il a bien cliquer dans la carte
                        Map[yevent][xevent] = selected_type
                if event.button == 3:
                    xevent = event.pos[0]//40
                    yevent = event.pos[1]//40
                    if xevent >= 0 and xevent <= 26 and yevent >=0 and yevent <=15:
                        Map[yevent][xevent] = 0
            if event.type == KEYDOWN:
                if event.key == K_s:                                                        #si on appuis sur "s"
                    fichiersauvgarde = input("entrez le nom de la sauvegarde sans le .txt") #on demande le nom dans lequelle on veut sauvgardé la carte
                    save=open("save/"+fichiersauvgarde+".txt","w")      #on ouvre le fichier ou a defaut on le crée
                    for  j in range (0,16):                     #on sauvgarde la matrice ds le fichier crée ou modifie
                        for i in range (0,27):
                            save.write(str(Map[j][i])+"|")
                        save.write("\n")
                    save.close()

                    listeF = open("liste.txt","r")           # on rajoute la carte a la liste des cartes
                    liste = listeF.readlines()
                    listeF.close()
                    marqueur = True
                    for i in range(0,len(liste)):                   #on regarde si elle y est deja
                        if liste[i] == fichiersauvgarde + "\n":
                            liste[i] = fichiersauvgarde + "\n"
                            marqueur = False
                    if marqueur:
                        liste.append(fichiersauvgarde+"\n")         #si elle ne l'est pas on la rajoute
                    listeF = open("liste.txt","w")
                    for i in range(0,len(liste)):
                        listeF.write(liste[i])

                if event.key == K_F1:
                    selected_type = 1
                if event.key == K_F2:
                    selected_type = 2
                if event.key == K_F3:
                    selected_type = 3
                if event.key == K_F4:
                    selected_type = 4
                if event.key == K_F5:
                    selected_type = 5
                if event.key == K_F6:
                    selected_type = 6
                if event.key == K_F7:
                    selected_type = 7

    	# on recolle les images à leur bonne position
        fenetre.blit(fond, (0,0))
        for i in range (0,27):
            for j in range (0,16):
                fenetre.blit(mur[int(Map[j][i])], (i*40,j*40))
        fenetre.blit(mur[selected_type],(520,640))

        # on rafraichie la fenètre
        pygame.display.flip()

    pygame.quit()

def parametre():
    global score, name1, name2, score, musique
    def retour_menu():
        MParametre.pack_forget()
        menu.pack()
    def avancer_choix_map():
        global name1, name2, score, obj, score, premierRound, musique
        def lancement(carte):
            global name1, name2, obj, score, premierRound, musique
            def retour_menu():
                global musique
                if musique:
                    pygame.mixer.quit()
                fin_de_jeu.pack_forget()
                menu.pack()
            if premierRound:
                J1=nomJ1.get()
                name1=J1
                J2=nomJ2.get()
                name2=J2
                obj=nbderound.get()
                premierRound = False
                if musique:
                    pygame.mixer.init()
                    pygame.mixer.music.load("musique.mp3")
                    pygame.mixer.music.play()
                MMap.forget()
                fen.lower()
                score = {name1:0,name2:0,"stop":0}
            jeu(name1, name2, carte)
            obj = int(obj)
            ajout_score = ""
            if score[name2] == obj:
                fin_de_jeu = Frame(fen)
                fin_de_jeu.pack()
                l = Label(fin_de_jeu,text=name1+" à gagner la partie", font = "Arial 20")
                l.pack()
                br = Button(fin_de_jeu, text="retour au menu", command=retour_menu)
                br.pack()
                ajout_score = name2
                fen.focus_force()
            elif score[name1] == obj:
                fin_de_jeu = Frame(fen)
                fin_de_jeu.pack()
                l = Label(fin_de_jeu,text=name2+" à gagner la partie", font = "Arial 20")
                l.pack()
                br = Button(fin_de_jeu, text="retour au menu", command=retour_menu)
                br.pack()
                ajout_score = name2
                fen.focus_force()
            elif score["stop"] == 1:
                fin_de_jeu = Frame(fen)
                fin_de_jeu.pack()
                l = Label(fin_de_jeu,text="partie arreter", font = "Arial 20")
                l.pack()
                br = Button(fin_de_jeu, text="retour au menu", command=retour_menu)
                br.pack()
                fen.focus_force()
            else:
                lancement(carte)
            if ajout_score != "" :
                scoresF = open("scores.txt","r")
                meilleurScore = scoresF.readlines()
                scoresF.close()

                t = True
                for i in range(0,len(meilleurScore)):
                    meilleurScore[i] = meilleurScore[i].split(":")

                for i in range(0,len(meilleurScore)):
                    if ajout_score == meilleurScore[i][0]:
                        meilleurScore[i][1] = str(int(meilleurScore[i][1]) + 1)
                        t = False
                if t: meilleurScore.append([ajout_score,"1"])


                meilleurScore = trifusion.tri_fusion(meilleurScore)
                scoresF = open("scores.txt","w")
                for i in range(0,len(meilleurScore)):
                    scoresF.write(meilleurScore[i][0]+":"+meilleurScore[i][1]+":\n")
                scoresF.close()


        def retour_parametre():
            MMap.pack_forget()
            MParametre.pack()
        def choixmapr():
            listeF = open("liste.txt","r")
            liste = listeF.readlines()
            listeF.close()
            rand = randrange(0,len(liste))
            lancement(liste[rand][:-1])
        def choixmap1():
            lancement("1")
        def choixmap2():
            lancement("2")
        def choixmap3():
            lancement("3")
        def choixmap4():
            lancement("4")
        def choixmap5():
            lancement("5")
        MParametre.pack_forget()
        MMap= Frame(fen)
        MMap.pack()
        premierRound = True
        bmapr=Button(MMap,image=carter ,command=choixmapr)
        bmapr.grid(column=3,row=0)
        bmap1=Button(MMap,image=carte1 ,command=choixmap1)
        bmap1.grid(column=0,row=1)
        bmap2=Button(MMap,image=carte2 ,command=choixmap2)
        bmap2.grid(column=3,row=1)
        bmap3=Button(MMap,image=carte3 ,command=choixmap3)
        bmap3.grid(column=5,row=1)
        bmap4=Button(MMap,image=carte4 ,command=choixmap4)
        bmap4.grid(column=2,row=3)
        bmap5=Button(MMap,image=carte5 ,command=choixmap5)
        bmap5.grid(column=4 ,row=3)
    menu.pack_forget()
    MParametre = Frame(fen)
    MParametre.pack()
    j1=Label(MParametre,text="Joueur 1")
    j1.grid(column=0,row=0)
    nomJ1=Entry(MParametre)
    nomJ1.grid(column=1,row=0)
    j2=Label(MParametre,text="Joueur 2")
    j2.grid(column=0,row=1)
    nomJ2=Entry(MParametre)
    nomJ2.grid(column=1,row=1)
    nbround=Label(MParametre,text="Nombre de manche pour gagner")
    nbround.grid(column=0,row=2)
    nbderound=Entry(MParametre)
    nbderound.grid(column=1,row=2)
    bretour = Button(MParametre, text="retour au menu", command=retour_menu)
    bretour.grid(column=0,row=3)
    bmap = Button(MParametre,text="Continuer", command=avancer_choix_map)
    bmap.grid(column=2,row=3)

def fscore():
    def retour_menu():
        MScore.pack_forget()
        menu.pack()
    menu.pack_forget()
    MScore = Frame(fen)
    MScore.pack()

    scoresF = open("scores.txt","r")
    meilleurScore = scoresF.readlines()
    scoresF.close()

    scoreboard = ""
    for i in range(1,len(meilleurScore)):
        if i <= 10:
            meilleurScore[i] = meilleurScore[i].split(":")
            scoreboard = scoreboard + "\n" + meilleurScore[i][0]+": "+meilleurScore[i][1]


    l1 =Label(MScore, text=scoreboard)
    l1.pack()


    b1 = Button(MScore, text="retour", command=retour_menu)
    b1.pack()


def aide():
    def retour_menu():
        aidee.pack_forget()
        menu.pack()
    menu.pack_forget()
    aidee=Frame(fen)
    aidee.pack()
    perso1=Label(aidee, text="Pour le personnage 1 : Avancer vers la gauche = Q , avancer vers la droite = D , sauter = Z , tirer = C")
    perso1.pack()

    perso2=Label(aidee, text="Pour le personnage 2 : Avancer vers la gauche = flèche gauche , avancer vers la droite = flèche droite , sauter = flèche vers le haut , tirer = virgule ")
    perso2.pack()

    b1 = Button(aidee, text="retour", command=retour_menu)
    b1.pack()

def musiqueon():
    global musique
    musique = True
    b6bis.pack_forget()
    b6.pack()

def musiqueoff():
    global musique
    musique = False
    b6.pack_forget()
    b6bis.pack()

def quitter():
    fen.destroy()

    #Menu final

fen=Tk()

son_on_img = PhotoImage(file="img/musique_on.gif")
son_off_img = PhotoImage(file="img/musique_off.gif")
carte1=PhotoImage(file="img/Map1.gif")
carte2=PhotoImage(file="img/Map2.gif")
carte3=PhotoImage(file="img/Map3.gif")
carte4=PhotoImage(file="img/Map4.gif")
carte5=PhotoImage(file="img/Map5.gif")
carter=PhotoImage(file="img/Maprandom.gif")


menu = Frame(fen)
menu.pack()

nom=Label(menu, text="Projet ISN")
nom.pack()

b1=Button(menu, text="Jouer",command=parametre)
b1.pack()

b2=Button(menu, text="Maping",command=maping)
b2.pack()

b3=Button(menu, text="Score",command=fscore)
b3.pack()

b4=Button(menu, text="Aide",command=aide)
b4.pack()

b5=Button(menu, text="Quitter",command=quitter)
b5.pack()

b6=Button(menu, image=son_on_img,command=musiqueoff)

musique = False

b6bis=Button(menu, image=son_off_img,command=musiqueon)
b6bis.pack()

menu.mainloop()










