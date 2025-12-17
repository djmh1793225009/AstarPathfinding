#A*算法寻路演示脚本
#请在与脚本相同目录下创建config.txt文件，第一行为演示速度（单位为毫秒），其余行为地图数据（行数和列数必须相等），o：可通行，x：障碍物，a：起点，b：终点
#作者：mECORI chatgpt-4o
#Github：https://github.com/djmh1793225009
#Telegram：https://t.me/yume_yuki
import pygame
import time
from queue import PriorityQueue
import os

scriptDir = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(scriptDir, "config.txt"), 'r') as f:
    executionSpeed = int(f.readline().strip())
    mapData = [line.strip() for line in f]

WIDTH = 800
HEIGHT = 800
ROWS = len(mapData)
COLS = len(mapData[0])
CELL_SIZE = min(WIDTH // COLS, HEIGHT // ROWS)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREY = (128, 128, 128)

pygame.init()
WIN = pygame.display.set_mode((COLS * CELL_SIZE, ROWS * CELL_SIZE))
pygame.display.set_caption("A*算法寻路演示")

class Node:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.x = col * CELL_SIZE
        self.y = row * CELL_SIZE
        self.color = WHITE
        self.neighbors = []
        self.gCost = float('inf')
        self.hCost = float('inf')
        self.fCost = float('inf')

def h(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def drawGrid():
    for i in range(ROWS + 1):
        pygame.draw.line(WIN, GREY, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE))
    for j in range(COLS + 1):
        pygame.draw.line(WIN, GREY, (j * CELL_SIZE, 0), (j * CELL_SIZE, HEIGHT))

def draw(grid):
    WIN.fill(WHITE)
    for row in grid:
        for node in row:
            pygame.draw.rect(WIN, node.color, (node.x, node.y, CELL_SIZE, CELL_SIZE))
    drawGrid()
    pygame.display.update()

def aStar(grid, start, end):
    count = 0
    openSet = PriorityQueue()
    openSet.put((0, count, start))
    cameFrom = {}
    grid[start[0]][start[1]].gCost = 0
    grid[start[0]][start[1]].fCost = h(start, end)

    openSetHash = {start}

    while not openSet.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = openSet.get()[2]
        openSetHash.remove(current)

        if current == end:
            while current in cameFrom:
                current = cameFrom[current]
                grid[current[0]][current[1]].color = YELLOW
                draw(grid)
            grid[end[0]][end[1]].color = RED
            return True

        for neighbor in [(current[0]-1, current[1]), (current[0]+1, current[1]), (current[0], current[1]-1), (current[0], current[1]+1)]:
            if 0 <= neighbor[0] < ROWS and 0 <= neighbor[1] < COLS and mapData[neighbor[0]][neighbor[1]] != 'x':
                tempGCost = grid[current[0]][current[1]].gCost + 1

                if tempGCost < grid[neighbor[0]][neighbor[1]].gCost:
                    cameFrom[neighbor] = current
                    grid[neighbor[0]][neighbor[1]].gCost = tempGCost
                    grid[neighbor[0]][neighbor[1]].hCost = h(neighbor, end)
                    grid[neighbor[0]][neighbor[1]].fCost = grid[neighbor[0]][neighbor[1]].gCost + grid[neighbor[0]][neighbor[1]].hCost

                    if neighbor not in openSetHash:
                        count += 1
                        openSet.put((grid[neighbor[0]][neighbor[1]].fCost, count, neighbor))
                        openSetHash.add(neighbor)
                        grid[neighbor[0]][neighbor[1]].color = BLUE

        draw(grid)

        if current != start:
            grid[current[0]][current[1]].color = GREEN

        time.sleep(executionSpeed / 1000.0)

    return False

def main():
    grid = [[Node(i, j) for j in range(COLS)] for i in range(ROWS)]
    start = None
    end = None
    for i in range(ROWS):
        for j in range(COLS):
            if mapData[i][j] == 'a':
                start = (i, j)
                grid[i][j].color = GREEN
            elif mapData[i][j] == 'b':
                end = (i, j)
                grid[i][j].color = RED
            elif mapData[i][j] == 'x':
                grid[i][j].color = BLACK

    pathFound = aStar(grid, start, end)

    if not pathFound:
        for i in range(ROWS):
            for j in range(COLS):
                if grid[i][j].color == GREEN:
                    grid[i][j].color = RED
        draw(grid)

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

    pygame.quit()

if __name__ == "__main__":
    main()