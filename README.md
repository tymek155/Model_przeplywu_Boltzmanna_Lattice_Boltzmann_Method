Go to [English version](#english-version)
# Ogólne informacje i wykorzystanie
## Projekt realizuje implementację symulacji modelu przepływu Boltzmanna - Lattice Boltzmann Method. Kod był uruchamiany i napisany w środowisku PyCharm.

Głównym elementem reprezentującym cząstki gazu w moim programie jest klasa `Cell`. 
W jej polach inicjowane są wartości, które mówią nam o dostępności piksela/punktu planszy 
(tj. czy stanowi on plansze, gdzie może poruszać się badany płyn, czy barierę, od której ma 
się odpowiednio odbijać), o aktualnej gęstości znajdującej się w punkcie, składowa pozioma prędkości, 
składowa pionowa prędkości oraz trzy listy, które zawierają informacje o wartościach dla rozkładu równowagowego, 
wejściowego oraz wyjściowego, zainicjowane na wartości zero. Dodatkowo dodana została funkcja umożliwiająca 
edytowanie wartości gęstości.

```python
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
```

W zakresie globalnym zainicjowana została siatka, startowo składająca się z obiektów klasy `Cell`, 
a każdy z nich jest ustawiony jako dostępny. Dodatkowo został zainicjowany wektor z wartościami wag `w`, 
tym razem zawiera on 9 wartości oraz listy `cx` oraz `cy` zawierające informacje o prędkościach w jakiej kolejności 
są przetwarzane.

```python
#Siatka komórek
grid = [[Cell(True) for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
w = [4/9, 1/9, 1/9, 1/9, 1/9, 1/36, 1/36, 1/36, 1/36]
cx = [0, 1, -1, 0, 0, 1, -1, -1, 1]
cy = [0, 0, 0, 1, -1, 1, 1, -1, -1]
```

Funkcja `eq_function` odpowiada za obliczenia rozkładu równowagi. Wyliczane są tu wartości 
we wszystkich dostępnych punktach sitaki zgodnie z zadanym wzorem. Wzór, na którym aktualnie 
pracujemy, różni się od tego z poprzedniej instrukcji z uwagi na zmianę typu modelu na `D2Q9`.

```python
def eq_function():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y][x].is_avalible:
                for i in range(9):
                    grid[y][x].f_eq[i] = w[i]*grid[y][x].ro *(1+3*(cx[i]*grid[y][x].ux + cy[i]*grid[y][x].uy)+4.5*(cx[i]*grid[y][x].ux + cy[i]*grid[y][x].uy)*(cx[i]*grid[y][x].ux + cy[i]*grid[y][x].uy)-1.5*((grid[y][x].ux)*(grid[y][x].ux)+(grid[y][x].uy)*(grid[y][x].uy)))

```

Funkcja `out_function` odpowiada za obliczenia rozkładu wyjściowego, domyślnie jednak przyjąłem wartość `tau=1.0` 
tak jak poprzednio, stąd wzór jest uproszczony do przypisania wartości `f_eq` do `f_out`.

```python
def out_function():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y][x].is_avalible:
                for i in range(9):
                    grid[y][x].f_out[i] = grid[y][x].f_eq[i]
```

Funkcja `collision` odpowiada za aktualizacje wartości rozkładu wejściowego na podstawie policzonego już rozkładu 
wyjściowego oraz z uwzględnieniem ewentualnego odbicia od ściany/przeszkody. Funkcja przechodzi przez dostępne 
pola całej siatki, bada czy sąsiedzi też byli dostępni (czy aby przypadkiem nie byli przeszkodą/ścianą). 
W pierwszej pętli przekazywane są wartości funkcji wyjścia do funkcji wejścia kolejno badanych sąsiadów 
(ich funkcji wejścia). W następnej pętli realizowane jest ewentualne odbicie, w zależności od stanu kolejnych 
elementów listy `neighbours`.

```python
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
```

Funkcje `clean_fin`, `clean_feq` oraz `clean_fout` odpowiadają za czyszczenie list funkcji równowagi, 
wejścia oraz wyjścia, w celu zapewnienia poprawnych wyników.

```python
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
```

Funkcje `update_ro`, `update_ux` i `update_uy` odpowiadają za aktualizacje wartości gęstości oraz prędkości - 
poziomej oraz pionowej, które w każdej iteracji programu aktualizują informacje o gęstości oraz obu składowych 
prędkości. Dla funkcji prędkości dodany został warunek zerowania przy niskiej gęstości, w celu uniknięcia 
ewentualnego dzielenia przez 0.

```python
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
                if grid[y][x].ro < 0.0001:
                    grid[y][x].ux = 0
                else:
                    grid[y][x].ux = (temp_ux/grid[y][x].ro)

def update_uy():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y][x].is_avalible:
                temp_uy = 0
                for i in range(9):
                    temp_uy += grid[y][x].f_in[i]*cy[i]
                if grid[y][x].ro < 0.0001:
                    grid[y][x].uy = 0
                else:
                    grid[y][x].uy = (temp_uy / grid[y][x].ro)
```

Funkcja `init_grid` odpowiada za zainicjowanie całej barier i przeszkód w siatce oraz za zainicjowanie 
wartości początkowych do symulacji dla lewej i prawej części sitaki. W tym przypadku lewa część ma gęstość 
w zakresie 100%, prawa natomiast to 10%.

```python
def init_grid():
    #Inicjalizacja warunków brzegowych i początkowych
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
```

Funkcja `draw_board` odpowiada za narysowanie w odpowiednim kolorze barier oraz komórek aktywnych w zależności 
poziomu prędkości (lub innej wartości) znajdującej się w nich (dla lepiej widocznej wizualizacji dodałem 
skalowanie). Dla łatwiejszej do interpretacji wizualizacji, pierwsza funkcja ustala kolory w zakresie od 
czerwieni do zielonego (czerwień to ujemne wartości prędkości, żółty to wartości bliskie 0, natomiast zieleń 
to wartości dodatnie). Dla gęstości przyjąłem jej drugą wersję widoczną również poniżej, w niej zastosowałem 
nieco inny rodzaj wyświetlania, gdyż w naszym zadaniu badamy gęstości o stosunkowo bliskich wartościach 
(zakres 0,95-1,0).

```python
#Skala prędkości
MIN_U = -1e-4  #Minimalna (najbardziej ujemna) wartość prędkości
MAX_U = 1e-4   #Maksymalna (najbardziej dodatnia) wartość prędkości

def draw_board(screen):
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if not grid[y][x].is_avalible:
                color = (255, 0, 255)  #Ścianki
            else:
                u = grid[y][x].uy
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
```

```python
def draw_board(screen):
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if not grid[y][x].is_avalible:
                color = (255, 0, 255) 
            else:
                raw_density = np.clip(grid[y][x].ro, 0.9, 1.0)

                if raw_density < 0.91:
                    color = (0, 32, 32)
                elif raw_density < 0.92:
                    color = (0, 64, 64)
                elif raw_density < 0.93:
                    color = (0, 96, 96)
                elif raw_density < 0.94:
                    color = (0, 128, 128)
                elif raw_density < 0.95:
                    color = (0, 160, 160)
                elif raw_density < 0.96:
                    color = (0, 192, 192)
                elif raw_density < 0.97:
                    color = (0, 208, 208)
                elif raw_density < 0.98:
                    color = (0, 224, 224)
                elif raw_density < 0.99:
                    color = (0, 240, 240)
                else:
                    color = (0, 255, 255)

            pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
```

# Technologie
W kodzie użyto:
* Python 3.12
* NumPy 2.2.2
* Pygame 2.6.1

# Przykładowe wizualizacje
## Wizualizacja gęstości

<div align="center">
  
![image](https://github.com/user-attachments/assets/5f0196cd-2a8f-43eb-ab63-e519673e8181)
<br>
![image](https://github.com/user-attachments/assets/e98d0693-1a1a-4a15-a1fe-db0b5febe78f)
<br>
![image](https://github.com/user-attachments/assets/b0e97c89-47e5-4902-b107-9fb52a743f25)
<br>
![image](https://github.com/user-attachments/assets/56e8dd3e-51b5-4d18-a922-8685e2c9044f)

</div>  


## Wizualizacja rozkładu prędkości poziomej

<div align="center">

![image](https://github.com/user-attachments/assets/cbd037b1-e42f-400a-aec2-a6bf2fedc606)  
<br>
![image](https://github.com/user-attachments/assets/b2a5a3b4-7182-4a91-8aa0-5e251598fce0)  
<br>
![image](https://github.com/user-attachments/assets/1d06fe1e-b0af-43aa-b486-24482120f010)  
<br>
![image](https://github.com/user-attachments/assets/e80ea5f8-fb33-47a0-aa52-43b8c16ca6b4)  

</div> 

## Wizualizacja rozkładu prędkości pionowej

<div align="center">
  
![image](https://github.com/user-attachments/assets/e0a0d982-dc66-4587-9249-3413bc96740c)
<br>
![image](https://github.com/user-attachments/assets/45da3d4f-18ac-45d4-8ced-fc1cefdb8354)
<br>
![image](https://github.com/user-attachments/assets/ce24033a-f7c9-49ee-acc4-d2120fb9a141)
<br>
![image](https://github.com/user-attachments/assets/1f829d60-3f5a-4707-9406-c3d705c6c453)  

</div>


# English version

# General Information and usage 
## The project implements the simulation of the Boltzmann flow model - Lattice Boltzmann Method. The code was run and written in the PyCharm environment.

The main element representing gas particles in my program is the `Cell` class. In its fields, 
values are initialized that inform us about the availability of a pixel/point on the grid (i.e., whether 
it represents a grid where the studied fluid can move or a barrier from which it should reflect properly), 
the current density at the point, the horizontal component of velocity, the vertical component of velocity, 
and three lists that contain information about the equilibrium, input, and output distribution values, 
initialized to zero. Additionally, a function has been added to allow editing the density values.

```python
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
```

On a global scale, a grid has been initialized, initially consisting of objects of the `Cell` class, 
and each of them is set as available. Additionally, a vector with weight values `w` has been initialized, 
which now contains 9 values, as well as the lists `cx` and `cy`, which contain information about the velocities 
in the order they are processed.

```python
#Siatka komórek
grid = [[Cell(True) for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
w = [4/9, 1/9, 1/9, 1/9, 1/9, 1/36, 1/36, 1/36, 1/36]
cx = [0, 1, -1, 0, 0, 1, -1, -1, 1]
cy = [0, 0, 0, 1, -1, 1, 1, -1, -1]
```

The `eq_function` is responsible for calculating the equilibrium distribution. Values are calculated here 
for all available points on the grid according to the given formula. The formula we are currently working 
with differs from the one in the previous instruction due to the change in the model type to `D2Q9`.

```python
def eq_function():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y][x].is_avalible:
                for i in range(9):
                    grid[y][x].f_eq[i] = w[i]*grid[y][x].ro *(1+3*(cx[i]*grid[y][x].ux + cy[i]*grid[y][x].uy)+4.5*(cx[i]*grid[y][x].ux + cy[i]*grid[y][x].uy)*(cx[i]*grid[y][x].ux + cy[i]*grid[y][x].uy)-1.5*((grid[y][x].ux)*(grid[y][x].ux)+(grid[y][x].uy)*(grid[y][x].uy)))

```

The `out_function` is responsible for calculating the output distribution, however, I have assumed the 
value `tau=1.0` by default, just like before, so the formula is simplified to assigning the value of `f_eq` 
to `f_out`.

```python
def out_function():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y][x].is_avalible:
                for i in range(9):
                    grid[y][x].f_out[i] = grid[y][x].f_eq[i]
```

The `collision` function is responsible for updating the input distribution values based on the already 
calculated output distribution, taking into account any potential reflection from a wall/obstacle. The 
function iterates through the available fields of the entire grid, checking if the neighbors were also 
available (i.e., whether they were not an obstacle/wall). In the first loop, the output function values are 
passed to the input function of the sequentially checked neighbors (their input functions). In the next loop, 
any potential reflection is performed, depending on the state of the subsequent elements in the `neighbours` list.

```python
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
```

The `clean_fin`, `clean_feq`, and `clean_fout` functions are responsible for clearing the lists of 
equilibrium, input, and output functions to ensure correct results.

```python
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
```

The `update_ro`, `update_ux`, and `update_uy` functions are responsible for updating the values of density 
and velocity — both horizontal and vertical — which in each iteration of the program update information about 
density and both velocity components. For the velocity functions, a condition has been added to reset the values 
in case of low density, to avoid potential division by zero.

```python
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
                if grid[y][x].ro < 0.0001:
                    grid[y][x].ux = 0
                else:
                    grid[y][x].ux = (temp_ux/grid[y][x].ro)

def update_uy():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y][x].is_avalible:
                temp_uy = 0
                for i in range(9):
                    temp_uy += grid[y][x].f_in[i]*cy[i]
                if grid[y][x].ro < 0.0001:
                    grid[y][x].uy = 0
                else:
                    grid[y][x].uy = (temp_uy / grid[y][x].ro)
```

The `init_grid` function is responsible for initializing all barriers and obstacles in the grid, 
as well as initializing the initial values for the simulation for the left and right parts of the grid. 
In this case, the left part has a density of 100%, while the right part has a density of 10%.

```python
def init_grid():
    #Inicjalizacja warunków brzegowych i początkowych
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
```

The `draw_board` function is responsible for drawing barriers and active cells in the appropriate color, 
depending on the velocity level (or another value) contained within them (for better visualization, 
I added scaling). For easier-to-interpret visualization, the first function sets colors in the range from red 
to green (red represents negative velocity values, yellow represents values close to 0, and green represents 
positive values). For density, I used its second version, also shown below, in which I applied a slightly 
different display method, as in our task we are examining densities with relatively close values (range 0.95-1.0).

```python
#Skala prędkości
MIN_U = -1e-4  #Minimalna (najbardziej ujemna) wartość prędkości
MAX_U = 1e-4   #Maksymalna (najbardziej dodatnia) wartość prędkości

def draw_board(screen):
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if not grid[y][x].is_avalible:
                color = (255, 0, 255)  #Ścianki
            else:
                u = grid[y][x].uy
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
```

```python
def draw_board(screen):
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if not grid[y][x].is_avalible:
                color = (255, 0, 255) 
            else:
                raw_density = np.clip(grid[y][x].ro, 0.9, 1.0)

                if raw_density < 0.91:
                    color = (0, 32, 32)
                elif raw_density < 0.92:
                    color = (0, 64, 64)
                elif raw_density < 0.93:
                    color = (0, 96, 96)
                elif raw_density < 0.94:
                    color = (0, 128, 128)
                elif raw_density < 0.95:
                    color = (0, 160, 160)
                elif raw_density < 0.96:
                    color = (0, 192, 192)
                elif raw_density < 0.97:
                    color = (0, 208, 208)
                elif raw_density < 0.98:
                    color = (0, 224, 224)
                elif raw_density < 0.99:
                    color = (0, 240, 240)
                else:
                    color = (0, 255, 255)

            pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
```

# Technologies
The code uses:
* Python 3.12
* NumPy 2.2.2
* Pygame 2.6.1

# Sample visualizations
## Density Visualization

<div align="center">
  
![image](https://github.com/user-attachments/assets/5f0196cd-2a8f-43eb-ab63-e519673e8181)
<br>
![image](https://github.com/user-attachments/assets/e98d0693-1a1a-4a15-a1fe-db0b5febe78f)
<br>
![image](https://github.com/user-attachments/assets/b0e97c89-47e5-4902-b107-9fb52a743f25)
<br>
![image](https://github.com/user-attachments/assets/56e8dd3e-51b5-4d18-a922-8685e2c9044f)

</div>

## Visualization of horizontal velocity distribution

<div align="center">

![image](https://github.com/user-attachments/assets/cbd037b1-e42f-400a-aec2-a6bf2fedc606)  
<br>
![image](https://github.com/user-attachments/assets/b2a5a3b4-7182-4a91-8aa0-5e251598fce0)  
<br>
![image](https://github.com/user-attachments/assets/1d06fe1e-b0af-43aa-b486-24482120f010)  
<br>
![image](https://github.com/user-attachments/assets/e80ea5f8-fb33-47a0-aa52-43b8c16ca6b4)  

</div>

## Visualization of vertical velocity distribution

<div align="center">
  
![image](https://github.com/user-attachments/assets/e0a0d982-dc66-4587-9249-3413bc96740c)
<br>
![image](https://github.com/user-attachments/assets/45da3d4f-18ac-45d4-8ced-fc1cefdb8354)
<br>
![image](https://github.com/user-attachments/assets/ce24033a-f7c9-49ee-acc4-d2120fb9a141)
<br>
![image](https://github.com/user-attachments/assets/1f829d60-3f5a-4707-9406-c3d705c6c453)  

</div>















