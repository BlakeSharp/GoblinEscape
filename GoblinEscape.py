import pygame, sys, math

from pygame.constants import K_BACKSPACE

#sets the size of the window
width = 520
height = 360
#radius of the lake?
radius = height/2.5
goblin = 0.0
boatx = 0.1 
boaty = 0.0
bspeed = 1.0
gspeeds = [2.5, 3.0, 3.5, 4.0, 4.2, 4.4, 4.6]
gspeed_ix = 0
speed_mult = 3.0
#game click
clicking = False
#main menu click
click = False
Shape = None
goblinx = 97.5
gobliny = 0.0

def draw_text(text, font, color, surface, x, y):
	textobj = font.render(text, 1, color)
	textrect = textobj.get_rect()
	textrect.topleft = (x, y)
	surface.blit(textobj, textrect)

def main_menu():
	
	while True:
		font = pygame.font.SysFont("Corbel", 50)
		window.fill((222, 232, 252))
		draw_text('MAIN MENU', font, (115, 151, 193), window, width/2-90, 20)
 
		mx, my = pygame.mouse.get_pos()
		font = pygame.font.SysFont("Corbel", 30)
		button_1 = pygame.Rect(65, 110, 150, 75)
		button_2 = pygame.Rect(65, 210, 150, 75)
		button_3 = pygame.Rect(315, 110, 150, 75)
		button_4 = pygame.Rect(315, 210, 150, 75)
		global shape
		if button_1.collidepoint((mx, my)):
			if click:
				shape = "circle"
				circleGame()
		if button_2.collidepoint((mx, my)):
			if click:
				shape = "square"
				squareGame()
		if button_3.collidepoint((mx, my)):
			if click:
				shape = "triangle"
		if button_4.collidepoint((mx, my)):
			if click:
				print("later pog")
		pygame.draw.rect(window, (115, 151, 193), button_1)
		pygame.draw.rect(window, (115, 151, 193), button_2)
		pygame.draw.rect(window, (115, 151, 193), button_3)
		pygame.draw.rect(window, (115, 151, 193), button_4)
		pygame.draw.circle(window,(70, 70, 91),(140,148),30)
		pygame.draw.polygon(surface=window, color=(70, 70, 91), points=[(430,170), (390,120), (350,170)])
		pygame.draw.polygon(surface=window, color=(70, 70, 91), points=[(110,217), (170,217), (170,277),(110,277)])
		font = pygame.font.SysFont("Corbel", 50)
		draw_text('HELP', font, (70, 70, 91), window, 345, 232)
 
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
	global goblin, boatx, boaty, clicking
	goblin = 0.0
	boatx = 0.1 
	boaty = 0.0
	clicking = False

pygame.init()
window = pygame.display.set_mode((width, height)) 
pygame.display.set_caption("Goblin Game")


##this is all the circle portion of the code
def clearCircle():
	radius_mult = bspeed / gspeeds[gspeed_ix]
	#window color
	window.fill((222, 232, 252))
	#lake circle
	pygame.draw.circle(window, (115, 151, 193), (int(width/2), int(height/2)), int(radius*1.00), 0)
	#inner circle
	pygame.draw.circle(window, (200,200,200), (int(width/2), int(height/2)), int(radius*radius_mult), 1)

def redrawCircle(draw_text=False,win=False):
	clearCircle()
	#boat circle
	pygame.draw.circle(window, (225, 0, 0), (int(width/2 + boatx),int(height/2 + boaty)), 6, 2)
	#goblin circle
	pygame.draw.circle(window, (0,0,0), (int(width/2 + radius*math.cos(goblin)),int(height/2 + radius*math.sin(goblin))), 6, 0) 

	if draw_text:
		font = pygame.font.Font(None, 72)
		if win:
			text = font.render("Escaped!", 1, (255, 255, 255))
		else:
			text = font.render("You Were Eaten", 1, (255, 0, 0))
		textpos = text.get_rect()
		textpos.centerx = window.get_rect().centerx
		textpos.centery = height/2
		window.blit(text, textpos)

	font = pygame.font.Font(None, 48)
	text = font.render("Goblin Speed: " + str(gspeeds[gspeed_ix]), 1, (255, 255, 255))
	textpos = text.get_rect()
	textpos.centerx = width/2
	textpos.centery = height - 20
	window.blit(text, textpos)
	
	pygame.display.flip()

def updateGoblin():
	global goblin
	gspeed = gspeeds[gspeed_ix]
	newang = math.atan2(boaty, boatx)
	diff = newang - goblin
	if diff < math.pi: diff += math.pi*2.0
	if diff > math.pi: diff -= math.pi*2.0
	if abs(diff)*radius <= gspeed * speed_mult:
		goblin = newang
	else:
		goblin += gspeed * speed_mult / radius if diff > 0.0 else -gspeed * speed_mult / radius
	if goblin < math.pi: goblin += math.pi*2.0
	if goblin > math.pi: goblin -= math.pi*2.0 

