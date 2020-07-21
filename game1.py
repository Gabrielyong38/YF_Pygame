# -*- coding: utf-8 -*-
"""
Created on Sat Nov 30 17:48:32 2019

@author: user
"""

import pygame
import time
import os
import random

WIN_WIDTH = 800
WIN_HEIGHT = 500

GIRL_IMGS = [pygame.image.load(os.path.join("imgs","girl_run_1.png")), 
             pygame.image.load(os.path.join("imgs","girl_run_5.png")), 
             pygame.image.load(os.path.join("imgs","girl_run_8.png")),
             pygame.image.load(os.path.join("imgs","girl_run_10.png")), 
             pygame.image.load(os.path.join("imgs","girl_run_13.png")),
             pygame.image.load(os.path.join("imgs","girl_run_16.png")), 
             pygame.image.load(os.path.join("imgs","girl_run_20.png"))]
GIRL_FALL_IMG = pygame.image.load(os.path.join("imgs","girl_dead.png"))
BOY_IMGS = [pygame.image.load(os.path.join("imgs","boy_run_1.png")), 
             pygame.image.load(os.path.join("imgs","boy_run_2.png")), 
             pygame.image.load(os.path.join("imgs","boy_run_4.png")),
             pygame.image.load(os.path.join("imgs","boy_run_6.png")), 
             pygame.image.load(os.path.join("imgs","boy_run_8.png")),
             pygame.image.load(os.path.join("imgs","boy_run_10.png")), 
             pygame.image.load(os.path.join("imgs","boy_run_11.png"))]
BOY_FALL_IMG = pygame.image.load(os.path.join("imgs","boy_dead.png"))
CLOUD_IMG = pygame.image.load(os.path.join("imgs","layer04_Clouds_t.png"))
BASE_IMG = pygame.image.load(os.path.join("imgs","layer01_Ground-1.png"))
BG_IMG = pygame.image.load(os.path.join("imgs","platformer_background_4.png"))
NUM_IMGS = [pygame.image.load(os.path.join("imgs","0.png")),
        pygame.image.load(os.path.join("imgs","1.png")),
        pygame.image.load(os.path.join("imgs","2.png")),
        pygame.image.load(os.path.join("imgs","3.png")),
        pygame.image.load(os.path.join("imgs","4.png")),
        pygame.image.load(os.path.join("imgs","5.png")),
        pygame.image.load(os.path.join("imgs","6.png")),
        pygame.image.load(os.path.join("imgs","7.png")),
        pygame.image.load(os.path.join("imgs","8.png")),
        pygame.image.load(os.path.join("imgs","9.png"))]
WELCOME_IMG = pygame.image.load(os.path.join("imgs","welcome.png"))
GAMEOVER_IMG = pygame.image.load(os.path.join("imgs","gameover.png"))

class Girl:
    IMGS = GIRL_IMGS
    ANIMATION_TIME = 7

    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.y2 = WIN_HEIGHT - BASE_IMG.get_height() * 1.3
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]
        self.falling = False

    def jump(self):
        self.vel = -12.5
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1

        d = self.vel * self.tick_count + 1.5 * self.tick_count ** 2

        if d >= 16: # terminal velocity
            d = 16

        if d < 0:
            d -= 2

    def draw(self, win):
        self.img_count += 1
        
       
        if self.falling:
            self.img = GIRL_FALL_IMG
            self.x = WIN_WIDTH//4 - 10
        
        
        else:
            # freeze jumping pose when jumping
            if self.y < self.y2: 
                self.img = self.IMGS[2]
                self.img_count = self.ANIMATION_TIME*2
        
            # complete cycle of girl running
            else:
                if self.img_count < self.ANIMATION_TIME:
                    self.img = self.IMGS[0]
                elif self.img_count < self.ANIMATION_TIME*2:
                    self.img = self.IMGS[1]
                elif self.img_count < self.ANIMATION_TIME*3:
                    self.img = self.IMGS[2]
                elif self.img_count < self.ANIMATION_TIME*4:
                    self.img = self.IMGS[3]
                elif self.img_count < self.ANIMATION_TIME*5:
                    self.img = self.IMGS[4]
                elif self.img_count < self.ANIMATION_TIME*6:
                    self.img = self.IMGS[5]
                elif self.img_count == self.ANIMATION_TIME*6 +1:
                    self.img = self.IMGS[6]
                    self.img_count = 0

        win.blit(self.img, (self.x, self.y)) # draw the girl

    # for collision, mask tells where the pixels are
    def get_mask(self): 
        return pygame.mask.from_surface(self.img)

