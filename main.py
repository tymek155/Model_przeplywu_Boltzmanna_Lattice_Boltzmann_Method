import pygame
import numpy as np

class Cell:
    def __init__(self, is_al):
        self.is_avalible = is_al
        self.ro = 0
        self.ux = 0
        self.uy = 0
        self.f_eq = [0.0]*9
        self.f_in = [0.0]*9
        self.f_out = [0.0]*9

    def set_ro(self, r):
        self.ro = r

#Parametry modelu
CELL_SIZE = 4
GRID_WIDTH = 50
GRID_HEIGHT = 50
WINDOW_WIDTH = GRID_WIDTH * CELL_SIZE
WINDOW_HEIGHT = GRID_HEIGHT * CELL_SIZE

# Siatka komórek
grid = [[Cell(True) for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
w = [4/9, 1/9, 1/9, 1/9, 1/9, 1/36, 1/36, 1/36, 1/36]
cx = [0, 1, -1, 0, 0, 1, -1, -1, 1]
cy = [0, 0, 0, 1, -1, 1, 1, -1, -1]

def eq_function():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y][x].is_avalible:
                for i in range(9):
                    grid[y][x].f_eq[i] = w[i]*grid[y][x].ro *(1+3*(cx[i]*grid[y][x].ux + cy[i]*grid[y][x].uy)+4.5*(cx[i]*grid[y][x].ux + cy[i]*grid[y][x].uy)*(cx[i]*grid[y][x].ux + cy[i]*grid[y][x].uy)-1.5*((grid[y][x].ux)*(grid[y][x].ux)+(grid[y][x].uy)*(grid[y][x].uy)))

def out_function():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y][x].is_avalible:
                for i in range(9):
                    grid[y][x].f_out[i] = grid[y][x].f_eq[i]

