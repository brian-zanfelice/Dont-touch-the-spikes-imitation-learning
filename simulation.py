import pygame
import numpy as np
import pandas as pd
import time

SCREEN_WIDTH = 484
SCREEN_HEIGHT = 784 + 10 + 60
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Important lines for the code, change the second line to False if the agent is playing or if you are running any test
# Change to True if you want the agent to play and to False otherwise
IsAgentPlaying = True
SaveState = False  # Change to True if you want to save the game state to the .csv and to False otherwise

# Player
BIRD_SIZE = 46
bird_leftImg = pygame.image.load("bird_left.png")
bird_rightImg = pygame.image.load("bird_right.png")
bird_leftImg = pygame.transform.scale(bird_leftImg, (BIRD_SIZE, BIRD_SIZE))
bird_rightImg = pygame.transform.scale(bird_rightImg, (BIRD_SIZE, BIRD_SIZE))
playerX = SCREEN_WIDTH / 2 - BIRD_SIZE / 2
playerY = 70 / 2 + SCREEN_HEIGHT / 2 - BIRD_SIZE / 2
playerX_velocity = 4
playerY_velocity = 0
previous_x = playerX
previous_y = playerY

# Constants
gravity = 0.3
up_velocity = 7.0
goingright = True
SCREEN_COLOR = (200, 200, 200)
SPIKE_COLOR = (130, 130, 130)
DEATH_COLOR = (255, 124, 124)
DEATH_SPIKE_COLOR = (255, 0, 0)
epsilon = 1.0
ALIVE = False
NUM_SPIKES = 3


# Spikes
matrix_spikes = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
spike_height = 50
spike_width = 28
gap = 14
HEIGHTS_OF_SPIKES_HITBOX = [109, 173, 237, 301, 365, 429, 493, 557, 621, 685, 749, 813]
SPIKE_HITBOX_HEIGHT = 15
SPIKE_HITBOX_WIDTH = 20
RIGHT_SPIKE_HITBOX = SCREEN_WIDTH - SPIKE_HITBOX_WIDTH

# Score
score_value = 0

# Function for saving the game state to the .csv
def save_state(jump):
    global previous_x, previous_y
    data = {
        "X": [],
        "Y": [],
        "Previous_X": [],
        "Previous_Y": [],
        "Spikes_Matrix": [],
        "Jump": [],
    }
    data["X"].append(playerX)
    data["Y"].append(playerY)
    data["Previous_X"].append(previous_x)
    data["Previous_Y"].append(previous_y)
    data["Spikes_Matrix"].append(matrix_spikes)
    data["Jump"].append(jump)
    save_data = pd.DataFrame(data)
    save_data.to_csv("data.csv", mode="a", header=False, index=False)
    previous_x = playerX
    previous_y = playerY


# The functions below are used to create the simulation in pygame and run the game
def alive_right(birdX, birdY):
    show_player_right(birdX, birdY)
    global playerX
    if birdX >= SCREEN_WIDTH - 46:
        playerX = SCREEN_WIDTH - 46
        hit_wall()
    if check_spikes():
        die()


def alive_left(birdX, birdY):
    show_player_left(birdX, birdY)
    global playerX
    if birdX <= 0:
        playerX = 0
        hit_wall()
    if check_spikes():
        die()


def hit_wall():
    global matrix_spikes, goingright, playerX_velocity, score_value
    goingright = not goingright
    score_value = score_value + 1
    playerX_velocity = -playerX_velocity
    if score_value <= 50:
        scheduler()
    if np.random.uniform(0, 1) < epsilon:
        num_spikes = NUM_SPIKES + 1
    else:
        num_spikes = NUM_SPIKES

    for i in range(12):
        matrix_spikes[i] = 0
    for i in range(num_spikes):
        randint = np.random.randint(12, size=1)[0]
        while matrix_spikes[randint]:
            randint = (randint + 1) % 12
        matrix_spikes[randint] = 1


def die():
    global ALIVE, playerX, playerY, playerX_velocity, playerY_velocity, goingright, matrix_spikes, NUM_SPIKES
    if score_value > 0 and ALIVE:
        save_score()
    ALIVE = False
    goingright = True
    playerX = SCREEN_WIDTH / 2 - 46 / 2
    playerY = 70 / 2 + SCREEN_HEIGHT / 2 - 46 / 2
    playerX_velocity = 4
    playerY_velocity = 0
    matrix_spikes = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    NUM_SPIKES = 3
    time.sleep(0.4)


# Function used to save the score to the .txt after you die
def save_score():
    f = open("score.txt", "a")
    f.write(str(score_value) + "\n")
    f.close()


def show_spikes():
    spike_y = 10 + 60 + gap
    spike_x = gap * 2
    y_top = 10 + 60
    y_bottom = SCREEN_HEIGHT - 1
    pygame.draw.rect(screen, SPIKE_COLOR, pygame.Rect(0, 0, SCREEN_WIDTH, 10 + 60))
    # Side spikes
    for i in range(12):
        if matrix_spikes[i]:
            show_spike(spike_y + (spike_height + gap) * i, goingright)
    for i in range(7):
        x_final = spike_x + spike_height
        # Top spikes
        pygame.draw.polygon(
            screen,
            SPIKE_COLOR,
            (
                (spike_x, y_top),
                (x_final, y_top),
                ((spike_x + x_final) / 2, y_top + spike_width),
            ),
        )
        # Bottom spikes
        pygame.draw.polygon(
            screen,
            SPIKE_COLOR,
            (
                (spike_x, y_bottom),
                (x_final, y_bottom),
                ((spike_x + x_final) / 2, y_bottom - spike_width),
            ),
        )
        spike_x = spike_x + spike_height + gap


