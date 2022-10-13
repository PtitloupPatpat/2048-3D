import random as rd
import pygame
import sys

pygame.init()

sizescreen= (weight,length) = (720,480)
screen=pygame.display.set_mode(sizescreen)
police=pygame.freetype.SysFont("Arial",12)

Background=pygame.image.load('2048 Fond.PNG')
touche=pygame.image.load('2048 Touche.PNG')


###On suppose la vue de base comme un cube de dimension cartésien(x,y,z)(respectant la règle de la main droite) avec l'origine positioné sur le coin (bas,gauche,derrière)
#Les fonctions sont définis par rapport à cette vue
#Matrice est le cube
#Les grilles sont les couches supperposer sur l'axe y
#Les lignes sont les rangées posées à la suite sur l'axe z
#Les valeurs des liste sont les cases à la suite sur l'axe x

#Attention les cases ne glissent pas jusqu'à une case vide, elle se déplace d'une case dans la direction choisit (si possible)
# ou fusionne avec la case adjacente si:
                                    # La case adjacente ne se déplace pas en même temps
                                    # Les deux cases ont la même valeur

N=4
Matrice={Y:{Z:[0,0,0,0] for Z in range(0,N)} for Y in range(0,N)}

def testplein(Matrice):
    for y in Matrice:
        for z in Matrice[y]:
            for x in Matrice[y][z]:
                if x==0:return False
    return True

def Ajout(Matrice):
    Ajout=True
    while Ajout:
        x,y,z=rd.randint(0,N-1),rd.randint(0,N-1),rd.randint(0,N-1)
        if Matrice[y][z][x]==0:
            Matrice[y][z][x]=2
            Ajout=False
            print(y,z,x)
    return Matrice

def DeplacementDroite(Matrice):
    for y in Matrice:
        for z in Matrice[y]:
            for x in (3,2,1):
                if Matrice[y][z][x]==0:
                    Matrice[y][z][x]=Matrice[y][z][x-1]
                    Matrice[y][z][x-1]=0
                if Matrice[y][z][x]==Matrice[y][z][x-1]:
                    Matrice[y][z][x]*=2
                    Matrice[y][z][x-1]=0
    return Matrice

def DeplacementGauche(Matrice):
    for y in Matrice:
        for z in Matrice[y]:
            for x in (0,1,2):
                if Matrice[y][z][x]==0:
                    Matrice[y][z][x]=Matrice[y][z][x+1]
                    Matrice[y][z][x+1]=0
                if Matrice[y][z][x]==Matrice[y][z][x+1]:
                    Matrice[y][z][x]*=2
                    Matrice[y][z][x+1]=0
    return Matrice

def DeplacementAvant(Matrice):
    for y in Matrice:
        for z in (3,2,1):
            for x in (0,1,2,3):
                if Matrice[y][z][x]==0:
                    Matrice[y][z][x]=Matrice[y][z-1][x]
                    Matrice[y][z-1][x]=0
                if Matrice[y][z][x]==Matrice[y][z-1][x]:
                    Matrice[y][z][x]*=2
                    Matrice[y][z-1][x]=0
    return Matrice

def DeplacementArriere(Matrice):
    for y in Matrice:
        for z in (0,1,2):
            for x in (0,1,2,3):
                if Matrice[y][z][x]==0:
                    Matrice[y][z][x]=Matrice[y][z+1][x]
                    Matrice[y][z+1][x]=0
                if Matrice[y][z][x]==Matrice[y][z+1][x]:
                    Matrice[y][z][x]*=2
                    Matrice[y][z+1][x]=0
    return Matrice

def DeplacementHaut(Matrice):
    for y in (3,2,1):
        for z in Matrice[y]:
            for x in (0,1,2,3):
                if Matrice[y][z][x]==0:
                    Matrice[y][z][x]=Matrice[y-1][z][x]
                    Matrice[y-1][z][x]=0
                if Matrice[y][z][x]==Matrice[y-1][z][x]:
                    Matrice[y][z][x]*=2
                    Matrice[y-1][z][x]=0
    return Matrice

def DeplacementBas(Matrice):
    for y in (0,1,2):
        for z in Matrice[y]:
            for x in (0,1,2,3):
                if Matrice[y][z][x]==0:
                    Matrice[y][z][x]=Matrice[y+1][z][x]
                    Matrice[y+1][z][x]=0
                if Matrice[y][z][x]==Matrice[y+1][z][x]:
                    Matrice[y][z][x]*=2
                    Matrice[y+1][z][x]=0
    return Matrice

def affichageMatrice(Matrice):
    screen.blit(Background,(120,0))
    screen.blit(police.render('X=0',(255,255,255))[0],(80,20))
    screen.blit(police.render('X=1', (255, 255, 255))[0], (620, 20))
    screen.blit(police.render('X=2', (255, 255, 255))[0], (80, 460))
    screen.blit(police.render('X=3', (255, 255, 255))[0], (620, 460))
    screen.blit(touche,(10,206))
    for y in Matrice:
        grille=(0,0)
        if y==1:grille=(0,1)
        if y==2:grille=(1,0)
        if y==3:grille=(1,1)
        for z in Matrice[y]:
            for x in range(N):
                tplValeur = police.render(str(Matrice[y][z][x]),(0,0,0))
                screen.blit(tplValeur[0],(150+x*60+grille[1]*240,30+z*60+grille[0]*240))
    pygame.display.update()

while testplein(Matrice)==False:
    Matrice=Ajout(Matrice)
    affichageMatrice(Matrice)
    action=True
    while action:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:Matrice=DeplacementDroite(Matrice)
                if event.key == pygame.K_q: Matrice = DeplacementGauche(Matrice)
                if event.key == pygame.K_e: Matrice = DeplacementHaut(Matrice)
                if event.key == pygame.K_a: Matrice = DeplacementBas(Matrice)
                if event.key == pygame.K_s: Matrice = DeplacementAvant(Matrice)
                if event.key == pygame.K_z: Matrice = DeplacementArriere(Matrice)
                action=False