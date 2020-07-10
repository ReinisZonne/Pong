'''
Pong game
Date: 10.07.20
'''

import pygame
pygame.font.init()
from random import randrange

class Paddle:

    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.width = 20
        self.height = 70
        self.speed = 5
        self.score = 0

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))


class Ball:

    def __init__(self, direction):
        self.x = 500
        self.y = 262
        self.direction = direction
        self.radius = 5
        self.color = (255, 255, 255)
        self.speedy = 5
        self.speedx = 5
        self.hitTop = False
        self.hitBottom = False

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius)

def drawMidLine(surface, x, y):
    pygame.draw.line(surface, (255, 255, 255), (x, y), (x, y + 10), 2)


# Main loop
def main():
    
    # Display settings
    width = 1000
    height = width * 9 // 16
    win = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Pong")
    clock = pygame.time.Clock()
    FPS = 30 # Frames per second
    #------------------

    # Redraws the game window
    def reDrawWindow(surface, player1, player2, b):
        surface.fill((0,0,0)) # Bg-color: Black

        # Draws mid Line
        lineX = width // 2
        lineY = 0
        while lineY <= height:
            drawMidLine(win, lineX, lineY)
            lineY += 25
        # ---------------

        # Display score
        font = pygame.font.SysFont("Comic sans MS", 24)
        score1 = font.render(str(player1.score), False, (255, 255, 255))
        score2 = font.render(str(player2.score), False, (255, 255, 255))

        win.blit(score1, (200, 50))
        win.blit(score2, (800, 50))
        # ---------------

        player1.draw(surface)
        player2.draw(surface)
        b.draw(surface)

        pygame.display.update()


    # Classes
    player1 = Paddle(10, height//2, (0, 255, 0))
    player2 = Paddle(970, height//2, (255, 0, 0))
    b = Ball(randrange(0,1))
    #-----------

    # Loop
    finished = False
    while not finished:
        clock.tick(FPS)
        
        # Key binding Player1
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and player1.y > 5:
            player1.y -= player1.speed
        elif keys[pygame.K_s] and player1.y + player1.height < height - 5:
            player1.y += player1.speed
        #--------------------
        # Key binding Player2
        if keys[pygame.K_UP] and player2.y > 5:
            player2.y -= player2.speed
        elif keys[pygame.K_DOWN] and player2.y + player2.height < height - 5:
            player2.y += player2.speed
        #--------------------

        # Ball movement
        if b.direction == 1:
            b.y += b.speedy
            b.x += b.speedx
        else:
            b.y += b.speedy
            b.x -= b.speedx

        # Collision with player1
        if b.x - b.radius < player1.x + player1.width and b.y > player1.y and b.y < player1.y + player1.height:
            b.speedx *= -1 # X values becomes positive
        #-----------------------

        # Collision with player2
        if b.x + b.radius > player2.x and b.y > player2.y and b.y < player2.y + player2.height:
            b.speedx *= -1 # X value becomes negative
        #-----------------------

        # Collision with top wall
        if b.y < b.radius + b.speedx:
            b.speedy *= -1
        #------------------
        # Collison with bottom wall
        elif b.y > height - b.radius - b.speedx:
            b.speedy *= -1
        #------------------
        # Collison with right wall
        elif b.x > width - b.radius - b.speedx:
            b = Ball(0)
            b.x = width // 2
            b.y = height // 2
            player1.score += 1
            
        #------------------
        # Collision with left wall
        elif b.x < b.radius + b.speedx:
            b = Ball(1)
            b.x = width // 2
            b.y = height // 2 
            player2.score += 1
            
        
        # Exit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
        #-----------------------
        
        reDrawWindow(win, player1, player2, b)
        


main()
pygame.quit()
