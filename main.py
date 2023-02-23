import pygame
import keras
from simulation import simulate


SCREEN_WIDTH = 484
SCREEN_HEIGHT = 784 + 10 + 60

# Intialize the pygame
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Don't Touch the Spikes")
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)
font = pygame.font.Font("freesansbold.ttf", 32)


# Game Loop
running = True
previous_keys = pygame.key.get_pressed()

# Neural Network loaded after the training
net = keras.models.load_model("my_model")

# Pygame loop for running the game
while running:

    clock.tick(60)
    keys = pygame.key.get_pressed()
    simulate(net, keys, previous_keys)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    previous_keys = keys
    pygame.display.update()
