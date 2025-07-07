import numpy as np
from PIL import Image

def resize_manual(img, new_shape):
    """new_shape: (height, width)"""
    if isinstance(img, np.ndarray):
        img = Image.fromarray(img)
    resized_img = img.resize((new_shape[1], new_shape[0]))  # width, height
    return np.array(resized_img)

def subtract_manual(img1, img2):
    result = np.clip(img1.astype(int) - img2.astype(int), 0, 255).astype(np.uint8)
    return result

def multiply_manual(img1, img2):
    result = np.clip((img1.astype(float) * img2.astype(float)) / 255.0, 0, 255).astype(np.uint8)
    return result

def image_arithmetic(img1, img2, operation):
    """
    img1, img2: RGB NumPy dizileri
    operation: "Çıkartma" veya "Çarpma"
    """
    if img1.shape != img2.shape:
        img2 = resize_manual(img2, img1.shape[:2])  # Yükseklik ve genişlik

    if operation == "Çıkartma":
        return subtract_manual(img1, img2)
    elif operation == "Çarpma":
        return multiply_manual(img1, img2)
    else:
        raise ValueError("Geçersiz işlem: 'Çıkartma' veya 'Çarpma' olmalı.")


