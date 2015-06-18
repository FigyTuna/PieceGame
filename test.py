import pygame
import sys
from pygame.locals import *
import random




class actor:

    def __init__(self, name, img):

        self.name = name
        self.img = img
        self.animation = 0
        self.animFrame = 0
        self.animSide = 1

        self.level = 1
        self.exp = 0
        
        self.strength = 10
        self.defense = 10
        self.skill = 10
        self.speed = 10
        
        self.hp = Gauge(20)
        self.mp = Gauge(10)

        self.move = []

        self.addMove(Move("Attack", 2, 0))

    def setBaseStats(self, st, de, sk, sp):#Add hp and mp
        self.strength = st
        self.defense = de
        self.skill = sp
        self.speed = sp

    def getStrength(self):
        return self.doMath(self.strength)

    def getDefense(self):
        return self.doMath(self.defense)

    def getSkill(self):
        return self.doMath(self.skill)

    def getSpeed(self):
        return self.doMath(self.speed)

    def doMath(self, var):
        return int(float(self.level) * (2 - (1 / float(var)))) + var

    def takeDamage(self, dmg):
        self.hp.dec(int((float(dmg) + ((1.0 / float(self.getDefense()) * float(dmg) * float(dmg)))) / 4.0))

    def isAlive(self):
        return self.hp.value > 0

    def displayHealth(self):
        return "Health: " + str(self.hp.getValue()) + "/" + str(self.hp.getMax())

    def displayMp(self):
        return "MP: " + str(self.mp.getValue()) + "/" + str(self.mp.getMax())

    def addMove(self, m):
        self.move.append(m)

    def setAnim(self, a, f):
        self.animation = a
        self.animFrame = f

    def anim(self):
        if self.animation == 1:
            x = 2 * ( -((self.animFrame - 2) * (self.animFrame)) + 6 )
            if x < 0:
                x = 0
            x = x * self.animSide
            return x, 0
        elif self.animation == 2:
            x = 2 * (((self.animFrame - 2) * (self.animFrame)) - 6 )
            y = 2 * ( -((self.animFrame - 2) * (self.animFrame)) + 6 )
            if x > 0 or self.animFrame < 0:
                x = 0
            if y < 0 or self.animFrame < 0:
                y = 0
            x = x * self.animSide
            if not self.isAlive() and self.animFrame > 20:
                self.setAnim(3, 0)
            return x, y
        elif self.animation == 3:
            y = 40 * self.animFrame
            if y > 600:
                y = 600
            return 0, y
        else:
            return 0, 0

    def display(self, x, y):
        fx, fy = self.anim()
        Zone.blit(self.img, (fx + x, fy + y))
        self.animFrame += 1



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

    def displayMP(self):
        return "MP: " + str(self.mp)

    def getDamage(self, attack, skill):

        if self.mp == 0:
            skill = attack

        return int(float(self.damage) * (2 - (1 / float(skill)))) + attack 


class Button:

    def __init__(self, name, x, y, sub = ""):

        self.name = name
        self.sub = sub
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
        Zone.blit(Text(self.name), (self.x + 10, self.y + 10))
        Zone.blit(Text(self.sub), (self.x + 10, self.y + 26))

class StatBox:

    def __init__(self):

        self.img = pygame.image.load("img/button.png")
        self.actors = []

    def addActor(self, a):

        self.actors.append(a)

    def isAlive(self):

        ret = False
        for i in range(0, len(self.actors)):
            if self.actors[i].hp.getValue() > 0:
                ret = True
        return ret

    def display(self, x, y):

        Zone.blit(self.img, (x, y))

        for i in range(0, len(self.actors)):
            Zone.blit(Text(self.actors[i].name), (x+30, y+20+(i*20)))
            Zone.blit(Text(self.actors[i].mp.bar(6)), (x+120, y+20+(i*20)))
            Zone.blit(Text(self.actors[i].hp.bar(10)), (x+200, y+20+(i*20)))
            #Zone.blit(Text(self.actors[i].displayMp()), (x+80, y+20+(i*20)))
            #Zone.blit(Text(self.actors[i].displayHealth()), (x+190, y+20+(i*20)))

