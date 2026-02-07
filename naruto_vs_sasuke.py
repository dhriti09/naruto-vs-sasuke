# pylint: disable=no-member
"""
A Naruto vs Sasuke fighting game using Pygame.
"""
import pygame

pygame.init()


WIN_WIDTH, WIN_HEIGHT = 700, 500
win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Naruto vs Sasuke")


WALK_RIGHT = [
    pygame.image.load('pics\\NR2.png'),
    pygame.image.load('pics\\NR3.png'),
    pygame.image.load('pics\\NR1.png')
]
WALK_LEFT = [
    pygame.image.load('pics\\NL2.png'),
    pygame.image.load('pics\\NL3.png'),
    pygame.image.load('pics\\NL1.png')
]
BG = pygame.image.load('pics\\bg.png')
NH = pygame.image.load('pics\\Nh.png')
SH = pygame.image.load('pics\\Sh.png')

# Load Sounds
HIT_SOUND = pygame.mixer.Sound("pics\\hit.wav")

CLOCK = pygame.time.Clock()


class Player:
    """Class representing the player character (Naruto)."""
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = 10
        self.isjump = False
        self.jump_height = 10
        self.left = False
        self.right = False
        self.walk_count = 0
        self.standing = True
        self.hitbox = (self.x + 10, self.y + 5, 80, 80)
        self.health = 200

    def draw(self, window):
        """Draws Naruto and his health bar."""
        if self.health > 0:
            if self.walk_count + 1 >= 6:
                self.walk_count = 0

            if not self.standing:
                if self.left:
                    window.blit(WALK_LEFT[self.walk_count // 2], (self.x, self.y))
                    self.walk_count += 1
                elif self.right:
                    window.blit(WALK_RIGHT[self.walk_count // 2], (self.x, self.y))
                    self.walk_count += 1
            else:
                img_path = 'pics\\NR1.png' if self.right else 'pics\\NL1.png'
                window.blit(pygame.image.load(img_path), (self.x, self.y))

            self.hitbox = (self.x + 10, self.y + 5, 80, 80)
            pygame.draw.rect(window, (255, 0, 0), (80, 40, 210, 25))
            pygame.draw.rect(window, (255, 255, 0), (80, 45, self.health, 15))
        else:
            font = pygame.font.SysFont('comicsans', 30, True)
            msg = font.render('Sasuke Wins', True, (255, 255, 255), (0, 0, 100))
            window.blit(msg, (180, 200))
            window.blit(pygame.image.load('pics\\Nd.png'), (self.x, self.y))

    def hit(self):
        """Reduces player health when hit."""
        if self.health > 0:
            self.health -= 5


class Weapons:
    """Class representing the projectile weapon."""
    def __init__(self, x, y, facing):
        self.x = x
        self.y = y
        self.facing = facing
        self.vel = 8 * facing
        self.hitbox = (self.x, self.y, 40, 40)

    def draw(self, window):
        """Draws the shuriken."""
        window.blit(pygame.image.load('pics\\shur.png'), (self.x, self.y))
        self.hitbox = (self.x, self.y, 40, 40)


class Enemy:
    """Class representing the enemy character (Sasuke)."""
    WALK_RIGHT_S = [
        pygame.image.load('pics\\SR2.png'),
        pygame.image.load('pics\\SR3.png'),
        pygame.image.load('pics\\SR1.png')
    ]
    WALK_LEFT_S = [
        pygame.image.load('pics\\SL2.png'),
        pygame.image.load('pics\\SL3.png'),
        pygame.image.load('pics\\SL1.png')
    ]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.speed = 8
        self.walk_count = 0
        self.hitbox = (self.x + 10, self.y + 5, 80, 80)
        self.health = 200

    def draw(self, window):
        """Moves and draws Sasuke."""
        self.move()
        if self.health > 0:
            if self.walk_count + 1 >= 6:
                self.walk_count = 0
            if self.speed > 0:
                window.blit(self.WALK_RIGHT_S[self.walk_count // 2], (self.x, self.y))
                self.walk_count += 1
            else:
                window.blit(self.WALK_LEFT_S[self.walk_count // 2], (self.x, self.y))
                self.walk_count += 1

            self.hitbox = (self.x + 10, self.y + 5, 80, 80)
            pygame.draw.rect(window, (255, 0, 0), (410, 40, 210, 25))
            pygame.draw.rect(window, (255, 255, 0), (620, 45, -self.health, 15))
        else:
            self.speed = 0
            font = pygame.font.SysFont('comicsans', 30, True)
            msg = font.render('Naruto Wins', True, (255, 100, 10), (0, 0, 100))
            window.blit(msg, (180, 200))
            window.blit(pygame.image.load('pics\\Sd.png'), (self.x, self.y))

    def move(self):
        """Logic for automatic movement along the path."""
        if self.speed > 0:
            if self.x + self.speed < self.path[1]:
                self.x += self.speed
            else:
                self.speed *= -1
                self.walk_count = 0
        else:
            if self.x - abs(self.speed) > self.path[0]:
                self.x += self.speed
            else:
                self.speed *= -1
                self.walk_count = 0

    def hit(self):
        """Reduces enemy health."""
        if self.health > 0:
            self.health -= 10


def redraw_game_window():
    """Renders all elements to the screen."""
    win.blit(BG, (0, 0))
    naruto.draw(win)
    sasuke.draw(win)
    win.blit(NH, (10, 10))
    win.blit(SH, (600, 10))
    for item in shurikens:
        item.draw(win)
    pygame.display.update()


# Game Instances
naruto = Player(30, 400, 100, 100)
sasuke = Enemy(100, 400, 100, 100, 600)
shurikens = []
THROW_SPEED = 0
RUN = True

# Main Loop
while RUN:
    CLOCK.tick(25)
    if THROW_SPEED > 0:
        THROW_SPEED += 1
    if THROW_SPEED > 3:
        THROW_SPEED = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUN = False

    # Collision: Naruto & Sasuke
    if naruto.health > 0 and sasuke.health > 0:
        if naruto.hitbox[1] < sasuke.hitbox[1] + sasuke.hitbox[3] and \
           naruto.hitbox[1] + naruto.hitbox[3] > sasuke.hitbox[1]:
            if naruto.hitbox[0] + naruto.hitbox[2] > sasuke.hitbox[0] and \
               naruto.hitbox[0] < sasuke.hitbox[0] + sasuke.hitbox[2]:
                naruto.hit()
                HIT_SOUND.play()
    else:
        if naruto.health <= 0:
            naruto.speed = 0

    # Shuriken Collision & Movement
    for shuriken in shurikens[:]:
        if sasuke.health > 0:
            # Check if shuriken hits Sasuke's hitbox
            if (shuriken.hitbox[1] + shuriken.hitbox[3] // 2 > sasuke.hitbox[1] and
                shuriken.hitbox[1] + shuriken.hitbox[3] // 2 < sasuke.hitbox[1] + sasuke.hitbox[3]):
                if (shuriken.hitbox[0] + shuriken.hitbox[2] > sasuke.hitbox[0] and
                    shuriken.hitbox[0] + shuriken.hitbox[2] < sasuke.hitbox[0] + sasuke.hitbox[2]):
                    sasuke.hit()
                    HIT_SOUND.play()
                    shurikens.remove(shuriken)
                    continue
        else:
            sasuke.speed = 0

        if 0 < shuriken.x < 700:
            shuriken.x += shuriken.vel
        else:
            shurikens.remove(shuriken)

    # Input Logic
    keys = pygame.key.get_pressed()

    # Throwing
    if keys[pygame.K_SPACE] and THROW_SPEED == 0:
        FACING = -1 if naruto.left else 1
        if len(shurikens) < 5:
            shurikens.append(Weapons(round(naruto.x + 60), round(naruto.y + 30), FACING))
        THROW_SPEED = 1

    # Horizontal Movement
    if keys[pygame.K_LEFT] and naruto.x > naruto.speed:
        naruto.x -= naruto.speed
        naruto.left, naruto.right, naruto.standing = True, False, False
    elif keys[pygame.K_RIGHT] and naruto.x < 690 - naruto.width - naruto.speed:
        naruto.x += naruto.speed
        naruto.left, naruto.right, naruto.standing = False, True, False
    else:
        naruto.standing = True
        naruto.walk_count = 0

    # Jump Logic
    if not naruto.isjump:
        if keys[pygame.K_UP]:
            naruto.isjump = True
            naruto.walk_count = 0
    else:
        if naruto.jump_height >= -10:
            NEG = 1 if naruto.jump_height >= 0 else -1
            naruto.y -= (naruto.jump_height ** 2) * 0.5 * NEG
            naruto.jump_height -= 1
        else:
            naruto.isjump = False
            naruto.jump_height = 10

    redraw_game_window()

pygame.quit()
