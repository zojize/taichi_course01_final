import taichi as ti
from ..Types import HittableObjectType, HitResult, make_object_constructor, HittableObject, HittableObjectDefaults


Sphere = make_object_constructor(
    HittableObjectType.SPHERE,
    HittableObject,
    HittableObjectDefaults,
)


@ti.func
def hit(sphere, ray, t_min=0.001, t_max=10e8):
    oc = ray.origin - sphere.center
    a = ray.direction.dot(ray.direction)
    b = 2 * ray.direction.dot(oc)
    c = oc.dot(oc) - sphere.radius * sphere.radius

    root = 0.
    discriminant = (b * b) - (4 * a * c)
    did_hit = False
    hit_point = ti.Vector([0., 0., 0.])
    hit_point_normal = ti.Vector([0., 0., 0.])
    front_face = False

    if discriminant > 0:
        discriminant_sqrt = ti.sqrt(discriminant)
        a2 = a * 2
        root = (-b - discriminant_sqrt) / a2
        if root < t_min or root > t_max:
            root = (-b + discriminant_sqrt) / a2
            if t_min <= root <= t_max:
                did_hit = True
        else:
            did_hit = True

    if did_hit:
        hit_point = ray.at(root)
        hit_point_normal = (hit_point - sphere.center) / sphere.radius
        # Check which side does the ray hit, we set the hit point normals always point outward from the surface
        if ray.direction.dot(hit_point_normal) < 0:
            front_face = True
        else:
            hit_point_normal = -hit_point_normal

    # return did_hit, root, self.color
    return HitResult(
        did_hit=did_hit,
        root=root,
        color=sphere.color,
        hit_point=hit_point,
        hit_point_normal=hit_point_normal,
        front_face=front_face,
        material=sphere.material,
        id=-1,
    )
