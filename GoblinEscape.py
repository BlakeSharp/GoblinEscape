#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame
import sys
import math

from pygame.constants import K_BACKSPACE

width = 520
height = 360

# radius of the lake
radius = height / 2.5
goblin = 0.0
boatx = 0.1
boaty = 0.0
bspeed = 1.00
gspeeds = [
	2.5,
	3.0,
	3.5,
	4.0,
	4.2,
	4.4,
	4.6,
	8.0,
	10.0
	]
gspeed_ix = 0
speed_mult = 3.0
wasd = False
# game click

clicking = False

# main menu click

click = False
Shape = None
goblinx = 97.5
gobliny = 0.0

pygame.init()
window = pygame.display.set_mode((width, height))
pygame.display.set_caption('Goblin Game')

def draw_text(
	text,
	font,
	color,
	surface,
	x,
	y,
	):
	textobj = font.render(text, 1, color)
	textrect = textobj.get_rect()
	textrect.topleft = (x, y)
	surface.blit(textobj, textrect)


def main_menu():

	while True:
		font = pygame.font.SysFont('Corbel', 50)
		window.fill((222, 232, 252))
		draw_text(
			'MAIN MENU',
			font,
			(115, 151, 193),
			window,
			width / 2 - 90,
			20,
			)
		(mx, my) = pygame.mouse.get_pos()
		font = pygame.font.SysFont('Corbel', 30)
		button_1 = pygame.Rect(65, 110, 150, 75)
		button_2 = pygame.Rect(65, 210, 150, 75)
		button_3 = pygame.Rect(315, 110, 150, 75)
		button_4 = pygame.Rect(315, 210, 150, 75)
		global shape
		if button_1.collidepoint((mx, my)):
			if click:
				shape = 'circle'
				circleGame()
		if button_2.collidepoint((mx, my)):
			if click:
				shape = 'square'
				squareGame()
		if button_3.collidepoint((mx, my)):
			if click:
				shape = 'triangle'
				TriGame()
		if button_4.collidepoint((mx, my)):
			if click:
				helpmenu()
		pygame.draw.rect(window, (115, 151, 193), button_1)
		pygame.draw.rect(window, (115, 151, 193), button_2)
		pygame.draw.rect(window, (115, 151, 193), button_3)
		pygame.draw.rect(window, (115, 151, 193), button_4)
		pygame.draw.circle(window, (70, 70, 91), (140, 148), 30)
		pygame.draw.polygon(surface=window, color=(70, 70, 91),
							points=[(430, 170), (390, 120), (350, 170)])
		pygame.draw.polygon(surface=window, color=(70, 70, 91),
							points=[(110, 217), (170, 217), (170, 277),
							(110, 277)])
		font = pygame.font.SysFont('Corbel', 50)
		draw_text(
			'HELP',
			font,
			(70, 70, 91),
			window,
			345,
			232,
			)

		click = False
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					click = True

		pygame.display.update()


def restart():
	global goblin, boatx, boaty, clicking, gobliny, goblinx
	goblin = 0.0
	boatx = 0.1
	boaty = 0.0
	gobliny = 0
	goblinx = 97.5
	clicking = False

def helpmenu():
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit(0)
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_BACKSPACE:
					main_menu()
		font = pygame.font.SysFont('Corbel', 50)
		window.fill((222, 232, 252))
		text = font.render('HELP MENU', 1, (115, 151, 193))
		window.blit(text, (width / 2 - 90,20))
		font = pygame.font.SysFont('Corbel', 30)
		text2 = font.render('W,A,S,D : UP,DOWN,LEFT,RIGHT', 1, (115, 151, 193))
		window.blit(text2, (100,125))
		text3 = font.render('HOLD LEFT CLICK : BOAT FOLLOWS CURSOR', 1, (115, 151, 193))
		window.blit(text3, (35,175))
		text4 = font.render('BACKSPACE : RETURN TO MAIN MENU', 1, (115, 151, 193))
		window.blit(text4, (60,225))
		text4 = font.render('+,- : INCREASE/DECREASE GOBLIN SPEED', 1, (115, 151, 193))
		window.blit(text4, (50,275))
		font = pygame.font.SysFont('Corbel', 15)
		text5 = font.render('THE OBJECTIVE IS TO GET THE BOAT (THE BLACK CIRCLE) TO SHORE ', 1, (115, 151, 193))
		window.blit(text5, (90,70))
		text6 = font.render('(THE LIGHT BLUE REGION) WITHOUT BEING CAUGHT BY THE GOBLIN (THE RED DOT).', 1, (115, 151, 193))
		window.blit(text6, (50,90))
		pygame.display.update()
