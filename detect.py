import cv2
import os
import matplotlib.pyplot as plt
import easyocr

# Path to the folder containing images
input_folder = 'processed_images/10693454'  # Replace with your folder path containing images
output_folder = 'image_crop/10693454'  # Folder where cropped images will be saved

def delete_box(boxes):
    h = len(boxes)
    i = 0
    while i < h:
        if abs(boxes[i][0][0][1] - boxes[i][0][2][1]) >= 200 :
            boxes.pop(i)
            h -= 1
        elif abs(boxes[i][0][0][0] - boxes[i][0][1][0]) <= 50:
            boxes.pop(i)
            h -= 1
        else:
            i += 1
    return boxes

def is_box_within(merged_box, non_merged_box):
    top_left_merged = merged_box[0]
    top_left_non_merged = non_merged_box[0]
    top_right_merged = merged_box[1]
    top_right_non_merged = non_merged_box[1]
    bottom_left_merged = merged_box[3]
    bottom_left_non_merged = non_merged_box[3]
    bottom_right_merged = merged_box[2]
    bottom_right_non_merged = non_merged_box[2]
    return ((top_left_merged[0] < top_left_non_merged[0]) and (top_left_merged[1] < top_left_non_merged[1]) 
        and (top_right_merged[0] > top_right_non_merged[0]) and (top_right_merged[1] < top_right_non_merged[1])
        and (bottom_left_merged[0] < bottom_left_non_merged[0]) and (bottom_left_merged[1] > bottom_left_non_merged[1])
        and (bottom_right_merged[0] > bottom_right_non_merged[0]) and (bottom_right_merged[1] > bottom_right_non_merged[1]))


# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Initialize the OCR reader
reader = easyocr.Reader(['vi', 'en'])  # 'vi' for Vietnamese

# Iterate through each image in the input folder
for filename in os.listdir(input_folder):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):  # Check for image file extensions
        image_path = os.path.join(input_folder, filename)
        image = cv2.imread(image_path)

        # Use EasyOCR to detect and read text from the image
        results = reader.readtext(image_path, height_ths=1.5, slope_ths=0.3, width_ths=6)

        # Extract bounding boxes and sort by the top-left y coordinate
        boxes = [(result[0], result[1]) for result in results]  # List of (bounding box, text)
        boxes.sort(key=lambda x: x[0][0][1])  # Sort by the y coordinate of the top-left corner
        boxes = delete_box(boxes)

        # Group boxes and merge as needed (logic as provided in previous step)
        merged_boxes = []
        non_merged_boxes = []  # List for non-merged boxes
        current_group = []
        variance_threshold = 40  # Y-coordinate variance threshold

        for bbox, text in boxes:
            if not current_group:
                current_group.append((bbox, text))
            else:
                if abs(bbox[0][1] - current_group[0][0][0][1]) <= variance_threshold:
                    current_group.append((bbox, text))
                else:
                    if len(current_group) > 1:
                        x_min = min([point[0] for box, _ in current_group for point in box])
                        y_min = min([point[1] for box, _ in current_group for point in box])
                        x_max = max([point[0] for box, _ in current_group for point in box])
                        y_max = max([point[1] for box, _ in current_group for point in box])
                        merged_boxes.append([[x_min, y_min], [x_max, y_min], [x_max, y_max], [x_min, y_max]])
                    else:
                        for box, _ in current_group:
                            merged_boxes.append(box)
                    current_group = [(bbox, text)]

        if len(current_group) > 1:
            x_min = min([point[0] for box, _ in current_group for point in box])
            y_min = min([point[1] for box, _ in current_group for point in box])
            x_max = max([point[0] for box, _ in current_group for point in box])
            y_max = max([point[1] for box, _ in current_group for point in box])
            merged_boxes.append([[x_min, y_min], [x_max, y_min], [x_max, y_max], [x_min, y_max]])
        else:
            for box, _ in current_group:
                merged_boxes.append(box)

        res = []
        # Remove boxes that are within other boxes
        for i in range(len(merged_boxes)):
            ok = False
            for j in range(len(merged_boxes)):
                if i != j and is_box_within(merged_boxes[j], merged_boxes[i]):
                    ok = True
                    break
            if not ok:
                res.append(merged_boxes[i])

        merged_boxes = res      

        # all_boxes = merged_boxes + non_merged_boxes
        merged_boxes.sort(key=lambda x: (x[0][1], x[0][0]))

        # Crop and save each box as an image
        for i, box in enumerate(merged_boxes):
            # Get the top-left and bottom-right points of the box
            top_left = tuple(map(int, box[0]))
            bottom_right = tuple(map(int, box[2]))

            # Crop the image using the bounding box coordinates
            cropped_image = image[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]

            # Save the cropped image to the output folder
            filename_without_extension = os.path.splitext(filename)[0]
            cropped_image_path = os.path.join(output_folder, f'{filename_without_extension}_cropped_{i + 1:03}.png')
            if cropped_image is None or cropped_image.size == 0:
                print("Error: Cropped image is empty.")
            else:
                cv2.imwrite(cropped_image_path, cropped_image)
                print(f"Image saved to {cropped_image_path}")
print("All images have been processed and cropped images have been saved successfully.")
