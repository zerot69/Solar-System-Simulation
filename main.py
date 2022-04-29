# ===========================================
# - Title:  Solar System Simulation
# - Author: @zerot69
# - Date:   27 Apr 2022
# ============================================

import pygame
import math

pygame.init()
WIDTH, HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
WINDOW = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
COLOR_WHITE = (255, 255, 255)
COLOR_UNIVERSE = (36, 36, 36)
COLOR_SUN = (252, 150, 1)
COLOR_MERCURY = (173, 168, 165)
COLOR_VENUS = (227, 158, 28)
COLOR_EARTH = (107, 147, 214)
COLOR_MARS = (193, 68, 14)
COLOR_JUPITER = (216, 202, 157)
COLOR_SATURN = (191, 189, 175)
COLOR_URANUS = (209, 231, 231)
COLOR_NEPTUNE = (63, 84, 186)
FONT_1 = pygame.font.SysFont("Trebuchet MS", 21)
FONT_2 = pygame.font.SysFont("Trebuchet MS", 16)
pygame.display.set_caption("Solar System Simulation")


class Planet:
    AU = 149.6e6 * 1000  # Astronomical unit
    G = 6.67428e-11  # Gravitational constant
    TIMESTEP = 60 * 60 * 24 * 2  # Seconds in 2 days
    SCALE = 200 / AU

    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass
        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0
        self.x_vel = 0
        self.y_vel = 0

    def draw(self, window, show, move_x, move_y, draw_line):
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2
        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                updated_points.append((x + move_x, y + move_y))
            if draw_line:
                pygame.draw.lines(window, self.color, False, updated_points, 1)
        pygame.draw.circle(window, self.color, (x + move_x, y + move_y), self.radius)
        if not self.sun:
            distance_text = FONT_2.render(f"{round(self.distance_to_sun * 1.057 * 10 ** -16, 8)} light years", True,
                                          COLOR_WHITE)
            if show:
                window.blit(distance_text, (x - distance_text.get_width() / 2 + move_x,
                                            y - distance_text.get_height() / 2 - 20 + move_y))

    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)
        if other.sun:
            self.distance_to_sun = distance
        force = self.G * self.mass * other.mass / distance ** 2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y

    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue
            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy
        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP
        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))

    def update_scale(self, scale):
        self.radius *= scale


