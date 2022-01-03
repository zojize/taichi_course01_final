import taichi as ti

from taichi_course01_final.Types import HitResult, HittableObject, HittableObjectType, MaterialType
import taichi_course01_final.HittableObject.Sphere as Sphere
import taichi_course01_final.HittableObject.Plane as Plane
import taichi_course01_final.HittableObject.Ellipse as Ellipse


@ti.data_oriented
class Scene:
    MAX_OBJECTS = 100

    def __init__(self):
        self.objects = HittableObject.field(shape=self.MAX_OBJECTS)
        self._obj_count = ti.field(dtype=ti.i32, shape=())

        self._portal_id_tmp = None

    def add(self, obj):
        if obj.material == MaterialType.PORTAL:
            if self._portal_id_tmp:
                self.objects[self._portal_id_tmp].portal_id = self._obj_count[None]
                obj.portal_id = self._portal_id_tmp
                self._portal_id_tmp = None
            else:
                self._portal_id_tmp = self._obj_count[None]

        self.objects[self._obj_count[None]] = obj
        self._obj_count[None] += 1

    @ti.kernel
    def write_portal_id(self, i: ti.i32, id: ti.i32):
        self.objects[i].portal_id = id

    @ti.func
    def hit(self, ray, t_min=0.001, t_max=10e8):
        res = res_tmp = HitResult(
            did_hit=False,
            root=0.,
            color=ti.Vector([0., 0., 0.]),
            hit_point=ti.Vector([0., 0., 0.]),
            hit_point_normal=ti.Vector([0., 0., 0.]),
            front_face=False,
            material=-1,
            id=-1,
        )

        for i in range(self._obj_count[None]):
            if self.objects[i].type == HittableObjectType.SPHERE:
                res_tmp = Sphere.hit(self.objects[i], ray, t_min, t_max)
            elif self.objects[i].type == HittableObjectType.PLANE:
                res_tmp = Plane.hit(self.objects[i], ray, t_min, t_max)
            elif self.objects[i].type == HittableObjectType.ELLIPSE:
                res_tmp = Ellipse.hit(self.objects[i], ray, t_min, t_max)
            if res_tmp.did_hit:
                res = res_tmp
                res.id = i
                t_max = res.root

        return res
