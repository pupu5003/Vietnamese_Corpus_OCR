import cv2
import numpy as np
import os

input_folder = "processed_images/10729371"
output_folder = "processed_second/10729371"

os.makedirs(output_folder, exist_ok=True)

# Define HSV ranges for red and pink
lower_red1 = np.array([0, 50, 50])    # Đỏ sáng
upper_red1 = np.array([10, 255, 255])
lower_red2 = np.array([170, 50, 50])  # Đỏ đậm
upper_red2 = np.array([180, 255, 255])
lower_pink = np.array([140, 50, 50])  # Hồng sáng
upper_pink = np.array([170, 255, 255])  # Hồng đậm

large_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (90, 50))
small_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))

for filename in os.listdir(input_folder):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)

        image = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
        if image is None:
            print(f"Error: Cannot load image {filename}. Skipping...")
            continue

        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
        mask_pink = cv2.inRange(hsv, lower_pink, upper_pink)

        mask_combined = cv2.bitwise_or(mask_red1, mask_red2)
        mask_combined = cv2.bitwise_or(mask_combined, mask_pink)

        mask_cleaned = cv2.morphologyEx(mask_combined, cv2.MORPH_CLOSE, small_kernel)
        mask_expanded = cv2.dilate(mask_cleaned, large_kernel, iterations=2)

        mask_inv = cv2.bitwise_not(mask_expanded)

        output = image.copy()
        output[mask_inv > 0] = [255, 255, 255]

        cv2.imwrite(output_path, output)
        print(f"Processed: {filename} -> {output_path}")

print("Processing complete. All images have been saved.")
