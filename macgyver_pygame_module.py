import pygame
from pygame.locals import *

resolution = (400,300)
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)

screen = pygame.display.set_mode(resolution)

class Ball:
    def __init__(self, xPos =  resolution[0] / 2, yPos = resolution[1] / 2, xVel = 1, yVel = 1, rad = 15):
        self.x = xPos
        self.y = yPos
        self.dx = xVel
        self.dy = yVel
        self.radius = rad
        self.type = "ball"

    def draw(self, surface):
        self.x = int(self.x)
        self.y = int(self.y)
        pygame.draw.circle(surface, black, (self.x, self.y), self.radius)

    def update(self):
        self.x += self.dx
        self.y += self.dy
        if (self.x <= 0 or self.x >= resolution[0]):
            self.dx *= -1
        if (self.y <= 0 or self.y >= resolution[1]):
            self.dy *= -1

class game():
    def __init__(self):
        pygame.init()
        
        self.screen = pygame.display.set_mode(resolution)
        self.clock = pygame.time.Clock()
        self.gameObjects = []
        self.gameObjects.append(Ball())
        self.gameObjects.append(Ball(100))

    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()

    def run(self):
        while True:
            self.handleEvents()

            for gameObj in self.gameObjects:
                gameObj.update()

            self.screen.fill(white)

            for gameObj in self.gameObjects:
                gameObj.draw(self.screen)

            self.clock.tick(60)
            pygame.display.flip()

game().run()