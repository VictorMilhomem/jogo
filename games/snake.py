"""
Jogo da cobrinha
"""
import pygame
import tkinter as tk
from tkinter import messagebox
import random
import math
import sys


class Cubo:
    rows = 20
    w = 500

    def __init__(self, start, dirnx=1, dirny=0, color=(255, 0, 0)):
        self.posicao = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color

    def mover(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.posicao = (self.posicao[0] + self.dirnx, self.posicao[1] + self.dirny)

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        i = self.posicao[0]
        j = self.posicao[1]
        
        pygame.draw.rect(surface, self.color, (i*dis+1, j*dis+1, dis-2, dis-2))
        if eyes:
            centre = dis//2
            radius = 3
            circle_middle = (i*dis+centre-radius, j*dis+8)
            circle_middle2 = (i*dis + dis -radius*2, j*dis+8)
            pygame.draw.circle(surface, (0, 0, 0), circle_middle, radius)
            pygame.draw.circle(surface, (0, 0, 0), circle_middle2, radius)


class Snake:
    body = []
    turns = {}

    def __init__(self, color, posicao):
        self.color = color
        self.head = Cubo(posicao)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1

    def move(self):
        """ Todos os movimentos possiveis de se fazer"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()
            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns[self.head.posicao[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_RIGHT]:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.posicao[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_UP]:
                    self.dirnx = 0
                    self.dirny = -1
                    self.turns[self.head.posicao[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_DOWN]:
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.posicao[:]] = [self.dirnx, self.dirny]
        for i, c in enumerate(self.body):
            p = c.posicao[:]
            if p in self.turns:
                turn = self.turns[p]
                c.mover(turn[0], turn[1])
                if i == len(self.body) -1:
                    self.turns.pop(p)
            else:
                if c.dirnx == -1 and c.posicao[0] <= 0:
                    c.posicao = (c.rows-1, c.posicao[1])
                elif c.dirnx == 1 and c.posicao[0] >= c.rows-1:
                    c.posicao = (0, c.posicao[1])
                elif c.dirny == 1 and c.posicao[1] >= c.rows-1:
                    c.posicao = (c.posicao[0], 0)
                elif c.dirny == -1 and c.posicao[1] <= 0:
                    c.posicao = (c.posicao[0], 0)
                else:
                    c.mover(c.dirnx, c.dirny)

    def reset(self, posicao):
        self.head = Cubo(posicao)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    def adi_cubo(self):
        """ Adiociona o corpo da cobra"""
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny
        if dx == 1 and dy == 0:
            self.body.append(Cubo((tail.posicao[0]-1, tail.posicao[1])))
        elif dx == -1 and dy == 0:
            self.body.append(Cubo((tail.posicao[0] + 1, tail.posicao[1])))
        elif dx == 0 and dy == 1:
            self.body.append(Cubo((tail.posicao[0], tail.posicao[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(Cubo((tail.posicao[0], tail.posicao[1] + 1)))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)


def grid(w, rows, surface):
    """ Cria o grid do jogo"""
    size_btwn = w // rows

    x = 0
    y = 0
    for l in range(rows):
        x += size_btwn
        y += size_btwn


def redraw_window(surface):
    global rows, largura, s, snack
    surface.fill((0, 0, 0))
    s.draw(surface)
    snack.draw(surface)
    grid(largura, rows, surface)
    pygame.display.update()


def random_snack(rows, item):
    """ Adiciona randomicamente um snack para a cobra
    :return: int
    """
    positions = item.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z: z.posicao == (x, y), positions))) > 0:
            continue
        else:
            break
    return x, y


def msg_box(subject, content):
    """ Cria um box dizendo que o jogador perdeu"""
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass


def main():
    global largura, rows, s, snack
    largura = 500
    rows = 20
    surface = pygame.display.set_mode((largura, largura))
    pygame.display.set_caption("Sanke")
    s = Snake((255, 0, 0), (10, 10))
    snack = Cubo(random_snack(rows, s), color=(0, 255, 0))
    flag = True

    clock = pygame.time.Clock()

    while flag:
        pygame.time.delay(50)
        clock.tick(10)
        s.move()
        if s.body[0].posicao == snack.posicao:
            s.adi_cubo()
            snack = Cubo(random_snack(rows, s), color=(0, 255, 0))

        for x in range(len(s.body)):
            if s.body[x].posicao in list(map(lambda z: z.posicao, s.body[x+1:])):
                print(f'Score, {len(s.body)}')
                msg_box('Você perdeu!!', 'Tente Novamente!')
                s.reset((10, 10))
                sys.exit()
        redraw_window(surface)


main()
