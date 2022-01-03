from curses import noraw
import taichi as ti
from ..Types import HittableObject, HittableObjectDefaults, HittableObjectType, HitResult, MaterialType, Vec3f


# Ellipse = make_object_constructor(
#     HittableObjectType.ELLIPSE,
#     HittableObject,
#     HittableObjectDefaults,
# )


def Ellipse(*, normal, up=Vec3f(0, 1, 0), **kwargs):
    v = -normal.cross(normal.cross(up.normalized())).normalized()
    w = normal.normalized()
    u = v.cross(w)

    return HittableObject(
        **{
            **HittableObjectDefaults,
            **kwargs,
            **dict(
                type=HittableObjectType.ELLIPSE,
                normal=normal,
                u=u,
                v=v,
                w=w,
            )
        },
    )


@ti.func
def hit(circle, ray, t_min=0.001, t_max=10e8):
    did_hit = False
    root = 0.
    hit_point = ti.Vector([0., 0., 0.])
    hit_point_normal = circle.normal
    front_face = False
    material = circle.material

    denominator = ray.direction.dot(circle.normal)
    if abs(denominator) > t_min:
        root = (
            (circle.center - ray.origin).dot(circle.normal)
            / denominator
        )
        if t_min <= root <= t_max:
            hit_point_tmp = ray.at(root)
            dist = (hit_point_tmp - circle.center).norm()
            if dist < circle.radius:
                did_hit = True
                hit_point = hit_point_tmp

                if circle.radius - dist < 0.03:
                    material = MaterialType.DIFFUSE

    if did_hit:
        if denominator < 0:
            front_face = True
        else:
            hit_point_normal = -hit_point_normal

    return HitResult(
        did_hit=did_hit,
        root=root,
        color=circle.color,
        hit_point=hit_point,
        hit_point_normal=hit_point_normal,
        front_face=front_face,
        material=material,
        id=-1,
    )
