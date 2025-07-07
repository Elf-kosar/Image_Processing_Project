import numpy as np

def zoom_islemi(input_array, scale, method='nearest'):
    
    input_array = np.array(input_array)
    
   
    is_color = len(input_array.shape) == 3 and input_array.shape[2] == 3
    
    if is_color:
      
        h, w, c = input_array.shape
        nh, nw = int(h * scale), int(w * scale)
        result = np.zeros((nh, nw, c), dtype=np.uint8)
        
        for i in range(c):
       
            channel = input_array[:, :, i]
            result[:, :, i] = yaklastirma_kanali(channel, scale, method)
        
        return result
    else:
       
        return yaklastirma_kanali(input_array, scale, method)

def yaklastirma_kanali(channel, scale, method):
    
    h, w = channel.shape
    nh, nw = int(h * scale), int(w * scale)
    
    if method == 'nearest':  
        y_idx = np.clip((np.arange(nh) / scale).astype(int), 0, h - 1)
        x_idx = np.clip((np.arange(nw) / scale).astype(int), 0, w - 1)
        result = channel[y_idx[:, None], x_idx]
    
    elif method == 'bilinear': 
        y, x = np.meshgrid(np.arange(nh), np.arange(nw), indexing='ij')
        y0 = np.floor(y / scale).astype(int)
        x0 = np.floor(x / scale).astype(int)
        y1 = np.clip(y0 + 1, 0, h - 1)
        x1 = np.clip(x0 + 1, 0, w - 1)
        
        dy = y / scale - y0
        dx = x / scale - x0
        
        f00 = channel[y0, x0]
        f01 = channel[y0, x1]
        f10 = channel[y1, x0]
        f11 = channel[y1, x1]
        
        result = (
            (1 - dy) * (1 - dx) * f00 +
            (1 - dy) * dx * f01 +
            dy * (1 - dx) * f10 +
            dy * dx * f11
        )
        result = np.clip(result, 0, 255).astype(np.uint8)
    
    else:
        raise ValueError(f"Desteklenmeyen interpolasyon yöntemi: {method}")
    
    return result

def process_array(input_array, olcek=1.0, yontem='nearest'):

    return zoom_islemi(input_array, olcek, yontem)