#(THE LIGHT BLUE REGION) WITHOUT BEING CAUGHT BY THE GOBLIN (THE RED DOT).

##this is all the circle portion of the code
def clearCircle():
	radius_mult = bspeed / gspeeds[gspeed_ix]

	# window color
	window.fill((222, 232, 252))

	# lake circle
	pygame.draw.circle(window, (115, 151, 193), (int(width / 2),
					   int(height / 2)), int(radius * 1.00), 0)

	# inner circle
	pygame.draw.circle(window, (200, 200, 200), (int(width / 2),
					   int(height / 2)), int(radius * radius_mult), 1)


def redrawCircle(draw_text=False, win=False):
	clearCircle()

	# boat circle
	pygame.draw.circle(window, (0, 0, 0), (int(width / 2 + boatx),
					   int(height / 2 + boaty)), 6, 2)

	# goblin circle
	pygame.draw.circle(window, (225, 0, 0), (int(width / 2 + radius
					   * math.cos(goblin)), int(height / 2 + radius
					   * math.sin(goblin))), 6, 0)

	if draw_text:
		font = pygame.font.Font(None, 72)
		if win:
			text = font.render('Escaped!', 1, (255, 255, 255))
		else:
			text = font.render('You Were Eaten', 1, (255, 0, 0))
		textpos = text.get_rect()
		textpos.centerx = window.get_rect().centerx
		textpos.centery = height / 2
		window.blit(text, textpos)

	font = pygame.font.Font(None, 48)
	text = font.render('Goblin Speed: ' + str(gspeeds[gspeed_ix]), 1,
					   (255, 255, 255))
	textpos = text.get_rect()
	textpos.centerx = width / 2
	textpos.centery = height - 20
	window.blit(text, textpos)

	pygame.display.flip()


def updateGoblin():
	global goblin
	gspeed = gspeeds[gspeed_ix]
	newang = math.atan2(boaty, boatx)
	diff = newang - goblin
	if diff < math.pi:
		diff += math.pi * 2.0
	if diff > math.pi:
		diff -= math.pi * 2.0
	if abs(diff) * radius <= gspeed * speed_mult:
		goblin = newang
	else:
		goblin += (gspeed * speed_mult / radius if diff
				   > 0.0 else -gspeed * speed_mult / radius)
	if goblin < math.pi:
		goblin += math.pi * 2.0
	if goblin > math.pi:
		goblin -= math.pi * 2.0


def moveBoat(x, y):
	global boatx, boaty, speed_mult
	dx = x - boatx
	dy = y - boaty
	mag = math.sqrt(dx * dx + dy * dy)
	if mag <= bspeed * speed_mult:
		boatx = x
		boaty = y
	else:
		boatx += bspeed * speed_mult * dx / mag
		boaty += bspeed * speed_mult * dy / mag


def detectWin():
	global gspeed_ix
	if boatx * boatx + boaty * boaty > radius * radius:
		diff = math.atan2(boaty, boatx) - goblin
		if diff < math.pi:
			diff += math.pi * 2.0
		if diff > math.pi:
			diff -= math.pi * 2.0
		while True:
			is_win = abs(diff) > 0.000001
			redrawCircle(True, is_win)
			events = [event.type for event in pygame.event.get()]
			if pygame.QUIT in events:
				sys.exit(0)
			elif pygame.MOUSEBUTTONDOWN in events:
				restart()
				if is_win:
					gspeed_ix += 1
				break


clock = pygame.time.Clock()


def circleGame():
	x = None
	clicking = False
	global speed_mult
	speed_mult = 3.0
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit(0)
			clicking = pygame.mouse.get_pressed()[0]
			if pygame.mouse.get_pressed()[2]:
				restart()
			if event.type == pygame.KEYDOWN:
				global gspeed_ix
				if event.key == pygame.K_BACKSPACE:
					main_menu()
				if event.key == 61 and gspeed_ix < len(gspeeds) - 1:
					gspeed_ix += 1
					restart()
				if event.key == 45 and gspeed_ix > 0:
					gspeed_ix -= 1
					restart()

		if clicking:
			(x, y) = pygame.mouse.get_pos()
			moveBoat(x - width / 2, y - height / 2)
		updateGoblin()
		detectWin()
		redrawCircle()
		clock.tick(60)


