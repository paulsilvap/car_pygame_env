import pygame
import pygame.freetype
from sys import exit
import random

WINDOW_HEIGHT = int(400 * 1)
WINDOW_WIDTH = int(WINDOW_HEIGHT * 2)
GRID_HEIGHT = WINDOW_HEIGHT
GRID_WIDTH = int(WINDOW_WIDTH / 2)
BLOCK_SIZE = int(50 * 1)
COLORS = [(255,255,204),(255,204,153),(255,102,102)]
GRID_DIMENSION = int((GRID_HEIGHT - BLOCK_SIZE*2) / BLOCK_SIZE)
BATTERY_LEVEL = 24
ELECTRICTY_PRICE = 0.45

grids = []
steps = 0
charging = False
charging_cost = 0

def drawString(font, str, surf, pos, color):
    text_rect = font.get_rect(str)
    text_rect.midleft = pos
    font.render_to(surf, text_rect, str, color)
    return text_rect.bottom

def drawGrid(screen, blockSize):
    for x in range(blockSize, GRID_WIDTH-blockSize, blockSize):
        for y in range(blockSize, GRID_HEIGHT-blockSize, blockSize):
            rect = pygame.Rect(x, y, blockSize, blockSize)
            index = random.randint(0,2)
            grids.append([rect, index])
            pygame.draw.rect(screen, COLORS[index], rect)

def updateLoad():
    for i in range(len(grids)):
        grids[i][1] = random.randint(0,2)

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
canvas = pygame.Surface((WINDOW_WIDTH,WINDOW_HEIGHT))
subrect1 = pygame.Rect(0,0,GRID_WIDTH,GRID_HEIGHT)
subrect2 = pygame.Rect(GRID_WIDTH,0,GRID_WIDTH,GRID_HEIGHT)
subsurface1 = canvas.subsurface(subrect1)
subsurface2 = canvas.subsurface(subrect2)
game_active = True

test_font = pygame.freetype.SysFont(None, BLOCK_SIZE*0.50)

# Car icon taken from: https://uxwing.com/car-icon/
car_surface = pygame.image.load('car.png').convert_alpha()
car_surface = pygame.transform.scale(car_surface,(int(BLOCK_SIZE*0.75), int(BLOCK_SIZE*0.75)))
# Charging icon taken from: https://uxwing.com/energy-green-icon/ 
charger_surface = pygame.image.load('energy-green.png').convert_alpha()
charger_surface = pygame.transform.scale(charger_surface,(int(BLOCK_SIZE*0.75), int(BLOCK_SIZE*0.75)))
# Green charging icon taken from: https://uxwing.com/green-energy-icon/
charging_surface = pygame.image.load('green-energy.png').convert_alpha()
charging_surface = pygame.transform.scale(charging_surface,(int(BLOCK_SIZE*0.75), int(BLOCK_SIZE*0.75)))

subsurface2.fill('Gray')
drawGrid(subsurface2, BLOCK_SIZE)
car_rect = car_surface.get_rect(center = grids[GRID_DIMENSION-1][0].center)
charger_rect = charger_surface.get_rect(center = grids[GRID_DIMENSION*(GRID_DIMENSION-1)][0].center)
charging_rect = charging_surface.get_rect(center = grids[GRID_DIMENSION*(GRID_DIMENSION-1)][0].center)
bat = BATTERY_LEVEL

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == pygame.KEYDOWN:
                steps += 1
                if steps % 5 == 0:
                    updateLoad()
                for (rect, index) in grids:
                    pygame.draw.rect(subsurface2, COLORS[index], rect)
                if event.key == pygame.K_UP and car_rect.top > BLOCK_SIZE * 2:
                    car_rect.top -= BLOCK_SIZE
                    bat -= 1
                elif event.key == pygame.K_DOWN and car_rect.bottom < GRID_HEIGHT - BLOCK_SIZE * 2:
                    car_rect.bottom += BLOCK_SIZE
                    bat -= 1
                elif event.key == pygame.K_LEFT and car_rect.left > BLOCK_SIZE * 2:
                    car_rect.left -= BLOCK_SIZE
                    bat -= 1
                elif event.key == pygame.K_RIGHT and car_rect.right < (GRID_WIDTH) - BLOCK_SIZE * 2:
                    car_rect.right += BLOCK_SIZE
                    bat -= 1
                if event.key == pygame.K_c and car_rect.center == charger_rect.center:
                    charging = True
                    charging_cost += ELECTRICTY_PRICE 
                    bat = min(BATTERY_LEVEL, int(bat + BATTERY_LEVEL*0.25))
                else:
                    charging = False
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    updateLoad()
                    for (rect, index) in grids:
                        pygame.draw.rect(subsurface2, COLORS[index], rect)
                    game_active = True
                    bat = BATTERY_LEVEL
                    steps = 0
                    car_rect.center = grids[GRID_DIMENSION-1][0].center

    if game_active:
        for (rect, _) in grids:
            pygame.draw.rect(subsurface2, 'Black', rect, 1)
        
        subsurface1.fill('Gray')
        drawString(test_font,f'Battery: {bat}', subsurface1, (BLOCK_SIZE,BLOCK_SIZE), (63,63,63))
        drawString(test_font,f'Steps: {steps}', subsurface1, (BLOCK_SIZE,BLOCK_SIZE*3/2), (63,63,63))
        drawString(test_font,f'Electricity Price: $ {ELECTRICTY_PRICE} kw/h', subsurface1, (BLOCK_SIZE,BLOCK_SIZE*2), (63,63,63))
        drawString(test_font,f'Charging Cost: $ {charging_cost:.2f}', subsurface1, (BLOCK_SIZE,BLOCK_SIZE*5/2), (63,63,63))

        screen.blit(subsurface1, (0,0))
        screen.blit(subsurface2, (GRID_WIDTH,0))

        if car_rect.center != charger_rect.center:
            subsurface2.blit(charger_surface, charger_rect)
        if car_rect.center == charger_rect.center and charging:
            subsurface2.blit(charging_surface, charging_rect)
        else:
            subsurface2.blit(car_surface,car_rect)
        if (bat == 0 and car_rect.center != charger_rect.center) or steps == 240:
            game_active = False
    else:
        screen.blit(subsurface2, (GRID_WIDTH,0))
        # pass
        
    pygame.display.update()


