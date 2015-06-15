import pygame
import sys
from pygame.locals import *






class actor:

    def __init__(self):

        self.attack = 10
        self.defence = 10
        self.max_health = 23
        self.health = self.max_health

    def getAttack(self):
        return self.attack
    
    def getDefence(self):
        return self.defence

    def getHealth(self):
        return self.health

    def getMaxHealth(self):
        return self.max_health

    def displayAttack(self):
        return "Attack: " + str(self.attack)

    def displauDefence(self):
        return "Defence: " + str(self.defence)

    def displayHealth(self):
        return "Health: " + str(self.health) + "/" + str(self.max_health)

    def displayHealthBar(self):
        
        ret = "["
        
        bar = int((float(self.health) / float(self.max_health)) * 10)
        
        if bar == 0 and self.health > 0:
            bar = 1

        for i in range(0, bar):
            ret += "#"
        for i in range(0, 10 - bar):
            ret += " "

        return ret + "]"

    def display(self):
        return "Attack: " + str(self.attack) + " - " + "Defence: " + str(self.defence) + " - " + "Health: " + str(self.health) + "/" + str(self.max_health)

    def takeDamage(self, value):

        self.health -= value

        if self.health < 1:
            self.health = 0
            return True

        return False

    def heal(self, value):

        self.health += value

        if self.health > self.max_health:
            self.health = self.max_health


class button:

    def __init__(self, img, x, y, width, height):

        self.img = img

        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def collides(self, x, y):
        if x >= self.x and x < self.x + self.width and y >= self.y and y < self.y + self.height:
            return True
        return False

    def getImg(self):
        return self.img

    def getCoords(self):
        return self.x, self.y

class StatBox:

    def __init__(self, img, a1, a2, a3):

        self.img = img
        self.a1 = a1
        self.a2 = a2
        self.a3 = a3

    def display(self, x, y):

        text = FONT.render(stats.a1.displayHealthBar(), True, (50, 0, 0))


        Zone.blit(self.img, (x, y))
        Zone.blit(text, (x+20, y+20))


pygame.init()
Zone = pygame.display.set_mode((600, 400))

buttonImg = pygame.image.load("button2.png")
boxImg = pygame.image.load("button.png")

stats = StatBox(boxImg, actor(), actor(), actor())

hpup = button(buttonImg, 10, 50, 123, 50)
hpdown = button(buttonImg, 10, 100, 123, 50)

FONT = pygame.font.SysFont('monospace', 16)

clock = pygame.time.Clock()




while True:



    Zone.fill((0,200,0))
    Zone.blit(hpup.getImg(), hpup.getCoords())
    Zone.blit(hpdown.getImg(), hpdown.getCoords())

    stats.display(10, 200)

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if hpup.collides(x, y):
                stats.a1.heal(4)
            if hpdown.collides(x, y):
                if stats.a1.takeDamage(7):
                    print("You died")

    clock.tick(30)
