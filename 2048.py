from ast import While
import random
import json
import sys
import time
from copy import deepcopy
import pygame
from pygame.locals import *
pygame.init()
c = json.load(open("constants.json", "r"))

my_font = pygame.font.SysFont(c["font"], c["font_size"], bold=True)
WHITE = (255, 255, 255)
WIDTH, HEIGHT = 900, 500
CAPTION = '2048'
screen = pygame.display.set_mode((WIDTH, HEIGHT))
TOP, LEFT = 125, 50
BLOCK_WIDTH, BLOCK_HEIGHT = 75, 75
GAP = 7

MAIN_MENU_FONT = pygame.font.SysFont('Tahoma', 45)
TITLE_FONT = pygame.font.SysFont('Tahoma', 75)
BLOCK_FONT = pygame.font.SysFont('Tahoma', 25)
STATS_FONT = pygame.font.SysFont('Tahoma', 30)
GAME_OVER_FONT = pygame.font.SysFont('Tahoma', 45)

# Credit for Colors 
BLACK = '#000000'
WHITE = '#ffffff'
BLUE =  '#0000ff'
RED =   '#ff0000'

BG_COLOR = '#bbada0'


def winCheck(board, status, theme, text_col):
    """
    Check game status and display win/lose result.
    """
    if status != "PLAY":
        size = c["size"]
        # Fill the window with a transparent background
        s = pygame.Surface((size, size), pygame.SRCALPHA)
        s.fill(c["colour"][theme]["over"])
        screen.blit(s, (0, 0))

        # Display win/lose status
        if status == "WIN":
            msg = "YOU WIN!"
        else:
            msg = "GAME OVER!"
        l = "FAIL"
        screen.blit(my_font.render(l, 1, text_col), (220, 140))
        screen.blit(my_font.render(msg, 1, text_col), (140, 180))
        # Ask user to play again
        screen.blit(my_font.render("Play again? (y/ n)", 1, text_col), (80, 255))

        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == QUIT or \
                        (event.type == pygame.KEYDOWN and event.key == K_n):
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN and event.key == K_y:
                    # 'y' is pressed to start a new game
                    board = newGame(theme, text_col)
                    return (board, "PLAY")
    return (board, status)

def checkGameStatus(board, max_tile=2048):
    """
    Update the game status by checking if the max. tile has been obtained.
    """
    flat_board = [cell for row in board for cell in row]
    if max_tile in flat_board:
        # game has been won if max_tile value is found
        return "WIN"

    for i in range(4):
        for j in range(4):
            # check if a merge is possible
            if j != 3 and board[i][j] == board[i][j+1] or \
                    i != 3 and board[i][j] == board[i + 1][j]:
                return "PLAY"

    if 0 not in flat_board:
        return "LOSE"
    else:
        return "PLAY"
def newGame(theme, text_col):
    """
    Start a new game by resetting the board.
    """
    # clear the board to start a new game
    board = [[0] * 4 for _ in range(4)]
    display(board, theme)

    screen.blit(my_font.render("NEW GAME!", 1, text_col), (130, 225))
    pygame.display.update()
    # wait for 1 second before starting over
    time.sleep(1)

    board = fillTwoOrFour(board, iter=2)
    display(board, theme)
    return board

def playGame(theme, difficulty):
    """
    Main game loop function.
    """
    # initialise game status
    status = "PLAY"
    # set text colour according to theme
    if theme == "light":
        text_col = tuple(c["colour"][theme]["dark"])
    else:
        text_col = WHITE
    board = newGame(theme, text_col)
    
    # main game loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or \
                    (event.type == pygame.KEYDOWN and event.key == K_q):
                # exit if q is pressed
                pygame.quit()
                sys.exit()

            # a key has been pressed
            if event.type == pygame.KEYDOWN:
                # 'n' is pressed to restart the game
                if event.key == pygame.K_n:
                    board = restart(board, theme, text_col)

                # convert the pressed key to w/a/s/d
                #key = c["keys"][str(event.key)]
                if event.key in [K_a, K_LEFT]:
                    key = 'a'
                if event.key in [K_d, K_RIGHT]:
                    key = 'd'
                if event.key in [K_w, K_UP]:
                    key = 'w'
                if event.key in [K_s, K_DOWN]:
                    key = 's'

                # obtain new board by performing move on old board's copy
                new_board = move(key, deepcopy(board))

                # proceed if change occurs in the board after making move
                if new_board != board:
                    # fill 2/4 after every move
                    board = fillTwoOrFour(new_board)
                    display(board, theme)
                    # update game status
                    status = checkGameStatus(board, difficulty)
                    # check if the game is over
                    (board, status) = winCheck(board, status, theme, text_col)

def restart(board, theme, text_col):
    """
    Ask user to restart the game if 'n' key is pressed.
    """
    # Fill the window with a transparent background
    s = pygame.Surface((c["size"], c["size"]), pygame.SRCALPHA)
    s.fill(c["colour"][theme]["over"])
    screen.blit(s, (0, 0))

    screen.blit(my_font.render("RESTART? (y / n)", 1, text_col), (85, 225))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or \
                    (event.type == pygame.KEYDOWN and event.key == K_n):
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == K_y:
                board = newGame(theme, text_col)
                return board