"""
def collision():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y][x].is_avalible:
                #Inicjalizacja sąsiadów
                neighbours = [-1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0]

                #Dolny sąsiad
                if y > 0 and grid[y-1][x].is_avalible:
                    neighbours[3] = grid[y-1][x].f_out[3]

                #Górny sąsiad
                if y < GRID_HEIGHT-1 and grid[y+1][x].is_avalible:
                    neighbours[4] = grid[y+1][x].f_out[4]

                #Lewy sąsiad
                if x > 0 and grid[y][x-1].is_avalible:
                    neighbours[2] = grid[y][x-1].f_out[1]

                #Prawy sąsiad
                if x < GRID_WIDTH-1 and grid[y][x+1].is_avalible:
                    neighbours[1] = grid[y][x+1].f_out[2]

                #Prawy górny sąsiąd
                if x < GRID_WIDTH-1 and y < GRID_HEIGHT-1 and grid[y+1][x+1].is_avalible:
                    neighbours[5] = grid[y+1][x+1].f_out[7]

                #Lewy dolny sąsiąd
                if x > 0 and y > 0 and grid[y-1][x-1].is_avalible:
                    neighbours[7] = grid[y-1][x-1].f_out[5]

                #Lewy górny sąsiąd
                if x > 0 and y < GRID_HEIGHT-1 and grid[y+1][x-1].is_avalible:
                    neighbours[6] = grid[y+1][x-1].f_out[8]

                #Prawy dolny sąsiąd
                if x < GRID_WIDTH - 1 and y > 0 and grid[y-1][x+1].is_avalible:
                    neighbours[8] = grid[y-1][x+1].f_out[6]

                neighbours[0] = grid[y][x].f_out[0]

                #Aktualizacja f_in
                for i in range(9):
                    if neighbours[i] == -1.0:
                        if i == 1:
                            grid[y][x].f_in[2] = grid[y][x].f_out[i]
                        elif i == 2:
                            grid[y][x].f_in[1] = grid[y][x].f_out[i]
                        elif i == 3:
                            grid[y][x].f_in[4] = grid[y][x].f_out[i]
                        elif i == 4:
                            grid[y][x].f_in[3] = grid[y][x].f_out[i]
                        elif i == 5:
                            grid[y][x].f_in[7] = grid[y][x].f_out[i]
                        elif i == 6:
                            grid[y][x].f_in[8] = grid[y][x].f_out[i]
                        elif i == 7:
                            grid[y][x].f_in[5] = grid[y][x].f_out[i]
                        elif i == 8:
                            grid[y][x].f_in[6] = grid[y][x].f_out[i]

                    else:
                        grid[y][x].f_in[i] = neighbours[i]
                        
                        
def collision():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y][x].is_avalible:
                #Inicjalizacja sąsiadów
                neighbours = [-1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0]

                for i in range(9):
                    if grid[y-cy[i]][x-cx[i]].is_avalible:
                        neighbours[i] = grid[y-cy[i]][x-cx[i]].f_out[i]

                for i in range(9):
                    if neighbours[i] != -1.0:
                        grid[y][x].f_in[i] += neighbours[i]
                    else:
                        if i == 1:
                            grid[y][x].f_in[2] = grid[y][x].f_out[i]
                        elif i == 2:
                            grid[y][x].f_in[1] = grid[y][x].f_out[i]
                        elif i == 3:
                            grid[y][x].f_in[4] = grid[y][x].f_out[i]
                        elif i == 4:
                            grid[y][x].f_in[3] = grid[y][x].f_out[i]
                        elif i == 5:
                            grid[y][x].f_in[7] = grid[y][x].f_out[i]
                        elif i == 6:
                            grid[y][x].f_in[8] = grid[y][x].f_out[i]
                        elif i == 7:
                            grid[y][x].f_in[5] = grid[y][x].f_out[i]
                        elif i == 8:
                            grid[y][x].f_in[6] = grid[y][x].f_out[i]
"""
def collision():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y][x].is_avalible:
                #Inicjalizacja sąsiadów
                neighbours = [False, False, False, False, False, False, False, False, False]

                for i in range(9):
                    if grid[y+cy[i]][x+cx[i]].is_avalible:
                        grid[y+cy[i]][x+cx[i]].f_in[i] = grid[y][x].f_out[i]
                        neighbours[i] = True

                for i in range(9):
                    if neighbours[i]:
                        continue
                    else:
                        if i == 1:
                            grid[y][x].f_in[2] = grid[y][x].f_out[i]
                        elif i == 2:
                            grid[y][x].f_in[1] = grid[y][x].f_out[i]
                        elif i == 3:
                            grid[y][x].f_in[4] = grid[y][x].f_out[i]
                        elif i == 4:
                            grid[y][x].f_in[3] = grid[y][x].f_out[i]
                        elif i == 5:
                            grid[y][x].f_in[7] = grid[y][x].f_out[i]
                        elif i == 6:
                            grid[y][x].f_in[8] = grid[y][x].f_out[i]
                        elif i == 7:
                            grid[y][x].f_in[5] = grid[y][x].f_out[i]
                        elif i == 8:
                            grid[y][x].f_in[6] = grid[y][x].f_out[i]


def clean_fin():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y][x].is_avalible:
                for i in range(9):
                    grid[y][x].f_in[i] = 0

def clean_feq():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y][x].is_avalible:
                for i in range(9):
                    grid[y][x].f_eq[i] = 0

def clean_fout():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y][x].is_avalible:
                for i in range(9):
                    grid[y][x].f_out[i] = 0

def update_ro():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y][x].is_avalible:
                grid[y][x].ro = sum(grid[y][x].f_in)

def update_ux():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y][x].is_avalible:
                temp_ux = 0
                for i in range(9):
                    temp_ux += grid[y][x].f_in[i]*cx[i]
                grid[y][x].ux = (temp_ux/grid[y][x].ro)

def update_uy():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y][x].is_avalible:
                temp_uy = 0
                for i in range(9):
                    temp_uy += grid[y][x].f_in[i]*cy[i]
                grid[y][x].uy = (temp_uy / grid[y][x].ro)

