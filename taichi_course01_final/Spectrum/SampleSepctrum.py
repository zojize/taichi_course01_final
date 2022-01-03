# https://www.pbr-book.org/3ed-2018/Color_and_Radiometry/The_SampledSpectrum_Class
import taichi as ti
from .CoefficientSpectrum import CoefficientSpectrum, lerp_spectrum
from taichi_course01_final.Utils import lerp, is_sorted
from taichi_course01_final.Types import Vec3f
from .Data import CIE_lambda, CIE_X, CIE_Y, CIE_Z, N_CIE_SAMPLES, CIE_Y_INTEGRAL


sampled_lambda_start = 400
sampled_lambda_end = 700
n_spectrum_samples = 60

SampledSpectrum = ti.types.vector(n_spectrum_samples, ti.f32)


@ti.func
def sort_spectrum_samples(lambdas, vals):
    pass


@ti.func
def from_sampled(lambdas, vals):
    if not is_sorted(lambdas):
        ''' TODO: sort lambdas and vals'''

    r = SampledSpectrum(0)
    for i in ti.static(range(n_spectrum_samples)):
        lambda0 = lerp(
            float(i) / float(n_spectrum_samples),
            sampled_lambda_start,
            sampled_lambda_end,
        )
        lambda1 = lerp(
            float(i + 1) / float(n_spectrum_samples),
            sampled_lambda_start,
            sampled_lambda_end,
        )
        # TODO
        r[i] = average_spectrum_samples(lambdas, vals, lambda0, lambda1)

    return r


@ti.func
def average_spectrum_samples(lambdas, vals, lambda_start, lambda_end):
    n = lambdas.shape[0]

    should_return = False
    res = 0.
    if lambda_end <= lambdas[0]:
        should_return = True
        res = vals[0]
    if lambda_start >= lambdas[n - 1]:
        should_return = True
        res = vals[n - 1]
    if n == 1:
        should_return = True
        res = vals[0]

    if not should_return:
        sum = 0.

        if lambda_start < lambdas[0]:
            sum += vals[0] * (lambdas[0] - lambda_start)
        if lambda_end > lambdas[n - 1]:
            sum += vals[n - 1] * (lambda_end - lambdas[n - 1])

        i = 0
        while lambda_start > lambdas[i + 1]:
            i += 1

        while i + 1 < n and lambda_end >= lambdas[i]:
            seg_lambda_start = max(lambda_start, lambdas[i])
            seg_lambda_end = min(lambda_end, lambdas[i + 1])
            sum += (
                0.5
                * (interp(lambdas, vals, seg_lambda_start, i)
                    + interp(lambdas, vals, seg_lambda_end, i))
                * (seg_lambda_end - seg_lambda_start)
            )
            i += 1

        res = sum / (lambda_end - lambda_start)

    return res


@ti.func
def interp(lambdas, vals, w, i):
    return lerp(
        (w - lambdas[i]) / (lambdas[i + 1] - lambdas[i]),
        vals[i],
        vals[i + 1]
    )


X = SampledSpectrum(0)
Y = SampledSpectrum(0)
Z = SampledSpectrum(0)


@ti.kernel
def init():
    for i in ti.static(range(n_spectrum_samples)):
        wl0 = lerp(
            float(i) / float(n_spectrum_samples),
            sampled_lambda_start, sampled_lambda_end
        )
        wl1 = lerp(
            float(i + 1) / float(n_spectrum_samples),
            sampled_lambda_start, sampled_lambda_end
        )

        X[i] = average_spectrum_samples(CIE_lambda, CIE_X, N_CIE_SAMPLES, wl0, wl1)
        Y[i] = average_spectrum_samples(CIE_lambda, CIE_Y, N_CIE_SAMPLES, wl0, wl1)
        Z[i] = average_spectrum_samples(CIE_lambda, CIE_Z, N_CIE_SAMPLES, wl0, wl1)


@ti.func
def to_xyz(s, xyz):
    xyz[0] = xyz[1] = xyz[2] = 0.
    for i in ti.static(range(n_spectrum_samples)):
        xyz[0] += X[i] * s[i]
        xyz[1] += Y[i] * s[i]
        xyz[2] += Z[i] * s[i]
    xyz *= (
        float(sampled_lambda_end - sampled_lambda_start)
        / float(CIE_Y_INTEGRAL * n_spectrum_samples)
    )

    return xyz


@ti.func
def y(s):
    yy = 0.
    for i in ti.static(range(n_spectrum_samples)):
        yy += Y[i] * s[i]
    return (
        yy * float(sampled_lambda_end, sampled_lambda_start)
        / float(n_spectrum_samples)
    )


@ti.func
def xyz_to_rgb(xyz, rgb):
    rgb[0] = 3.240479 * xyz[0] - 1.537150 * xyz[1] - 0.498535 * xyz[2]
    rgb[1] = -0.969256 * xyz[0] + 1.875991 * xyz[1] + 0.041556 * xyz[2]
    rgb[2] = 0.055648 * xyz[0] - 0.204043 * xyz[1] + 1.057311 * xyz[2]


@ti.func
def rgb_to_xyz(rgb, xyz):
    xyz[0] = 0.412453 * rgb[0] + 0.357580 * rgb[1] + 0.180423 * rgb[2]
    xyz[1] = 0.212671 * rgb[0] + 0.715160 * rgb[1] + 0.072169 * rgb[2]
    xyz[2] = 0.019334 * rgb[0] + 0.119193 * rgb[1] + 0.950227 * rgb[2]


@ti.func
def to_rbg(s, rgb):
    xyz = ti.Vector([0., 0., 0.])
    to_xyz(s, xyz)
    xyz_to_rgb(xyz, rgb)
