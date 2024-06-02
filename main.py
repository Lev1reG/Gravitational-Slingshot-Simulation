import math
import random as rd
import pygame

pygame.init()

WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gravitational Slingshot Effect Simulation")

# Constants
PLANET_MASS = 100
ASTEROID_MASS = 5
G = 5
FPS = 60
PLANET_RADIUS = 60
ASTEROID_RADIUS = 35
VEL_SCALE = 100

BG = pygame.transform.scale(pygame.image.load("background.jpg"), (WIDTH, HEIGHT))
ASTEROID = pygame.transform.scale(
    pygame.image.load("asteroid.png"), (ASTEROID_RADIUS, ASTEROID_RADIUS)
)

class Planet:
    def __init__(self, x, y, MASS, PLANET_NAME, PLANET_RADIUS):
        self.x = x
        self.y = y
        self.MASS = MASS
        self.PLANET_RADIUS = PLANET_RADIUS
        self.PLANET_NAME = PLANET_NAME
        self.PLANET = pygame.transform.scale(pygame.image.load(self.PLANET_NAME + ".png"), (self.PLANET_RADIUS * 2, self.PLANET_RADIUS * 2))

    def draw(self):
        win.blit(self.PLANET, (self.x - self.PLANET_RADIUS, self.y - self.PLANET_RADIUS))

    def simulate(self):
        running = True
        clock = pygame.time.Clock()

        planet = Planet(WIDTH // 2, HEIGHT // 2, self.MASS, self.PLANET_NAME, self.PLANET_RADIUS) 
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
                pygame.draw.line(win, (255, 255, 255), temp_obj_pos, mouse_pos, 2)
                win.blit(ASTEROID, (temp_obj_pos[0], temp_obj_pos[1]))

            for obj in objects[:]:
                obj.draw()
                obj.move(planet)
                off_screen = obj.x < 0 or obj.x > WIDTH or obj.y < 0 or obj.y > HEIGHT
                collided = math.sqrt((obj.x - planet.x)**2 + (obj.y - planet.y)**2) <= PLANET_RADIUS
                if off_screen or collided:
                    objects.remove(obj)

            planet.draw()

            pygame.display.update()

        pygame.quit()

class Asteroid:
    def __init__(self, x, y, vel_x, vel_y, mass):
        self.x = x
        self.y = y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.mass = mass

    def move(self, planet):
        distance = math.sqrt((self.x - planet.x)**2 + (self.y - planet.y)**2)

        force = (G * self.mass * planet.MASS) / distance**2
        acceleration = force / self.mass
        angle = math.atan2(planet.y - self.y, planet.x - self.x)

        acceleration_x = acceleration * math.cos(angle)
        acceleration_y = acceleration * math.sin(angle)

        self.vel_x += acceleration_x
        self.vel_y += acceleration_y

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
    planet = Planet(WIDTH // 2, HEIGHT // 2, PLANET_MASS, "jupiter", PLANET_RADIUS)
    planet.simulate()

if __name__ == "__main__":
    main()
