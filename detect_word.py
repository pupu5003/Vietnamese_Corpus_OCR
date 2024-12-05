import cv2
import matplotlib.pyplot as plt
import easyocr
image_path = "./processed_images/10693040/10693040_page_001.jpeg"

# Load the image
image = cv2.imread(image_path)
reader = easyocr.Reader(['vi', 'en'])  # 'vi' for Vietnamese

# Use EasyOCR to detect and read text from the image
results = reader.readtext(image_path, height_ths =1.5, slope_ths = 2, width_ths = 0.1) #, height_ths = 0., width_ths = 0, ycenter_ths = 0)

for result in results:
    # Extract bounding box coordinates and text
    box, text, confidence = result
    # Format coordinates to 2 decimal places
    formatted_box = [[round(coord[0], 2), round(coord[1], 2)] for coord in box]
    # Print results
    print(f"{formatted_box}, '{text}', {round(confidence, 4)}")

# Print the extracted text with confidence and bounding box
for (bbox, text, confidence) in results:
    # Draw bounding box without adding text
    (top_left, top_right, bottom_right, bottom_left) = bbox
    top_left = tuple(map(int, top_left))
    bottom_right = tuple(map(int, bottom_right))
    cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)  # Bounding box in green

# Display the image with bounding boxes only
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.axis('off')  # Hide axes
plt.show()