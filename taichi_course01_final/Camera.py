import taichi as ti
from math import degrees, radians, pi as PI
from taichi_course01_final.Ray import Ray


@ti.data_oriented
class Camera:
    _fov = radians(60)
    _aspect_ratio = 1.0

    def __init__(self, *,
                 #  look_from=[0.0, 1.0, -5.0], look_at=[0.0, 1.0, -1.0], up=[0.0, 1.0, 0.0],
                 fov=60, aspect_ratio=1.0):
        self._up = ti.Vector.field(3, dtype=ti.f32, shape=())
        self._look_from = ti.Vector.field(3, dtype=ti.f32, shape=())
        self._look_at = ti.Vector.field(3, dtype=ti.f32, shape=())
        self._cam_lower_left_corner = ti.Vector.field(3, dtype=ti.f32, shape=())
        self._cam_horizontal = ti.Vector.field(3, dtype=ti.f32, shape=())
        self._cam_vertical = ti.Vector.field(3, dtype=ti.f32, shape=())

        self.fov = fov
        self._aspect_ratio = aspect_ratio

        self.reset()

    @ti.kernel
    def reset(self):
        self._look_from[None] = [0.0, 1.0, -5.0]
        self._look_at[None] = [0.0, 1.0, 0.0]
        self._up[None] = [0.0, 1.0, 0.0]

        theta = self._fov
        half_height = ti.tan(theta / 2.0)
        half_width = half_height * self._aspect_ratio

        w = (self._look_from[None] - self._look_at[None]).normalized()
        u = (self._up[None].cross(w)).normalized()
        v = w.cross(u)

        self._cam_lower_left_corner[None] = (
            self._look_from[None]
            - (half_width * u)
            - (half_height * v)
            - w
        )

        self._cam_horizontal[None] = 2 * half_width * u
        self._cam_vertical[None] = 2 * half_height * v

    @ti.func
    def cast_ray(self, u, v) -> Ray:
        return Ray(
            origin=self._look_from[None],
            direction=(
                self._cam_lower_left_corner[None]
                + (u * self._aspect_ratio * self._cam_horizontal[None])
                + (v * self._cam_vertical[None])
                - self._look_from[None]
            )
        )

    @property
    def fov(self):
        return degrees(self._fov)

    @fov.setter
    def fov(self, fov):
        self._fov = radians(fov)
        self.reset()
