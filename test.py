import pygame
import sys
from pygame.locals import *
import random




class actor:

    def __init__(self, name, img):

        self.name = name
        self.img = img

        self.attack = 3
        self.defence = 2
        self.speed = 10

        self.hp = Gauge(23)
        self.mp = Gauge(20)

        self.move = []

    def setAttack(self, value):
        self.attack = value
    
    def setDefence(self, value):
        self.defence = value

    def setSpeed(self, value):
        self.speed = value

    def setMaxHealth(self, value):
        self.max_health = value

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


class Button:

    def __init__(self, name, x, y):

        self.name = name
        self.img = pygame.image.load("img/button2.png")

        self.x = x
        self.y = y
        self.width = 123
        self.height = 50

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

        for i in range(0, len(self.actors)):
            Zone.blit(Text(self.actors[i].name), (x+30, y+20+(i*20)))
            Zone.blit(Text(self.actors[i].mp.bar(6)), (x+120, y+20+(i*20)))
            Zone.blit(Text(self.actors[i].hp.bar(10)), (x+200, y+20+(i*20)))

class field:

    def __init__(self, stats, enemy):

        self.stats = stats
        self.enemy = enemy

        self.b = ButtonField()
        self.s = Scene()

        self.turn = True
        self.sub_turn = 0

        self.drawButtons()

    def drawButtons(self):
        for i in range(0, len(self.stats.actors[self.sub_turn].move)):
            self.b.addButton(Button(self.stats.actors[self.sub_turn].move[i].name, 10, 10+(i*70)))

    def clicked(self, x, y):

        if self.turn:
            for i in range(0, len(self.b.buttons)):
                if self.b.buttons[i].collides(x, y):
                    print(self.b.buttons[i].name)
                    self.s.addAction(Action(True, self.stats.actors[i].move[0], self.stats.actors[i], 0))#PLACEHOLDER MOVE[0] and target 0
                    self.sub_turn += 1
                    if self.sub_turn >= len(self.stats.actors):
                        self.sub_turn = 0
                        self.takeEnemyTurn()
                        #self.turn = False
        else:
            print("Fun")
        
        self.b.reset()
        self.drawButtons()

        
    def takeEnemyTurn(self):
        for i in range(0, len(self.enemy.actors)):
            choice = random.randint(0, len(self.enemy.actors[i].move) - 1)
            print(self.enemy.actors[i].move[choice].name)
            self.s.addAction(Action(False, self.enemy.actors[i].move[0], self.enemy.actors[i], 0))

        self.s.arrange()
        self.s.p()
        self.s.reset()
        
    def display(self):

        self.stats.display(10, 450)
        self.enemy.display(400, 450)

        for i in range(0, len(self.stats.actors)):
            Zone.blit(self.stats.actors[i].img, (30+(i*100), 100))

        for i in range(0, len(self.enemy.actors)):
            Zone.blit(self.enemy.actors[i].img, (430+(i*100), 100))

        self.b.display()#Cpnditipm this

class Scene:

    def __init__(self):

        self.actions = []

    def reset(self):
        self.actions.clear()

    def addAction(self, action):

        self.actions.append(action)

    def arrange(self):

        self.actions = self.readied()

    def readied(self):

        ret = []
        sp = 100

        while sp > 0:
            fast = []

            for i in range(0, len(self.actions)):
                if self.actions[i].user.speed == sp:
                    fast.append(i)

            while len(fast) > 0:
                selection = random.randint(0, len(fast) - 1)
                ret.append(self.actions[fast[selection]])
                fast.pop(selection)

            sp -= 1

        return ret

    def p(self):

        for i in range(0, len(self.actions)):
            print(self.actions[i].user.name)

class Action:

    def __init__(self, side, move, user, target):

        self.side = side
        self.move = move
        self.user = user
        self.target = target

class ButtonField:

    def __init__(self):

        self.buttons = []

    def addButton(self, b):
        self.buttons.append(b)

    def reset(self):
        self.buttons.clear()
        

    def display(self):         
        for i in range(0, len(self.buttons)):
            self.buttons[i].display()


def Text(t):
    return FONT.render(t, True, (50, 0, 0))


pygame.init()
Zone = pygame.display.set_mode((800, 600))

guy = actor("Guy", pygame.image.load("img/1.png"))
bro = actor("Bro", pygame.image.load("img/2.png"))

guy.addMove(Move("Attack", 3, 1))
guy.addMove(Move("Smash", 5, 4))
guy.addMove(Move("Boom", 6, 6))
bro.addMove(Move("Axe", 4, 2))

guy.setSpeed(13)
bro.setSpeed(7)

stats = StatBox()
stats.addActor(guy)
stats.addActor(bro)

doofus = actor("Doofus", pygame.image.load("img/3.png"))
poo = actor("Poo", pygame.image.load("img/4.png"))
thing = actor("Thing", pygame.image.load("img/5.png"))

doofus.addMove(Move("Chain whip", 4, 1))
doofus.addMove(Move("Stomp", 6, 4))
poo.addMove(Move("Throw", 3, 2))
thing.addMove(Move("Grab", 2, 1))

enemy = StatBox()
enemy.addActor(doofus)
enemy.addActor(poo)
enemy.addActor(thing)

f = field(stats, enemy)

FONT = pygame.font.SysFont('monospace', 16)

clock = pygame.time.Clock()




while True:

    Zone.fill((0,200,0))

    f.display()

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            f.clicked(x, y)

    clock.tick(30)
