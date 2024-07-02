import pygame
from random import choice

CELSIZE =32
MAZESIZE = [50, 25]
WALLWIDTH = 2
RES = [CELSIZE * MAZESIZE[0] + WALLWIDTH, CELSIZE * MAZESIZE[1] + WALLWIDTH]
FPS = 60
COLORS = {'walls' : (255, 0, 68), 'notVisited': (255, 255, 255), 'current': (99, 199, 77), 'stack': (99, 199, 77), 'visited': (24, 20, 37)}

class Cell():
    def __init__(self, x, y, backgroundColor=(255, 255, 255)):
        self.x, self.y = x, y
        self.visited = False
        self.width, self.height = CELSIZE, CELSIZE
        self.walls = {'top': True, 'left': True, 'bottom': True, 'right': True}
        self.rect = pygame.Rect(self.x*CELSIZE, self.y*CELSIZE, self.width, self.height)
        self.backgroundColor = backgroundColor
        self.wallColor = COLORS['walls']

    def drawCurrentCell(self, surf):
        pygame.draw.rect(surf, COLORS['current'], self.rect)

    def draw(self, surf):
        x, y = self.x * CELSIZE, self.y * CELSIZE
        if not self.visited:
            pygame.draw.rect(surf, COLORS['notVisited'], self.rect)
        else:
            pygame.draw.rect(surf, COLORS['visited'], self.rect)

        if self.walls['top']:
            pygame.draw.line(surf, self.wallColor, (x, y), (x + CELSIZE, y), WALLWIDTH)
        if self.walls['left']:
            pygame.draw.line(surf, self.wallColor, (x, y), (x, y+ CELSIZE), WALLWIDTH)
        if self.walls['bottom']:
            pygame.draw.line(surf, self.wallColor, (x, y+ CELSIZE), (x + CELSIZE, y+ CELSIZE), WALLWIDTH)
        if self.walls['right']:
            pygame.draw.line(surf, self.wallColor, (x+ CELSIZE, y), (x + CELSIZE, y+ CELSIZE), WALLWIDTH)

    def checkCell(self, x, y, cells):
        cols = ((RES[0] - 2) // CELSIZE)
        rows = (((RES[1] - 2)) // CELSIZE)
        findIndex = lambda x, y: x + y * cols

        if x < 0 or x > cols - 1 or y < 0 or y > rows - 1:
            return False
        return cells[findIndex(x, y)]

    def checkNeighbors(self, cells):
        neighbors = []

        top = self.checkCell(self.rect.x//CELSIZE, self.rect.y //CELSIZE - 1, cells)
        right = self.checkCell(self.rect.x//CELSIZE + 1, self.rect.y //CELSIZE, cells)
        bottom = self.checkCell(self.rect.x//CELSIZE, self.rect.y //CELSIZE + 1, cells)
        left = self.checkCell(self.rect.x//CELSIZE - 1, self.rect.y //CELSIZE, cells)

        if top and not top.visited:
            neighbors.append(top)
        if right and not right.visited:
            neighbors.append(right)
        if bottom and not bottom.visited:
            neighbors.append(bottom)
        if left and not left.visited:
            neighbors.append(left)

        return choice(neighbors) if neighbors else False

def depthFirstRecursive(cells, surf):
    global currentCell, stack
    if currentCell == None:
        return
    
    nextCell = currentCell.checkNeighbors(cells)

    if nextCell:
        nextCell.visited = True
        nextCell.drawCurrentCell(surf)
        stack.append(currentCell)

        dx = currentCell.x - nextCell.x
        dy = currentCell.y - nextCell.y
        
        if dx == 1:
            currentCell.walls['left'] = False
            nextCell.walls['right'] = False
        if dx == -1:
            currentCell.walls['right'] = False
            nextCell.walls['left'] = False
        
        if dy == 1:
            currentCell.walls['top'] = False
            nextCell.walls['bottom'] = False
        if dy == -1:
            currentCell.walls['bottom'] = False
            nextCell.walls['top'] = False

        currentCell = nextCell
        
    elif stack:
        currentCell = stack.pop()
        currentCell.drawCurrentCell(surf)
    else:
        currentCell = None


pygame.init()
win = pygame.display.set_mode((RES[0], RES[1]))
pygame.display.set_caption('Maze Generator')
clock = pygame.time.Clock()


readCells = True

cells = []
stack = []

for y in range(RES[1]//CELSIZE):
    for x in range(RES[0]//CELSIZE):
        cells.append(Cell(x, y))

currentCell = choice(cells)
currentCell.visited = True
currentCell.drawCurrentCell(win)

def main():
    run = True
    
    while run:
        win.fill(COLORS['notVisited'])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for cell in cells:
            cell.draw(win)

        for cell in stack:
            if(cell != currentCell):
                pygame.draw.rect(win, COLORS['stack'], cell.rect)

        if currentCell != None:
            depthFirstRecursive(cells, win)
            
        pygame.display.update()
        #clock.tick(FPS)
    pygame.quit()



if __name__ == '__main__':
    main()
