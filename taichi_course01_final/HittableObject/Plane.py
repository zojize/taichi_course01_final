import taichi as ti
from ..Types import HittableObject, HittableObjectDefaults, HittableObjectType, HitResult, HittableObjectBase, extends, Vec3f, make_object_constructor


Plane = make_object_constructor(
    HittableObjectType.PLANE,
    HittableObject,
    HittableObjectDefaults,
)


@ti.func
def hit(plane, ray, t_min=0.001, t_max=10e8):
    did_hit = False
    root = 0.
    hit_point = ti.Vector([0., 0., 0.])
    hit_point_normal = plane.normal
    front_face = False

    denominator = ray.direction.dot(plane.normal)
    if abs(denominator) > t_min:
        root = (
            (plane.center - ray.origin).dot(plane.normal)
            / denominator
        )
        if t_min <= root <= t_max:
            did_hit = True

    if did_hit:
        hit_point = ray.at(root)
        if denominator < 0:
            front_face = True
        else:
            hit_point_normal = -hit_point_normal

    return HitResult(
        did_hit=did_hit,
        root=root,
        color=plane.color,
        hit_point=hit_point,
        hit_point_normal=hit_point_normal,
        front_face=front_face,
        material=plane.material,
        id=-1,
    )
