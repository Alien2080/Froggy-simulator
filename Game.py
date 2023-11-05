# Froggy pet simulator.
# By Eleanor Aylen and Tom Aylen
# Created 4/11/23

# Import and initialise the pygame library.
import pygame
import random
pygame.init()

# constants.
BLACK = (0, 0, 0)
WHITE = (250, 250, 250)
POOP_BROWN = (87, 53, 4)
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500


# Define the Froggy object by extending pygame.sprite.Sprite
class Froggy(pygame.sprite.Sprite):
    def __init__(self):
        super(Froggy, self).__init__()
        # use convert.alpha for a transperent background.
        self.image = pygame.image.load("Images\Frog.svg").convert_alpha()
        self.rect = self.image.get_rect()
        # set the initial staarting position of the Frog.
        self.rect.center = [250, 250]

    def update(self):
        self.rect.move_ip(random.randint(-1, 1), random.randint(-1, 1))
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
        self.surface = pygame.Surface((40, 40), pygame.SRCALPHA)
        # now we can draw poopy on the surface.
        pygame.draw.circle( self.surface, POOP_BROWN, (20, 20), 20)
        # now we can use the surface, with the drawn poopy, as the sprite image
        self.image =  self.surface
        # create a rect (hitbox) for the sprite.
        self.rect = self.image.get_rect()
        # move the sprite to the given Froggy position.
        self.rect.center = froggy_position


# Set up the drawing window.
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption('Froggy simulator demo')

# Set up Froggy.
froggy = Froggy()

# create group for frog sprites.
frog_sprites = pygame.sprite.Group()
frog_sprites.add(froggy)
# create group for poop sprites.
poop_sprites = pygame.sprite.Group()

# Create custom event to control Frog movement.
MOVEFROGGY = pygame.USEREVENT + 1
pygame.time.set_timer(MOVEFROGGY, 100)

# Main game loop.
running = True
while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == MOVEFROGGY:
            frog_sprites.update()
            poop_sprites.add(Poop(froggy.rect.center))

    # first draw the black over everything to remove old sprites.
    screen.fill("black")
    poop_sprites.draw(screen)
    frog_sprites.draw(screen)
    pygame.display.update()

# Done! Time to quit.
pygame.quit()