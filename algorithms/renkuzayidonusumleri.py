import cv2
import numpy as np

def show_rgb(img1):
    converted = img1[..., ::-1]
    return converted

def show_hsv(img1):
    img = img1.astype(np.float32) / 255.0
    b, g, r = img[..., 0], img[..., 1], img[..., 2]
    cmax = np.maximum.reduce([r, g, b])
    cmin = np.minimum.reduce([r, g, b])
    delta = cmax - cmin

    h = np.zeros_like(cmax)
    mask = delta != 0
    h[mask & (cmax == r)] = ((g - b)[mask & (cmax == r)] / delta[mask & (cmax == r)]) % 6
    h[mask & (cmax == g)] = ((b - r)[mask & (cmax == g)] / delta[mask & (cmax == g)]) + 2
    h[mask & (cmax == b)] = ((r - g)[mask & (cmax == b)] / delta[mask & (cmax == b)]) + 4
    h *= 60
    h[h < 0] += 360

    s = np.zeros_like(cmax)
    s[cmax != 0] = delta[cmax != 0] / cmax[cmax != 0]
    v = cmax

    hsv = np.stack([h / 360.0, s, v], axis=-1)
    converted = (hsv * 255).astype(np.uint8)
    return converted

def show_ycrcb(img1):
    img = img1.astype(np.float32)
    b, g, r = img[..., 0], img[..., 1], img[..., 2]
    y = 0.299*r + 0.587*g + 0.114*b
    cr = (r - y) * 0.713 + 128
    cb = (b - y) * 0.564 + 128
    converted = np.stack([y, cr, cb], axis=-1)
    converted = np.clip(converted, 0, 255).astype(np.uint8)
    return converted

def show_lab(img1):
    img = img1.astype(np.float32) / 255.0
    b, g, r = img[..., 0], img[..., 1], img[..., 2]
    X = (r * 0.412453 + g * 0.357580 + b * 0.180423) / 0.950456
    Y = (r * 0.212671 + g * 0.715160 + b * 0.072169)
    Z = (r * 0.019334 + g * 0.119193 + b * 0.950227) / 1.088754

    def f(t):
        return np.where(t > 0.008856, t ** (1/3), (903.3 * t + 16) / 116)
    
    L = 116 * f(Y) - 16
    A = 500 * (f(X) - f(Y))
    B = 200 * (f(Y) - f(Z))

    lab = np.stack([L, A, B], axis=-1)
    converted = np.clip(lab * 255 / np.max(lab), 0, 255).astype(np.uint8)
    return converted

def show_xyz(img1):
    img = img1.astype(np.float32)
    b, g, r = img[..., 0], img[..., 1], img[..., 2]
    X = 0.4124564*r + 0.3575761*g + 0.1804375*b
    Y = 0.2126729*r + 0.7151522*g + 0.0721750*b
    Z = 0.0193339*r + 0.1191920*g + 0.9503041*b
    xyz = np.stack([X, Y, Z], axis=-1)
    converted = np.clip(xyz, 0, 255).astype(np.uint8)
    return converted

def show_hls(img1):
    img = img1.astype(np.float32) / 255.0
    b, g, r = img[..., 0], img[..., 1], img[..., 2]
    max_rgb = np.max(img, axis=-1)
    min_rgb = np.min(img, axis=-1)
    delta = max_rgb - min_rgb

    l = (max_rgb + min_rgb) / 2
    s = np.zeros_like(l)
    s[delta != 0] = delta[delta != 0] / (1 - np.abs(2 * l[delta != 0] - 1))

    h = np.zeros_like(l)
    mask = delta != 0
    h[mask & (max_rgb == r)] = (g[mask & (max_rgb == r)] - b[mask & (max_rgb == r)]) / delta[mask & (max_rgb == r)] % 6
    h[mask & (max_rgb == g)] = (b[mask & (max_rgb == g)] - r[mask & (max_rgb == g)]) / delta[mask & (max_rgb == g)] + 2
    h[mask & (max_rgb == b)] = (r[mask & (max_rgb == b)] - g[mask & (max_rgb == b)]) / delta[mask & (max_rgb == b)] + 4

    h = (h / 6) * 360
    hls = np.stack([h / 360, l, s], axis=-1)
    converted = (hls * 255).astype(np.uint8)
    return converted

def show_yuv(img1):
    img = img1.astype(np.float32)
    b, g, r = img[..., 0], img[..., 1], img[..., 2]
    y = 0.299*r + 0.587*g + 0.114*b
    u = -0.14713*r - 0.28886*g + 0.436*b + 128
    v = 0.615*r - 0.51499*g - 0.10001*b + 128
    yuv = np.stack([y, u, v], axis=-1)
    converted = np.clip(yuv, 0, 255).astype(np.uint8)
    return converted

def show_luv(img1):
    img = img1.astype(np.float32) / 255.0
    b, g, r = img[..., 0], img[..., 1], img[..., 2]
    X = 0.4124564 * r + 0.3575761 * g + 0.1804375 * b
    Y = 0.2126729 * r + 0.7151522 * g + 0.0721750 * b
    Z = 0.0193339 * r + 0.1191920 * g + 0.9503041 * b
    Xn, Yn, Zn = 0.950456, 1.0, 1.088754

    L = np.where(Y > 0.008856, 116 * Y ** (1/3) - 16, 903.3 * Y)
    u_prime = (4 * X) / (X + 15 * Y + 3 * Z + 1e-6)
    v_prime = (9 * Y) / (X + 15 * Y + 3 * Z + 1e-6)
    un = 0.1978398
    vn = 0.4683363
    U = 13 * L * (u_prime - un)
    V = 13 * L * (v_prime - vn)
    luv = np.stack([L, U, V], axis=-1)
    converted = np.clip(luv, 0, 255).astype(np.uint8)
    return converted
