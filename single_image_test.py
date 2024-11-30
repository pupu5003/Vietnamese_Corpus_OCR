import cv2
import matplotlib.pyplot as plt
import easyocr

# Path to the image
image_path = '67a4a488-24ce-4989-a715-9c5947d84784.jpeg'  # Replace with your actual image path

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
results = reader.readtext(image_path, height_ths=1, slope_ths=0.3, width_ths=6)

# Define a color for the bounding box (e.g., red in BGR format)
box_color = (255, 0, 0)  # Blue box
box_thickness = 1  # Thickness of the bounding box lines

# Draw bounding boxes on the image
print(len(results))
results = delete_box(results)
print(len(results))
for result in results:
    bbox = result[0]  # Bounding box coordinates
    print(bbox)
    top_left = tuple(map(int, bbox[0]))
    bottom_right = tuple(map(int, bbox[2]))
    cv2.rectangle(image, top_left, bottom_right, box_color, box_thickness)

# Display the image with bounding boxes
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.axis('off')  # Hide axes
plt.show()