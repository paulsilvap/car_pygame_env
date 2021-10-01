import pygame
from sys import exit
import random

WINDOW_HEIGHT = int(400 * 1)
WINDOW_WIDTH = int(400 * 1)
BLOCK_SIZE = int(50 * 1)
COLORS = [(255,255,204),(255,204,153),(255,102,102)]

grids = []
steps = 0

def drawGrid(screen, blockSize):
    for x in range(blockSize, WINDOW_WIDTH-blockSize, blockSize):
        for y in range(blockSize, WINDOW_HEIGHT-blockSize, blockSize):
            rect = pygame.Rect(x, y, blockSize, blockSize)
            index = random.randint(0,2)
            grids.append([rect, index])
            pygame.draw.rect(screen, COLORS[index], rect)

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Car icon taken from: https://uxwing.com/car-icon/
car_surface = pygame.image.load('car.png').convert_alpha()
car_surface = pygame.transform.scale(car_surface,(int(BLOCK_SIZE*0.75), int(BLOCK_SIZE*0.75)))
car_rect = car_surface.get_rect(center = (BLOCK_SIZE + (BLOCK_SIZE/2), WINDOW_WIDTH - (BLOCK_SIZE + (BLOCK_SIZE/2))))

screen.fill('Gray')
drawGrid(screen, BLOCK_SIZE)

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
                pygame.draw.rect(screen, COLORS[index], rect)
            if event.key == pygame.K_UP and car_rect.top > BLOCK_SIZE * 2:
                car_rect.top -= BLOCK_SIZE
            elif event.key == pygame.K_DOWN and car_rect.bottom < WINDOW_WIDTH - BLOCK_SIZE * 2:
                car_rect.bottom += BLOCK_SIZE
            elif event.key == pygame.K_LEFT and car_rect.left > BLOCK_SIZE * 2:
                car_rect.left -= BLOCK_SIZE
            elif event.key == pygame.K_RIGHT and car_rect.right < WINDOW_WIDTH - BLOCK_SIZE * 2:
                car_rect.right += BLOCK_SIZE

    for (rect, _) in grids:
        pygame.draw.rect(screen, 'Black', rect, 1)

    screen.blit(car_surface,car_rect)

    pygame.display.update()