class Boy:
    IMGS = BOY_IMGS
    VEL = 24 # pipe moving
    ANIMATION_TIME = 7
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.height = 0

        self.img_count = 0
        self.img = self.IMGS[0]

        # if the girl's already passed by the boy, for collision purposes
        self.passed = False

        
    def move(self):
        self.x -= self.VEL
        
    def draw(self,win, girl):
        self.img_count += 1
        
        if girl.falling:
            self.img = BOY_FALL_IMG
            self.VEL = 0
            self.x = girl.x + 90
            #self.y = girl.y - 20
            
        else:    
            # complete cycle of boy running
            if self.img_count < self.ANIMATION_TIME:
                self.img = self.IMGS[0]
            elif self.img_count < self.ANIMATION_TIME*2:
                self.img = self.IMGS[1]
            elif self.img_count < self.ANIMATION_TIME*3:
                self.img = self.IMGS[2]
            elif self.img_count < self.ANIMATION_TIME*4:
                self.img = self.IMGS[3]
            elif self.img_count < self.ANIMATION_TIME*5:
                self.img = self.IMGS[4]
            elif self.img_count < self.ANIMATION_TIME*6:
                self.img = self.IMGS[5]
            elif self.img_count == self.ANIMATION_TIME*6 +1:
                self.img = self.IMGS[6]
                self.img_count = 0
        
        win.blit(self.img, (self.x, self.y))
        
    # on each of these boys, every time move the girl, check if the girl collides with whatever boys on the screen
    def collide(self, girl):
        girl_mask = girl.get_mask()
        boy_mask = pygame.mask.from_surface(self.img)
        
       #check how far away the top left hand corners are from each other 

        boy_offset = (round(self.x - girl.x), round(self.y - girl.y))
        
        any_point = girl_mask.overlap(boy_mask, boy_offset)
        
        
        if any_point:
            return True # which is colliding, then do sth in main loop, make girl die 
        
        return False

class Objects:
     
    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH
        
    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL
        
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH
            
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH 

    def draw(self, win, girl):
        
        if girl.falling:
            self.VEL = 0
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))

class Base(Objects):
    VEL = 14
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG
    
        
class Cloud(Objects):
    VEL = 2
    IMG = CLOUD_IMG
    WIDTH = CLOUD_IMG.get_width()
    
        
class Score:
    
    def __init__(self, score):
        self.score = score
        
    def draw(self, win):
        scoreDigits = [int(x) for x in list(str(self.score))]
        totalWidth = 0 # total width of all numbers to be printed

        for digit in scoreDigits:
            totalWidth += NUM_IMGS[digit].get_width()

        Xoffset = (WIN_WIDTH - totalWidth) / 2

        for digit in scoreDigits:
            win.blit(NUM_IMGS[digit], (Xoffset, WIN_HEIGHT * 0.1))
            Xoffset += NUM_IMGS[digit].get_width()


# welcome message
def show_welcome(win, girl, base, cloud):
    win.blit(BG_IMG, (0,0))
    
    base.draw(win, girl)
    cloud.draw(win, girl)
    
    win.blit(WELCOME_IMG, (0,0))

    girl.draw(win)
    
    pygame.display.update()

#draw the window first and then other elements on top of it
def draw_window(win, girl, boys, base, cloud, scores):
    win.blit(BG_IMG,(0,0)) # draw the background
    
    base.draw(win, girl)
    
    scores.draw(win)
    
    cloud.draw(win, girl)
    
    for boy in boys: 
        boy.draw(win, girl)
    
    girl.draw(win)
    pygame.display.update()