def check_corners():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if not grid[y][x].is_avalible:
                # Prawy sąsiad (1)
                if x < GRID_WIDTH - 1 and grid[y][x + 1].is_avalible:
                    if grid[y][x+1].ro < 0.7:
                        grid[y][x+1].ro = 0.7

                # Lewy sąsiad (2)
                if x > 0 and grid[y][x - 1].is_avalible:
                    if grid[y][x - 1].ro < 0.7:
                        grid[y][x -1].ro = 0.7

                # Gorny sąsiad (3)
                if y > 0 and grid[y - 1][x].is_avalible:
                    if grid[y-1][x].ro < 0.7:
                        grid[y-1][x].ro = 0.7

                # Dolny sąsiad (4)
                if y < GRID_HEIGHT - 1 and grid[y + 1][x].is_avalible:
                    if grid[y+1][x].ro < 0.7:
                        grid[y+1][x].ro = 0.7

                # Prawy górny sąsiad (5)
                if x < GRID_WIDTH - 1 and y > 0 and grid[y - 1][x + 1].is_avalible:
                    if grid[y-1][x + 1].ro < 0.7:
                        grid[y-1][x + 1].ro = 0.7

                # Lewy górny sąsiad (6)
                if x > 0 and y > 0 and grid[y - 1][x - 1].is_avalible:
                    if grid[y-1][x-1].ro < 0.7:
                        grid[y-1][x-1].ro = 0.7

                # Lewy dolny sąsiad (7)
                if x > 0 and y < GRID_HEIGHT - 1 and grid[y + 1][x - 1].is_avalible:
                    if grid[y+1][x-1].ro < 0.7:
                        grid[y+1][x-1].ro = 0.7

                # Prawy dolny sąsiad (8)
                if x < GRID_WIDTH - 1 and y < GRID_HEIGHT - 1 and grid[y + 1][x + 1].is_avalible:
                    if grid[y+1][x+1].ro < 0.7:
                        grid[y+1][x+1].ro = 0.7

def init_grid():
    # Inicjalizacja warunków brzegowych i początkowych
    for x in range(GRID_WIDTH):
        grid[0][x] = Cell(False)
        grid[GRID_HEIGHT - 1][x] = Cell(False)
    for y in range(GRID_HEIGHT):
        grid[y][0] = Cell(False)
        grid[y][GRID_WIDTH - 1] = Cell(False)

    barrier_x = GRID_WIDTH // 4

    for y in range(GRID_HEIGHT):
        if GRID_HEIGHT // 2 - 10 <= y <= GRID_HEIGHT // 2 + 10:
            temp = Cell(True)
            temp.set_ro(0.95)
            grid[y][barrier_x] = temp
            continue
        grid[y][barrier_x] = Cell(False)

    #Lewa część siatki
    for y in range(1, GRID_HEIGHT - 1):
        for x in range(1, barrier_x):
            temp = Cell(True)
            temp.set_ro(1.0)
            grid[y][x] = temp

    #Prawa część siatki
    for y in range(1, GRID_HEIGHT - 1):
        for x in range(barrier_x + 1, GRID_WIDTH - 1):
            temp = Cell(True)
            temp.set_ro(0.95)
            grid[y][x] = temp



#Skala prędkości
MIN_U = -1e-4  #Minimalna (najbardziej ujemna) wartość prędkości
MAX_U = 1e-4   #Maksymalna (najbardziej dodatnia) wartość prędkości

def draw_board(screen):
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if not grid[y][x].is_avalible:
                color = (255, 0, 255)  #Ścianki
            else:
                u = grid[y][x].ux
                #Normalizacja wartości
                scaled_u = (u - MIN_U) / (MAX_U - MIN_U)
                scaled_u = np.clip(scaled_u, 0, 1)

                #Interpolacja kolorów (czerwony -> żółty -> zielony)
                if scaled_u < 0.5:
                    intensity = scaled_u * 2
                    color = (255, int(255 * intensity), 0)
                else:
                    intensity = (scaled_u - 0.5) * 2
                    color = (int(255 * (1 - intensity)), 255, 0)
            pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))