##this begins the square portion of the game

def clearSquare():

	# window color

	window.fill((222, 232, 252))

	# lake Square

	pygame.draw.rect(window, (115, 151, 193), pygame.Rect(width / 2 - 100, height / 2 - 100, 200, 200))


def redrawSquare(draw_text=False, win=False):
	clearSquare()

	# boat Square

	pygame.draw.circle(window, (255, 0, 0), (int(width / 2 + boatx), int(height / 2 + boaty)), 6, 2)

	# goblin Square

	pygame.draw.circle(window, (0, 0, 0), (int(width / 2 + goblinx), int(height / 2 + gobliny)), 6, 0)

	if draw_text:
		font = pygame.font.Font(None, 72)
		if win:
			text = font.render('Escaped!', 1, (255, 255, 255))
		else:
			text = font.render('You Were Eaten', 1, (255, 0, 0))
		textpos = text.get_rect()
		textpos.centerx = window.get_rect().centerx
		textpos.centery = height / 2
		window.blit(text, textpos)

	font = pygame.font.Font(None, 48)
	text = font.render('Goblin Speed: ' + str(gspeeds[gspeed_ix]), 1,
					   (255, 255, 255))
	textpos = text.get_rect()
	textpos.centerx = width / 2
	textpos.centery = height - 20
	window.blit(text, textpos)

	pygame.display.flip()


def updateGoblinSquare():
	global boatx, boaty
	gspeed = gspeeds[gspeed_ix]
	#is it closer to a the left or right
	#positive means that it is closer to left or right
	diff = abs(boatx)-abs(boaty)
	global gobliny, goblinx
	if(diff>=0):
		if(boatx>0):
			if(goblinx!=97.5 and abs(gobliny)!=97.5):
				if(boaty>0):gobliny+=gspeed;
				elif(boaty<0):gobliny-=gspeed;
			elif(goblinx!=97.5 and abs(gobliny)==97.5):
				goblinx+=gspeed
			elif(goblinx==97.5):
				if(boaty<gobliny):gobliny-=gspeed;
				elif(boaty>gobliny):gobliny+=gspeed;
		elif(boatx<0):
			if(goblinx!=-97.5 and abs(gobliny)!=97.5):
				if(boaty>0):gobliny+=gspeed;
				elif(boaty<0):gobliny-=gspeed;
			elif(goblinx!=-97.5 and abs(gobliny)==97.5):goblinx-=gspeed;
			elif(goblinx==-97.5):
				if(boaty<gobliny):gobliny-=gspeed;
				elif(boaty>gobliny):gobliny+=gspeed;
	elif(diff<0):
		if(boaty>0):
			if(gobliny!=97.5 and abs(goblinx)!=97.5):
				if(boatx>0):goblinx+=gspeed;
				elif(boatx<=0):goblinx-=gspeed;
			elif(gobliny!=97.5 and abs(goblinx)==97.5):gobliny+=gspeed;
			elif(gobliny==97.5):
				if(boatx<goblinx):goblinx-=gspeed;
				elif(boatx>goblinx):goblinx+=gspeed;
		elif(boaty<0):
			if(gobliny!=-97.5 and abs(goblinx)!=97.5):
				if(boatx>0):goblinx+=gspeed;
				elif(boatx<=0):goblinx-=gspeed;
			elif(gobliny!=-97.5 and abs(goblinx)==97.5):gobliny-=gspeed;
			elif(gobliny==-97.5):
				if(boatx<goblinx):goblinx-=gspeed;
				elif(boatx>goblinx):goblinx+=gspeed;
	if(goblinx>97.5):goblinx = 97.5;
	if(goblinx<-97.5):goblinx = -97.5;
	if(gobliny>97.5):gobliny = 97.5;
	if(gobliny<-97.5):gobliny = -97.5;
	
def detectWinSquare():
	global gspeed_ix
	if abs(boatx) >= 96 or abs(boaty) >= 96:
		diff = boatx - goblinx + boaty - gobliny
		while True:
			is_win = abs(diff) > 10
			redrawSquare(True, is_win)
			events = [event.type for event in pygame.event.get()]
			if pygame.QUIT in events:
				sys.exit(0)
			elif pygame.MOUSEBUTTONDOWN in events:
				restart()
				break


clock = pygame.time.Clock()


