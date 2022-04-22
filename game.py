# Start out program

# import the pygame module
import pygame

# from pygame.math import Vector
from pygame.math import Vector2

# import pygame.locals for easier access to key coordinates
from pygame.locals import (
    RLEACCEL,
    K_SPACE,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# init pygame
pygame.init()

# set game window width and height (DEFAULT: SCREEN_WIDTH = 1200, SCREEN_HEIGHT = 800)
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

# Create the screen object
display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Py_Bots', './assets/imgs/icon.png')


class Background(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load('./assets/imgs/background_1.png').convert()
        self.rect = self.surf.get_rect()


screen = Background()

# create sprite groups
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
game_objects = pygame.sprite.Group()


class GameObjects(pygame.sprite.Sprite):
    p_velo = Vector2(1, 0)
    e_velo = Vector2(-1, 0)

    def __init__(self):
        super().__init__()

    def _get_game_objects(self):
        game_objects.add(*enemies, *bullets)

        if player:
            game_objects.add(player)

        return game_objects


class Bullet(GameObjects):
    def __init__(self, b_type, velo_type):
        super().__init__()
        self.surf = b_type
        self.surf.set_colorkey((100, 0, 86.2), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.bounding_rect = self.surf.get_bounding_rect()
        self.velocity = velo_type


class Enemy(GameObjects):
    type_e = pygame.image.load('./assets/imgs/enemy_bullet.png')
    type_e.set_colorkey((100, 0, 86.2), RLEACCEL)
    
    def __init__(self):
        super().__init__()

    class Crocodile(GameObjects):
        def __init__(self, x_pos, y_pos):
            super().__init__()
            self.surf = pygame.image.load('./assets/imgs/crocodile.png')
            self.surf.set_colorkey((100, 0, 86.2), RLEACCEL)
            self.rect = self.surf.get_rect(center=(x_pos, y_pos))
            self.velocity = Vector2(-0.3, 0)

        def update(self):
            # Check if any bullets have collided with the enemy
            if pygame.sprite.spritecollideany(self, bullets):
                # If so, then remove the player and stop the loop
                player.kill()
                self.surf = pygame.image.load('./assets/imgs/explosion.png').convert()
                self.kill()

    class SawBot(GameObjects):
        def __init__(self, x_pos, y_pos):
            super().__init__()
            self.surf = pygame.image.load('./assets/imgs/saw_bot.png').convert()
            self.surf.set_colorkey((100, 0, 86.2), RLEACCEL)
            self.rect = self.surf.get_rect(center=(x_pos, y_pos))
            self.velocity = Vector2(-0.3, 0)

        def update(self):
            # Check if any bullets have collided with the enemy
            if pygame.sprite.spritecollideany(self, bullets):
                # If so, then remove the player and stop the loop
                self.surf = pygame.image.load('./assets/imgs/explosion.png').convert()

                self.kill()

    class Turret(GameObjects):
        def __init__(self, x_pos, y_pos):
            super().__init__()
            self.surf = pygame.image.load('./assets/imgs/turret_open.png').convert()
            self.surf.set_colorkey((100, 0, 86.2), RLEACCEL)
            self.rect = self.surf.get_rect(center=(x_pos, y_pos))
            self.functioning = 1

        def update(self):
            # Check if any bullets have collided with the enemy
            if pygame.sprite.spritecollideany(self, bullets):
                # If so, then remove the player and stop the loop
                self.functioning = 0
                self.surf = pygame.image.load('./assets/imgs/explosion.png').convert()
                self.kill()

            while self.functioning > 0:

                e_bullet = Bullet(Enemy.type_e, GameObjects.e_velo)
                bullets.add(e_bullet)


class Player(GameObjects):
    HEALTH = 3

    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load('./assets/imgs/player_bot_1.png').convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(center=(SCREEN_WIDTH-1100, SCREEN_HEIGHT-120))
        self.hit = False

    def update(self, pressed_keys):

        # if hit, subtract one player.HEALTH point
        if self.HEALTH <= 0:
            self.surf = pygame.image.load('./assets/imgs/explosion.png').convert()
            self.kill()

        # Check if any enemies have collided with the player
        if pygame.sprite.spritecollideany(player, enemies):
            # If so, then the player loses a life
            self.hit = True

        if self.hit:
            self.HEALTH = player.HEALTH - 1
            self.hit = False

        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-2, 0)

        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(2, 0)

        if pressed_keys[K_SPACE]:
            type_p = pygame.image.load('./assets/imgs/player_bullet.png').convert()
            type_p.set_colorkey((100, 0, 86.2), RLEACCEL)
            bullet = Bullet(type_p, GameObjects.p_velo)
            bullets.add(bullet)

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0


# create player
player = Player()

# add player to game_objects group
game_objects.add(player)

# create enemies for the game start and add them to 
turret_1 = Enemy.Turret(SCREEN_WIDTH-200, SCREEN_HEIGHT-100)
saw_bot_1 = Enemy.SawBot(SCREEN_WIDTH-460, SCREEN_HEIGHT-100)
crocodile = Enemy.Crocodile(SCREEN_WIDTH-500, SCREEN_HEIGHT-100)
turret_2 = Enemy.Turret(SCREEN_WIDTH-150, SCREEN_HEIGHT-150)
saw_bot_2 = Enemy.SawBot(SCREEN_WIDTH-440, SCREEN_HEIGHT-100)

enemies.add(turret_1, saw_bot_1, turret_2, saw_bot_2, crocodile)

# variable to keep main loop running
running = True

# MAIN LOOP
while running:
    # Look at event queue
    for event in pygame.event.get():
        # Did the user hit a key?
        if event.type == KEYDOWN:
            # Was it the Escape key? If so, stop the loop
            if event.key == K_ESCAPE:
                running = False

        # Did the user click the 'Close' button? If so, stop the loop
        elif event.type == QUIT:
            running = False

    # fill screen with background image
    display.blit(screen.surf, screen.rect)

    # get currently pressed keys
    pressed_keys = pygame.key.get_pressed()

    # update player sprite based on user key presses
    player.update(pressed_keys)

    # Draw all sprites
    for entity in game_objects:
        display.blit(entity.surf, entity.rect)

    pygame.display.flip()