def draw_board_speed(screen):
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if not grid[y][x].is_avalible:
                color = (255, 0, 255)  # Ścianki
            else:
                # Pobranie surowej wartości prędkości
                raw_speed = np.clip(grid[y][x].uy, 0, 1)

                # Skala kolorystyczna dla prędkości
                if raw_speed < 0.1:
                    color = (32, 0, 32)  # Najciemniejszy odcień
                elif raw_speed < 0.2:
                    color = (64, 0, 64)
                elif raw_speed < 0.3:
                    color = (96, 0, 96)
                elif raw_speed < 0.4:
                    color = (128, 0, 128)
                elif raw_speed < 0.5:
                    color = (160, 0, 160)
                elif raw_speed < 0.6:
                    color = (192, 0, 192)
                elif raw_speed < 0.7:
                    color = (208, 0, 208)
                elif raw_speed < 0.8:
                    color = (224, 0, 224)
                elif raw_speed < 0.9:
                    color = (240, 0, 240)
                else:
                    color = (255, 0, 255)  # Najjaśniejszy odcień

            # Rysowanie prostokąta na ekranie
            pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))


def check_dens():
    sum = 0
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y][x].is_avalible:
                sum += grid[y][x].ro

    print(sum)

def check_fout():
    sum = 0
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y][x].is_avalible:
                for i in range(9):
                    sum += grid[y][x].f_out[i]

    print(sum)

def check_fin():
    sum = 0
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y][x].is_avalible:
                for i in range(9):
                    sum += grid[y][x].f_in[i]

    print(sum)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()
    running = True
    paused = False
    init_grid()

    licz = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused

        if not paused:
            #Aktualizacja planszy
            #check_dens()
            update_ux()
            update_uy()
            eq_function()
            out_function()
            #check_fout()

            clean_fin()
            clean_feq()

            collision()

            clean_fout()

            update_ro()

            print("Liczba iteracji: ", licz)
            licz+=1
            #print('ux: ', grid[3][2].ux)
            #print('uy: ', grid[3][2].uy)

            #check_corners()

            # Rysowanie planszy
            screen.fill((0, 0, 0))
            draw_board(screen)

            pygame.display.flip()
            clock.tick(60)

    pygame.quit()

main()


"""
def collision():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y][x].is_avalible:
                temp_lewy = 0
                temp_prawy = 0
                temp_dol = 0
                temp_gora = 0
                temp_prawy_dol = 0
                temp_lewy_dol = 0
                temp_prawy_gora = 0
                temp_lewy_gora = 0

                if not grid[y][x-1].is_avalible:
                    temp_lewy += grid[y][x].f_out[2]
                if not grid[y][x+1].is_avalible:
                    temp_prawy += grid[y][x].f_out[1]
                if not grid[y-1][x].is_avalible:
                    temp_gora += grid[y][x].f_out[3]
                if not grid[y+1][x].is_avalible:
                    temp_dol += grid[y][x].f_out[4]
                if not grid[y-1][x-1].is_avalible:
                    temp_lewy_gora += grid[y][x].f_out[6]
                if not grid[y-1][x+1].is_avalible:
                    temp_prawy_gora += grid[y][x].f_out[5]
                if not grid[y+1][x-1].is_avalible:
                    temp_lewy_dol += grid[y][x].f_out[7]
                if not grid[y+1][x+1].is_avalible:
                    temp_prawy_dol += grid[y][x].f_out[8]

                grid[y][x - 1].f_in[2] += (grid[y][x].f_out[2] + (temp_prawy))
                grid[y][x + 1].f_in[1] += (grid[y][x].f_out[1] + (temp_lewy))
                grid[y-1][x].f_in[3] += (grid[y][x].f_out[3] + (temp_gora))
                grid[y + 1][x].f_in[4] += (grid[y][x].f_out[4] + (temp_dol))
                grid[y-1][x-1].f_in[6] += (grid[y][x].f_out[6] + (temp_prawy_dol))
                grid[y - 1][x + 1].f_in[5] += (grid[y][x].f_out[5] + (temp_lewy_dol))
                grid[y + 1][x - 1].f_in[7] += (grid[y][x].f_out[7] + (temp_prawy_gora))
                grid[y + 1][x + 1].f_in[8] += (grid[y][x].f_out[8] + (temp_lewy_gora))

                grid[y][x].f_in[0] += grid[y][x].f_out[0]
                #grid[y][x].f_in[0] += ((temp_prawy/3)+ (temp_lewy/3)+ (temp_dol/3) + (temp_gora/3) + (temp_prawy_dol/3) + (temp_lewy_dol/3) + (temp_prawy_gora/3)+ (temp_lewy_gora/3))
"""


