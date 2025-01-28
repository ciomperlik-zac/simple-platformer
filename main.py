import pygame
import math as m

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

RED = (255, 0, 0, 255)
BLUE = (0, 0, 255, 255)

class Player(pygame.sprite.Sprite):
    def __init__(self, loc, color):
        super(Player, self).__init__()

        self.key_inf = [0, 0, 0]

        self.loc = loc

        self.color = color

        self.image = pygame.Surface((25, 25), pygame.SRCALPHA)
        self.image.fill(color)
        self.rect = self.image.get_rect(center=self.loc)

        self.jumping = 0
    
    def gravity(self):
        collide = pygame.sprite.spritecollide(self, platforms, False)

        if not collide:
            self.rect.centery += 0.5
        else:
            self.jumping = 0

    def move_left(self):
        self.rect.centerx -= 1

    def move_right(self):
        self.rect.centerx += 1

    def jump(self):
        if self.jumping < 50:
            self.rect.centery -= 3

        self.jumping += 1

class Platform(pygame.sprite.Sprite):
    def __init__(self, loc, vx, vy, color):
        super(Platform, self).__init__()

        self.loc = loc

        self.color = color

        self.vx = vx
        self.vy = vy

        self.image = pygame.Surface((200, 10), pygame.SRCALPHA)
        self.image.fill(color)
        self.rect = self.image.get_rect(center=self.loc)

    def move(self):
        if self.rect.left < 0:
            self.vx = abs(self.vx)
        elif self.rect.right > 800:
            self.vx = -abs(self.vx)

        self.rect.centerx += self.vx
        self.rect.centerx += self.vy

players = pygame.sprite.Group()
player1 = Player((295, 450), RED)
players.add(player1)
player2 = Player((505, 400), BLUE)
players.add(player2)

platforms = pygame.sprite.Group()
platforms.add(Platform((295, 500), 0, 0, RED))
platforms.add(Platform((505, 450), 0, 0, BLUE))

platforms.add(Platform((195, 400), 1, 0, RED))
platforms.add(Platform((605, 350), -1, 0, BLUE))

running = True
while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # Player 1 Controls
            if event.key == pygame.K_a:
                player1.key_inf[0] = 1
            elif event.key == pygame.K_d:
                player1.key_inf[1] = 1
            elif event.key == pygame.K_w:
                player1.key_inf[2] = 1

            # Player 2 Controls
            if event.key == pygame.K_LEFT:
                player2.key_inf[0] = 1
            elif event.key == pygame.K_RIGHT:
                player2.key_inf[1] = 1
            elif event.key == pygame.K_UP:
                player2.key_inf[2] = 1

        elif event.type == pygame.KEYUP:
            # Player 1 Controls
            if event.key == pygame.K_a:
                player1.key_inf[0] = 0
            elif event.key == pygame.K_d:
                player1.key_inf[1] = 0
            elif event.key == pygame.K_w:
                player1.key_inf[2] = 0
                player1.jumping = 100

            # Player 2 Controls
            if event.key == pygame.K_LEFT:
                player2.key_inf[0] = 0
            elif event.key == pygame.K_RIGHT:
                player2.key_inf[1] = 0
            elif event.key == pygame.K_UP:
                player2.key_inf[2] = 0
                player2.jumping = 100

    for p in players:
        if p.key_inf[0] == 1:
            p.move_left()
        if p.key_inf[1] == 1:
            p.move_right()
        if p.key_inf[2] == 1:
            p.jump()

        p.gravity()

    for p in platforms:
        p.move()

    players.draw(screen)
    platforms.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()