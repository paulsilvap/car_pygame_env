import pygame
import pygame.freetype
from sys import exit
import random
from pygame.sprite import Group
from scipy.stats import truncnorm
import numpy as np

WINDOW_HEIGHT = int(400 * 1)
WINDOW_WIDTH = int(WINDOW_HEIGHT * 2)
GRID_HEIGHT = WINDOW_HEIGHT
GRID_WIDTH = int(WINDOW_WIDTH / 2)
BLOCK_SIZE = int(50 * 1)
COLORS = [(255,255,204),(255,204,153),(255,102,102)]
GRID_DIMENSION = int((GRID_HEIGHT - BLOCK_SIZE*2) / BLOCK_SIZE)
BATTERY_LEVEL = 24

grids = []
steps = 0
charging = False
charging_cost = 0
mid_penalty = 1
high_penalty = 2

def truncatedNormalDistribution(bound_a, bound_b, mean, std, step):
    a, b = (bound_a - mean) / std, (bound_b - mean) / std
    x_range = np.linspace(bound_a, bound_b, int(((bound_b - bound_a)/step)+1))

    p = truncnorm.pdf(x_range, a, b, loc = mean, scale = std)
    sum_p = sum(p)
    p_norm = [i/sum_p for i in p]
    # p_norm = [round(i/sum_p,6) for i in p]

    return round(np.random.choice(x_range,size = 1, p=p_norm)[0],2)

def drawString(font, str, surf, pos, color):
    text_rect = font.get_rect(str)
    text_rect.bottomleft = pos
    font.render_to(surf, text_rect, str, color)

def drawGrid(screen, block_size):
    for x in range(block_size, GRID_WIDTH-block_size, block_size):
        for y in range(block_size, GRID_HEIGHT-block_size, block_size):
            rect = pygame.Rect(x, y, block_size, block_size)
            index = random.randint(0,2)
            grids.append([rect, index])
            pygame.draw.rect(screen, COLORS[index], rect)

def updateLoad():
    for i in range(len(grids)):
        grids[i][1] = random.randint(0,2)

def getPosition(center, block_size, dim):
    x, y = center
    row = (y-block_size/2)/block_size
    col = (x-block_size/2)/block_size
    return int((col * dim - dim) + row - 1)

def getLoad(pos, dim, dir):
    if pos % dim != 0 and dir == "n": 
        load = grids[pos-1][1]
    elif pos + dim <= (dim ** 2) - 1 and dir == "e":
        load = grids[pos + dim][1]
    elif pos % dim != dim - 1 and dir == "s":
        load = grids[pos+1][1]
    elif pos - dim >= 0 and dir == "w": 
        load = grids[pos - dim][1]
    elif dir == "c":
        load = grids[pos][1]
    else:
        load = "none"
    return load

def loadToText(load):
    return 'low' if load == 0 else 'mid' if load == 1 else 'high' if load == 2 else load

