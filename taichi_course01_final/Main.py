# make sure taichi is initiated before anything is imported
from zoneinfo import available_timezones
import taichi as ti
from taichi_course01_final.HittableObject.Ellipse import Ellipse  # noqa
ti.init(arch=ti.gpu)  # noqa

# TODO: per-file-ignores don't seem to work
from taichi_course01_final.Utils import from_hex
from taichi_course01_final.Types import HittableObjectType, MaterialType, Vec3f
from taichi_course01_final.HittableObject.Plane import Plane
from taichi_course01_final.HittableObject.Sphere import Sphere
from taichi_course01_final.Scene import Scene
from taichi_course01_final.Renderer import PathTracerRenderer, ColorOnlyRenderer
from taichi_course01_final.Camera import Camera


def main():

    aspect_ratio = 1.0
    image_width = 800
    image_height = int(image_width / aspect_ratio)

    camera = Camera(aspect_ratio=aspect_ratio)
    scene = Scene()

    # Light source
    scene.add(Sphere(center=Vec3f(0, 5.4, -1), radius=3.0, material=MaterialType.LIGHT, color=ti.Vector([10.0, 10.0, 10.0])))
    # Ground
    scene.add(Plane(center=Vec3f(0.0, -0.5, 0.0), normal=Vec3f(0.0, -1.0, 0.0), material=MaterialType.DIFFUSE, color=from_hex(0xcccccc)))
    # scene.add(Sphere(center=Vec3f(0, -100.5, -1), radius=100.0, material=1, color=Vec3f(0.8, 0.8, 0.8)))
    # ceiling
    scene.add(Plane(center=Vec3f(0.0, 2.5, -1), normal=Vec3f(0.0, 1.0, 0.0), material=MaterialType.DIFFUSE, color=from_hex(0xffd0da)))
    # scene.add(Sphere(center=Vec3f(0, 102.5, -1), radius=100.0, material=MaterialType.DIFFUSE, color=from_hex(0xffd0da)))
    # back wall
    scene.add(Plane(center=Vec3f(0.0, 0.0, 2.5), normal=Vec3f(0.0, 0.0, 1.0), material=MaterialType.DIFFUSE, color=from_hex(0xeeee00)))
    # behind camera wall
    scene.add(Plane(center=Vec3f(0.0, 0.0, -5), normal=Vec3f(0.0, 0.0, 1.0), material=MaterialType.METAL, color=from_hex(0xeeee00)))
    # scene.add(Sphere(center=Vec3f(0, 1, 101), radius=100.0, material=MaterialType.DIFFUSE, color=Vec3f(0.8, 0.8, 0.8)))
    # right wall
    scene.add(Plane(center=Vec3f(-1.5, 2.5, -1), normal=Vec3f(1.0, 0.0, 0.0), material=MaterialType.DIFFUSE, color=from_hex(0xcc0000)))
    # scene.add(Sphere(center=Vec3f(-101.5, 0, -1), radius=100.0, material=MaterialType.DIFFUSE, color=Vec3f(0.6, 0.0, 0.0)))
    # left wall
    scene.add(Plane(center=Vec3f(1.5, 2.5, -1), normal=Vec3f(-1.0, 0.0, 0.0), material=MaterialType.DIFFUSE, color=from_hex(0x00cc00)))
    # scene.add(Sphere(center=Vec3f(101.5, 0, -1), radius=100.0, material=MaterialType.DIFFUSE, color=Vec3f(0.0, 0.6, 0.0)))

    # Diffuse ball
    scene.add(Sphere(center=Vec3f(0, -0.2, -1.5), radius=0.3, material=MaterialType.DIFFUSE, color=from_hex(0xcc4c4c)))
    # Metal ball
    scene.add(Sphere(center=Vec3f(-0.8, 0.2, -1), radius=0.7, material=MaterialType.METAL, color=from_hex(0x99cccc)))
    # Glass ball
    scene.add(Sphere(center=Vec3f(0.7, 0, -0.5), radius=0.5, material=MaterialType.DIELECTRIC, color=from_hex(0xffffff)))
    # Metal ball-2
    scene.add(Sphere(center=Vec3f(0.6, -0.3, -2.0), radius=0.2, material=MaterialType.FUZZY, color=from_hex(0xcc9933)))

    scene.add(Ellipse(center=Vec3f(0.0, .5, .3), radius=0.3, normal=Vec3f(0.0, 0.0, -1.0), material=MaterialType.PORTAL, color=from_hex(0xcc0000)))
    scene.add(Ellipse(center=Vec3f(1.3, 1., -.8), radius=0.3, normal=Vec3f(-1.0, -0.5, 0.0).normalized(), material=MaterialType.PORTAL, color=from_hex(0xcc0000)))

    # for i in range(scene._obj_count):
    # print(scene.objects)

    renderer = PathTracerRenderer(image_width, image_height, title="Ray Tracing")
    # renderer = ColorOnlyRenderer(image_width, image_height, title="Color Only")
    renderer.show(camera, scene)


def test():
    print("some test")
    ...