class Notify:

    def __init__(self):
        self.message = ""
        self.visible = False

    def setMessage(self, value):
        self.message = value
        self.visible = True

    def setInvisible(self):
        self.visible = False

    def isVisible(self):
        return self.visible

    def display(self):
        Zone.blit(Text(self.message), (250, 50))

class field:

    def __init__(self, stats, enemy):

        self.stats = stats
        self.enemy = enemy

        for i in range(0, len(self.enemy.actors)):
            self.enemy.actors[i].animSide = -1

        self.b = ButtonField()
        self.s = Scene()
        self.notify = Notify()

        self.turn = 0
        self.sub_turn = 0

        self.drawButtons()

    def drawButtons(self):
        if self.turn == 0:
            for i in range(0, len(self.stats.actors[self.sub_turn].move)):
                self.b.addButton(Button(self.stats.actors[self.sub_turn].move[i].name, 10, 10+(i*70), self.stats.actors[self.sub_turn].move[i].displayMP()))
        elif self.turn == 1:
            for i in range(0, len(self.enemy.actors)):
                self.b.addButton(Button(self.enemy.actors[i].name, 10, 10+(i*70)))
        elif self.turn == 2:
            self.b.addButton(Button("Next", 10, 10))
        

    def clicked(self, x, y):

        self.notify.setInvisible()

        if self.turn == 0:
            for i in range(0, len(self.b.buttons)):
                if self.b.buttons[i].collides(x, y):
                    if self.stats.actors[self.sub_turn].mp.value >= self.stats.actors[self.sub_turn].move[i].mp:
                        self.s.addAction(Action(True, self.stats.actors[self.sub_turn].move[i], self.stats.actors[self.sub_turn], self.enemy.actors[0], self.enemy))
                        self.turn = 1
                    else:
                        print("Not enough MP.")
                                            
        elif self.turn == 1:
            for i in range(0, len(self.b.buttons)):
                if self.b.buttons[i].collides(x, y):
                    self.s.fixTarget(self.s.getLength()-1, self.enemy.actors[i])
                    self.turn = 0
                    
                    self.sub_turn += 1
                    if not self.sub_turn >= len(self.stats.actors):
                        self.checkAlive()
                    
                    if self.sub_turn >= len(self.stats.actors):
                        self.sub_turn = 0
                        self.takeEnemyTurn()
                        self.turn = 2
                        self.s.readOut()
                    
        elif self.turn == 2:
            if self.s.clicked():
                self.s.reset()
                self.turn = 0
                self.gameEnder()
                self.checkAlive()
        
        self.b.reset()
        self.drawButtons()


    def checkAlive(self):
        if not self.stats.actors[self.sub_turn].isAlive():
            self.sub_turn += 1
            if not self.sub_turn >= len(self.stats.actors):
                self.checkAlive()

    def gameEnder(self):

        if not self.stats.isAlive():
            print("You lose...")
            pygame.quit()
            input("")
            sys.exit()
        elif not self.enemy.isAlive():
            print("You win!")
            pygame.quit()
            input("")
            sys.exit()
            
    
    def takeEnemyTurn(self):
        for i in range(0, len(self.enemy.actors)):
            if self.enemy.actors[i].isAlive():
                notDone = True
                choiceMove = 0
                choiceTarget = 0
                while notDone:
                    notDone = False
                    choiceMove = random.randint(0, len(self.enemy.actors[i].move) - 1)
                    if self.enemy.actors[i].move[choiceMove].mp > self.enemy.actors[i].mp.value:
                        notDone = True
                notDone = True
                while notDone:
                    notDone = False
                    choiceTarget = random.randint(0, len(self.stats.actors) - 1)
                    if not self.stats.actors[choiceTarget].isAlive():
                        notDone = True
                self.s.addAction(Action(False, self.enemy.actors[i].move[choiceMove], self.enemy.actors[i], self.stats.actors[choiceTarget], self.stats))

        self.s.arrange()

    def setMessage(self, value):
        self.notify.setMessage(value)
        
    def display(self):

        self.stats.display(10, 450)
        self.enemy.display(400, 450)

        for i in range(0, len(self.stats.actors)):
            self.stats.actors[i].display(30+(i*100), 100)

        for i in range(0, len(self.enemy.actors)):
            self.enemy.actors[i].display(430+(i*100), 100)

        if self.notify.isVisible():
            self.notify.display()

        self.b.display()