def show_spike(y_0, right):
    y_final = y_0 + spike_height
    if right:
        x = SCREEN_WIDTH
        x_point = x - spike_width
    else:
        x = 0
        x_point = x + spike_width
    pygame.draw.polygon(
        screen,
        SPIKE_COLOR,
        (
            (x, y_0),
            (x, y_final),
            (x_point, (y_final + y_0) / 2),
        ),
    )


def show_score(x, y):
    font = pygame.font.Font("freesansbold.ttf", 32)
    score = font.render("Score : " + str(score_value), True, (0, 0, 0))
    screen.blit(score, (x, y))


def check_spikes():
    dead = False
    if playerY >= SCREEN_HEIGHT - 46 - spike_width + 16:
        dead = True
    if playerY <= 60 + spike_width - 16:
        dead = True
    if goingright and playerX + BIRD_SIZE >= RIGHT_SPIKE_HITBOX:
        dead = check_spikes_right()
        if dead:
            return dead
    if not goingright and playerX <= SPIKE_HITBOX_WIDTH:
        dead = check_spikes_left()
        if dead:
            return dead

    return dead


def check_spikes_left():
    y_real = playerY - 70
    index = int(y_real / (gap + spike_height))
    vetor = [(index - 1) % 12, index, (index + 1) % 12]
    for i in vetor:
        if matrix_spikes[i]:
            spike_hitbox = pygame.Rect(
                0,
                HEIGHTS_OF_SPIKES_HITBOX[i] - SPIKE_HITBOX_HEIGHT / 2,
                SPIKE_HITBOX_WIDTH,
                SPIKE_HITBOX_HEIGHT,
            )
            bird_hitbox = pygame.Rect(playerX, playerY, BIRD_SIZE, BIRD_SIZE)
            hit = pygame.Rect.colliderect(spike_hitbox, bird_hitbox)
            if hit:
                return True
    return False


def check_spikes_right():
    y_real = playerY - 70
    index = int(y_real / (gap + spike_height))
    vetor = [(index - 1) % 12, index, (index + 1) % 12]
    for i in vetor:
        if matrix_spikes[i]:
            spike_hitbox = pygame.Rect(
                RIGHT_SPIKE_HITBOX,
                HEIGHTS_OF_SPIKES_HITBOX[i] - SPIKE_HITBOX_HEIGHT / 2,
                SPIKE_HITBOX_WIDTH,
                SPIKE_HITBOX_HEIGHT,
            )
            bird_hitbox = pygame.Rect(playerX, playerY, BIRD_SIZE, BIRD_SIZE)
            hit = pygame.Rect.colliderect(spike_hitbox, bird_hitbox)
            if hit:
                return True
    return False


# A scheduler used to increase the number of spikes and the X velocity of the birds
def scheduler():
    global playerX_velocity, NUM_SPIKES, epsilon, SCREEN_COLOR, SPIKE_COLOR
    if score_value % 5 == 0:
        if playerX_velocity > 0:
            playerX_velocity += 0.3
        else:
            playerX_velocity -= 0.3

    if score_value % 10 == 0:
        NUM_SPIKES += 1
        epsilon -= 0.2
    if score_value == 50:
        SCREEN_COLOR = DEATH_COLOR
        SPIKE_COLOR = DEATH_SPIKE_COLOR


def game_over(keys, previous_keys):
    global ALIVE, score_value, playerY_velocity, SCREEN_COLOR, SPIKE_COLOR
    over_font = pygame.font.Font("freesansbold.ttf", 32)
    over_text = over_font.render("PRESS SPACE TO START", True, (255, 255, 255))
    screen.blit(over_text, (0 + 50, SCREEN_HEIGHT / 2 + 100))
    show_player_right(playerX, playerY)
    SCREEN_COLOR = (200, 200, 200)
    SPIKE_COLOR = (130, 130, 130)
    if keys[pygame.K_SPACE] and not previous_keys[pygame.K_SPACE] or IsAgentPlaying:
        playerY_velocity = up_velocity
        ALIVE = True
        score_value = 0


def show_player_right(x, y):
    screen.blit(bird_rightImg, (x, y))


def show_player_left(x, y):
    screen.blit(bird_leftImg, (x, y))


# The main function that calls other functions and runs the game
def simulate(net, keys, previous_keys):

    screen.fill(SCREEN_COLOR)
    global playerY_velocity, playerX, playerY, ALIVE
    if ALIVE:
        playerY_velocity = playerY_velocity - gravity
        jump = 0

        # If the agent is playing
        if IsAgentPlaying:
            input_predict = [
                [
                    playerX + playerX_velocity,
                    playerY - playerY_velocity,
                    playerX,
                    playerY,
                    *matrix_spikes,
                ]
            ]
            jump_predict = net.predict(input_predict)
            print(jump_predict[0][0])
            if jump_predict[0][0] >= 0.5:
                jump = 1
        if (keys[pygame.K_SPACE] and not previous_keys[pygame.K_SPACE]) or jump:
            playerY_velocity = up_velocity
            jump = 1
        if SaveState:
            save_state(jump)
        playerX = playerX + playerX_velocity
        playerY = playerY - playerY_velocity
        if goingright:
            alive_right(playerX, playerY)
        else:
            alive_left(playerX, playerY)

        show_spikes()
        show_score(10, 10)

    else:
        game_over(keys, previous_keys)
        show_score(10, 10)
