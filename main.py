import math
import random as rd

import pygame

pygame.init()

WIDTH, HEIGHT = 1920, 1200
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gravitational Slingshot Effect Simulation")

# Constants
G = 6 * 10**-5
FPS = 60
VEL_SCALE = 100
ASTEROID_RADIUS = rd.randint(10, 20)

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
        self.PLANET = pygame.transform.scale(
            pygame.image.load(self.PLANET_NAME + ".png"),
            (self.PLANET_RADIUS * 2, self.PLANET_RADIUS * 2),
        )
        self.MAX_ASTEROIDS = rd.randint(50, 100)

    def draw(self):
        win.blit(
            self.PLANET, (self.x - self.PLANET_RADIUS, self.y - self.PLANET_RADIUS)
        )

    def simulate(self, MAX_ASTEROID_MASS, MIN_ASTEROID_VEL, MAX_ASTEROID_VEL):
        running = True
        clock = pygame.time.Clock()

        planet = Planet(
            WIDTH // 2, HEIGHT // 2, self.MASS, self.PLANET_NAME, self.PLANET_RADIUS
        )
        objects = []
        done_adding_asteroids = False

        while running:
            clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                while not done_adding_asteroids:
                    for i in range(1, self.MAX_ASTEROIDS):
                        obj = Asteroid(MAX_ASTEROID_MASS)
                        obj.set_velocity(MIN_ASTEROID_VEL, MAX_ASTEROID_VEL)
                        objects.append(obj)
                    done_adding_asteroids = True

            win.blit(BG, (0, 0))

            for obj in objects[:]:
                obj.draw()
                obj.move(planet)
                off_screen = obj.x < 0 or obj.x > WIDTH or obj.y < 0 or obj.y > HEIGHT
                collided = (
                    math.sqrt((obj.x - planet.x) ** 2 + (obj.y - planet.y) ** 2)
                    <= self.PLANET_RADIUS
                )
                if off_screen or collided:
                    objects.remove(obj)

            planet.draw()

            pygame.display.update()

        pygame.quit()


class Asteroid:
    def __init__(self, MAX_MASS):
        self.x = rd.randint(0, WIDTH)
        self.y = rd.randint(0, HEIGHT)
        self.MASS = rd.randint(1, MAX_MASS)

    def set_velocity(self, min_vel, max_vel):
        self.vel_x = rd.randint(min_vel, max_vel)
        self.vel_x /= VEL_SCALE
        self.vel_y = rd.randint(min_vel, max_vel)
        self.vel_y /= VEL_SCALE

    def move(self, planet):
        distance = math.sqrt((self.x - planet.x) ** 2 + (self.y - planet.y) ** 2)

        force = (G * self.MASS * planet.MASS) / distance**2
        acceleration = force / self.MASS
        angle = math.atan2(planet.y - self.y, planet.x - self.x)

        acceleration_x = acceleration * math.cos(angle)
        acceleration_y = acceleration * math.sin(angle)

        self.vel_x += acceleration_x
        self.vel_y += acceleration_y

        self.x += self.vel_x
        self.y += self.vel_y

    def draw(self):
        win.blit(ASTEROID, (int(self.x), int(self.y)))


def jupiter():
    MAX_ASTEROID_MASS = 6
    MIN_ASTEROID_VEL = -100
    MAX_ASTEROID_VEL = 100
    PLANET_MASS = 100
    PLANET_RADIUS = 70
    planet = Planet(WIDTH // 2, HEIGHT // 2, PLANET_MASS, "jupiter", PLANET_RADIUS)
    planet.simulate(MAX_ASTEROID_MASS, MIN_ASTEROID_VEL, MAX_ASTEROID_VEL)


def main():
    jupiter()


if __name__ == "__main__":
    main()
