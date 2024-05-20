import cv2
from PIL import Image
import numpy as np
import shutil
import os

def clear_directory(folder):
    # Check if directory exists
    if not os.path.exists(folder):
        os.makedirs(folder)
    # Remove files and directories in the folder
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')

def is_far_enough(contour1, contour2, min_distance=10):
    x1, y1, w1, h1 = cv2.boundingRect(contour1)
    x2, y2, w2, h2 = cv2.boundingRect(contour2)

    # Calculate distance between closest points
    horizontal_dist = max(x1 - (x2 + w2), x2 - (x1 + w1))
    vertical_dist = max(y1 - (y2 + h2), y2 - (y1 + h1))

    # If distances are negative, contours are overlapping or touching
    return horizontal_dist >= min_distance and vertical_dist >= min_distance

def extract_subjects(image_path, output_folder):
    # Read the image with alpha channel
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    
    # Check if the image has an alpha channel, if not, add one
    if image.shape[2] == 3:  # No alpha channel
        image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)

    # Apply adaptive thresholding to find contours
    # thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 15, 12)
    # thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 91, 12)

    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    # Filter contours based on distance and size
    filtered_contours = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        # Check if the contour is large enough
        if w > 10 and h > 10:
            if all(is_far_enough(contour, test_contour) for test_contour in filtered_contours):
                filtered_contours.append(contour)

    # Loop through filtered contours and save each as a separate image
    for i, contour in enumerate(filtered_contours):
        # Get bounding box coordinates
        x, y, w, h = cv2.boundingRect(contour)
        
        # Extract the region of interest with the alpha channel
        roi = image[y:y+h, x:x+w]

        # Convert to PIL Image to save in PNG format with transparency
        roi_pil = Image.fromarray(roi, 'RGBA')  # Ensure using 'RGBA' mode for transparency
        
        # Save image
        roi_pil.save(f"{output_folder}/subject_{i+1}.png")
# Usage

clear_directory('./splited_images')
extract_subjects('test.png', './splited_images')
