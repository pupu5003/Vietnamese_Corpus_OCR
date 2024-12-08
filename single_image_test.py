import cv2
import matplotlib.pyplot as plt
import easyocr

# Path to the imagecropped_setence_004.png
# image_path = 'image_crop/10723635/10723635_page_014/cropped_002/cropped_word/cropped_word_003.png'  # Replace with your actual image path
image_path = 'image_crop/10693040/10693040_page_030/cropped_005/cropped_setence_005.png'  # Replace with your actual image path
# image_path = 'processed_images/10693040/10693040_page_043.jpeg'  # Replace with your actual image path


def delete_box(boxes):
    h = len(boxes)
    i = 0
    while i < h:
        print(boxes[i][0][0][1], boxes[i][0][2][1])
        if abs(boxes[i][0][0][1] - boxes[i][0][2][1]) >= 250 :
            print('hihi')
            boxes.pop(i)
            h -= 1
        else:
            i += 1
    return boxes


# Load the image
image = cv2.imread(image_path)
reader = easyocr.Reader(['vi', 'en'])  # 'vi' for Vietnamese

# Use EasyOCR to detect and read text from the image
results = reader.readtext(image_path, height_ths=1.5, slope_ths=5, width_ths=0.01)
print(results)

# Define a color for the bounding box (e.g., red in BGR format)
box_color = (255, 0, 0)  # Blue box
box_thickness = 1  # Thickness of the bounding box lines
word = [(result[0], result[1]) for result in results]  # List of (bounding box, text)
word.sort(key=lambda x: x[0][0][0]) 
print(word)
i = 0
# while i < len(word) - 1:
#     # Check if the current box intersects with the next box
#     if word[i][0][0][0] <= word[i+1][0][0][0] <= word[i][0][2][0]:
#         # Merge the bounding boxes
#         x_min = min(word[i][0][0][0], word[i+1][0][0][0])
#         y_min = min(word[i][0][0][1], word[i+1][0][0][1])
#         x_max = max(word[i][0][2][0], word[i+1][0][2][0])
#         y_max = max(word[i][0][2][1], word[i+1][0][2][1])

#         # Merge the text associated with the boxes
#         merged_text = word[i][1] + word[i+1][1]

#         # Update the current box with merged values
#         word[i] = ([[x_min, y_min], [x_max, y_min], [x_max, y_max], [x_min, y_max]], merged_text)

#         # Remove the next box since it's merged
#         word.pop(i+1)
#     else:
#         # Move to the next box if no merge occurs
#         i += 1

# Draw bounding boxes on the image
# results = delete_box(results)
for result in word:
    bbox = result[0]  # Bounding box coordinates
    print(bbox)
    top_left = tuple(map(int, bbox[0]))
    bottom_right = tuple(map(int, bbox[2]))
    print(image.shape[1])
    cv2.rectangle(image, top_left, bottom_right, box_color, box_thickness)

# Display the image with bounding boxes
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.axis('off')  # Hide axes
plt.show()