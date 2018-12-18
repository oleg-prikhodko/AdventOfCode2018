import re
from collections import namedtuple
from PIL import Image
import numpy as np

from day_2 import load_strings

Position = namedtuple("Position", "x y")
Velocity = namedtuple("Velocity", "x y")

particle_pattern = re.compile(r"position=<(.+), (.+)> velocity=<(.+), (.+)>")


class BBox:
    def __init__(self, x_min, y_min, x_max, y_max):
        self.x_min = x_min
        self.y_min = y_min
        self.x_max = x_max
        self.y_max = y_max

    def get_size(self):
        width = abs(self.x_max) + abs(self.x_min)
        height = abs(self.y_min) + abs(self.y_max)
        return width, height


class Particle:
    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity

    def step(self):
        self.position = Position(
            self.position.x + self.velocity.x,
            self.position.y + self.velocity.y,
        )

    def __repr__(self):
        return f"Particle<{self.position}, {self.velocity}>"


def load_particle_data(lines):
    particles = []
    for line in lines:
        match = re.search(particle_pattern, line)
        pos = Position(int(match.group(1)), int(match.group(2)))
        vel = Velocity(int(match.group(3)), int(match.group(4)))
        particles.append(Particle(pos, vel))

    return particles


def get_bounding_box(particles):
    get_pos_x = lambda particle: particle.position.x
    get_pos_y = lambda particle: particle.position.y
    x_min = min(particles, key=get_pos_x).position.x
    x_max = max(particles, key=get_pos_x).position.x
    y_min = min(particles, key=get_pos_y).position.y
    y_max = max(particles, key=get_pos_y).position.y
    return BBox(x_min, y_min, x_max, y_max)


def run(particles, outfilename="out.txt"):
    timer = 0
    # with open(outfilename, "at") as out_file:
    while timer < 20000:
        bbox = get_bounding_box(particles)

        if bbox.get_size()[0] <= 413:
            arr = particles_to_array(
                offset_particles(particles, bbox), bbox.get_size()
            )
            image_from_array(arr, f"out_{timer}")
        # out_file.write(f"{bbox.get_size()}\n")
        for particle in particles:
            particle.step()

        timer += 1


def how_many_lines(lines):
    interesting_lines = [line for line in lines if eval(line)[0] <= 413]
    print(len(interesting_lines))


def offset_particles(particles, bbox):
    offset_x = abs(bbox.x_min)
    offset_y = abs(bbox.y_min)
    return [
        Particle(
            Position(
                particle.position.x + offset_x, particle.position.y + offset_y
            ),
            particle.velocity,
        )
        for particle in particles
    ]


def particles_to_array(particles_transformed, size):
    size = size[0] + 1, size[1] + 1
    arr = np.zeros(size, dtype=np.uint8)
    for particle in particles_transformed:
        arr[particle.position.x, particle.position.y] = 255
    return arr


def image_from_array(arr, filename):
    # arr = np.random.randint(0, 255, (100, 100), np.uint8)
    img = Image.fromarray(arr)
    img.save(f"out/{filename}.jpg", format="JPEG")


if __name__ == "__main__":
    lines = load_strings(filename="input_10.txt")
    particles = load_particle_data(lines)
    run(particles)
    # how_many_lines(load_strings("out.txt"))
    # image_from_array()
