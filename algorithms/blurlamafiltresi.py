import numpy as np

def blur_cekirdek_olustur(ksize, angle):

    kernel = np.zeros((ksize, ksize), dtype=np.float32)
    center = ksize // 2

   
    rad = np.deg2rad(angle)

    
    dx = np.cos(rad)
    dy = np.sin(rad)

   
    for i in range(-center, center + 1):
        x = int(round(center + dx * i))
        y = int(round(center + dy * i))
        if 0 <= x < ksize and 0 <= y < ksize:
            kernel[y, x] = 1.0

   
    kernel /= np.sum(kernel)
    return kernel

def blurlastirma(image, ksize, angle):

    if ksize < 1:
        raise ValueError("Kernel boyutu pozitif olmalı ve tek sayı olması önerilir")

    
    kernel = blur_cekirdek_olustur(ksize, angle)

    
    height, width, channels = image.shape
    pad = ksize // 2

 
    padded_image = np.pad(image, ((pad, pad), (pad, pad), (0, 0)), mode='reflect')
    output = np.zeros_like(image)

   
    for y in range(height):
        for x in range(width):
            for c in range(channels):
                region = padded_image[y:y+ksize, x:x+ksize, c]
                output[y, x, c] = np.clip(np.sum(region * kernel), 0, 255)

    return output.astype(np.uint8)