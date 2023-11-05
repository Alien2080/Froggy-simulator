# Froggy pet simulator.
# By Eleanor Aylen and Tom Aylen
# Created 4/11/23

# Import and initialize the pygame library
import pygame
import random
pygame.init()

# constants.
BLACK = (0, 0, 0)
WHITE = (250, 250, 250)
POOP_BROWN = (87, 53, 4)
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

# Define the Player object by extending pygame.sprite.Sprite
# Instead of a surface, use an image for a better-looking sprite
class Froggy(pygame.sprite.Sprite):
    def __init__(self):
        super(Froggy, self).__init__()
        self.image = pygame.image.load("Images\Frog.svg").convert()
        self.rect = self.image.get_rect()
        self.rect.center =  [250, 250]

    def move(self):
        screen.fill((0, 0, 0))
        self.rect.move_ip(random.randint(-5, 5), random.randint(-5, 5))
        if (self.rect.right > SCREEN_WIDTH):
            self.rect.right = SCREEN_WIDTH
        if (self.rect.top > SCREEN_HEIGHT):
            self.rect.top = SCREEN_HEIGHT
        if (self.rect.left < 0):
            self.rect.left = 0
        if (self.rect.bottom < 0):
            self.rect.bottom = 0

class Poop(pygame.sprite.Sprite):
    def __init__(self, froggy_position):
        super(Poop, self).__init__()
        # first we need surface to draw poopy on
        self.image = pygame.Surface((20, 20))
        self.image.fill(BLACK)  
        pygame.draw.circle(screen, POOP_BROWN, froggy_position, 20, 5)
        self.rect = self.image.get_rect()

# Set up the drawing window
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption('Froggy simulator demo')

#set up Froggy\ draw Froggy
froggy = Froggy()

all_sprites = pygame.sprite.Group()
all_sprites.add(froggy)

MOVEFROGGY = pygame.USEREVENT + 1
pygame.time.set_timer(MOVEFROGGY, 500)

# Run until the user asks to quit
running = True
while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Add a new cloud?
        elif event.type == MOVEFROGGY:
            froggy.move()
            poop = Poop(froggy.rect.center)
            all_sprites.add(poop)

    # Flip the display
    pygame.display.flip()
    all_sprites.draw(screen)

# Done! Time to quit.
pygame.quit()