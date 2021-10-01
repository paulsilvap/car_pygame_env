import pygame
from sys import exit
import random

# def display_score():
#     current_time = int(pygame.time.get_ticks()/1000) - start_time
#     score_surf = text_font.render(f'{current_time}', False, (64,64,64))
#     score_rect = score_surf.get_rect(center = (400, 50))
#     screen.blit(score_surf,score_rect)

# pygame.init()
# screen = pygame.display.set_mode((800,400))
# pygame.display.set_caption('Car')
# clock = pygame.time.Clock()
# text_font = pygame.font.Font('font/Pixeltype.ttf', 50)
# game_active = True
# start_time = 0

# sky_surface = pygame.image.load('graphics/Sky.png').convert()
# ground_surface = pygame.image.load('graphics/ground.png').convert()

# snail_surface = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
# snail_rect = snail_surface.get_rect(midbottom = (600, 300))

# player_surf = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
# player_rect = player_surf.get_rect(midbottom = (80,300))
# player_gravity = 0

# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             exit()

#         if game_active:
#             if event.type == pygame.MOUSEBUTTONDOWN:
#                 if player_rect.collidepoint(event.pos) and player_rect.bottom == 300:
#                         player_gravity = -20

#             if event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_SPACE and player_rect.bottom == 300:
#                         player_gravity = -20
#         else:
#             if event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_RETURN:
#                     game_active = True
#                     snail_rect.right = 800
#                     start_time = int(pygame.time.get_ticks()/1000)

#     if game_active:
#         screen.blit(sky_surface,(0,0))
#         screen.blit(ground_surface,(0,300))
#         # pygame.draw.rect(screen,'#c0e8ec', score_rect)
#         # pygame.draw.rect(screen,'#c0e8ec', score_rect, 10)

#         display_score()

#         snail_rect.left -= 5
#         if snail_rect.right <= 0:
#             snail_rect.left = 800
#         screen.blit(snail_surface, snail_rect)

#         # Player
#         player_gravity += 1
#         player_rect.bottom += player_gravity
#         if player_rect.bottom >= 300:
#             player_rect.bottom = 300
#         screen.blit(player_surf, player_rect)

#         if snail_rect.colliderect(player_rect):
#             game_active = False

#     else:
#         screen.fill('Yellow')
    
#     pygame.display.update()
#     clock.tick(60)

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


