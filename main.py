import pygame, random, math

from settings import *
from colors import *

# PyGame Setup
pygame.init()

if FULLSCREEN:
    SCREEN = pygame.display.set_mode(RESOLUTION, pygame.FULLSCREEN)
else:
    SCREEN = pygame.display.set_mode(RESOLUTION)

pygame.display.set_caption(WINDOW_NAME)
clock = pygame.time.Clock()
delta_time = 0

tracing_limit = 2000

G = 1
time_step = 1

bodies = []


class Vector2:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def get_tup(self):
        return self.x, self.y

    def zero():
        return Vector2(0, 0)

    def one():
        return Vector2(1, 1)

    def up():
        return Vector2(0, 1)

    def down():
        return Vector2(0, -1)

    def right():
        return Vector2(1, 0)

    def left():
        return Vector2(-1, 0)

    def random(self, max_value=1):
        vector = Vector2(random.random() * 2 - 1, random.random() * 2 - 1).normalize()
        return Vector2(vector.x * max_value, vector.y * max_value)

    def magnitude(self, vector=None):
        """
        Don't pass in anything to get magnitude existing vector.
        """
        try:
            if vector == None:
                return math.sqrt(self.x**2 + self.y**2)
            else:
                return math.sqrt(vector.x**2 + vector.y**2)
        except ZeroDivisionError:
            print("Zero Division Error at magnitude function, Vector2")
            return 0

    def normalize(self, vector=None):
        """
        Don't pass in anything to normalize existing vector.
        """
        try:
            if vector == None:
                magnitude = math.sqrt(self.x**2 + self.y**2)
                return Vector2(self.x / magnitude, self.y / magnitude)
            else:
                magnitude = math.sqrt(vector.x**2 + vector.y**2)
                return Vector2(vector.x / magnitude, vector.y / magnitude)
        except ZeroDivisionError:
            print(
                f"Zero Division Error at normalize function, Vector2. Vector input: {vector}, current vector: {self.x, self.y}"
            )
            return Vector2.zero()


class CelestialBody:
    def __init__(
        self,
        start_pos=Vector2.zero(),
        mass=1,
        radius=50,
        initial_vel=Vector2.zero(),
        color=WHITE,
        tracable=False,
    ) -> None:
        self.position = start_pos
        self.mass = mass
        self.radius = radius
        self.velocity = initial_vel
        self.color = color

        self.tracable = tracable
        self.tracing = []

    def update_vel(self, bodies):
        for i in range(len(bodies)):
            if i != self:
                sqr_dst = (
                    Vector2(
                        (bodies[i].position.x - self.position.x),
                        (bodies[i].position.y - self.position.y),
                    ).magnitude()
                    ** 2
                )

                force_dir = Vector2(
                    (bodies[i].position.x - self.position.x),
                    (bodies[i].position.y - self.position.y),
                ).normalize()

                try:
                    force = Vector2(
                        (force_dir.x * G * self.mass * bodies[i].mass) / sqr_dst,
                        (force_dir.y * G * self.mass * bodies[i].mass) / sqr_dst,
                    )
                except ZeroDivisionError:
                    force = Vector2(
                        force_dir.x * G * self.mass * bodies[i].mass,
                        force_dir.y * G * self.mass * bodies[i].mass,
                    )

                acceleration = Vector2(force.x / self.mass, force.y / self.mass)

                self.velocity.x += acceleration.x * time_step
                self.velocity.y += acceleration.y * time_step

    def update_pos(self):
        self.position.x += self.velocity.x
        self.position.y += self.velocity.y

    def draw(self):
        pygame.draw.circle(
            SCREEN,
            self.color,
            (
                self.position.x + WIDTH // 2,
                -self.position.y + HEIGHT // 2,
            ),
            self.radius,
        )


def create_body(
    start_pos=Vector2.zero(),
    mass=1,
    radius=50,
    initial_vel=Vector2.zero(),
    color=WHITE,
    tracable=False,
):
    b = CelestialBody(start_pos, mass, radius, initial_vel, color, tracable)
    bodies.append(b)

    return b


def n_body_simulation():
    for i in range(len(bodies)):
        bodies[i].update_vel(bodies)

    for i in range(len(bodies)):
        bodies[i].update_pos()

    for i in range(len(bodies)):
        if bodies[i].tracable:
            bodies[i].tracing.append(
                (bodies[i].position.x + WIDTH // 2, -bodies[i].position.y + HEIGHT // 2)
            )


def draw():
    SCREEN.fill(BLACK)

    for i in range(len(bodies)):

        if bodies[i].tracable:

            length_tracing = len(bodies[i].tracing)

            if length_tracing > tracing_limit:
                bodies[i].tracing.pop(0)

            length_tracing = len(bodies[i].tracing)

            for j in range(length_tracing - 1):

                if j < length_tracing:

                    pygame.draw.line(
                        SCREEN,
                        WHITE,
                        bodies[i].tracing[j],
                        bodies[i].tracing[j + 1],
                        width=2,
                    )

        bodies[i].draw()

    pygame.display.flip()


def main():
    global delta_time

    running = True
    get_ticks_last_frame = 0.0

    sun = create_body(Vector2(0, 0), 100000, 50, Vector2(0, 0), YELLOW, False)
    earth = create_body(Vector2(-500, 0), 10, 25, Vector2(0, -13), CYAN, True)

    # black_hole = create_body(Vector2(0, 0), 2500000, 25, Vector2.zero(), BLACK, False)
    # particle = create_body(Vector2(-250, 0), 0.01, 5, Vector2(0, -100), CYAN, False)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        n_body_simulation()

        draw()
        clock.tick(FPS)

        t = pygame.time.get_ticks()
        delta_time = (1 - get_ticks_last_frame) / 1000.0
        get_ticks_last_frame = t

    pygame.quit()


if __name__ == "__main__":
    main()
