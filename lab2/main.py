import pygame
import numpy as np
import random
from collections import deque

# Константи для стін: кожен біт відповідає окремій стіні
N, S, E, W = 1, 2, 4, 8
# Зміщення для кожного напрямку (x, y)
DX = {E: 1, W: -1, N: 0, S: 0}
DY = {E: 0, W: 0, N: -1, S: 1}
# Протилежні стіни
OPPOSITE = {N: S, S: N, E: W, W: E}

class Maze:
    def __init__(self, width, height, cell_size=20, delay=30, extra_passage_prob=0.1):
        """
        width, height       - розмір лабіринту (кількість клітинок по горизонталі та вертикалі)
        cell_size           - розмір клітинки у пікселях
        delay               - затримка між кроками візуалізації (у мілісекундах)
        extra_passage_prob  - ймовірність додаткового проходу (для створення циклів)
        """
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.delay = delay
        self.extra_passage_prob = extra_passage_prob

        # Кожна клітинка спочатку має всі 4 стіни (бітова маска 15)
        self.maze = np.full((height, width), 15, dtype=np.int32)
        # Масив для відстеження відвіданих клітинок при генерації
        self.visited = np.zeros((height, width), dtype=bool)

        # Визначення кандидатів для входу/виходу – це клітинки на межі лабіринту
        border_candidates = {}
        for y in range(height):
            for x in range(width):
                if x == 0 or x == width - 1 or y == 0 or y == height - 1:
                    possible_walls = []
                    if y == 0:
                        possible_walls.append(N)
                    if y == height - 1:
                        possible_walls.append(S)
                    if x == 0:
                        possible_walls.append(W)
                    if x == width - 1:
                        possible_walls.append(E)
                    border_candidates[(x, y)] = possible_walls

        candidate_cells = list(border_candidates.keys())
        # Випадковий вибір входу та видалення однієї з зовнішніх стін
        entrance_cell = random.choice(candidate_cells)
        candidate_cells.remove(entrance_cell)
        # Випадковий вибір виходу (якщо є інший кандидат)
        exit_cell = random.choice(candidate_cells) if candidate_cells else entrance_cell

        entrance_wall = random.choice(border_candidates[entrance_cell])
        exit_wall = random.choice(border_candidates[exit_cell])

        self.maze[entrance_cell[1], entrance_cell[0]] &= ~entrance_wall
        self.maze[exit_cell[1], exit_cell[0]] &= ~exit_wall

        self.entrance = (entrance_cell[0], entrance_cell[1], entrance_wall)
        self.exit = (exit_cell[0], exit_cell[1], exit_wall)

        # Ініціалізація pygame
        pygame.init()
        self.screen = pygame.display.set_mode((width * cell_size, height * cell_size))
        pygame.display.set_caption("Генерація лабіринту")
        self.clock = pygame.time.Clock()

    def draw_maze(self, current_cell=None, path=None):
        """
        Малює лабіринт:
          - Внутрішні стіни (тонкими лініями)
          - Товста обводка зовнішніх стін з прорізами для входу та виходу
          - Вхід (зелений) та вихід (синій)
          - Якщо current_cell задана, вона виділяється червоним прямокутником
          - Якщо path задано (послідовність клітинок), малюється шлях лінією (фіолетовим)
        """
        self.screen.fill((255, 255, 255))
        for y in range(self.height):
            for x in range(self.width):
                cell = self.maze[y, x]
                x1, y1 = x * self.cell_size, y * self.cell_size
                if cell & N:
                    pygame.draw.line(self.screen, (0, 0, 0), (x1, y1), (x1 + self.cell_size, y1), 2)
                if cell & S:
                    pygame.draw.line(self.screen, (0, 0, 0), (x1, y1 + self.cell_size), (x1 + self.cell_size, y1 + self.cell_size), 2)
                if cell & E:
                    pygame.draw.line(self.screen, (0, 0, 0), (x1 + self.cell_size, y1), (x1 + self.cell_size, y1 + self.cell_size), 2)
                if cell & W:
                    pygame.draw.line(self.screen, (0, 0, 0), (x1, y1), (x1, y1 + self.cell_size), 2)

        # Позначення входу (зелений) та виходу (синій)
        ex, ey, _ = self.entrance
        entrance_center = (ex * self.cell_size + self.cell_size // 2,
                           ey * self.cell_size + self.cell_size // 2)
        pygame.draw.circle(self.screen, (0, 255, 0), entrance_center, self.cell_size // 4)

        ex, ey, _ = self.exit
        exit_center = (ex * self.cell_size + self.cell_size // 2,
                       ey * self.cell_size + self.cell_size // 2)
        pygame.draw.circle(self.screen, (0, 0, 255), exit_center, self.cell_size // 4)

        # Виділення активної клітинки
        if current_cell:
            cx, cy = current_cell
            rect = (cx * self.cell_size + 2, cy * self.cell_size + 2, self.cell_size - 4, self.cell_size - 4)
            pygame.draw.rect(self.screen, (255, 0, 0), rect)

        # Якщо задано шлях, малюємо його (з'єднуємо центри клітинок)
        if path and len(path) > 1:
            points = [(x * self.cell_size + self.cell_size // 2, y * self.cell_size + self.cell_size // 2) for x, y in path]
            pygame.draw.lines(self.screen, (128, 0, 128), False, points, 4)

        # Товста обводка зовнішніх стін
        border_thick = 4
        maze_width_px = self.width * self.cell_size
        maze_height_px = self.height * self.cell_size
        pygame.draw.rect(self.screen, (0, 0, 0), (0, 0, maze_width_px, maze_height_px), border_thick)

        # Прорізи в зовнішній рамці для входу та виходу
        def make_gap(cell_info):
            x, y, wall = cell_info
            if wall == N:
                return (x * self.cell_size, 0, self.cell_size, border_thick)
            elif wall == S:
                return (x * self.cell_size, maze_height_px - border_thick, self.cell_size, border_thick)
            elif wall == W:
                return (0, y * self.cell_size, border_thick, self.cell_size)
            elif wall == E:
                return (maze_width_px - border_thick, y * self.cell_size, border_thick, self.cell_size)
            return None

        for cell in [self.entrance, self.exit]:
            gap = make_gap(cell)
            if gap:
                pygame.draw.rect(self.screen, (255, 255, 255), gap)

        pygame.display.flip()

    def generate_maze(self):
        """Генерує лабіринт ідеальним алгоритмом DFS (починаємо з точки входу)."""
        x, y, _ = self.entrance
        self.visited[y, x] = True
        stack = [(x, y)]
        self.draw_maze(current_cell=(x, y))

        while stack:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            cx, cy = stack[-1]
            neighbors = []
            for direction in [N, S, E, W]:
                nx = cx + DX[direction]
                ny = cy + DY[direction]
                if 0 <= nx < self.width and 0 <= ny < self.height and not self.visited[ny, nx]:
                    neighbors.append((nx, ny, direction))
            if neighbors:
                nx, ny, direction = random.choice(neighbors)
                self.maze[cy, cx] &= ~direction
                self.maze[ny, nx] &= ~OPPOSITE[direction]
                self.visited[ny, nx] = True
                stack.append((nx, ny))
            else:
                stack.pop()

            self.draw_maze(current_cell=(cx, cy))
            pygame.time.delay(self.delay)
            self.clock.tick(60)
        self.draw_maze()

    def add_extra_passages(self):
        """Додає додаткові проходи (цикли) всередині лабіринту для створення альтернативних шляхів."""
        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                for direction in [N, S, E, W]:
                    nx = x + DX[direction]
                    ny = y + DY[direction]
                    if 0 < nx < self.width - 1 and 0 < ny < self.height - 1:
                        if self.maze[y, x] & direction:
                            if random.random() < self.extra_passage_prob:
                                self.maze[y, x] &= ~direction
                                self.maze[ny, nx] &= ~OPPOSITE[direction]
        self.draw_maze()

    def solve_maze_bfs(self):
        """
        Знаходить найкоротший шлях у лабіринті (від точки входу до виходу) за допомогою алгоритму BFS.
        Процес пошуку візуалізується: на кожному кроці відображається активна клітинка та реконструйований шлях.
        """
        start = (self.entrance[0], self.entrance[1])
        goal = (self.exit[0], self.exit[1])
        queue = deque([start])
        parents = {start: None}
        visited = {start}

        found = False
        while queue:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            current = queue.popleft()
            # Реконструюємо шлях від входу до поточної клітинки за допомогою словника батьків
            path = []
            temp = current
            while temp is not None:
                path.append(temp)
                temp = parents[temp]
            path.reverse()

            self.draw_maze(current_cell=current, path=path)
            pygame.time.delay(self.delay)
            self.clock.tick(60)

            if current == goal:
                found = True
                break

            cx, cy = current
            cell = self.maze[cy, cx]
            for direction in [N, S, E, W]:
                # Якщо відповідна стіна відсутня – існує прохід
                if not (cell & direction):
                    nx = cx + DX[direction]
                    ny = cy + DY[direction]
                    if 0 <= nx < self.width and 0 <= ny < self.height:
                        next_cell = (nx, ny)
                        if next_cell not in visited:
                            visited.add(next_cell)
                            parents[next_cell] = current
                            queue.append(next_cell)

        if found:
            # Реконструюємо найкоротший шлях від входу до виходу
            path = []
            temp = goal
            while temp is not None:
                path.append(temp)
                temp = parents[temp]
            path.reverse()
            self.draw_maze(path=path)
        else:
            print("Шлях не знайдено!")

    def run_all(self):
        """
        Запускає повний цикл:
          1. Генерує лабіринт
          2. Додає додаткові проходи
          3. Чекає підтвердження у консолі для запуску алгоритму знаходження шляху (BFS)
          4. Візуалізує процес пошуку найкоротшого шляху
        """
        self.generate_maze()
        self.add_extra_passages()
        print("Лабіринт згенеровано. Натисніть Enter для запуску алгоритму знаходження найкоротшого шляху...")
        input()
        self.solve_maze_bfs()
        # Утримання вікна відкритим після завершення
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
        pygame.quit()

def main():
    try:
        width = int(input("Введіть ширину лабіринту (кількість клітинок): "))
        height = int(input("Введіть висоту лабіринту (кількість клітинок): "))
        cell_size = int(input("Введіть розмір клітинки (у пікселях, наприклад 20): "))
        delay = int(input("Введіть затримку між кроками (у мілісекундах, наприклад 30): "))
        extra_prob = float(input("Введіть ймовірність додаткового проходу (від 0 до 1, наприклад 0.1): "))
    except ValueError:
        print("Будь ласка, введіть коректні числові значення!")
        return

    maze = Maze(width, height, cell_size, delay, extra_prob)
    maze.run_all()

if __name__ == "__main__":
    main()
