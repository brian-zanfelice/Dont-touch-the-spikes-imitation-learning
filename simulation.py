import pygame
import numpy as np
from utils import game_state
import time

SCREEN_WIDTH = 484
SCREEN_HEIGHT = 784 + 10 + 60
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Change to True if you want the agent to play and to False otherwise
IS_AGENT_PLAYING = False
SAVE_STATE = True  # Change to True if you want to save the game state to the .csv and to False otherwise
JUMP_THRESHOLD = 0.07

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
SPIKES_MATRIX = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
spike_height = 50
spike_width = 28
GAP = 14
HEIGHTS_OF_SPIKES_HITBOX = [109, 173, 237, 301, 365, 429, 493, 557, 621, 685, 749, 813]
SPIKE_HITBOX_HEIGHT = 15
SPIKE_HITBOX_WIDTH = 20
RIGHT_SPIKE_HITBOX = SCREEN_WIDTH - SPIKE_HITBOX_WIDTH

# Score
score_value = 0
GAME_STATE = game_state(playerX, playerY, SPIKES_MATRIX)

# Function for saving the game state to the .csv
def save_state(state: game_state, jump: bool, x_velocity: float):
    state.save_state(jump, x_velocity)
    state.previous_x = state.x
    state.previous_y = state.y
    return state


# The functions below are used to create the simulation in pygame and run the game
def alive_right(state):
    show_player_right(state.x, state.y)
    if state.x >= SCREEN_WIDTH - 46:
        state.x = SCREEN_WIDTH - 46
        state = hit_wall(state)
    if check_spikes(state):
        state = die()
    return state


def alive_left(state):
    show_player_left(state.x, state.y)
    if state.x <= 0:
        state.x = 0
        state = hit_wall(state)
    if check_spikes(state):
        state = die()
    return state


def hit_wall(state):
    global goingright, playerX_velocity, score_value
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
        state.spikes_matrix[i] = 0
    for i in range(num_spikes):
        randint = np.random.randint(12, size=1)[0]
        while state.spikes_matrix[randint]:
            randint = (randint + 1) % 12
        state.spikes_matrix[randint] = 1
    return state


def die():
    global ALIVE, playerX_velocity, playerY_velocity, goingright, NUM_SPIKES
    if score_value > 0 and ALIVE:
        save_score()
    ALIVE = False
    goingright = True
    playerX_velocity = 4
    playerY_velocity = 0
    NUM_SPIKES = 3
    time.sleep(0.35)
    state = game_state(playerX, playerY, SPIKES_MATRIX)
    return state


# Function used to save the score to the .txt after you die
def save_score():
    file = "score.txt"
    if IS_AGENT_PLAYING:
        file = "agent_score.txt"
    f = open(file, "a")
    f.write(str(score_value) + "\n")
    f.close()


def show_spikes(state: game_state):
    spike_y = 10 + 60 + GAP
    spike_x = GAP * 2

    y_top = 10 + 60
    y_bottom = SCREEN_HEIGHT - 1
    pygame.draw.rect(screen, SPIKE_COLOR, pygame.Rect(0, 0, SCREEN_WIDTH, 10 + 60))
    # Side spikes
    for i in range(12):
        if state.spikes_matrix[i]:

            show_spike(spike_y + (spike_height + GAP) * i, goingright)

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
        spike_x = spike_x + spike_height + GAP


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


def check_spikes(state):
    dead = False
    if state.y >= SCREEN_HEIGHT - 46 - spike_width + 16:
        return True
    if state.y <= 60 + spike_width - 16:
        return True
    if goingright and (state.x + BIRD_SIZE >= RIGHT_SPIKE_HITBOX):
        dead = check_spikes_right(state)
        if dead:
            return dead
    elif not goingright and (state.x <= SPIKE_HITBOX_WIDTH):
        dead = check_spikes_left(state)
        if dead:
            return dead
    return dead


def check_spikes_left(state):
    y_real = state.y - 70
    index = int(y_real / (GAP + spike_height))

    vector = [(index - 1) % 12, index, (index + 1) % 12]
    for i in vector:
        if state.spikes_matrix[i]:
            spike_hitbox = pygame.Rect(
                0,
                HEIGHTS_OF_SPIKES_HITBOX[i] - SPIKE_HITBOX_HEIGHT / 2,
                SPIKE_HITBOX_WIDTH,
                SPIKE_HITBOX_HEIGHT,
            )
            bird_hitbox = pygame.Rect(state.x, state.y, BIRD_SIZE, BIRD_SIZE)
            hit = pygame.Rect.colliderect(spike_hitbox, bird_hitbox)
            if hit:
                return True
    return False


def check_spikes_right(state):
    y_real = state.y - 70

    index = int(y_real / (GAP + spike_height))

    vetor = [(index - 1) % 12, index, (index + 1) % 12]
    for i in vetor:
        if state.spikes_matrix[i]:
            spike_hitbox = pygame.Rect(
                RIGHT_SPIKE_HITBOX,
                HEIGHTS_OF_SPIKES_HITBOX[i] - SPIKE_HITBOX_HEIGHT / 2,
                SPIKE_HITBOX_WIDTH,
                SPIKE_HITBOX_HEIGHT,
            )
            bird_hitbox = pygame.Rect(state.x, state.y, BIRD_SIZE, BIRD_SIZE)
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


def game_over(keys, previous_keys, state):
    global ALIVE, score_value, playerY_velocity, SCREEN_COLOR, SPIKE_COLOR
    over_font = pygame.font.Font("freesansbold.ttf", 32)
    over_text = over_font.render("PRESS SPACE TO START", True, (255, 255, 255))
    screen.blit(over_text, (0 + 50, SCREEN_HEIGHT / 2 + 100))
    show_player_right(state.x, state.y)
    SCREEN_COLOR = (200, 200, 200)
    SPIKE_COLOR = (130, 130, 130)
    if (keys[pygame.K_SPACE] and not previous_keys[pygame.K_SPACE]) or IS_AGENT_PLAYING:
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
    global playerY_velocity, ALIVE, GAME_STATE

    if ALIVE:
        playerY_velocity = playerY_velocity - gravity
        jump = 0
        # If the agent is playing
        if IS_AGENT_PLAYING:
            input_predict = [
                [
                    GAME_STATE.x + playerX_velocity,
                    GAME_STATE.y - playerY_velocity,
                    GAME_STATE.x,
                    GAME_STATE.y,
                    playerX_velocity,
                ]
                + [spike for spike in GAME_STATE.spikes_matrix]
            ]
            jump_predict = net.predict(input_predict)
            print(jump_predict[0][0])
            if jump_predict[0][0] >= JUMP_THRESHOLD:
                jump = 1
        if (keys[pygame.K_SPACE] and not previous_keys[pygame.K_SPACE]) or jump:
            playerY_velocity = up_velocity
            jump = 1
        if SAVE_STATE:
            GAME_STATE = save_state(GAME_STATE, jump, playerX_velocity)
        GAME_STATE.x = GAME_STATE.x + playerX_velocity
        GAME_STATE.y = GAME_STATE.y - playerY_velocity
        if goingright:
            GAME_STATE = alive_right(GAME_STATE)
        else:
            GAME_STATE = alive_left(GAME_STATE)

        show_spikes(GAME_STATE)
        show_score(10, 10)

    else:
        game_over(keys, previous_keys, GAME_STATE)
        show_score(10, 10)
