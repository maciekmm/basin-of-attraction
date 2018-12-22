# MOWNiT
# Zadanie zadano: 18.12.2018
# Prowadzący: prof. Monika Dekster
# Autor: Maciej Mionskowski
from PIL import Image
import numpy
import math

ITERATIONS = 1 << 32
PRECISION = 1e-7
DEFAULT_COLOR = [0, 0, 0]

roots = [
    (-1) ** (1 / 5),
    -((-1) ** (2 / 5)),
    (-1) ** (3 / 5),
    -(-1) ** (4 / 5),
    -1
]

colors = [
    [255, 0, 0],  # Red
    [0, 255, 0],  # Green
    [0, 255, 255],  # Blue
    [255, 255, 0],  # Yellow
    [255, 0, 255]  # Pink
]


def darken(color, fraction):
    return [p * (1 - fraction) for p in color]


def base_fun(z):
    return z ** 5 + 1


def derivative_fun(z):
    return 5 * z ** 4


def point_color(z):
    for i in range(ITERATIONS):
        # Newton
        der = derivative_fun(z)
        if der == 0:
            return DEFAULT_COLOR

        z -= base_fun(z) / der

        for root_id, root in enumerate(roots):
            diff = z - root

            if abs(diff.real) > PRECISION or abs(diff.imag) > PRECISION:
                continue

            # Found which attractor the point belongs to
            #
            color_intensity = max(min(i / (1 << 5), 0.95), 0)
            return darken(colors[root_id], color_intensity)
    return DEFAULT_COLOR


bounds_x = (-1.5, 1.5)
width = 1024
bounds_y = (-1.5, 1.5)
height = 1024


def normalize(bounds, perc):
    a = bounds[0]
    b = bounds[1]
    return (b - a) * perc + a


def pixel_color(x, y):
    # normalize
    real = normalize(bounds_x, x / width)
    ima = normalize(bounds_y, y / height)
    return point_color(real + ima * 1j)


data = numpy.zeros((height, width, 3), dtype=numpy.uint8)

for x in range(width):
    print(x / width)
    for y in range(height):
        data[y][x] = pixel_color(x, y)

image = Image.fromarray(numpy.asarray(data))
image.save("out"+str(width)+"-"+str(height)+".png")
