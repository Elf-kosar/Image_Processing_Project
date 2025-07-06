import numpy as np
import random


def add_salt_and_pepper_noise(img, prob):
    
    if img.ndim == 2:

        height, width = img.shape
        for _ in range(int(prob * height * width)):
            x = random.randint(0, height - 1)
            y = random.randint(0, width - 1)
            img[x, y] = 0 if random.random() < 0.5 else 255
    elif img.ndim == 3:

        height, width, _ = img.shape
        for _ in range(int(prob * height * width)):
            x = random.randint(0, height - 1)
            y = random.randint(0, width - 1)
            color = 0 if random.random() < 0.5 else 255
            img[x, y] = [color] * 3
    else:
        raise ValueError("Giriş görüntüsü 2D (gri) veya 3D (renkli) olmalıdır.")

    return img



import numpy as np

def mean_filter(image, kernel_size):
    h = len(image)
    w = len(image[0]) if h else 0
    pad = kernel_size // 2

    temp = [[[0, 0, 0] for _ in range(w)] for __ in range(h)]

    for y in range(h):
        for x in range(w):
            for c in range(3):
                sum_val = 0
                count = 0
                for ky in range(-pad, pad + 1):
                    for kx in range(-pad, pad + 1):
                        ny, nx = y + ky, x + kx
                        if 0 <= ny < h and 0 <= nx < w:
                            sum_val += int(image[ny][nx][c])
                            count += 1
                temp[y][x][c] = int(sum_val / count)

    return np.array(temp, dtype=np.uint8)



def median_filter(img, kernel_size):

    height, width = img.shape[:2]
    pad = kernel_size // 2
    filtered_img = np.zeros_like(img, dtype=np.uint8) 
    padded_img = np.pad(img, ((pad, pad), (pad, pad), (0, 0)), mode='constant', constant_values=0) 

    for i in range(height):
        for j in range(width):
           
            kernel_values = padded_img[i:i+kernel_size, j:j+kernel_size, :]
            median_values = []

            for k in range(3):  
                channel_values = kernel_values[:, :, k].flatten()
                channel_values.sort()  
                median_value = channel_values[len(channel_values) // 2]  
                median_values.append(median_value)

            filtered_img[i, j, :] = np.array(median_values, dtype=np.uint8)

    return filtered_img




