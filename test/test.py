from tkinter import *
import keyboard
from PIL import Image, ImageTk
import math


hauteur = 600
largeur = 1000

lObstacles = [[200, 80, largeur - 200, 100], [20, 220, 120, 240], [largeur - 120, 220, largeur - 20, 240]]


##texture  nombre de sauts    hauteur de saut   multiplicateur Vitesse     fonction de kb     puissance d'attaque
L = [["pass", 2, 4, 1, math.sqrt, 1]]
projectiles = []
tremblements = 0

class objet():
    def __init__(self, px, py, i):
        self.x = px
        self.y = py
        self.xInit = px
        self.yInit = py
        self.coteInit = 0
        self.vx = 0
        self.vy = 0
        self.cx = 0
        self.cid = i
        self.hauteur = 70
        self.largeur = 20
        self.sauts = 0
        self.delai = 20
        self.protec = 100
        self.prot = False
        self.temps = 0
        self.cote = 0
        self.kbMult = 1
        self.attaqueT = 0
        self.maint = False
        self.projT = 0
        self.cInit = 0

    def sautsMax(self):
        return L[self.cid][1]

    def multAttaque(self):
        return L[self.cid][5]

    def puissanceSaut(self):
        return L[self.cid][2]

    def multVitesse(self):
        return L[self.cid][3]

    def maj(self):
        for obstacle in lObstacles:
            if abs(obstacle[0] - self.x) < self.largeur / 2 or abs(obstacle[2] - self.x) < self.largeur / 2 or (self.x >= obstacle[0] and self.x <= obstacle[2]):
                if obstacle[3] > self.y + self.vy and obstacle[3]-0.1 <= self.y:
                    if self.vy < 0:
                        self.vy = 0
                        self.y = obstacle[3]
                    self.sauts = self.sautsMax()
                    self.delai = 50
                    self.vx *= 0.7
                    self.cx *= 0.7
                    
        self.y += self.vy
        self.x += self.vx + self.cx

        if self.y < -hauteur:
            self.reapparait()

        if self.vy != 0:
            self.delai -= 1

        if self.projT > 0:
            self.projT -= 1
            
        self.temps += 1
        self.vy -= 0.05
        self.vy *= 0.997
        self.vx *= 0.99
        self.cx *= 0.99
        if self.attaqueT > 0:
            self.attaqueT -= 1

    def attaque(self, autre):
        if self.attaqueT == 0 and not self.maint:
            self.attaqueT = 20
            if abs(autre.y - self.y) < self.hauteur:
                if abs(autre.x - (self.x + self.cote * 30)) < 30:
                    autre.degats(self, 10 * self.multAttaque())
        self.maint = True

    def attaqueProj(self, autre):
        if not self.maint:
            autre.degats(self, 10 * self.multAttaque())
        self.maint = True

    def degats(self, autre, n):
        global tremblements
        if self.protec > 0 and self.prot:
            self.protec -= n
        else:
            d = math.sqrt((self.x - autre.x) ** 2 + (self.y - autre.y) ** 2)
            dx = autre.cote * n * (1 + L[self.cid][4](self.kbMult)) * 2
            dy = 0
            tremblements = int(2 * math.pi / 0.3)
            if d != 0:
                dx = (autre.x - self.x) / d * n * (1 + L[self.cid][4](self.kbMult)) * 0.2
                dy = 1##(autre.y - self.y) / d * n * (1 + L[self.cid][4](self.kbMult)) * 0.05 + 1.5
            self.cx = -dx
            self.vy += dy
            self.kbMult += (1 + 20 * n / 100)
                

    def reapparait(self):
        self.x = self.xInit
        self.y = self.yInit
        self.vx = 0
        self.vy = 0
        self.cx = 0
        self.hauteur = 70
        self.largeur = 20
        self.sauts = 0
        self.delai = 20
        self.protec = 100
        self.prot = False
        self.temps = 0
        self.cote = self.cInit
        self.kbMult = 1
        self.attaqueT = 0
        self.maint = False

    def essaieSauter(self):
        if self.sauts > 0 and self.delai <= 0:
            self.vy = self.puissanceSaut()
            self.sauts -= 1
            self.delai = 50
        elif self.sauts == self.sautsMax():
            self.vy = self.puissanceSaut()
            self.sauts -= 1

    def animation(self):
        t = (self.temps // 5) % 5
        s = ""
        if self.cote == -1:
            s = "_m"
        if self.attaqueT > 0:
            return L[self.cid][0] + "/hit" + s
        elif abs(self.vx) > 0.1 and self.vy <= 0 and self.vy > -0.2:
            return L[self.cid][0] + "/course_" + str(t) + s
        elif self.vx != 0 and self.vy > 0:
            return L[self.cid][0] + "/saut" + s
        elif abs(self.vy) < 0.1 and self.prot and self.protec > 0:
            return L[self.cid][0] + "/prot" + s
        elif self.vy < -0.2:
            return L[self.cid][0] + "/chute" + s
        else:
            return L[self.cid][0] + "/rien" + s


def chargeSprites():
    d = {}
    listeS = []
    for i in range(len(L)):
        listeS.append(L[i][0] + "/hit")
        listeS.append(L[i][0] + "/course_0")
        listeS.append(L[i][0] + "/course_1")
        listeS.append(L[i][0] + "/course_2")
        listeS.append(L[i][0] + "/course_3")
        listeS.append(L[i][0] + "/course_4")
        listeS.append(L[i][0] + "/saut")
        listeS.append(L[i][0] + "/prot")
        listeS.append(L[i][0] + "/chute")
        listeS.append(L[i][0] + "/rien")
        listeS.append(L[i][0] + "/proj")
    
    listeS.append("base/prot1")
    listeS.append("base/prot2")
    
    for spr in listeS:
        d[spr] = ImageTk.PhotoImage(Image.open(spr + ".png", mode="r").resize((48,96)))
        d[spr + "_m"] = ImageTk.PhotoImage(Image.open(spr + ".png", mode="r").resize((48,96)).transpose(Image.FLIP_LEFT_RIGHT))
    return d

class proj():
    def __init__(self, x, y, vx, vy, grav, taille, lanceur):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.grav = grav
        self.taille = taille
        self.lanceur = lanceur
        self.aDetruire = False
        self.temps = 0

    def miseAJour(self, joueurs):

        for j in joueurs:
            if j != self.lanceur and abs(j.x - self.x) < self.taille and (j.y - self.taille / 2) < self.y < (j.y + j.hauteur + self.taille / 2):
                self.lanceur.attaqueProj(j)
                self.aDetruire = True
        if self.temps > 10000:
            self.aDetruire = True
            
        self.x += self.vx
        self.y += self.vy
        self.vy -= self.grav
        self.temps += 1
                
                        

joueur2 = objet(300, 300, 0)
joueur1 = objet(largeur-300, 300, 0)
joueur2.cInit = 1
joueur1.cInit = -1
joueur2.cote = 1
joueur1.cote = -1

tk = Tk()

dessin = Canvas(tk, height = hauteur, width = largeur, bg = 'white')
dessin.pack()

sprites = chargeSprites()

def miseAJourGlob():
    global sprites, tremblements, projectiles
    dessin.delete("scene")
    joueur1.maj()
    joueur2.maj()
    
    freq = 0.3
    ampl = 5
    
    for obs in lObstacles:
        dessin.create_rectangle(obs[0] + ampl * math.asin(math.sin(tremblements * freq)), hauteur-obs[1], obs[2] + ampl * math.asin(math.sin(tremblements * freq)), hauteur-obs[3], fill="black", tags="scene")

    dessin.create_image(joueur1.x + ampl * math.asin(math.sin(tremblements * freq)), hauteur-joueur1.y-joueur1.hauteur / 2, image = sprites[joueur1.animation()], tags="scene")
    if joueur1.prot and joueur1.protec > 0:
        dessin.create_image(joueur1.x + ampl * math.asin(math.sin(tremblements * freq)), hauteur-joueur1.y-joueur1.hauteur / 2, image = sprites["base/prot1"], tags="scene")
    
    dessin.create_image(joueur2.x + ampl * math.asin(math.sin(tremblements * freq)), hauteur-joueur2.y-joueur2.hauteur / 2, image = sprites[joueur2.animation()], tags="scene")

    if joueur2.prot and joueur2.protec > 0:
        dessin.create_image(joueur2.x + ampl * math.asin(math.sin(tremblements * freq)), hauteur-joueur2.y-joueur1.hauteur / 2, image = sprites["base/prot2"], tags="scene")

    for p in projectiles:
        dessin.create_image(p.x + ampl * math.asin(math.sin(tremblements * freq)), hauteur-p.y, image = sprites[L[p.lanceur.cid][0] + "/proj"], tags="scene")
        p.miseAJour([joueur1, joueur2])
        if p.aDetruire:
            projectiles.remove(p)

    if tremblements > 0:
        tremblements -= 1
        
    if keyboard.is_pressed("down"):
        joueur1.prot = True
    else:
        joueur1.prot = False
        if keyboard.is_pressed("right"):
            joueur1.vx = 3 * joueur1.multVitesse()
            joueur1.cote = 1
            if joueur1.cx < 0:
                joueur1.cx += 0.05
        if keyboard.is_pressed("left"):
            joueur1.vx = -3 * joueur1.multVitesse()
            joueur1.cote = -1
            if joueur1.cx > 0:
                joueur1.cx -= 0.05
        if keyboard.is_pressed("up"):
            joueur1.essaieSauter()
        if keyboard.is_pressed("space"):
            joueur1.attaque(joueur2)
        else:
            joueur1.maint = False

    if keyboard.is_pressed("s"):
        joueur2.prot = True
    else:
        joueur2.prot = False
        if keyboard.is_pressed("d"):
            joueur2.vx = 3 * joueur2.multVitesse()
            joueur2.cote = 1
            if joueur2.cx < 0:
                joueur2.cx += 0.05
        if keyboard.is_pressed("q"):
            joueur2.vx = -3 * joueur2.multVitesse()
            joueur2.cote = -1
            if joueur2.cx > 0:
                joueur2.cx -= 0.05
        if keyboard.is_pressed("z"):
            joueur2.essaieSauter()
        if keyboard.is_pressed("r"):
            joueur2.attaque(joueur1)
        if keyboard.is_pressed("e") and joueur2.attaqueT <= 0 and joueur2.projT <= 0:
            joueur2.projT = 200
            joueur2.attaqueT = 20
            projectiles.append(proj(joueur2.x, joueur2.y + joueur2.hauteur / 2, joueur2.cote * 4, 1.5, 0.06, 32, joueur2))
        if keyboard.is_pressed("enter") and joueur1.attaqueT <= 0 and joueur1.projT <= 0:
            joueur1.projT = 200
            joueur1.attaqueT = 20
            projectiles.append(proj(joueur1.x, joueur1.y + joueur1.hauteur / 2, joueur1.cote * 4, 1.5, 0.06, 32, joueur1))
        else:
            joueur2.maint = False
        
    dessin.after(5, miseAJourGlob)
        
dessin.after(5, miseAJourGlob)

tk.mainloop()
    
