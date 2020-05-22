import numpy as np
import pygame
import sys
import math

amarelo = (255, 255, 0)
vermelho = (255, 0, 0)
preto = (0, 0, 0)
azul = (0, 0, 255)
linhas = 6
colunas = 7


def create_board():
    board = np.zeros((linhas, colunas))
    return board


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def is_valid_location(board, col):
    return board[linhas - 1][col] == 0


def get_next_open_row(board, col):
    for r in range(linhas):
        if board[r][col] == 0:
            return r


def print_board(board):
    print(np.flip(board, 0))


def winning_move(board, piece):
    # Checar posições horizontais
    for c in range(colunas-3):
        for r in range(linhas):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # Checar posições verticais
    for c in range(colunas):
        for r in range(linhas-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True
    # Checar diagonais positivas
    for c in range(colunas-3):
        for r in range(linhas-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # Checar diagonais negativas
    for c in range(colunas-3):
        for r in range(3, linhas):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True


def draw_board(board):
    for c in range(colunas):
        for r in range(linhas):
            pygame.draw.rect(screen, azul, (c*squaresize, r*squaresize + squaresize, squaresize, squaresize))
            pygame.draw.circle(screen, preto, (int(c * squaresize + squaresize / 2), int(r * squaresize + squaresize + squaresize / 2)), radius)

    for c in range(colunas):
        for r in range(linhas):
            if board[r][c] == 1:
                pygame.draw.circle(screen, vermelho, (int(c * squaresize + squaresize / 2), height - int(r * squaresize + squaresize / 2)), radius)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, amarelo, (int(c * squaresize + squaresize / 2), height - int(r * squaresize + squaresize / 2)), radius)
    pygame.display.update()


board = create_board()
print_board(board)
game_over = False
turn = 0

pygame.init()

squaresize = 100

width = colunas * squaresize
height = (linhas + 1) * squaresize

size = (width, height)

radius = int(squaresize/2 - 5)

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Connect4")
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont('monospace', 75)

while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, preto, (0, 0, width, squaresize))
            posx = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, vermelho, (posx, int(squaresize/2)), radius)
            else:
                pygame.draw.circle(screen, amarelo, (posx, int(squaresize / 2)), radius)
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, preto, (0, 0, width, squaresize))

            if turn == 0:
                posx = event.pos[0]
                col = int(math.floor(posx/squaresize))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 1)

                    if winning_move(board, 1):
                        label = myfont.render('Jogador 1 win!', 1, vermelho)
                        screen.blit(label, (40, 10))
                        game_over = True

            else:
                posx = event.pos[0]
                col = int(math.floor(posx/squaresize))
                   
                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 2)

                    if winning_move(board, 2):
                        label = myfont.render('Jogador 2 win!', 1, amarelo)
                        screen.blit(label, (40, 10))
                        game_over = True

            print_board(board)
            draw_board(board)
            # Alternando entre um jogador e outro
            turn += 1
            turn = turn % 2
            if game_over:
                pygame.time.wait(3000)