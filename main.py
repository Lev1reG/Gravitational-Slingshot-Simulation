import math

import pygame

pygame.init()

WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gravitational Slingshot Effect Simulation")

PLANET_MASS = 100
OBJ_MASS = 5
G = 5
FPS = 60
PLANET_RADIUS = 60
OBJ_SIZE = 5
VEL_SCALE = 100

BG = pygame.transform.scale(pygame.image.load("background.jpg"), (WIDTH, HEIGHT))
PLANET = pygame.transform.scale(
    pygame.image.load("jupiter.png"), (PLANET_RADIUS * 2, PLANET_RADIUS * 2)
)

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)


def main():
    running = True
    clock = pygame.time.Clock()

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        win.blit(BG, (0, 0))
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
