import taichi as ti
from taichi_course01_final.Utils import is_sorted

n_spectrum_samples = 8
CoefficientSpectrum = ti.types.vector(n_spectrum_samples, ti.f32)


@ti.func
def new(v):
    return CoefficientSpectrum(v)


@ti.func
def lerp_spectrum(t, s1, s2):
    return (1 - t) * s1 + t * s2


@ti.func
def clamp_spectrum(s, low, high):
    s_ = s
    for i in ti.static(range(n_spectrum_samples)):
        s_[i] = min(high, max(low, s[i]))
    return s_


ti.init()

