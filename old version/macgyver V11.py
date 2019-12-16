from tkinter import *
import random
import time


"""


 ---------------------------------------
|	X	////////////////////////|verbose|
|		////////////////////////| cloke |
|	////////		////	O	|  Pos	|
|				I				|		|
|///////////////////////////////|  Map	|
|-------------------------------|  Map	|
| V 	GAME INFO		 QUIT	|		|
 ---------------------------------------


il génère des parcours de merde quand même......




une petite fonction de back up pour voir comment il dessine le chemin aléatoire,
un petit truc qui ajoute en string les "" color "", ca pourrait etre style,
affiche pendant une demi seconde la solution trouvé,
en rouge si pas bonne
en gris si bonne validé

et générateur d'obstacle

ou de chemins de deception


Ou le generateur de chemin aleatoire genere un chemin a la snake,
puis à la fin, prend deux cases au hasard pour mettre les objectifs

Ou mieux encore, il génere plusieurs chemins, puis place les objectifs

attention au jeu impossible si il place l'ennemi avant l'item secondaire



best idea

il génere le ou les chemin(s)

il génère les obstacles, les autres chemins si il faut

une fois fini, il le parcours une fois pour placer l'item secondaire, puis continu pour
placer le dernier item,
comme ça on sait que le jeu comporte au moins une solution.

il faudrait qu'il mesure le parcours pour mettre les trucs à la fin,
faut pas qu'il les mette au début.


"""

"""
# ------- V17 ------- #

V check all class and all function

main create Window
	>> Window
	
main create Grid
	< in window
	Grid create
		>> Grid
		>> Cases
		>> funct for coordinates
	
main create Path (Path_generator)
	< Grid
	< Cases
	< funct for coord
	>> Path
		>> Pos start (Mac Gyver)
		>> Pos Middle goal
		>> Pos Final Goal

main create Macguver
	< Pos start
	< Cases
	>> MacGiver
		> sac

main create middle
	< Pos Middle
	< Cases
	>> Middle Goal

main create final goal
	< Final goal
	< Cases
	>> Final Goal
	
main create ball
	>> ball

main START MAIN GAME
	while playing :
		ball is moving
		if mac gyver touch wall case -> cant move in this direction
		if mac gyver touch free case -> move to this direction
		if mac gyver touch middle goal -> middle goal in backpack + move to this pos
		if mac gyver touch final goal WITHOUT middle goal -> GAME OVER
		if mac gyver touch final goal WITH middle goal -> WIN
		if ball touch macgyver -> HIT
			if 5 HIT > GAME OVER
		if quit -> playong = False
		
		Update all graphic interface
"""

class V


class Window


class Grid


class Case


class Path Generator


class MacGyver


class Ball