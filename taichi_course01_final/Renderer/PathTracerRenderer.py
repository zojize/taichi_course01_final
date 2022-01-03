import taichi as ti
import numpy as np

from taichi_course01_final.Types import HittableObjectType, MaterialType
from taichi_course01_final.Utils import random_unit_vector, reflect, reflectance, refract
from taichi_course01_final.Ray import Ray

MAX_DEPTH = 10
# MIN_DEPTH = 2


@ti.data_oriented
class PathTracerRenderer:
    def __init__(self, width, height, *, samples_per_pixel=36, title=""):
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
        color = ti.Vector([0.0, 0.0, 0.0])
        brightness = ti.Vector([1.0, 1.0, 1.0])
        scattered_origin = ray.origin
        scattered_direction = ray.direction
        p_RR = 0.80

        for i in range(MAX_DEPTH):
            if ti.random() > p_RR:
                break
            res = scene.hit(
                Ray(scattered_origin, scattered_direction))
            if not res.did_hit:
                break
            if res.material == MaterialType.LIGHT:
                color = res.color * brightness

            else:
                obj = scene.objects[res.id]

                # if hit portal
                if (
                    res.material == MaterialType.PORTAL
                    and obj.type == HittableObjectType.ELLIPSE
                    # and res.front_face
                ):
                    to_obj = scene.objects[obj.portal_id]
                    vec = obj.center - res.hit_point
                    x = vec.dot(obj.u)
                    y = vec.dot(obj.v)
                    scattered_origin = to_obj.center + x * to_obj.u + y * to_obj.v
                    scattered_direction = to_obj.normal
                # Diffuse
                elif res.material == MaterialType.DIFFUSE or res.material == MaterialType.PORTAL:
                    target = res.hit_point + res.hit_point_normal
                    target += random_unit_vector()
                    scattered_direction = target - res.hit_point
                    scattered_origin = res.hit_point
                    brightness *= res.color
                # Metal and Fuzz Metal
                elif res.material == MaterialType.METAL or res.material == MaterialType.FUZZY:
                    fuzz = 0.0
                    if res.material == 4:
                        fuzz = 0.4
                    scattered_direction = reflect(scattered_direction.normalized(),
                                                  res.hit_point_normal)
                    scattered_direction += fuzz * random_unit_vector()
                    scattered_origin = res.hit_point
                    if scattered_direction.dot(res.hit_point_normal) < 0:
                        break
                    else:
                        brightness *= res.color
                # Dielectric
                elif res.material == MaterialType.DIELECTRIC:
                    refraction_ratio = 1.5
                    if res.front_face:
                        refraction_ratio = 1 / refraction_ratio
                    cos_theta = min(-scattered_direction.normalized().dot(res.hit_point_normal), 1.0)
                    sin_theta = ti.sqrt(1 - cos_theta * cos_theta)
                    # total internal reflection
                    if refraction_ratio * sin_theta > 1.0 or reflectance(cos_theta, refraction_ratio) > ti.random():
                        scattered_direction = reflect(scattered_direction.normalized(), res.hit_point_normal)
                    else:
                        scattered_direction = refract(
                            scattered_direction.normalized(),
                            res.hit_point_normal, refraction_ratio)
                    scattered_origin = res.hit_point
                    brightness *= res.color
                brightness /= p_RR
        return color
