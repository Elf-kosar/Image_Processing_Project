import cv2
import numpy as np
import os
from PIL import Image, ImageTk

def yardimcifonk_gorsel_yukle(file_path):
   
    try:
        if not os.path.exists(file_path):
            raise ValueError(f"Dosya bulunamadı: {file_path}")
            
        file_size = os.path.getsize(file_path)
        if file_size == 0:
            raise ValueError(f"Dosya boş: {file_path}")
        
        try:
            from PIL import Image
            pil_img = Image.open(file_path)
            if pil_img.mode == 'RGBA':
                pil_img = pil_img.convert('RGB')
            
            img_array = np.array(pil_img)

           
            if len(img_array.shape) == 3 and img_array.shape[2] == 3:
                img_array = img_array[..., ::-1]  

            return img_array

        except Exception as pil_error:
            print(f"PIL ile yükleme başarısız oldu: {str(pil_error)}. OpenCV ile deneniyor...")

        img = cv2.imread(file_path)
        if img is None:
            raise ValueError(f"Görüntü yüklenemedi. Dosya formatı desteklenmiyor olabilir: {file_path}")
        return img
    except Exception as e:
        raise ValueError(f"Görüntü yükleme hatası: {str(e)}. Dosya formatı desteklenmiyor veya dosya bozuk olabilir.")

def yardimcifonk_gorsel_kaydet(image, file_path):
  
    try:
        cv2.imwrite(file_path, image)
    except Exception as e:
        raise ValueError(f"Error saving image: {str(e)}")

def yardimcifonk_gorsel_goster(image):
    
    if image is None:
        return None

  
    if len(image.shape) == 3:
        image = image[..., ::-1]  

    return ImageTk.PhotoImage(Image.fromarray(image))

def yardimcifonk_gorsel_boyutlandir(image, max_size=400):
  
    if image is None:
        return None
        
    height, width = image.shape[:2]
    scale = min(max_size/width, max_size/height)
    new_width = int(width * scale)
    new_height = int(height * scale)
    
    return cv2.resize(image, (new_width, new_height))