def actions(event, car_rect, bat, steps, charging_cost, charging):
    if event.key == pygame.K_UP and car_rect.top > BLOCK_SIZE * 2:
        car_rect.top -= BLOCK_SIZE
        bat = max(0, bat - BATTERY_LEVEL * 0.015)
        steps += 1
    elif event.key == pygame.K_DOWN and car_rect.bottom < GRID_HEIGHT - BLOCK_SIZE * 2:
        car_rect.bottom += BLOCK_SIZE
        bat = max(0, bat - BATTERY_LEVEL * 0.015)
        steps += 1
    elif event.key == pygame.K_LEFT and car_rect.left > BLOCK_SIZE * 2:
        car_rect.left -= BLOCK_SIZE
        bat = max(0, bat - BATTERY_LEVEL * 0.015)
        steps += 1
    elif event.key == pygame.K_RIGHT and car_rect.right < (GRID_WIDTH) - BLOCK_SIZE * 2:
        car_rect.right += BLOCK_SIZE
        bat = max(0, bat - BATTERY_LEVEL * 0.015)
        steps += 1
    if event.key == pygame.K_c and car_rect.center == charger_rect.center:
        charging = True
        charging_cost += price * 0.1
        bat = min(BATTERY_LEVEL, bat + BATTERY_LEVEL*0.025)
        steps += 1
    else:
        charging = False
    if event.key == pygame.K_p:
        steps += 1
    return car_rect, bat, steps, charging_cost, charging

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
bat = truncatedNormalDistribution(5, 15, 10, 1, 1)
price = truncatedNormalDistribution(0.40, 0.90, 0.50, 0.10, 0.01)
car_pos = getPosition(car_rect.center,BLOCK_SIZE, GRID_DIMENSION)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == pygame.KEYDOWN:
                if steps != 0 and steps % 10 == 0:
                    price = truncatedNormalDistribution(0.40, 0.90, 0.50, 0.10, 0.01)
                if steps != 0 and steps % 5 == 0:
                    updateLoad()
                for (rect, index) in grids:
                    pygame.draw.rect(subsurface2, COLORS[index], rect)
                current_load = getLoad(car_pos, GRID_DIMENSION, "c")
                if current_load == 1:
                    if mid_penalty == 0:
                        car_rect, bat, steps, charging_cost, charging = actions(event, car_rect, bat, steps, charging_cost, charging)
                        mid_penalty = 1
                        high_penalty = 2
                    else:
                        mid_penalty -= 1
                        high_penalty -= 1
                        steps += 1
                elif current_load == 2:
                    if high_penalty == 0:
                        car_rect, bat, steps, charging_cost, charging = actions(event, car_rect, bat, steps, charging_cost, charging)
                        high_penalty = 2
                        mid_penalty = 1
                    else:
                        high_penalty -= 1
                        mid_penalty = max (0, mid_penalty - 1)
                        steps += 1
                else:
                    car_rect, bat, steps, charging_cost, charging = actions(event, car_rect, bat, steps, charging_cost, charging)
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    updateLoad()
                    for (rect, index) in grids:
                        pygame.draw.rect(subsurface2, COLORS[index], rect)
                    game_active = True
                    bat = truncatedNormalDistribution(5, 15, 10, 1, 1)
                    steps = 0
                    car_rect.center = grids[GRID_DIMENSION-1][0].center

    if game_active:
        for (rect, _) in grids:
            pygame.draw.rect(subsurface2, 'Black', rect, 1)
        
        car_pos = getPosition(car_rect.center,BLOCK_SIZE, GRID_DIMENSION)

        subsurface1.fill('Gray')
        drawString(test_font,f'SOC: {(bat/BATTERY_LEVEL):.2f}', subsurface1, (BLOCK_SIZE,BLOCK_SIZE), (63,63,63))
        drawString(test_font,f'Steps: {steps}', subsurface1, (BLOCK_SIZE,BLOCK_SIZE*3/2), (63,63,63))
        drawString(test_font,f'Electricity Price: $ {price:.2f} kw/h', subsurface1, (BLOCK_SIZE,BLOCK_SIZE*2), (63,63,63))
        drawString(test_font,f'Total Cost: $ {charging_cost:.2f}', subsurface1, (BLOCK_SIZE,BLOCK_SIZE*5/2), (63,63,63))
        drawString(test_font,f'Load', subsurface1, (BLOCK_SIZE,BLOCK_SIZE*7/2), (63,63,63))
        drawString(test_font,f'N: {loadToText(getLoad(car_pos, GRID_DIMENSION, "n"))}', subsurface1, (BLOCK_SIZE,BLOCK_SIZE*4), (63,63,63))
        drawString(test_font,f'E: {loadToText(getLoad(car_pos, GRID_DIMENSION, "e"))}', subsurface1, (BLOCK_SIZE,BLOCK_SIZE*9/2), (63,63,63))
        drawString(test_font,f'S: {loadToText(getLoad(car_pos, GRID_DIMENSION, "s"))}', subsurface1, (GRID_WIDTH/2,BLOCK_SIZE*4), (63,63,63))
        drawString(test_font,f'W: {loadToText(getLoad(car_pos, GRID_DIMENSION, "w"))}', subsurface1, (GRID_WIDTH/2,BLOCK_SIZE*9/2), (63,63,63))
        drawString(test_font,f'Penalties', subsurface1, (BLOCK_SIZE, BLOCK_SIZE*11/2), (63,63,63))
        drawString(test_font,f'medium {mid_penalty}', subsurface1, (BLOCK_SIZE, BLOCK_SIZE*6), (63,63,63))
        drawString(test_font,f'high {high_penalty}', subsurface1, (GRID_WIDTH/2, BLOCK_SIZE*6), (63,63,63))

        screen.blit(subsurface1, (0,0))
        screen.blit(subsurface2, (GRID_WIDTH,0))

        if car_rect.center != charger_rect.center:
            subsurface2.blit(charger_surface, charger_rect)
        if car_rect.center == charger_rect.center and charging:
            subsurface2.blit(charging_surface, charging_rect)
        else:
            subsurface2.blit(car_surface,car_rect)
        if (bat <= 0 and car_rect.center != charger_rect.center) or steps == 240:
            game_active = False
    else:
        screen.blit(subsurface2, (GRID_WIDTH,0))
        
    pygame.display.update()
