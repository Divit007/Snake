import random
import tkinter as tk
from tkinter import messagebox

import pygame

pygame.init()
pygame.mixer.music.load('music.mp3')
pygame.mixer.music.play(-1, 4)


class Cube(object):
    rows = 20
    w = 500

    def __init__(self, start, dirnx=1, dirny=0, color=(255, 0, 0)):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, eyes=False):
        distance = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]
        pygame.draw.rect(surface, self.color, (i * distance + 1, j * distance + 1, distance - 2, distance - 2))
        if eyes:
            center = distance // 2
            radius = 3
            circle_middle_1 = (i * distance + center - radius, j * distance + 8)
            circle_middle_2 = (i * distance + distance - radius * 2, j * distance + 8)
            pygame.draw.circle(surface, (0, 0, 0), circle_middle_1, radius)
            pygame.draw.circle(surface, (0, 0, 0), circle_middle_2, radius)


class Snake(object):
    body = []
    turns = {}

    def __init__(self, color, pos):
        self.color = color
        self.head = Cube(pos)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            keys = pygame.key.get_pressed()
            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                elif keys[pygame.K_RIGHT]:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                elif keys[pygame.K_UP]:
                    self.dirnx = 0
                    self.dirny = -1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                elif keys[pygame.K_DOWN]:
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            else:
                if c.dirnx == -1 and c.pos[0] <= 0:
                    c.pos = (c.rows - 1, c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= c.rows - 1:
                    c.pos = (0, c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= c.rows - 1:
                    c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0], c.rows - 1)
                else:
                    c.move(c.dirnx, c.dirny)

    def reset(self, pos):
        self.head = Cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny
        if dx == 1 and dy == 0:
            self.body.append(Cube((tail.pos[0] - 1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(Cube((tail.pos[0] + 1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] + 1)))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)


def drawGrid(w, rows, surface):
    between = w // rows
    x = 0
    y = 0
    for random_var in range(rows):
        x += between
        y += between
        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, w))
        pygame.draw.line(surface, (255, 255, 255), (0, y), (w, y))


def redrawWindow(surface):
    surface.fill((0, 0, 0))
    snaker.draw(surface)
    apple.draw(surface)
    drawGrid(square, board, surface)
    pygame.display.update()


def updateFile():
    f = open("scores.txt", "r")
    file = f.readlines()
    last = int(file[0])

    if last < len(snaker.body):
        f.close()
        file = open("scores.txt", "w")
        file.write(str(len(snaker.body)))
        file.close()
        return len(snaker.body)
    return str(last)


def randomSnack(rows, item):
    positions = item.body

    while True:
        x = random.randrange(board)
        y = random.randrange(board)
        if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:
            continue
        else:
            break
    return (x, y)


def message_box():
    high_score = updateFile()
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()

    messagebox.showinfo("Results!", f"Your score was {len(snaker.body)} and your high score was {high_score}")
    try:
        root.destroy()
    except:
        pass


def main():
    global square, board, snaker, apple
    square = 500
    board = 20
    screen = pygame.display.set_mode((square, square))
    snaker = Snake((255, 0, 0), (10, 10))
    apple = Cube(randomSnack(board, snaker), color=(255, 255, 0))
    pygame.display.set_caption('Snaker')
    clock = pygame.time.Clock()
    run = True
    while run:
        pygame.time.delay(50)
        clock.tick(10)
        snaker.move()
        if snaker.body[0].pos == apple.pos:
            snaker.addCube()
            apple = Cube(randomSnack(board, snaker), color=(255, 255, 0))
        for x in range(len(snaker.body)):
            if snaker.body[x].pos in list(map(lambda z: z.pos, snaker.body[x + 1:])):
                message_box()
                snaker.reset((10, 10))
                break
        redrawWindow(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False


main()
