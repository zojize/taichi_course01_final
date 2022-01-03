from re import A
import taichi as ti


@ti.data_oriented
class Ray:
    def __init__(self, origin, direction) -> None:
        self.origin = origin
        self.direction = direction

    @ti.func
    def at(self, t):
        return self.origin + t * self.direction