class Scene:

    def __init__(self):

        self.actions = []
        self.count = 0

    def reset(self):
        self.actions.clear()
        self.count = 0

    def addAction(self, action):

        self.actions.append(action)

    def fixTarget(self, i, target):

        self.actions[i].target = target

    def getLength(self):

        return len(self.actions)

    def arrange(self):

        self.actions = self.readied()

    def readied(self):

        ret = []
        sp = 100

        while sp > 0:
            fast = []

            for i in range(0, len(self.actions)):
                if self.actions[i].user.getSpeed() == sp:
                    fast.append(i)

            while len(fast) > 0:
                selection = random.randint(0, len(fast) - 1)
                ret.append(self.actions[fast[selection]])
                fast.pop(selection)

            sp -= 1

        return ret

    def clicked(self):

        if self.count < len(self.actions):
            self.readOut()
        elif self.count == len(self.actions):
            return True
        return False

    def readOut(self):

        end = False

        for i in range(0, len(self.actions)):
            if not self.actions[i].altTeam.isAlive():
                end = True
                self.count = len(self.actions)

        while not end and not self.actions[self.count].user.isAlive():

            self.count += 1
            
            if self.count >= len(self.actions):
                end = True


        if not end:

            while not self.actions[self.count].target.isAlive():
                self.actions[self.count].target = self.actions[self.count].altTeam.actors[random.randint(0, len(self.actions[self.count].altTeam.actors)-1)]

            self.actions[self.count].user.mp.dec(self.actions[self.count].move.mp)
            self.actions[self.count].target.takeDamage(self.actions[self.count].move.getDamage(self.actions[self.count].user.getStrength(),self.actions[self.count].user.getSkill()))

            self.actions[self.count].user.setAnim(1, 0)
            self.actions[self.count].target.setAnim(2, -5)
        
            f.setMessage(self.actions[self.count].user.name + " used " + self.actions[self.count].move.name + " on " + self.actions[self.count].target.name + ".")
        
            self.count += 1
        

    def p(self):

        for i in range(0, len(self.actions)):
            print(self.actions[i].user.name)

class Action:

    def __init__(self, side, move, user, target, altTeam):

        self.side = side
        self.move = move
        self.user = user
        self.target = target
        self.altTeam = altTeam

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
FONT = pygame.font.SysFont('monospace', 16)
clock = pygame.time.Clock()

#------------------

guy = actor("Guy", pygame.image.load("img/1.png"))
bro = actor("Bro", pygame.image.load("img/2.png"))

guy.addMove(Move("Smash", 5, 4))
guy.addMove(Move("Boom", 6, 6))
bro.addMove(Move("Axe", 4, 2))

guy.speed = 13
bro.speed = 7

doofus = actor("Doofus", pygame.image.load("img/3.png"))
poo = actor("Poo", pygame.image.load("img/4.png"))
thing = actor("Thing", pygame.image.load("img/5.png"))

doofus.addMove(Move("Chain whip", 4, 1))
doofus.addMove(Move("Stomp", 6, 4))
poo.addMove(Move("Throw", 3, 2))
thing.addMove(Move("Grab", 2, 1))

stats = StatBox()
stats.addActor(doofus)
stats.addActor(bro)
stats.addActor(guy)

enemy = StatBox()
enemy.addActor(poo)
enemy.addActor(thing)

f = field(stats, enemy)

#------------------





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
