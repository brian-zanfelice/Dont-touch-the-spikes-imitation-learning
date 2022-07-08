import pygame
import simulation


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


def process_inputs():
    global accelerated_mode, training, accelerated_factor
    if keys[pygame.K_a] and not previous_keys[pygame.K_a]:
        accelerated_mode = not accelerated_mode
    if keys[pygame.K_PLUS] and not previous_keys[pygame.K_PLUS]:
        accelerated_factor += 1
    if keys[pygame.K_MINUS] and not previous_keys[pygame.K_MINUS]:
        accelerated_factor -= 1
    accelerated_factor = min(max(1, accelerated_factor), 10)


# Game Loop
running = True
accelerated_mode = (
    False  # If the execution is in accelerated_mode (faster than real world)
)
accelerated_factor = 2
previous_keys = pygame.key.get_pressed()


while running:

    clock.tick(60)
    keys = pygame.key.get_pressed()
    process_inputs()
    simulation.simulate(keys, previous_keys)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    previous_keys = keys
    pygame.display.update()
