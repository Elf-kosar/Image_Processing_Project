import numpy as np
def double_threshold(image, low_threshold=50, high_threshold=150):
    """
    Apply double thresholding to an image.
    
    Args:
        image: Input image (grayscale)
        low_threshold: Low threshold value
        high_threshold: High threshold value
    
    Returns:
        Thresholded image
    """
    # Convert to grayscale if needed
    if len(image.shape) == 3:
        height, width = image.shape[:2]
        grayscale_img = np.zeros((height, width), dtype=np.uint8)
        
        for y in range(height):
            for x in range(width):
                b, g, r = image[y, x]
                gray_value = int(0.299 * r + 0.587 * g + 0.114 * b)
                grayscale_img[y, x] = gray_value
    else:
        grayscale_img = image
        
    # Get image dimensions
    height, width = grayscale_img.shape
    
    # Create output image
    result = np.zeros((height, width), dtype=np.uint8)
    
    # Apply double thresholding
    for y in range(height):
        for x in range(width):
            pixel = grayscale_img[y, x]
            
            if pixel >= high_threshold:
                result[y, x] = 255  # Strong edge
            elif pixel >= low_threshold:
                result[y, x] = 128  # Weak edge
            else:
                result[y, x] = 0    # Not an edge
                
    return result