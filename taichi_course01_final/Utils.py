from math import pi
from typing import Union
import taichi as ti


@ti.func
def rand3():
    return ti.Vector([ti.random(), ti.random(), ti.random()])


@ti.func
def random_in_unit_sphere():
    p = 2.0 * rand3() - ti.Vector([1, 1, 1])
    while p.norm() >= 1.0:
        p = 2.0 * rand3() - ti.Vector([1, 1, 1])
    return p


@ti.func
def random_unit_vector():
    return random_in_unit_sphere().normalized()


@ti.func
def reflectance(cosine, ref_idx):
    # Use Schlick's approximation for reflectance.
    r0 = (1 - ref_idx) / (1 + ref_idx)
    r0 = r0 * r0
    return r0 + (1 - r0) * pow((1 - cosine), 5)


@ti.func
def reflect(v, normal):
    return v - 2 * v.dot(normal) * normal


@ti.func
def refract(uv, n, etai_over_etat):
    cos_theta = min(n.dot(-uv), 1.0)
    r_out_perp = etai_over_etat * (uv + cos_theta * n)
    r_out_parallel = -ti.sqrt(abs(1.0 - r_out_perp.dot(r_out_perp))) * n
    return r_out_perp + r_out_parallel


def from_hex(hex: Union[str, int]):
    if isinstance(hex, int):
        hex = f"{hex:0>6x}"
    if len(hex) in (4, 7):
        hex = hex[1:]
    if len(hex) == 3:
        hex = "".join(map("".join, zip(hex, hex)))
    return ti.Vector([int(hex[i:i + 2], 16) / 2**8 for i in (0, 2, 4)])


@ti.func
def dist_normal(mean=0, std=1):
    # TODO
    return ti.sqrt(-2.0 * ti.log(ti.randn())) * ti.cos(2 * pi * ti.randn())


@ti.func
def lerp(t, v0, v1):
    return (1 - t) * v0 + t * v1


@ti.func
def is_sorted(xs):
    sorted = True
    for i in xs:
        if i > 0 and xs[i - 1] > xs[i]:
            sorted = False
    return sorted


MAX_LEVELS = 64

beg = ti.field(dtype=ti.i32, shape=MAX_LEVELS)
end = ti.field(dtype=ti.i32, shape=MAX_LEVELS)


# https://stackoverflow.com/a/55011578/14835397
@ti.func
def quick_sort(xs):
    n = xs.shape[0]
    L = R = i = 0

    beg[0] = 0
    end[0] = n

    while i >= 0:
        L = beg[i]
        R = end[i]
        R -= 1
        if L < R:
            piv = xs[L]
            # if i == MAX_LEVELS - 1:
            #     return - 1
            while L < R:
                while xs[R] >= piv and L < R:
                    R -= 1
                if L < R:
                    xs[L] = xs[R]
                    L += 1
                while xs[L] <= piv and L < R:
                    L += 1
                if L < R:
                    xs[R] = xs[L]
                    R -= 1
            xs[L] = piv
            if L - beg[i] > end[i] - R:
                beg[i + 1] = L + 1
                end[i + 1] = end[i]
                end[i] = L
                i += 1
            else:
                beg[i + 1] = beg[i]
                end[i + 1] = L
                beg[i] = L + 1
                i += 1
        else:
            i -= 1

    return 0


@ti.func
def matrix_rotate_x(theta):
    cos_theta = ti.cos(theta)
    sin_theta = ti.sin(theta)
    return ti.Matrix([
        [1, 0, 0],
        [0, cos_theta, -sin_theta],
        [0, sin_theta, cos_theta],
    ])


@ti.func
def matrix_rotate_y(theta):
    cos_theta = ti.cos(theta)
    sin_theta = ti.sin(theta)
    return ti.Matrix([
        [cos_theta, 0, sin_theta],
        [0, 1, 0],
        [- sin_theta, 0, cos_theta],
    ])


@ti.func
def matrix_rotate_z(theta):
    cos_theta = ti.cos(theta)
    sin_theta = ti.sin(theta)
    return ti.Matrix([
        [cos_theta, -sin_theta, 0],
        [sin_theta, cos_theta, 0],
        [0, 0, 1],
    ])