def squareGame():
	x = None
	clicking = False
	global speed_mult, gspeed_ix
	speed_mult = 1.5
	
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit(0)
			clicking = pygame.mouse.get_pressed()[0]
			if pygame.mouse.get_pressed()[2]:
				restart()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_BACKSPACE:
					main_menu()
				if event.key == 61 and gspeed_ix < len(gspeeds) - 1:
					gspeed_ix += 1
					restart()
				if event.key == 45 and gspeed_ix > 0:
					gspeed_ix -= 1
					restart()

		if clicking:
			(x, y) = pygame.mouse.get_pos()
			moveBoat(x - width / 2, y - height / 2)
		updateGoblinSquare()
		detectWinSquare()
		redrawSquare()
		clock.tick(60)


##this begins the triangle portion of the game

def clearTri():

	# window color

	window.fill((222, 232, 252))

	# lake Square

	pygame.draw.polygon(surface=window, color=(115, 151, 193), points=[(112,250), (262,75), (412,250)])


def redrawTri(draw_text=False, win=False):
	clearTri()

	# boat Square

	pygame.draw.circle(window, (0, 0, 0), (int(width / 2 + boatx), int(height / 2 + boaty)), 6, 2)

	# goblin Square

	pygame.draw.circle(window, (255, 0, 0), (int(width / 2 + goblinx), int(height / 2 + gobliny)), 6, 0)

	if draw_text:
		font = pygame.font.Font(None, 72)
		if win:
			text = font.render('Escaped!', 1, (255, 255, 255))
		else:
			text = font.render('You Were Eaten', 1, (255, 0, 0))
		textpos = text.get_rect()
		textpos.centerx = window.get_rect().centerx
		textpos.centery = height / 2
		window.blit(text, textpos)

	font = pygame.font.Font(None, 48)
	text = font.render('Goblin Speed: ' + str(gspeeds[gspeed_ix]), 1,
					   (255, 255, 255))
	textpos = text.get_rect()
	textpos.centerx = width / 2
	textpos.centery = height - 20
	window.blit(text, textpos)

	pygame.display.flip()


def updateGoblinTri():
	global boatx, boaty
	gspeed = gspeeds[gspeed_ix]
	#is it closer to a the left or right
	#positive means that it is closer to left or right

	#equation : y = +-31/148(goblinx+-gspeed) - 100
	diff = boaty-abs(boatx)
	global gobliny, goblinx
	print(str(diff) + " diff | boat y " + str(boaty) + " | boat x " + str(boatx) + " | goblin x " + str(goblinx)  + " | gobliny " + str(gobliny))
	if(boaty>0 and diff>-50):
		#if its not on the bottom line
		if(gobliny<70):
			if(goblinx<0):
				goblinx -=gspeed
				gobliny = ((-1.1)*(goblinx))-100
			elif goblinx>=0:
				goblinx +=gspeed
				gobliny = ((1.1)*(goblinx))-100
		if(gobliny>=70 and abs(goblinx-boatx)>5):
			if(boatx>goblinx):
				goblinx+=gspeed
			elif(boatx<goblinx):
				goblinx-=gspeed
	#if the boat is on the left
	if(boatx>0):
		print("thing")


	

	
def detectWinTri():
	global gspeed_ix
	thing = False
	diff = abs(boatx-goblinx) + abs(boaty-gobliny)
	if (boaty>=71) or (boaty<=(1.1)*(boatx)-100 and boatx>=0) or (boaty<=(-1.1)*(boatx)-100 and boatx<0):
		while True:
			is_win = abs(diff) > 10
			redrawTri(True, is_win)
			events = [event.type for event in pygame.event.get()]
			if pygame.QUIT in events:
				sys.exit(0)
			elif pygame.MOUSEBUTTONDOWN in events:
				restart()
				break


clock = pygame.time.Clock()


def TriGame():
	x = None
	clicking = False
	global goblinx, gobliny
	goblinx=1
	gobliny = -100
	global speed_mult, gspeed_ix
	speed_mult = 3.0
	
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit(0)
			clicking = pygame.mouse.get_pressed()[0]
			if pygame.mouse.get_pressed()[2]:
				restart()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_BACKSPACE:
					main_menu()
				if event.key == 61 and gspeed_ix < len(gspeeds) - 1:
					gspeed_ix += 1
					restart()
				if event.key == 45 and gspeed_ix > 0:
					gspeed_ix -= 1
					restart()

		if clicking:
			(x, y) = pygame.mouse.get_pos()
			moveBoat(x - width / 2, y - height / 2)
		updateGoblinTri()
		detectWinTri()
		redrawTri()
		clock.tick(60)


main_menu()
