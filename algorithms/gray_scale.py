import numpy as np

def gri_tonlama_donusumu_ve_goster(img):

    yukseklik, genislik, _ = img.shape
    
    gri_img = np.zeros((yukseklik, genislik), dtype=np.uint8)


    for i in range(yukseklik):
        for j in range(genislik):
            b, g, r = img[i, j]
            gri_deger = int(0.299 * r + 0.587 * g + 0.114 * b)
            gri_img[i, j] = gri_deger

    return gri_img

