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
        # glide or hop.
        self.movementStyle = 'hop'
        # set the initial direction of movement of the Frog. Used in the glide movement.
        self.dx = 0
        self.dy = 0
        # below is used in the hop movement.
        self.hopping = False   
        self.hopSteps = []
        self.hopIndex = 0
        self.hunger = 0
  
    def calculateHop(self, landingPosition_x, landingPosition_y):
        # Clear previous values.
        self.hopIndex = 0
        self.hopSteps = []
        # Detemine which plane the greatest hop length is in.
        if (landingPosition_x > self.rect.centerx):
            hopLength_x = landingPosition_x - self.rect.centerx
            xModifier = 1
        else:
            hopLength_x = self.rect.centerx - landingPosition_x
            xModifier = -1

        if (landingPosition_y > self.rect.centery):
            hopLength_y = landingPosition_y - self.rect.centery
            yModifier = 1
        else:
            hopLength_y = self.rect.centery - landingPosition_y
            yModifier = -1

        # Calculate the hop steps.
        if (hopLength_x > hopLength_y):
            if (hopLength_x <= 0):
                   return           
            for pixel in range(0, hopLength_x + 1, 1):
                self.hopSteps.append((int(self.rect.centerx + (pixel * xModifier)), self.rect.centery + int(((pixel * yModifier) * (hopLength_y/hopLength_x)))))
        else:
            if (hopLength_y <= 0):
                   return
            for pixel in range(0, hopLength_y + 1,1 ):
                self.hopSteps.append((self.rect.centerx + int(((pixel * xModifier) * (hopLength_x/hopLength_y))), int(self.rect.centery + (pixel * yModifier))))  

        self.addHopVertical(self.hopSteps)  
        # add step to ensure hop finishes on the exact landing position.
        self.hopSteps.append((landingPosition_x, landingPosition_y))
        self.hopping = True
        self.movementStyle = 'hop'

    def addHopVertical(self, hopSteps):
        maxHeightAdded = 2 + 0.5 * len(hopSteps)
        exp = 0.4
        #Find mid step
        midPoint = int(len(hopSteps)/2)
        for i in range(0, midPoint, 1):
            delta_y = int(maxHeightAdded*(pow(i+1, exp)/pow(midPoint, exp)))
            hopSteps[i] = list(hopSteps[i])[0], list(hopSteps[i])[1] - delta_y
            hopSteps[len(hopSteps) - 1 - i] = list(hopSteps[len(hopSteps) - 1 - i])[0], list(hopSteps[len(hopSteps) - 1 - i])[1] - delta_y   
        if len(hopSteps)%2 == 1:           
            hopSteps[midPoint] = list(hopSteps[midPoint])[0], list(hopSteps[midPoint])[1] - maxHeightAdded

    def update(self):
        match (self.movementStyle):
            case 'hop':
                if (self.hopIndex >= len(self.hopSteps) or len(self.hopSteps) == 0):
                    self.hopping = False
                    # self.movementStyle = 'glide'
                else:
                    self.rect.center = self.hopSteps[self.hopIndex]
                    self.hopIndex += 1
            case 'glide':
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
        pygame.draw.circle(self.surface, POOP_BROWN, (20, 20), 5) 
        pygame.draw.circle(self.surface, BLACK, (20, 20), 5, 2)       
        # now we can use the surface, with the drawn poopy, as the sprite image
        self.image = self.surface
        # create a rect (hitbox) for the sprite.
        self.rect = self.image.get_rect()
        # move the sprite to the given Froggy position.
        self.rect.center = froggy_position


class FoodButton(pygame.sprite.Sprite):
    def __init__(self):
        super(FoodButton, self).__init__()
        self.image = pygame.image.load("Images\FoodBowl_button.svg").convert_alpha()
        self.rect = self.image.get_rect()
        # set the initial starting position of the Frog.
        self.rect.center = [450, 450]


def renderUItext(screen):
    # render hunger level.
    hunger_img = font.render('Hunger: {}'.format(froggy.hunger), True, WHITE)
    screen.blit(hunger_img, (20, 20))


# Set up the drawing window.
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption('Froggy simulator demo')

# Set up font for UI elements.
font = pygame.font.SysFont(None, 24)

# Set up Froggy.
froggy = Froggy()

# create group for frog sprites.
frog_sprites = pygame.sprite.Group()
frog_sprites.add(froggy)
# create group for poop sprites.
poop_sprites = pygame.sprite.Group()
#create group for buttons
buttons_sprites = pygame.sprite.Group()
buttons_sprites.add(FoodButton())

# Create custom event to draw Frog movement.
MOVEFROGGY = pygame.USEREVENT + 1
# 15 milliseconds refresh rate is a bit over 60 FPS. So this should be smooth movement.
pygame.time.set_timer(MOVEFROGGY, 15)

# Create custom event to change Frog direction.
CHANGEGLIDEDIRECTION = pygame.USEREVENT + 2
pygame.time.set_timer(CHANGEGLIDEDIRECTION, random.randint(1000, 3000))

# Create custom event to poop.
POOPTIME = pygame.USEREVENT + 3
pygame.time.set_timer(POOPTIME, random.randint(15000, 30000))

# Create custom event to poop.
HOP = pygame.USEREVENT + 4
pygame.time.set_timer(HOP, random.randint(4000, 6000))

HUNGERTIME = pygame.USEREVENT + 5
pygame.time.set_timer(HUNGERTIME, 4*1000)

# Main game loop.
print('starting game loop')
running = True
while running:
    
    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == MOVEFROGGY:
            # Move from in current direction.
            frog_sprites.update()

        elif event.type == CHANGEGLIDEDIRECTION:
            if (froggy.movementStyle == 'glide'):
                # Randomly pick a new x and y direction. 0 means it will not move in that direction.
                newdx = random.randint(-1, 1)
                newdy = random.randint(-1, 1)
                froggy.dx = newdx
                froggy.dy = newdy
                pygame.time.set_timer(CHANGEGLIDEDIRECTION, random.randint(1000, 3000))
                print('changing glide direction: {}, {}'.format(newdx, newdy))
        
        elif event.type == POOPTIME:
            if (not froggy.hopping):
                # If poop time add a new Poop sprite to the poop group at Froggies current location.
                poop_sprites.add(Poop(froggy.rect.center))
                pygame.time.set_timer(POOPTIME, random.randint(5000, 15000))

        elif event.type == HOP:
            if (not froggy.hopping):
                newdx = random.randint(150, 350)
                newdy = random.randint(150, 350)
                froggy.calculateHop(newdx, newdy)
                print('calculating new hoop: {}, {}'.format(newdx, newdy))

        elif event.type == HUNGERTIME:
             froggy.hunger = froggy.hunger + 1
             print('Hunger: {}'.format(froggy.hunger))
             if (froggy.hunger == 10):
                 print( "froggy dead you lose")
        
    # First draw black over everything to remove old sprites.
    screen.fill("black")
    poop_sprites.draw(screen)
    frog_sprites.draw(screen)
    buttons_sprites.draw(screen)
    renderUItext(screen)
    pygame.display.update()

# Done! Time to quit.
pygame.quit()