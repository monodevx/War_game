import pygame
import random

pygame.init()

FPS = 60
WIDTH = 1000
HEIGHT = 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (14, 21, 27)

sc = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
player_r = pygame.image.load("img/player/1_r.png")
player_l = pygame.image.load("img/player/1_l.png")
bullet = pygame.image.load("img/bullet.png")
grass = pygame.image.load("img/grass.png")
grasscenter = pygame.image.load("img/grassCenter.png")
unit_r = pygame.image.load("img/enemy 1/1_r.png")
unit_l = pygame.image.load("img/enemy 1/1_l.png")

cloud = pygame.image.load("img/cloud.png")
timer_cloud = 0


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_r
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.mask_outline = self.mask.outline()
        self.mask_list = []
        self.rect.x = 300
        self.rect.y = 200
        self.jump_step = -25
        self.jump = False
        self.gravity = 10
        self.direction = "left"
        self.on_earth = True
        self.hp = 10

    def update(self):
        self.rect.y += self.gravity
        keystate = pygame.key.get_pressed()
        if pygame.sprite.spritecollide(self, earth_gr, False):
            self.jump = False
            self.jump_step = -25
            self.on_earth = True
        if keystate[pygame.K_SPACE] and self.on_earth:
            self.jump = True
        if keystate[pygame.K_d]:
            self.direction = "right"
            self.rect.x += 5
            self.image = player_r
            
            if self.rect.right > 800:
                self.rect.right = 800
                earth_gr.update(-5)
                unit_group.update(-5)
                fon_group.update(-5)

        if keystate[pygame.K_a]:
            self.direction = "left"
            self.rect.x -= 5
            self.image = player_l
            if self.rect.left < 200:
                self.rect.left = 200
                earth_gr.update(5)
                unit_group.update(5)
                fon_group.update(5)

        if self.jump:
            self.on_earth = False
            if self.jump_step <= 25:
                self.rect.y += self.jump_step
                self.jump_step += 1
            else:
                self.jump = False
                self.jump_step = -25

        self.mask_list = []
        for i in self.mask_outline:
            self.mask_list.append((i[0] + self.rect.x, i[1] + self.rect.y))


class Unit(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = unit_r
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1] - 50
        self.speed = 2

    def update(self, stepx):
        self.rect.x += stepx
        self.rect.x += self.speed
        if pygame.sprite.spritecollide(self, earth_gr, False):
            self.speed *= -1
        if self.speed >= 0:
            self.image = unit_r
        elif self.speed <= 0:
            self.image = unit_l

class Block(pygame.sprite.Sprite):
    def __init__(self, pos, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def update(self, stepx):

        self.rect.x += stepx
        if pygame.sprite.spritecollide(self, player_gr, False):

            # ограничегое персонажа в случае, если над ним блок

            if abs(self.rect.bottom - player.rect.top) < 20:
                player.jump = False
                player.jump_step = -25
                player.on_earth = False

            # ограничение, чтобы персонаж не проваливался

            if (
                abs(self.rect.top - player.rect.bottom) < 20
                and abs(self.rect.left - player.rect.right) > 20
                and abs(player.rect.left - self.rect.right) > 20
            ):
                player.rect.bottom = self.rect.top
            # ограничение на прохождение блоков при движение вправо/влево
            elif (
                abs(self.rect.bottom - player.rect.bottom) < 8
                or abs(self.rect.top - player.rect.top) < 50
            ):

                if (
                    player.direction == "left"
                    and abs(player.rect.left - self.rect.right) < 30
                ):
                    player.rect.left = self.rect.right

                if (
                    player.direction == "right"
                    and abs(player.rect.right - self.rect.left) < 30
                ):
                    player.rect.right = self.rect.left


class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = cloud
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(1000, 1500)
        self.rect.y = random.randint(50, 300)

    def update(self, step):
        if step == 0:
            self.rect.x -= 2
        else:
            self.rect.x += step
        if self.rect.right < 0:
            self.kill()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, rot):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet
        self.rect = self.image.get_rect()
        self.rect.x = tank_pos[0]
        self.rect.y = tank_pos[1]


earth_gr = pygame.sprite.Group()
fon_group = pygame.sprite.Group()

unit_group = pygame.sprite.Group()
earth_gr.add()
player = Player()
player_gr = pygame.sprite.Group()
player_gr.add(player)


def draw_maps(file_name):
    maps = []
    source = "ltiles/" + str(file_name)
    with open(source, "r") as file:
        for i in range(0, 13):
            maps.append(list(file.readline().replace("\n", ""))[0:-1])
    pos = [0, 0]
    for i in range(0, len(maps)):
        pos[1] = i * 50
        for j in range(0, len(maps[0])):
            if maps[i][j] == "2":
                pos[0] = 50 * j
                block = Block(pos, grasscenter)
                earth_gr.add(block)
            elif maps[i][j] == "1":
                pos[0] = 50 * j
                block = Block(pos, grass)
                earth_gr.add(block)
            elif maps[i][j] == "u":
                pos[0] = 50 * j
                unit = Unit(pos)
                unit_group.add(unit)


draw_maps("begin.md")


def test():
    global timer_cloud
    timer_cloud += 1
    if timer_cloud // FPS > random.randint(0, 5):
        cloud = Cloud()
        fon_group.add(cloud)
        timer_cloud = 0
    sc.fill((78, 185, 255))
    fon_group.update(0)
    fon_group.draw(sc)
    earth_gr.update(0)
    earth_gr.draw(sc)
    player_gr.update()
    player_gr.draw(sc)
    unit_group.update(0)
    unit_group.draw(sc)
    pygame.display.update()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    test()
    clock.tick(FPS)