# display highscore and leave it at top right corner of screen
def endScreen():
    global pause, objects, speed, score
    objects = []
    speed = 30
    
    run = True
    while run:
        pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                run == False
        win.blit(BG_IMG, (0,0))
        largeFont = pygame.font.SysFont('comicsans', 80)
        previousScore = largeFont.render('Previous Score' + str(updateFile()), 1, (255,255,255))
        win.blit(previousScore, (W/2 - previousScore.get_width()/2, 200))
        newScore = largeFont.render('Score', + str(score), 1, (255,255,255))
        win.blit(newScore, (W/2 - newScore.get_width()/2, 320))
        pygame.display.update()
        
    score = 0
        
runner = Girl(200,313,64,64)
pygame.time.set_timer(USEREVENT+1,500)
pygame.time.set_timer(USEREVENT+2,random.randrange(2000,3500))
speed = 30            
run = True

pause = 0
fallspeed = 0
objects = []

# game over message    
def show_gameover(win):
    win.blit(GAMEOVER_IMG, (WIN_WIDTH//2 - GAMEOVER_IMG.get_width()//2, WIN_HEIGHT//2 - GAMEOVER_IMG.get_height()//2))
    pygame.display.update()

# saves a list of highscores in external text file
def updateFile():
    f = open('scores.txt', 'r')
    file = f.readlines()
    last = int(file[0])
    
    if last < int(score):
        f.close()
        file = open('scores.txt', 'w')
        file.write(str(score))
        file.close()
        
        return score
    
    return last


# main loop
def main():
    girl = Girl(WIN_WIDTH//5, WIN_HEIGHT - BASE_IMG.get_height() * 1.2) #starting position
    base = Base(WIN_HEIGHT - BASE_IMG.get_height() * 0.7)
    cloud = Cloud(20)
    boys = [Boy(WIN_WIDTH, WIN_HEIGHT - BASE_IMG.get_height() * 1.3)]
    win = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT)) # draw the window
    pygame.display.set_caption("YELLOW FEVER")
    clock = pygame.time.Clock()
    
    score = 0
    
    isJump = False
    jumpCount = 10    

    run = True
    speed = 30
    not_start = True
    
    while run:
        # no of ticks every second
        clock.tick(speed) 
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                
        keys = pygame.key.get_pressed()
        
        if not_start:
            show_welcome(win, girl, base, cloud)
            base.move()
            cloud.move()
            if keys[pygame.K_SPACE]:
                not_start = False
        
        else:
            if not(isJump):
                if keys[pygame.K_SPACE]:
                    isJump = True
                    girl.jump()
            else:
                if jumpCount >= -10:
                    girl.y -= (jumpCount * abs(jumpCount)) * 0.5
                    jumpCount -= 1
                else: 
                    jumpCount = 10
                    isJump = False
            
            add_boy = False
            rem = []
            for boy in boys:
                if boy.collide(girl):
                    girl.falling = True
                
                # checking if the boy is completely off the screen
                if boy.x + boy.img.get_width() < 0:
                    rem.append(boy)
                    
                # as soon as pass the boy, generate new boy
                if not boy.passed and boy.x < girl.x:
                    boy.passed = True
                    add_boy = True
                
                boy.move()
                
            # if girl passes the boy, add score
            if add_boy:
                score += 1
                # distance between boy, randomly generated
                boys.append(Boy(random.randrange(WIN_WIDTH, WIN_WIDTH + 400), WIN_HEIGHT - BASE_IMG.get_height() * 1.3)) 
                
            for r in rem:
                boys.remove(r)
                
            cloud.move()
            base.move()
            
            scores = Score(score)
            
            draw_window(win, girl, boys, base, cloud, scores)
        
        if girl.falling == True:
            show_gameover(win)
            
            if keys[pygame.K_SPACE]:
                girl.falling = False
                main()
        
    pygame.quit()
    os._exit(0)
    quit() # quit the programme as well

main()