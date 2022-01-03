import taichi as ti


class HittableObjectType:
    NULL = 0
    SPHERE = 1
    PLANE = 2
    ELLIPSE = 3


class MaterialType:
    LIGHT = 0
    DIFFUSE = 1
    METAL = 2
    DIELECTRIC = 3
    FUZZY = 4
    PORTAL = 5


Vec3f = ti.types.vector(3, ti.f32)

HitResult = ti.types.struct(
    did_hit=ti.i32,
    root=ti.f32,
    color=Vec3f,
    hit_point=Vec3f,
    hit_point_normal=Vec3f,
    front_face=ti.i32,
    material=ti.i32,
    id=ti.i32,
)

HittableObjectBase = ti.types.struct(
    type=ti.i32,
    material=ti.i32,
    color=Vec3f,
)


def extends(base, **extra_fields):
    return ti.types.struct(
        **{
            **(base if isinstance(base, dict) else base.members),
            **extra_fields,
        }
    )


def make_object_constructor(type, struct, defaults={}):
    return lambda **kwargs: struct(
        **{
            **defaults,
            **kwargs,
            "type": type,
        },
    )


HittableObject = extends(
    HittableObjectBase,
    center=Vec3f,
    radius=ti.f32,
    normal=Vec3f,
    portal_id=ti.i32,
    theta=ti.f32,
    u=Vec3f,
    v=Vec3f,
    w=Vec3f,
    width=ti.f32,
    height=ti.f32,
)

HittableObjectDefaults = dict(
    type=-1,
    material=-1,
    color=Vec3f(0),
    center=Vec3f(0),
    radius=0,
    normal=Vec3f(0),
    portal_id=-1,
    theta=0,
    u=Vec3f(1, 0, 0),
    v=Vec3f(0, 1, 0),
    w=Vec3f(0, 0, 1),
    width=0,
    height=0,
)
