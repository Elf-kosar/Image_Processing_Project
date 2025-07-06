import numpy as np

def rgb2gray(img):

    R = img[:, :, 0]
    G = img[:, :, 1]
    B = img[:, :, 2]
    gray = 0.2989 * R + 0.5870 * G + 0.1140 * B
    return gray.astype(np.uint8)


def gaussian_filtre(size=5, sigma=1):
   
    ax = np.arange(-(size // 2), size // 2 + 1)
    xx, yy = np.meshgrid(ax, ax)
    kernel = np.exp(-(xx**2 + yy**2) / (2 * sigma*2))
    kernel /= np.sum(kernel)
    return kernel


def konvolusyon_filtre(image, kernel):
   
    k = kernel.shape[0]
    pad = k // 2
    padded = np.pad(image, pad, mode='constant')
    output = np.zeros_like(image)

    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            region = padded[i:i+k, j:j+k]
            output[i, j] = np.sum(region * kernel)
    return output


def sobel_filtre(img):
  
    Kx = np.array([[1, 0, -1], [2, 0, -2], [1, 0, -1]])
    Ky = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]])

    Ix = konvolusyon_filtre(img, Kx)
    Iy = konvolusyon_filtre(img, Ky)

    G = np.hypot(Ix, Iy)
    G = (G / G.max()) * 255
    theta = np.arctan2(Iy, Ix)
    return G.astype(np.uint8), theta


def kenar_inceltme(G, theta):
   
    M, N = G.shape
    Z = np.zeros((M, N), dtype=np.uint8)
    angle = theta * 180. / np.pi
    angle[angle < 0] += 180

    for i in range(1, M-1):
        for j in range(1, N-1):
            q = 255
            r = 255
            a = angle[i, j]

            if (0 <= a < 22.5) or (157.5 <= a <= 180):
                q = G[i, j+1]
                r = G[i, j-1]
            elif 22.5 <= a < 67.5:
                q = G[i+1, j-1]
                r = G[i-1, j+1]
            elif 67.5 <= a < 112.5:
                q = G[i+1, j]
                r = G[i-1, j]
            elif 112.5 <= a < 157.5:
                q = G[i-1, j-1]
                r = G[i+1, j+1]

            if (G[i, j] >= q) and (G[i, j] >= r):
                Z[i, j] = G[i, j]
            else:
                Z[i, j] = 0
    return Z


def threshold(img, low, high):

    M, N = img.shape
    res = np.zeros((M, N), dtype=np.uint8)

    weak = 25
    strong = 255

    strong_i, strong_j = np.where(img >= high)
    zeros_i, zeros_j = np.where(img < low)

    weak_i, weak_j = np.where((img <= high) & (img >= low))

    res[strong_i, strong_j] = strong
    res[weak_i, weak_j] = weak

    return res, weak, strong


def kenartakibi(img, weak, strong=255):
   
    M, N = img.shape
    for i in range(1, M-1):
        for j in range(1, N-1):
            if img[i, j] == weak:
                if np.any(img[i-1:i+2, j-1:j+2] == strong):
                    img[i, j] = strong
                else:
                    img[i, j] = 0
    return img


def canny_edge_detector(img, lowThresh, highThresh):
    
    if img.ndim == 3:
        gray = rgb2gray(img)
    else:
        gray = img
    kernel = gaussian_filtre(size=5, sigma=1)
    blurred = konvolusyon_filtre(gray, kernel)
    G, theta = sobel_filtre(blurred)
    nonMax = kenar_inceltme(G, theta)
    thresh, weak, strong = threshold(nonMax, lowThresh, highThresh)
    result = kenartakibi(thresh, weak, strong)
    return result