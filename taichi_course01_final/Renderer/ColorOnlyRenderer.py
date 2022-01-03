import taichi as ti
import numpy as np

from taichi_course01_final.Types import MaterialType
from taichi_course01_final.Utils import random_unit_vector, reflect, reflectance, refract
from taichi_course01_final.Ray import Ray

MAX_DEPTH = 10
MIN_DEPTH = 2


@ti.data_oriented
class ColorOnlyRenderer:
    def __init__(self, width, height, *, samples_per_pixel=4, title=""):
        self.width = width
        self.height = height
        self.samples_per_pixel = samples_per_pixel

        self.canvas = ti.Vector.field(3, dtype=ti.f32, shape=(width, height))

        self.gui = ti.GUI(title, res=(self.width, self.height))

    @ti.kernel
    def render(self, camera: ti.template(), scene: ti.template(), cnt: ti.i32):
        canvas, width, height, samples_per_pixel = ti.static(
            self.canvas, self.width, self.height, self.samples_per_pixel)
        for i, j in canvas:
            u = (i + ti.random()) / width
            v = (j + ti.random()) / height
            color = ti.Vector([0.0, 0.0, 0.0])
            for _ in range(samples_per_pixel):
                ray = camera.cast_ray(u, v)
                color += self.ray_color(ray, scene)
            color /= samples_per_pixel
            canvas[i, j] += color

    def show(self, camera, scene):
        self._cnt = 0
        while self.gui.running:
            self.render(camera, scene, self._cnt)
            self._cnt += 1
            self.gui.set_image(np.sqrt(self.canvas.to_numpy() / self._cnt))
            self.gui.show()

    @ti.func
    def ray_color(self, ray, scene):
        res = scene.hit(ray)
        color = ti.Vector([0.0, 0.0, 0.0])

        if res.did_hit:
            color = res.color

        return color