def display(board, theme):
    """
    Display the board 'matrix' on the game window.
    """
    screen.fill(tuple(c["colour"][theme]["background"]))
    box = c["size"] // 4
    padding = c["padding"]
    for i in range(4):
        for j in range(4):
            colour = tuple(c["colour"][theme][str(board[i][j])])
            pygame.draw.rect(screen, colour, (j * box + padding,
                                              i * box + padding,
                                              box - 2 * padding,
                                              box - 2 * padding), 0)
            if board[i][j] != 0:
                if board[i][j] in (2, 4):
                    text_colour = tuple(c["colour"][theme]["dark"])
                else:
                    text_colour = tuple(c["colour"][theme]["light"])
                # display the number at the centre of the tile
                screen.blit(my_font.render("{:>4}".format(
                    board[i][j]), 1, text_colour),
                    # 2.5 and 7 were obtained by trial and error
                    (j * box + 2.5 * padding, i * box + 7 * padding))
    sum = score(board)
    best = bestscore(sum)
    l = STATS_FONT.render(f'Best Score: {best}', 1, WHITE)
    screen.blit(l, (530, 20))
    label = STATS_FONT.render(f'Current Score: {sum}', 1, WHITE)
    screen.blit(label, (530, 20+l.get_rect().height))
    start_y = 30 + label.get_rect().height 
    drawGameIntro(screen, 530, start_y)
    pygame.display.update()
    
def drawGameIntro(screen, start_x, start_y):
    start_y += 40
    font_color = (255, 255, 255)
    font_big = pygame.font.SysFont('Tahoma', 25)
    font_small = pygame.font.SysFont('Tahoma', 15)
    intros = ['TIPS:', 'Use arrow keys/wasd to move the number blocks.', 'Adjacent blocks with the same number will', 'be merged. Just try to merge the blocks as', 'many as you can!']
    for idx, intro in enumerate(intros):
        font = font_big if idx == 0 else font_small
        text = font.render(intro, True, font_color)
        screen.blit(text, (start_x, start_y))
        start_y += text.get_rect().height + 10
def bestscore(currentscore):
    cbestscore = readMaxScore()
    if cbestscore == 0:
        saveMaxScore(currentscore)
        return currentscore
    else:
        if cbestscore <= currentscore:
            saveMaxScore(currentscore)
            return currentscore
        else:
            saveMaxScore(cbestscore)
            return cbestscore

def score(board):
    sum = 0
    for x in range(4):
        for y in range(4):
            sum += board[x][y]
    return sum

def saveMaxScore(best):
    f = open("bestscore.csv", 'w', encoding='utf-8')
    f.write(str(best))
    f.close()

def readMaxScore():
    try:
        f = open("bestscore.csv", 'r', encoding='utf-8')
        score = int(f.read().strip())
        f.close()
        return score
    except:
        return 0

def fillTwoOrFour(board, iter=1):
    """
    Randomly fill 2 or 4 in available spaces on the board.

    """
    for _ in range(iter):
        a = random.randint(0, 3)
        b = random.randint(0, 3)
        while(board[a][b] != 0):
            a = random.randint(0, 3)
            b = random.randint(0, 3)

        if sum([cell for row in board for cell in row]) in (0, 2):
            board[a][b] = 2
        else:
            board[a][b] = random.choice((2, 4))
    return board


def move(direction, board):
    if direction == "w":
        return moveUp(board)
    if direction == "s":
        return moveDown(board)
    if direction == "a":
        return moveLeft(board)
    if direction == "d":
        return moveRight(board)

def moveLeft(board):

    # initial shift
    shiftLeft(board)

    # merge cells
    for i in range(4):
        for j in range(3):
            if board[i][j] == board[i][j + 1] and board[i][j] != 0:
                board[i][j] *= 2
                board[i][j + 1] = 0
                j = 0

    # final shift
    shiftLeft(board)
    return board


def moveUp(board):
    board = rotateLeft(board)
    board = moveLeft(board)
    board = rotateRight(board)
    return board


def moveRight(board):
    # initial shift
    shiftRight(board)

    # merge cells
    for i in range(4):
        for j in range(3, 0, -1):
            if board[i][j] == board[i][j - 1] and board[i][j] != 0:
                board[i][j] *= 2
                board[i][j - 1] = 0
                j = 0

    # final shift
    shiftRight(board)
    return board


def moveDown(board):
    board = rotateLeft(board)
    board = moveLeft(board)
    shiftRight(board)
    board = rotateRight(board)
    return board


def shiftLeft(board):
    # remove 0's in between numbers
    for i in range(4):
        nums, count = [], 0
        for j in range(4):
            if board[i][j] != 0:
                nums.append(board[i][j])
                count += 1
        board[i] = nums
        board[i].extend([0] * (4 - count))


def shiftRight(board):
    # remove 0's in between numbers
    for i in range(4):
        nums, count = [], 0
        for j in range(4):
            if board[i][j] != 0:
                nums.append(board[i][j])
                count += 1
        board[i] = [0] * (4 - count)
        board[i].extend(nums)

def rotateLeft(board):
    """
    90 degree counter-clockwise rotation.
    """
    b = [[board[j][i] for j in range(4)] for i in range(3, -1, -1)]
    
    return b


def rotateRight(board):
    """
    270 degree counter-clockwise rotation.
    """
    b = rotateLeft(board)
    b = rotateLeft(b)
    return rotateLeft(b)



a ="light"
playGame(a,2048)