def moveBoat(x,y):
	global boatx, boaty
	dx = x - boatx
	dy = y - boaty
	mag = math.sqrt(dx*dx + dy*dy)
	if mag <= bspeed * speed_mult:
		boatx = x
		boaty = y
	else:
		boatx += bspeed * speed_mult * dx/mag
		boaty += bspeed * speed_mult * dy/mag 
	
def detectWin():
	global gspeed_ix
	if boatx*boatx + boaty*boaty > radius*radius:
		diff = math.atan2(boaty, boatx) - goblin
		if diff < math.pi: diff += math.pi*2.0
		if diff > math.pi: diff -= math.pi*2.0
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
				if event.key == 61 and (gspeed_ix<len(gspeeds)-1):
					gspeed_ix +=1
					restart()
				if event.key == 45 and gspeed_ix>0:
					gspeed_ix -=1
					restart()


		if clicking:
			x,y = pygame.mouse.get_pos()
			moveBoat(x - width/2, y - height/2)
		updateGoblin()
		detectWin()
		redrawCircle()
		clock.tick(60)



##this begins the square portion of the game
def clearSquare():
	#window color
	window.fill((222, 232, 252))
	#lake Square
	pygame.draw.rect(window, (115, 151, 193), pygame.Rect(width/2-100, height/2-100, 200, 200))

def redrawSquare(draw_text=False,win=False):
	clearSquare()
	#boat Square
	pygame.draw.circle(window, (255, 0, 0), (int(width/2 + boatx),int(height/2 + boaty)), 6, 2)
	#goblin Square
	pygame.draw.circle(window, (0,0,0), (int(width/2 + goblinx),int(height/2 + gobliny)), 6, 0) 

	if draw_text:
		font = pygame.font.Font(None, 72)
		if win:
			text = font.render("Escaped!", 1, (255, 255, 255))
		else:
			text = font.render("You Were Eaten", 1, (255, 0, 0))
		textpos = text.get_rect()
		textpos.centerx = window.get_rect().centerx
		textpos.centery = height/2
		window.blit(text, textpos)

	font = pygame.font.Font(None, 48)
	text = font.render("Goblin Speed: " + str(gspeeds[gspeed_ix]), 1, (255, 255, 255))
	textpos = text.get_rect()
	textpos.centerx = width/2
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
		if(abs(goblinx)!=97.5):
			print("getting1")
			if(boatx<0):
				goblinx-=gspeed
			else:
				goblinx+=gspeed
		else:
			print("getting2")
			if((abs(gobliny-boaty)>1)):
				if(gobliny<boaty):
					print("getting3")
					
					gobliny+=gspeed
				else:
					print("getting4")
					gobliny-=gspeed
	else:
		if(abs(gobliny)!=97.5):
			print("getting1")
			if(boaty<0):
				gobliny-=gspeed
			else:
				gobliny+=gspeed
		else:
			print("getting2")
			if((abs(goblinx-boatx)>1)):
				if(goblinx<boatx):
					print("getting3")
					
					goblinx+=gspeed
				else:
					print("getting4")
					goblinx-=gspeed
	if(goblinx>97.5):
		goblinx=97.5
	if(gobliny>97.5):
		gobliny=97.5
	if(goblinx<-97.5):
		goblinx=-97.5
	if(gobliny<-97.5):
		gobliny=-97.5

def moveBoat(x,y):
	global boatx, boaty, goblinx, gobliny
	dx = x - boatx
	dy = y - boaty
	mag = math.sqrt(dx*dx + dy*dy)
	if mag <= bspeed * speed_mult:
		boatx = x
		boaty = y
	else:
		boatx += bspeed * speed_mult * dx/mag
		boaty += bspeed * speed_mult * dy/mag 
	
def detectWinSquare():
	global gspeed_ix
	if boatx*boatx + boaty*boaty > radius*radius:
		diff = math.atan2(boaty, boatx) - goblin
		if diff < math.pi: diff += math.pi*2.0
		if diff > math.pi: diff -= math.pi*2.0
		while True:
			is_win = abs(diff) > 0.000001
			redrawSquare(True, is_win)
			events = [event.type for event in pygame.event.get()]
			if pygame.QUIT in events: 
				sys.exit(0)
			elif pygame.MOUSEBUTTONDOWN in events:
				restart()
				if is_win:
					gspeed_ix += 1
				break

clock = pygame.time.Clock()
def squareGame():
	x = None
	clicking = False
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
				if event.key == 61 and (gspeed_ix<len(gspeeds)-1):
					gspeed_ix +=1
					restart()
				if event.key == 45 and gspeed_ix>0:
					gspeed_ix -=1
					restart()


		if clicking:
			x,y = pygame.mouse.get_pos()
			moveBoat(x - width/2, y - height/2)
		updateGoblinSquare()
		detectWinSquare()
		redrawSquare()
		clock.tick(60)

main_menu()
