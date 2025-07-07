import numpy as np

def median_filter_pipeline(image_array, kernel_size):

    def bubble_sort(arr):
        n = len(arr)
        for i in range(n):
            for j in range(n - i - 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
        return arr


    def get_median(values):
        sorted_vals = bubble_sort(values[:])
        n = len(sorted_vals)
        if n % 2 == 0:
            return (sorted_vals[n // 2 - 1] + sorted_vals[n // 2]) // 2
        return sorted_vals[n // 2]

  
    def apply_median_filter(single_channel, kernel_size):
        if kernel_size % 2 == 0 or kernel_size < 3:
            raise ValueError("Çekirdek boyutu tek sayı ve 3 veya daha büyük olmalıdır.")

        pad = kernel_size // 2
        height, width = single_channel.shape
        padded_img = np.pad(single_channel, pad, mode='edge')
        filtered_array = np.zeros_like(single_channel)

        for y in range(height):
            for x in range(width):
                neighborhood = []
                for dy in range(-pad, pad + 1):
                    for dx in range(-pad, pad + 1):
                        pixel = padded_img[y + pad + dy, x + pad + dx]
                        neighborhood.append(int(pixel))
                filtered_array[y, x] = get_median(neighborhood)

        return filtered_array

  
    if image_array.ndim == 2:
       
        return apply_median_filter(image_array, kernel_size)
    elif image_array.ndim == 3:
       
        channels = []
        for c in range(image_array.shape[2]):
            filtered = apply_median_filter(image_array[:, :, c], kernel_size)
            channels.append(filtered)
        return np.stack(channels, axis=2)
    else:
        raise ValueError("Geçersiz görüntü boyutu. Giriş 2D (gri) veya 3D (renkli) olmalıdır.")
