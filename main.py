import pygame
import math as m

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

bg = pygame.image.load("bg.png")

RED = (255, 0, 0, 255)
BLUE = (0, 0, 255, 255)
GRAY = (128, 128, 128, 255)
GREEN = (0, 200, 0, 255)
GOLD = (255, 215, 0, 255)

players_alive = 2

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

    def die(self):
        global players_alive

        self.kill()
        players_alive -= 1

        disp.set_text(f"Player {"BLUE" if self.color == RED else "RED"} won!")
    
    def gravity_collide(self):
        collide_plat = pygame.sprite.spritecollide(self, platforms, False)
        collide_enemy = pygame.sprite.spritecollide(self, enemies, False)

        if not collide_plat:
            self.rect.centery += 0.5
        else:
            self.rect.centerx += collide_plat[0].vx
            self.rect.centery += collide_plat[0].vy

            self.jumping = 0

            if collide_plat[0].color not in [self.color, GRAY, GOLD]:
                self.die()

            if collide_plat[0].color == GOLD:
                for player in players:
                    if player.color != self.color:
                        player.die()

        if len(collide_enemy) > 0 or self.rect.top > 600:
            self.die()

    def move_left(self):
        self.rect.centerx -= 1

    def move_right(self):
        self.rect.centerx += 1

    def jump(self):
        if self.jumping < 50:
            self.rect.centery -= 3

        self.jumping += 1

class Platform(pygame.sprite.Sprite):
    def __init__(self, loc, vx, vy, vxl, vyl, color):
        super(Platform, self).__init__()

        self.loc = loc

        self.color = color

        self.vx = vx
        self.vy = vy

        self.vxl = vxl
        self.vyl = vyl

        self.image = pygame.Surface((150, 10), pygame.SRCALPHA)
        self.image.fill(color)
        self.rect = self.image.get_rect(center=self.loc)

    def move(self):
        if self.rect.left < self.vxl[0]:
            self.vx = abs(self.vx)
        elif self.rect.right > self.vxl[1]:
            self.vx = -abs(self.vx)

        if self.rect.top < self.vyl[0]:
            self.vy = abs(self.vy)
        elif self.rect.bottom > self.vyl[1]:
            self.vy = -abs(self.vy)

        self.rect.centerx += self.vx
        self.rect.centery += self.vy

class Enemy(pygame.sprite.Sprite):
    def __init__(self, loc, vx, vy, vxl, vyl, color):
        super(Enemy, self).__init__()

        self.loc = loc

        self.color = color

        self.vx = vx
        self.vy = vy

        self.vxl = vxl
        self.vyl = vyl

        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (10, 10), 10)
        self.rect = self.image.get_rect(center=self.loc)

    def move(self):
        if self.rect.left < self.vxl[0]:
            self.vx = abs(self.vx)
        elif self.rect.right > self.vxl[1]:
            self.vx = -abs(self.vx)

        if self.rect.top < self.vyl[0]:
            self.vy = abs(self.vy)
        elif self.rect.bottom > self.vyl[1]:
            self.vy = -abs(self.vy)

        self.rect.centerx += self.vx
        self.rect.centery += self.vy

class TextScreen():
    def __init__(self, text):
        super(TextScreen, self).__init__()

        self.text = text

        self.font = pygame.font.SysFont("Comic Sans MS", 50)

        self.image = self.font.render(self.text, False, (255, 255, 255))

        self.size = self.font.size(self.text)

    def set_text(self, text):
        self.text = text

        self.font = pygame.font.SysFont("Comic Sans MS", 50)

        self.image = self.font.render(self.text, False, (255, 255, 255))

        self.size = self.font.size(self.text)

players = pygame.sprite.Group()
player1 = Player((300, 400), RED)
players.add(player1)
player2 = Player((500, 450), BLUE)
players.add(player2)

platforms = pygame.sprite.Group()
platforms.add(Platform((300, 500), 0, 0, [0, 0], [0, 0], RED))
platforms.add(Platform((500, 500), 0, 0, [0, 0], [0, 0], BLUE))

platforms.add(Platform((125, 450), 0, 1, [0, 0], [350, 500], RED))
platforms.add(Platform((675, 450), 0, 1, [0, 0], [350, 500], BLUE))

platforms.add(Platform((300, 350), 0, 0, [0, 0], [0, 0], GRAY))
platforms.add(Platform((500, 350), 0, 0, [0, 0], [0, 0], GRAY))

platforms.add(Platform((225, 225), 1, 0, [50, 375], [0, 0], BLUE))
platforms.add(Platform((575, 225), 1, 0, [425, 750], [0, 0], RED))

platforms.add(Platform((400, 100), 0, 0, [0, 0], [0, 0], GOLD))

enemies = pygame.sprite.Group()
enemies.add(Enemy((300, 285), 1, 1, [225, 375], [305, 345], GREEN))
enemies.add(Enemy((500, 285), -1, 1, [425, 575], [305, 345], GREEN))

disp = TextScreen("")

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
                player1.jumping = 1000

            # Player 2 Controls
            if event.key == pygame.K_LEFT:
                player2.key_inf[0] = 0
            elif event.key == pygame.K_RIGHT:
                player2.key_inf[1] = 0
            elif event.key == pygame.K_UP:
                player2.key_inf[2] = 0
                player2.jumping = 1000

    if players_alive == 2:
        for p in players:
            if p.key_inf[0] == 1:
                p.move_left()
            if p.key_inf[1] == 1:
                p.move_right()
            if p.key_inf[2] == 1:
                p.jump()

            p.gravity_collide()

        for p in platforms:
            p.move()

        for e in enemies:
            e.move()

    screen.blit(bg, (0,0))

    players.draw(screen)
    platforms.draw(screen)
    enemies.draw(screen)

    screen.blit(disp.image, ((400)-(disp.size[0]/2), 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()