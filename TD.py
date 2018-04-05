import pygame
import random
from os import path
textures_dir = 'textures'
animations_dir = 'animations'
sons_dir = 'sons'



WIDTH = 480
HEIGHT = 600
FPS = 60

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# initialize Pygame and create window
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load(path.join(sons_dir, 'musique2.wav'))
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rick's invaders")
clock = pygame.time.Clock()

font_name = pygame.font.match_font('arial')



def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)
def mobrespawn():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)
def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    if pct == 100:
        pygame.draw.rect(surf, GREEN, fill_rect)
    if pct > 20 and pct < 99:
        pygame.draw.rect(surf, YELLOW, fill_rect)
    if pct <= 20:
        pygame.draw.rect(surf, RED, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 5)

class Player(pygame.sprite. Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_textures, (100, 75 ))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.hp = 100
        self.shoot_delay = 200
        self.last_shot = pygame.time.get_ticks()

    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        if keystate[pygame.K_SPACE]:
            self.shoot()
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)
    #def alternariveshoot(self):

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_images)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_textures
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill()

 # Load all game graphics
background = pygame.image.load(path.join(textures_dir, "starfield.png")).convert()
background_rect = background.get_rect()
player_textures = pygame.image.load(path.join(textures_dir, "ship.png")).convert()
morthy_textures = pygame.image.load(path.join(textures_dir, "cat.png")).convert()
bullet_textures = pygame.image.load(path.join(textures_dir, "laserRed16.png")).convert()
Altshoot_textures = pygame.image.load(path.join(textures_dir, "laserRed16.png")).convert()
menu = pygame.image.load(path.join(textures_dir, "menu.png")).convert()
menu_rect = menu.get_rect()

meteor_images = []
meteor_list =['cat.png','blue head.png',
              'green head.png','red head.png',
              'yellow head.png']
for img in meteor_list:
    meteor_images.append(pygame.image.load(path.join(textures_dir, img)).convert())


all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

difficulty = 8
for i in range (difficulty):
    mobrespawn()
#Game loop
#game_intro()
running = True
pygame.mixer.music.play(loops = -1)
combo = 0
score = 0
if score > 100:
    difficulty = 10
elif score > 1000:
    difficulty = 12
elif score > 10000:
    difficulty = 15

start_screen = 0
while running:
    if start_screen == 0:
        screen.blit(menu, menu_rect)
        for event in pygame.event.get():
            # check for closing window
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    print("Press")
                    start_screen = 1


    elif start_screen == 1:
        # Process input (events)
        for event in pygame.event.get():
            # check for closing window
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()

        # Update
        all_sprites.update()
        # check to see if a bullet hit a mob
        hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
        for hit in hits:
            combo +=1
            score = combo * 10
            mobrespawn()

        # check to see if a mob hit the player
        hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
        if hits:
            player.hp -= 40
            mobrespawn()
        if player.hp <= 0:
            running = False

        # Draw / render
        screen.fill(BLACK)
        screen.blit(background, background_rect)
        all_sprites.draw(screen)
        draw_text(screen, str(score), 18, WIDTH / 2, 10)
        draw_shield_bar(screen, 5, 5, player.hp)


    # keep loop running at the right speed
    clock.tick(FPS)
    # *after* drawing everything, flip the display
    pygame.display.update()

pygame.quit()