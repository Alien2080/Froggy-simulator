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


# Set up the drawing window
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

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
   
    # Draw a solid blue circle in the center
    # pygame.draw.circle(screen, (0, 0, 255), (250, 250), 75)

    
    # Flip the display
    pygame.display.flip()

    all_sprites.draw(screen)

# Done! Time to quit.
pygame.quit()