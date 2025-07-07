import numpy as np


def griye_cevir(img):
    img_array = np.array(img)
    if len(img_array.shape) == 3:
        return np.dot(img_array[..., :3], [0.299, 0.587, 0.114]).astype(np.uint8)
    return img_array

def binary_donusum(gri_array, esik=128):
    return np.where(gri_array > esik, 255, 0).astype(np.uint8)

def process_array(input_array, esik_degeri=128):
    gri = griye_cevir(input_array)
    binary = binary_donusum(gri, esik_degeri)
    return binary
