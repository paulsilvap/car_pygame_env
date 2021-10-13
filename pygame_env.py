import pygame
from sys import exit
import random

WINDOW_HEIGHT = int(400 * 2)
WINDOW_WIDTH = int(WINDOW_HEIGHT * 2)
GRID_HEIGHT = WINDOW_HEIGHT
GRID_WIDTH = int(WINDOW_WIDTH / 2)
BLOCK_SIZE = int(50 * 1)
COLORS = [(255,255,204),(255,204,153),(255,102,102)]
GRID_DIMENSION = int((GRID_HEIGHT - BLOCK_SIZE*2) / BLOCK_SIZE)

grids = []
steps = 0

def drawGrid(screen, blockSize):
    for x in range(blockSize, GRID_WIDTH-blockSize, blockSize):
        for y in range(blockSize, GRID_HEIGHT-blockSize, blockSize):
            rect = pygame.Rect(x, y, blockSize, blockSize)
            index = random.randint(0,2)
            grids.append([rect, index])
            pygame.draw.rect(screen, COLORS[index], rect)

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
canvas = pygame.Surface((WINDOW_WIDTH,WINDOW_HEIGHT))
subrect1 = pygame.Rect(0,0,GRID_WIDTH,GRID_HEIGHT)
subrect2 = pygame.Rect(GRID_WIDTH,0,GRID_WIDTH,GRID_HEIGHT)
subsurface1 = canvas.subsurface(subrect1)
subsurface2 = canvas.subsurface(subrect2)

# Car icon taken from: https://uxwing.com/car-icon/
car_surface = pygame.image.load('car.png').convert_alpha()
car_surface = pygame.transform.scale(car_surface,(int(BLOCK_SIZE*0.75), int(BLOCK_SIZE*0.75)))
car_rect = car_surface.get_rect(center = (GRID_WIDTH + BLOCK_SIZE + (BLOCK_SIZE/2), GRID_HEIGHT - (BLOCK_SIZE + (BLOCK_SIZE/2))))

subsurface1.fill('Gray')
subsurface2.fill('Gray')
drawGrid(subsurface2, BLOCK_SIZE)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            steps += 1
            if steps % 5 == 0:
                for i in range(len(grids)):
                    grids[i][1] = random.randint(0,2)
            for (rect, index) in grids:
                pygame.draw.rect(subsurface2, COLORS[index], rect)
            if event.key == pygame.K_UP and car_rect.top > BLOCK_SIZE * 2:
                car_rect.top -= BLOCK_SIZE
            elif event.key == pygame.K_DOWN and car_rect.bottom < GRID_WIDTH - BLOCK_SIZE * 2:
                car_rect.bottom += BLOCK_SIZE
            elif event.key == pygame.K_LEFT and car_rect.left > GRID_WIDTH + BLOCK_SIZE * 2:
                car_rect.left -= BLOCK_SIZE
            elif event.key == pygame.K_RIGHT and car_rect.right < (GRID_WIDTH * 2) - BLOCK_SIZE * 2:
                car_rect.right += BLOCK_SIZE

    for (rect, _) in grids:
        pygame.draw.rect(screen, 'Black', rect, 1)

    screen.blit(subsurface1, (0,0))
    screen.blit(subsurface2, (GRID_WIDTH,0))

    screen.blit(car_surface,car_rect)

    pygame.display.update()


