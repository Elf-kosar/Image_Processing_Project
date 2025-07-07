import numpy as np


def pad_image(image, pad_value, pad_size):
    if image.ndim == 2:  # Gri görüntü
        return np.pad(image, pad_width=pad_size, mode='constant', constant_values=pad_value)
    elif image.ndim == 3:  # Renkli görüntü
        return np.pad(image, pad_width=((pad_size, pad_size), (pad_size, pad_size), (0, 0)),
                      mode='constant', constant_values=pad_value)


def dilate(image, se_size):
    structuring_element = np.ones((se_size, se_size), dtype=np.uint8)
    pad = se_size // 2
    padded = pad_image(image, 0, pad)
    result = np.zeros_like(image)

    if image.ndim == 2:  # Gri
        for y in range(image.shape[0]):
            for x in range(image.shape[1]):
                region = padded[y:y+se_size, x:x+se_size]
                result[y, x] = np.max(region[structuring_element == 1])
    elif image.ndim == 3:  # Renkli
        for c in range(image.shape[2]):
            for y in range(image.shape[0]):
                for x in range(image.shape[1]):
                    region = padded[y:y+se_size, x:x+se_size, c]
                    result[y, x, c] = np.max(region[structuring_element == 1])
    return result


def erozyon(image, se_size):
    structuring_element = np.ones((se_size, se_size), dtype=np.uint8)
    pad = se_size // 2
    padded = pad_image(image, 255, pad)
    result = np.zeros_like(image)

    if image.ndim == 2:  # Gri
        for y in range(image.shape[0]):
            for x in range(image.shape[1]):
                region = padded[y:y+se_size, x:x+se_size]
                result[y, x] = np.min(region[structuring_element == 1])
    elif image.ndim == 3:  # Renkli
        for c in range(image.shape[2]):
            for y in range(image.shape[0]):
                for x in range(image.shape[1]):
                    region = padded[y:y+se_size, x:x+se_size, c]
                    result[y, x, c] = np.min(region[structuring_element == 1])
    return result


def acma(image, se_size):
    return dilate(erozyon(image, se_size), se_size)

def kapama(image, se_size):
    return erozyon(dilate(image, se_size), se_size)


def iterasyon_sayisi(image, operation_func, se_size, iterations=1):
    result = image.copy()
    for _ in range(iterations):
        result = operation_func(result, se_size)
    return result
