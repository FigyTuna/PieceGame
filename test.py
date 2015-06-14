import pygame
from pygame.locals import *






class actor:

    def __init__(self):

        self.attack = 10
        self.defence = 10
        self.max_health = 10
        self.health = self.max_health

    def display(self):

        return "Attack: " + str(self.attack) + " - " + "Defence: " + str(self.defence) + " - " + "Health: " + str(self.health) + "/" + str(self.max_health)

    def takeDamage(self, value):

        self.health -= value

        if self.health < 1:
            return True

        return False

    def heal(self, value):

        self.health += value

        if self.health > self.max_health:
            self.health = self.max_health


pygame.init()
Zone = pygame.display.set_mode((600, 400))

FONT = pygame.font.Font('freesansbold.ttf', 32)

clock = pygame.time.Clock()



guy = actor()
guy.display()
if guy.takeDamage(6):
    print("Dead")
guy.display()
guy.heal(4)
guy.display()
guy.heal(10)
guy.display()
if guy.takeDamage(15):
    print("Dead")
guy.display()




while True:

    
    stats_text = FONT.render(guy.display(), True, (255, 200, 255))


    Zone.fill((0,200,0))
    Zone.blit(stats_text, (10, 10))

    pygame.display.update()

    clock.tick(1)
