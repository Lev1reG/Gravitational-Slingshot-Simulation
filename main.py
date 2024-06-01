import math

import pygame

pygame.init()

WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gravitational Slingshot Effect Simulation")

PLANET_MASS = 100
ASTEROID_MASS = 5
G = 5
FPS = 60
PLANET_RADIUS = 60
ASTEROID_RADIUS = 35
VEL_SCALE = 100

BG = pygame.transform.scale(pygame.image.load("background.jpg"), (WIDTH, HEIGHT))
PLANET = pygame.transform.scale(
    pygame.image.load("jupiter.png"), (PLANET_RADIUS * 2, PLANET_RADIUS * 2)
)
ASTEROID = pygame.transform.scale(
    pygame.image.load("asteroid.png"), (ASTEROID_RADIUS, ASTEROID_RADIUS)
)

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

class Asteroid:
    def __init__(self, x, y, vel_x, vel_y, mass):
        self.x = x
        self.y = y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.mass = mass

    def move(self, planet = None):
        self.x += self.vel_x
        self.y += self.vel_y


    def draw(self):
        win.blit(ASTEROID, (int(self.x), int(self.y)))

def create_asteroid(location, mouse):
    t_x, t_y = location
    m_x, m_y = mouse
    vel_x = (m_x - t_x) / VEL_SCALE
    vel_y = (m_y - t_y) / VEL_SCALE
    obj = Asteroid(t_x, t_y, vel_x, vel_y, ASTEROID_MASS) 
    return obj

def main():
    running = True
    clock = pygame.time.Clock()

    objects = []
    temp_obj_pos = None

    while running:
        clock.tick(FPS)

        mouse_pos = pygame.mouse.get_pos()  # get the mouse position (x, y)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # if the mouse is clicked
            if event.type == pygame.MOUSEBUTTONDOWN:
                if temp_obj_pos:
                    obj = create_asteroid(temp_obj_pos, mouse_pos)
                    objects.append(obj)
                    temp_obj_pos = None
                else:
                    temp_obj_pos = mouse_pos

        win.blit(BG, (0, 0))

        if temp_obj_pos:
            pygame.draw.line(win, WHITE, temp_obj_pos, mouse_pos, 2)
            win.blit(ASTEROID, (temp_obj_pos[0], temp_obj_pos[1]))

        for obj in objects[:]:
            obj.draw()
            obj.move()
            off_screen = obj.x < 0 or obj.x > WIDTH or obj.y < 0 or obj.y > HEIGHT
            if off_screen:
                objects.remove(obj)

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