"""
#ta gorsza

def collision():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y][x].is_avalible:
                temp_lewy = 0
                temp_prawy = 0
                temp_dol = 0
                temp_gora = 0
                temp_prawy_dol = 0
                temp_lewy_dol = 0
                temp_prawy_gora = 0
                temp_lewy_gora = 0

                if not grid[y][x-1].is_avalible:
                    grid[y][x+1].f_in[1] += grid[y][x].f_out[2]
                    if not grid[y][x+1].is_avalible:
                        print('dupa')
                else:
                    grid[y][x - 1].f_in[2] += grid[y][x].f_out[2]

                if not grid[y][x+1].is_avalible:
                    grid[y][x - 1].f_in[2] += grid[y][x].f_out[1]
                    if not grid[y][x - 1].is_avalible:
                        print('dupa')
                else:
                    grid[y][x + 1].f_in[1] += grid[y][x].f_out[1]

                if not grid[y-1][x].is_avalible:
                    grid[y +1][x].f_in[3] += grid[y][x].f_out[4]
                    if not grid[y +1][x].is_avalible:
                        print('dupa')
                else:
                    grid[y - 1][x].f_in[4] += grid[y][x].f_out[4]

                if not grid[y+1][x].is_avalible:
                    grid[y-1][x].f_in[4] += grid[y][x].f_out[3]
                    if not grid[y-1][x].is_avalible:
                        print('dupa')
                else:
                    grid[y + 1][x].f_in[3] += grid[y][x].f_out[3]

                if not grid[y-1][x-1].is_avalible:
                    if not grid[y+1][x+1].is_avalible:
                        grid[y][x].f_in[0] += grid[y][x].f_out[7]
                    else:
                        grid[y][x].f_in[0] += grid[y][x].f_out[7]
                else:
                    grid[y - 1][x - 1].f_in[7] += grid[y][x].f_out[7]

                if not grid[y-1][x+1].is_avalible:
                    if not grid[y + 1][x - 1].is_avalible:
                        grid[y][x].f_in[0] += grid[y][x].f_out[8]
                    else:
                        grid[y + 1][x - 1].f_in[6] += grid[y][x].f_out[8]
                else:
                    grid[y-1][x+1].f_in[8] += grid[y][x].f_out[8]

                if not grid[y+1][x-1].is_avalible:
                    if not grid[y -1][x +1].is_avalible:
                        grid[y][x].f_in[0] += grid[y][x].f_out[6]
                    else:
                        grid[y -1][x +1].f_in[8]+=grid[y][x].f_out[6]
                else:
                    grid[y + 1][x - 1].f_in[6]+=grid[y][x].f_out[6]

                if not grid[y+1][x+1].is_avalible:
                    if not grid[y - 1][x - 1].is_avalible:
                        grid[y][x].f_in[0]+=grid[y][x].f_out[5]
                    else:
                        grid[y - 1][x - 1].f_in[7] += grid[y][x].f_out[5]
                else:
                    grid[y + 1][x + 1].f_in[5] += grid[y][x].f_out[5]


                grid[y][x].f_in[0] += grid[y][x].f_out[0]
                #grid[y][x].f_in[0] += ((temp_prawy/3)+ (temp_lewy/3)+ (temp_dol/3) + (temp_gora/3) + (temp_prawy_dol/3) + (temp_lewy_dol/3) + (temp_prawy_gora/3)+ (temp_lewy_gora/3))

"""

"""
#wyswietlanie MOJE

def draw_board(screen):
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if not grid[y][x].is_avalible:
                color = (255, 0, 255)  # Ścianki
            else:
                print(grid[y][x].ux)
                intensity = int(np.clip(grid[y][x].ux, 0, 1) * 255)
                color = (0, intensity, intensity)  # Skala żółci
            pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
"""