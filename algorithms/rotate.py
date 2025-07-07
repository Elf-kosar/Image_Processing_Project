import math
import numpy as np

def gorsel_dondurme(image_array, angle_degrees):
    
    angle_radians = math.radians(angle_degrees)
    cos_a = math.cos(angle_radians)
    sin_a = math.sin(angle_radians)

    height, width = image_array.shape[:2]
    cx, cy = width // 2, height // 2

    rotated = np.zeros_like(image_array)

    for y in range(height):
        for x in range(width):
            x_rel = x - cx
            y_rel = y - cy

            x_new = int(cx + x_rel * cos_a - y_rel * sin_a)
            y_new = int(cy + x_rel * sin_a + y_rel * cos_a)

            if 0 <= x_new < width and 0 <= y_new < height:
                rotated[y, x] = image_array[y_new, x_new]

    return rotated
