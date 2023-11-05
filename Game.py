# Froggy pet simulator.
# By Eleanor Aylen and Tom Aylen
# Created 4/11/23

# Import and initialise the pygame library.
import pygame
import random
pygame.init()

# Constants.
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
        # set the initial starting position of the Frog.
        self.rect.center = [250, 250]
        # set the initial direction of movement of the Frog.
        self.dx = 0
        self.dy = 0

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy
        # If touching the edge then reverse direction in that plane.
        if (self.rect.right > SCREEN_WIDTH):           
            self.dx = 0 - self.dx
        if (self.rect.top < 0):
            self.dy = 0 - self.dy
        if (self.rect.left < 0):
            self.dx = 0 - self.dx
        if (self.rect.bottom > SCREEN_HEIGHT):
            self.dy = 0 - self.dy


class Poop(pygame.sprite.Sprite):
    def __init__(self, froggy_position):
        super(Poop, self).__init__()
        # first we need surface to draw poopy on
        self.surface = pygame.Surface((40, 40), pygame.SRCALPHA)
        # now we can draw poopy on the surface.
        pygame.draw.circle(self.surface, POOP_BROWN, (20, 20), 20) 
        pygame.draw.circle(self.surface, BLACK, (20, 20), 20, 2)       
        # now we can use the surface, with the drawn poopy, as the sprite image
        self.image = self.surface
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

# Create custom event to draw Frog movement.
MOVEFROGGY = pygame.USEREVENT + 1
# 15 milliseconds refresh rate is a bit over 60 FPS. So this should be smooth movement.
pygame.time.set_timer(MOVEFROGGY, 15)

# Create custom event to change Frog direction.
CHANGEMOVEMENT = pygame.USEREVENT + 2
pygame.time.set_timer(CHANGEMOVEMENT, random.randint(1000, 3000))

# Create custom event to poop.
POOPTIME = pygame.USEREVENT + 3
pygame.time.set_timer(POOPTIME, random.randint(5000, 15000))

# Main game loop.
running = True
while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == MOVEFROGGY:
            # Move from in current direction.
            frog_sprites.update()

        elif event.type == CHANGEMOVEMENT:
            # Randomly pick a new x and y direction. 0 means it will not move in that direction.
            froggy.dx = random.randint(-1, 1)
            froggy.dy = random.randint(-1, 1)
            pygame.time.set_timer(CHANGEMOVEMENT, random.randint(1000, 3000))
        
        elif event.type == POOPTIME:
            # If poop time add a new Poop sprite to the poop group at Froggies current location.
            poop_sprites.add(Poop(froggy.rect.center))
            pygame.time.set_timer(POOPTIME, random.randint(5000, 15000))

        
    # First draw black over everything to remove old sprites.
    screen.fill("black")
    poop_sprites.draw(screen)
    frog_sprites.draw(screen)
    pygame.display.update()

# Done! Time to quit.
pygame.quit()