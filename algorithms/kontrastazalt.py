import numpy as np

def kontrast_ayarla(array, oran):

    ortalama = np.mean(array)
    kontrast = oran * array + (1 - oran) * ortalama
    return np.clip(kontrast, 0, 255).astype(np.uint8)

def process_array(input_array, kontrast_orani=0.5):

    input_array = np.array(input_array)

    is_color = len(input_array.shape) == 3 and input_array.shape[2] == 3
    
    if is_color:
   
        result = np.zeros_like(input_array)
        for i in range(3):
            channel = input_array[..., i]
            result[..., i] = kontrast_ayarla(channel, kontrast_orani)
        return result
    else:
       
        return kontrast_ayarla(input_array, kontrast_orani)
