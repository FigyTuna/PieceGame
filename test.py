import pygame
import sys
from pygame.locals import *




class actor:

    def __init__(self, name):

        self.name = name

        self.attack = 10
        self.defence = 10

        self.hp = Gauge(23)
        self.mp = Gauge(20)

        self.move = []

    def getAttack(self):
        return self.attack
    
    def getDefence(self):
        return self.defence

    def getHealth(self):
        return self.health

    def getMaxHealth(self):
        return self.max_health

    def displayName(self):
        return self.name

    def displayAttack(self):
        return "Attack: " + str(self.attack)

    def displauDefence(self):
        return "Defence: " + str(self.defence)

    def displayHealth(self):
        return "Health: " + str(self.hp.getValue()) + "/" + str(self.hp.getMax)

    def displayMp(self):
        return "MP: " + str(self.mp.getValue()) + "/" + str(self.mp.getMax())

    def addMove(self, m):
        self.move.append(m)



class Gauge:

    def __init__(self, value):

        self.max_value = value
        self.value = self.max_value

    def getValue(self):
        return self.value

    def getMax(self):
        return self.max_value

    def inc(self, value):
        
        self.value += value

        if self.value > self.max_value:
            self.value = self.max_value

    def dec(self, value):

        self.value -= value

        if self.value < 1:
            self.value = 0
            return True

        return False

    def bar(self, size):
        
        ret = "["
        
        bar = int((float(self.value) / float(self.max_value)) * size)
        
        if bar == 0 and self.value > 0:
            bar = 1

        for i in range(0, bar):
            ret += "#"
        for i in range(0, size - bar):
            ret += " "

        return ret + "]"

class Move:

    def __init__(self, name, damage, mp):

        self.name = name
        self.damage = damage
        self.mp = mp


class button:

    def __init__(self, name, img, x, y, width, height):

        self.name = name
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

    def display(self):
        Zone.blit(self.img, self.getCoords())
        Zone.blit(Text(self.name), (self.x + 20, self.y + 10))

class StatBox:

    def __init__(self):

        self.img = pygame.image.load("img/button.png")
        self.actors = []

    def addActor(self, a):

        self.actors.append(a)

    def display(self, x, y):

        Zone.blit(self.img, (x, y))

        for i in range(0, len(stats.actors)):
            Zone.blit(Text(stats.actors[i].displayName()), (x+30, y+20+(i*20)))
            Zone.blit(Text(stats.actors[i].mp.bar(4)), (x+100, y+20+(i*20)))
            Zone.blit(Text(stats.actors[i].hp.bar(10)), (x+200, y+20+(i*20)))


def Text(t):
    return FONT.render(t, True, (50, 0, 0))


pygame.init()
Zone = pygame.display.set_mode((800, 600))

buttonImg = pygame.image.load("img/button2.png")

stats = StatBox()
stats.addActor(actor("Guy"))
stats.addActor(actor("Bro"))

hpup = button("HP Up", buttonImg, 10, 50, 123, 50)
hpdown = button("HP Down", buttonImg, 10, 100, 123, 50)

FONT = pygame.font.SysFont('monospace', 16)

clock = pygame.time.Clock()




while True:

    Zone.fill((0,200,0))

    hpup.display()
    hpdown.display()

    stats.display(10, 450)

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if hpup.collides(x, y):
                stats.actors[0].hp.inc(4)
            if hpdown.collides(x, y):
                if stats.actors[0].hp.dec(7):
                    print("You died")

    clock.tick(30)
