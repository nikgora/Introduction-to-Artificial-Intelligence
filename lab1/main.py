import os

os.environ['SDL_VIDEO_MINIMIZE_ON_FOCUS_LOSS'] = '0'

import numpy as np
import pygame

# Define colors
DIE_COLOR = (255, 0, 0)
LIVE_COLOR = (0, 255, 0)
BG_COLOR = (47, 79, 79)
GRID_COLOR = (70, 130, 180)


def update_grid(surface: pygame, matrix: np.array, scale: int) -> np.array:
    """
    Update the grid based on Conway's Game of Life rules and draw the new state.

    Parameters:
        surface: The pygame surface to draw on.
        matrix: 2D numpy array representing the current grid state.
        scale: The pixel size of each cell.

    Returns:
        A new numpy array representing the updated grid state.
    """
    new_matrix = np.zeros(matrix.shape)

    # Count the number of live neighbors for each cell (toroidal grid)
    neighbor_count = (
            np.roll(matrix, 1, axis=0) + np.roll(matrix, -1, axis=0) +  # Up and down
            np.roll(matrix, 1, axis=1) + np.roll(matrix, -1, axis=1) +  # Left and right
            np.roll(np.roll(matrix, 1, axis=0), 1, axis=1) +  # Upper right
            np.roll(np.roll(matrix, 1, axis=0), -1, axis=1) +  # Upper left
            np.roll(np.roll(matrix, -1, axis=0), 1, axis=1) +  # Lower right
            np.roll(np.roll(matrix, -1, axis=0), -1, axis=1)  # Lower left
    )

    for i, j in np.ndindex(matrix.shape):
        live_neighbors = neighbor_count[i, j]

        if matrix[i, j] == 1:
            # Live cell: dies if underpopulated or overpopulated
            if live_neighbors < 2 or live_neighbors > 3:
                cell_color = DIE_COLOR
            else:
                new_matrix[i, j] = 1
                cell_color = LIVE_COLOR
        else:
            # Dead cell: becomes alive if exactly 3 live neighbors
            if live_neighbors == 3:
                new_matrix[i, j] = 1
                cell_color = LIVE_COLOR
            else:
                cell_color = BG_COLOR

        # Draw the cell on the surface
        pygame.draw.rect(surface, cell_color, (j * scale, i * scale, scale - 1, scale - 1))

    return new_matrix


def initialize_grid(width: int, height: int) -> np.array:
    """
    Initialize the grid with an initial pattern.

    Parameters:
        width: Number of columns in the grid.
        height: Number of rows in the grid.

    Returns:
        A numpy array representing the initial grid state.
    """
    grid = np.zeros((height, width))

    # Classic patterns of the game "Life”
    patterns = {
        "block": np.array([
            [1, 1],
            [1, 1]
        ]),
        "blinker": np.array([
            [1, 1, 1]
        ]),
        "toad": np.array([
            [0, 1, 1, 1],
            [1, 1, 1, 0]
        ]),
        "glider": np.array([
            [0, 1, 0],
            [0, 0, 1],
            [1, 1, 1]
        ]),
        "beacon": np.array([
            [1, 1, 0, 0],
            [1, 1, 0, 0],
            [0, 0, 1, 1],
            [0, 0, 1, 1]
        ]),
        "lwss": np.array([
            [0, 1, 0, 0, 1],
            [1, 0, 0, 0, 0],
            [1, 0, 0, 0, 1],
            [1, 1, 1, 1, 0]
        ])
    }

    # Positions to place patterns (row, column)
    positions = {
        "block": (20, 2),
        "blinker": (0, 1),
        "toad": (2, 20),
        "glider": (10, 2),
        "beacon": (10, 10),
        "lwss": (101, 95)
    }

    # Place each pattern at a given grid position
    for name, pat in patterns.items():
        pos = positions[name]
        ph, pw = pat.shape
        grid[pos[0]:pos[0] + ph, pos[1]:pos[1] + pw] = pat

    # Add random cells throughout the grid (10% probability of occurrence)
    random_cells = (np.random.rand(height, width) < 0.10).astype(int)
    # Combine patterns with random cells (if both have live cells, 1 is left)
    grid = np.maximum(grid, random_cells)

    return grid


def main():
    pygame.init()
    pygame.display.set_caption("Game of Life")

    # Grid dimensions and cell size
    width, height, scale = 192, 108, 10
    screen = pygame.display.set_mode((width * scale, height * scale))

    cells = initialize_grid(width, height)
    clock = pygame.time.Clock()
    running = True

    while running:
        clock.tick(60)  # Set the update speed (60 frames per second)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Fill background with the grid color
        screen.fill(GRID_COLOR)

        # Update grid and draw cells
        cells = update_grid(screen, cells, scale)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