def main():
    run = True
    pause = False
    show_distance = False
    clock = pygame.time.Clock()
    move_x = 0
    move_y = 0
    draw_line = True

    # Metric from: https://nssdc.gsfc.nasa.gov/planetary/factsheet/

    sun = Planet(0, 0, 30 * Planet.SCALE * 10 ** 9, COLOR_SUN, 1.98892 * 10 ** 30)
    sun.sun = True

    mercury = Planet(-0.387 * Planet.AU, 0, 5 * Planet.SCALE * 10 ** 9, COLOR_MERCURY, 3.30 * 10 ** 23)
    mercury.y_vel = 47.4 * 1000

    venus = Planet(-0.723 * Planet.AU, 0, 9 * Planet.SCALE * 10 ** 9, COLOR_VENUS, 4.8685 * 10 ** 24)
    venus.y_vel = 35.02 * 1000

    earth = Planet(-1 * Planet.AU, 0, 10 * Planet.SCALE * 10 ** 9, COLOR_EARTH, 5.9722 * 10 ** 24)
    earth.y_vel = 29.783 * 1000

    mars = Planet(-1.524 * Planet.AU, 0, 5 * Planet.SCALE * 10 ** 9, COLOR_MARS, 6.39 * 10 ** 23)
    mars.y_vel = 24.077 * 1000

    jupiter = Planet(-5.204 * Planet.AU, 0, 20 * Planet.SCALE * 10 ** 9, COLOR_JUPITER, 1.898 * 10 ** 27)
    jupiter.y_vel = 13.06 * 1000

    saturn = Planet(-9.573 * Planet.AU, 0, 18 * Planet.SCALE * 10 ** 9, COLOR_SATURN, 5.683 * 10 ** 26)
    saturn.y_vel = 9.68 * 1000

    uranus = Planet(-19.165 * Planet.AU, 0, 14 * Planet.SCALE * 10 ** 9, COLOR_URANUS, 8.681 * 10 ** 25)
    uranus.y_vel = 6.80 * 1000

    neptune = Planet(-30.178 * Planet.AU, 0, 12 * Planet.SCALE * 10 ** 9, COLOR_NEPTUNE, 1.024 * 10 ** 26)
    neptune.y_vel = 5.43 * 1000

    planets = [neptune, uranus, saturn, jupiter, mars, earth, venus, mercury, sun]

    while run:
        clock.tick(60)
        WINDOW.fill(COLOR_UNIVERSE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and
                                             (event.key == pygame.K_x or event.key == pygame.K_ESCAPE)):
                run = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                pause = not pause
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                show_distance = not show_distance
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_c:
                move_x, move_y = -sun.x * sun.SCALE, -sun.y * sun.SCALE
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                draw_line = not draw_line
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
                Planet.SCALE *= 0.75
                for planet in planets:
                    planet.update_scale(0.75)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
                Planet.SCALE *= 1.25
                for planet in planets:
                    planet.update_scale(1.25)

        keys = pygame.key.get_pressed()
        mouse_x, mouse_y = pygame.mouse.get_pos()
        window_w, window_h = pygame.display.get_surface().get_size()
        distance = 10
        if keys[pygame.K_LEFT] or mouse_x == 0:
            move_x += distance
        if keys[pygame.K_RIGHT] or mouse_x == window_w - 1:
            move_x -= distance
        if keys[pygame.K_UP] or mouse_y == 0:
            move_y += distance
        if keys[pygame.K_DOWN] or mouse_y == window_h - 1:
            move_y -= distance

        for planet in planets:
            if not pause:
                planet.update_position(planets)
            if show_distance:
                planet.draw(WINDOW, 1, move_x, move_y, draw_line)
            else:
                planet.draw(WINDOW, 0, move_x, move_y, draw_line)

        fps_text = FONT_1.render("FPS: " + str(int(clock.get_fps())), True, COLOR_WHITE)
        WINDOW.blit(fps_text, (15, 15))
        text_surface = FONT_1.render("Press X or ESC to exit", True, COLOR_WHITE)
        WINDOW.blit(text_surface, (15, 45))
        text_surface = FONT_1.render("Press D to turn on/off distance", True, COLOR_WHITE)
        WINDOW.blit(text_surface, (15, 75))
        text_surface = FONT_1.render("Press S to turn on/off drawing orbit lines", True, COLOR_WHITE)
        WINDOW.blit(text_surface, (15, 105))
        text_surface = FONT_1.render("Use mouse or arrow keys to move around", True, COLOR_WHITE)
        WINDOW.blit(text_surface, (15, 135))
        text_surface = FONT_1.render("Press C to center", True, COLOR_WHITE)
        WINDOW.blit(text_surface, (15, 165))
        text_surface = FONT_1.render("Press Space to pause/unpause", True, COLOR_WHITE)
        WINDOW.blit(text_surface, (15, 195))
        text_surface = FONT_1.render("Use scroll-wheel to zoom", True, COLOR_WHITE)
        WINDOW.blit(text_surface, (15, 225))
        sun_surface = FONT_1.render("- Sun", True, COLOR_SUN)
        WINDOW.blit(sun_surface, (15, 285))
        mercury_surface = FONT_1.render("- Mercury", True, COLOR_MERCURY)
        WINDOW.blit(mercury_surface, (15, 315))
        venus_surface = FONT_1.render("- Venus", True, COLOR_VENUS)
        WINDOW.blit(venus_surface, (15, 345))
        earth_surface = FONT_1.render("- Earth", True, COLOR_EARTH)
        WINDOW.blit(earth_surface, (15, 375))
        mars_surface = FONT_1.render("- Mars", True, COLOR_MARS)
        WINDOW.blit(mars_surface, (15, 405))
        jupiter_surface = FONT_1.render("- Jupiter", True, COLOR_JUPITER)
        WINDOW.blit(jupiter_surface, (15, 435))
        saturn_surface = FONT_1.render("- Saturn", True, COLOR_SATURN)
        WINDOW.blit(saturn_surface, (15, 465))
        uranus_surface = FONT_1.render("- Uranus", True, COLOR_URANUS)
        WINDOW.blit(uranus_surface, (15, 495))
        neptune_surface = FONT_1.render("- Neptune", True, COLOR_NEPTUNE)
        WINDOW.blit(neptune_surface, (15, 525))

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
