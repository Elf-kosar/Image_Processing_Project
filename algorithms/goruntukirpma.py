import numpy as np

def crop_image(image: np.ndarray, x: int, y: int, w: int, h: int) -> np.ndarray:

    height, width = image.shape[:2]


    if not (0 <= x < width and 0 <= y < height and x + w <= width and y + h <= height):
        raise ValueError("Kırpma koordinatları görüntü sınırlarını aşıyor")


    return image[y:y + h, x:x + w]
