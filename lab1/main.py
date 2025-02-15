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
    for i, j in np.ndindex(matrix.shape):
        # Count live neighbors
        live_neighbors = np.sum(matrix[i - 1:i + 2, j - 1:j + 2]) - matrix[i, j]

        if matrix[i, j] == 1:
            # Live cell: dies if underpopulated or overpopulated
            if live_neighbors < 2 or live_neighbors > 3:
                cell_color = DIE_COLOR
            else:
                # Cell lives on
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
    cells = np.zeros((height, width))

    # Define an initial pattern (an 8-row pattern in this case)
    initial_pattern = np.array([
        [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0],
        [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]
    ])

    # Place the initial pattern at position (10, 10) in the grid
    pos = (10, 10)
    h, w = initial_pattern.shape
    cells[pos[0]:pos[0] + h, pos[1]:pos[1] + w] = initial_pattern
    return cells


def main():
    pygame.init()
    pygame.display.set_caption("Game of Life")

    # Grid dimensions and cell size
    width, height, scale = 50, 30, 10
    screen = pygame.display.set_mode((width * scale, height * scale))

    cells = initialize_grid(width, height)
    clock = pygame.time.Clock()
    running = True

    while running:
        clock.tick(10)  # Set the update speed (10 frames per second)
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
    exit(0)
