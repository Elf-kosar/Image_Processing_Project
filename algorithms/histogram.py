import numpy as np
import matplotlib.pyplot as plt


def histogram_germe_gray(image):
    image_float = image.copy().astype(np.float32)
    
    min_val = float('inf')
    max_val = float('-inf')
    
    rows, cols = image_float.shape
    for i in range(rows):
        for j in range(cols):
            if image_float[i, j] < min_val:
                min_val = image_float[i, j]
            if image_float[i, j] > max_val:
                max_val = image_float[i, j]
    
    stretched = np.zeros_like(image_float)
    for i in range(rows):
        for j in range(cols):
            if max_val - min_val != 0:
                stretched[i, j] = min(255.0, max(0.0, (image_float[i, j] - min_val) * 255.0 / (max_val - min_val)))
            else:
                stretched[i, j] = image_float[i, j]
    
    return stretched.astype(np.uint8)


def histogram_germe_color(image):
    rows, cols, channels = image.shape
    stretched = np.zeros_like(image)
    
    for c in range(channels):
        min_val = float('inf')
        max_val = float('-inf')
        
        for i in range(rows):
            for j in range(cols):
                if float(image[i, j, c]) < min_val:
                    min_val = float(image[i, j, c])
                if float(image[i, j, c]) > max_val:
                    max_val = float(image[i, j, c])
        
        for i in range(rows):
            for j in range(cols):
                if max_val - min_val != 0:
                    stretched[i, j, c] = int((float(image[i, j, c]) - min_val) * 255 / (max_val - min_val))
                else:
                    stretched[i, j, c] = image[i, j, c]
    
    return stretched


def histogram_genisletme_gray(image):
    rows, cols = image.shape
    
    hist = [0] * 256
    for i in range(rows):
        for j in range(cols):
            hist[image[i, j]] += 1
    
    cdf = [0] * 256
    cdf[0] = hist[0]
    for i in range(1, 256):
        cdf[i] = cdf[i-1] + hist[i]
    
    cdf_min = 0
    for i in range(256):
        if cdf[i] > 0:
            cdf_min = cdf[i]
            break
    
    cdf_normalized = [0] * 256
    for i in range(256):
        if cdf[i] > 0:
            cdf_normalized[i] = int(100 + ((cdf[i] - cdf_min) * (200 - 100)) / (rows * cols - cdf_min))
        else:
            cdf_normalized[i] = 0
    
    equalized = np.zeros_like(image)
    for i in range(rows):
        for j in range(cols):
            equalized[i, j] = cdf_normalized[image[i, j]]
    
    return equalized


import numpy as np

def histogram_genisletme_color(image):
    rows, cols, _ = image.shape
    
    ycrcb = np.zeros_like(image, dtype=np.float32)
    
    b_channel = np.zeros((rows, cols), dtype=np.float32)
    g_channel = np.zeros((rows, cols), dtype=np.float32)
    r_channel = np.zeros((rows, cols), dtype=np.float32)
    
    for i in range(rows):
        for j in range(cols):
            b_channel[i, j] = float(image[i, j, 0])
            g_channel[i, j] = float(image[i, j, 1])
            r_channel[i, j] = float(image[i, j, 2])
    
    y_channel = np.zeros((rows, cols), dtype=np.float32)
    cr_channel = np.zeros((rows, cols), dtype=np.float32)
    cb_channel = np.zeros((rows, cols), dtype=np.float32)
    
    for i in range(rows):
        for j in range(cols):
            y_channel[i, j] = 0.299 * r_channel[i, j] + 0.587 * g_channel[i, j] + 0.114 * b_channel[i, j]
            cr_channel[i, j] = 128 + 0.5 * r_channel[i, j] - 0.419 * g_channel[i, j] - 0.081 * b_channel[i, j]
            cb_channel[i, j] = 128 - 0.169 * r_channel[i, j] - 0.331 * g_channel[i, j] + 0.5 * b_channel[i, j]
    
    y_channel_uint8 = np.zeros((rows, cols), dtype=np.uint8)
    for i in range(rows):
        for j in range(cols):
            pixel_value = int(round(y_channel[i, j]))
            if pixel_value < 0:
                pixel_value = 0
            elif pixel_value > 255:
                pixel_value = 255
            y_channel_uint8[i, j] = pixel_value
    
    hist = [0] * 256
    total_pixels = rows * cols
    
    for i in range(rows):
        for j in range(cols):
            hist[y_channel_uint8[i, j]] += 1
    
    cdf = [0] * 256
    cdf[0] = hist[0]
    for i in range(1, 256):
        cdf[i] = cdf[i-1] + hist[i]
    
    cdf_min = 0
    for i in range(256):
        if cdf[i] > 0:
            cdf_min = cdf[i]
            break
    
    mapping = [0] * 256
    for i in range(256):
        if cdf[i] == 0:
            mapping[i] = 0
        else:
            mapping[i] = max(100, min(200, round(((cdf[i] - cdf_min) * (200 - 100)) / (total_pixels - cdf_min) + 100)))
    
    y_eq = np.zeros((rows, cols), dtype=np.uint8)
    for i in range(rows):
        for j in range(cols):
            y_eq[i, j] = mapping[y_channel_uint8[i, j]]
    
    result = np.zeros_like(image)
    
    for i in range(rows):
        for j in range(cols):
            y = float(y_eq[i, j])
            cr = cr_channel[i, j]
            cb = cb_channel[i, j]
            
            r = y + 1.403 * (cr - 128)
            g = y - 0.714 * (cr - 128) - 0.344 * (cb - 128)
            b = y + 1.773 * (cb - 128)
            
            r = max(100, min(200, round(r)))
            g = max(100, min(200, round(g)))
            b = max(100, min(200, round(b)))
            
            result[i, j, 0] = b
            result[i, j, 1] = g
            result[i, j, 2] = r
    
    return result


def grafik_histogram(original, processed):
    fig, axes = plt.subplots(2, 1, figsize=(5, 4))
    
    if len(original.shape) == 2:
        axes[0].hist(original.ravel(), bins=256, color='gray')
        axes[0].set_title("Orijinal Görüntü Histogramı")
    else:
        colors = ('b', 'g', 'r')
        for i, color in enumerate(colors):
            axes[0].hist(original[:, :, i].ravel(), bins=256, color=color, alpha=0.5)
        axes[0].set_title("Orijinal Görüntü Histogramı")

    if len(processed.shape) == 2:
        axes[1].hist(processed.ravel(), bins=256, color='gray')
        axes[1].set_title("İşlenmiş Görüntü Histogramı")
    else:
        colors = ('b', 'g', 'r')
        for i, color in enumerate(colors):
            axes[1].hist(processed[:, :, i].ravel(), bins=256, color=color, alpha=0.5)
        axes[1].set_title("İşlenmiş Görüntü Histogramı")

    plt.tight_layout()
    return fig