import pygame
import sys
import random

# Define the dimensions of the grid and size of each cell
GRID_WIDTH = 200
GRID_HEIGHT = 200
CELL_SIZE = 4
WINDOW_WIDTH = GRID_WIDTH * CELL_SIZE
WINDOW_HEIGHT = GRID_HEIGHT * CELL_SIZE

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (200, 200, 200)
GREEN = (0, 255, 0)
LIGHT_BLUE = (173, 216, 230)
LIGHT_GREY = (211, 211, 211)


# this class is not usable in this version of the simulation!
class Speed:
    def __init__(self):
        self.speed = 200
        self.ACC = 0.9

    def get_speed(self):
        return int(self.speed)

    def calc_speed(self):
        self.speed = self.speed * self.ACC
        

def draw_grid(grid , screen):
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            color = BLACK if grid[row][col] == 0 else (LIGHT_BLUE if grid[row][col] == 1 else GREEN)
            cell_rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        



    # Draw grid frame
    pygame.draw.rect(screen, GREY, (0, 0, GRID_WIDTH * CELL_SIZE, GRID_HEIGHT * CELL_SIZE), 1)

def update_grains(grains, grid):
    for i in range(len(grains)-1, -1, -1):
        row, col, grain_speed = grains[i]
        if row < GRID_HEIGHT - 1:
            if grid[row+1][col] != 1 and grid[row+1][col] != 2:
                grain_speed.calc_speed()
                grains[i] = (row + 1, col, grain_speed)
                grid[row][col] = 0
                grid[row+1][col] = 1
            else:
                grains.pop(i)
        else:
            grains.pop(i)
    return grains

def main_loop(screen, Speed):

    intensity = 0.1  # Intensity of snowfall


    grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    grains = []  # List to store the positions and speeds of each sand grain
    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # button to change intensity of snowfall
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and intensity < 0.9:
                    intensity += 0.10
                if event.key == pygame.K_DOWN and intensity > 0.1:
                    intensity -= 0.10
                if event.key == pygame.K_ESCAPE:
                    running = False    


        


        # Generate new sand grains randomly
        if random.random() < intensity:
            col = random.randint(0, GRID_WIDTH - 1)
            grain_speed = Speed()
            grains.append((0, col, grain_speed))

        # Update sand grains
        grains = update_grains(grains, grid)

        # Render
        draw_grid(grid, screen)
        # show the intensity of snowfall on the screen
        font = pygame.font.Font(None, 36)
        text = font.render("Snow Intensity: {:.2f}%".format(intensity*100), True, GREEN)
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, 20))
        screen.blit(text, text_rect)

        text = font.render("Press UP and DOWN to change intensity", True, GREY)
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, 60))
        screen.blit(text, text_rect)


        # bottom left corner text
        text = font.render("Made by Sapir Talker", True, GREY)
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 20))
        screen.blit(text, text_rect)


        pygame.display.flip()

        # Control speed
        pygame.time.wait(1)  # Adjust this value for smoother animation


        


    pygame.quit()
    sys.exit()

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Snow Simulation")

    main_loop(screen, Speed)

if __name__ == '__main__':
    main()

