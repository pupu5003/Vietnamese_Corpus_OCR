import cv2
import os
import matplotlib.pyplot as plt
import easyocr

# Path to the folder containing images
input_folder = 'processed_images/10693040'  
output_folder = 'image_crop/10693040'
sentence_per_image = 12
def delete_box(boxes):
    h = len(boxes)
    i = 0
    while i < h:
        if abs(boxes[i][0][0][1] - boxes[i][0][2][1]) >= 150:
            boxes.pop(i)
            h -= 1
        elif abs(boxes[i][0][0][0] - boxes[i][0][1][0]) <= 400:
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
reader = easyocr.Reader(['vi', 'en'])  

# Iterate through each image in the input folder
for filename in os.listdir(input_folder):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')): 
        image_path = os.path.join(input_folder, filename)
        image = cv2.imread(image_path)
        image_tmp = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        _, binary = cv2.threshold(image_tmp, 150, 255, cv2.THRESH_BINARY)
        cv2.imwrite('enhanced_image.png', binary)
        results = reader.readtext('enhanced_image.png', height_ths=2, slope_ths=0.9, width_ths=6)


        # Extract bounding boxes and sort by the top-left y coordinate
        boxes = [(result[0], result[1]) for result in results]  # List of (bounding box, text)
        boxes.sort(key=lambda x: x[0][0][1])  # Sort by the y coordinate of the top-left corner
        #Draw bounding box without adding text
        # for box in boxes:
        #     (top_left, top_right, bottom_right, bottom_left) = box[0]
        #     top_left = tuple(map(int, top_left))
        #     bottom_right = tuple(map(int, bottom_right))
        #     cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)  # Bounding box in green
        # plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        # plt.axis('off')  # Hide axes
        # plt.show()

        #boxes = delete_box(boxes)

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
        # Create a subfolder for the current file
        filename_without_extension = os.path.splitext(filename)[0]
        file_output_folder = os.path.join(output_folder, filename_without_extension)
        if not os.path.exists(file_output_folder):
            os.makedirs(file_output_folder)

        index = 0
        # Crop and save each box as an image
        for box in merged_boxes:
            # Get the top-left and bottom-right points of the box
            top_left = tuple(map(int, box[0]))
            bottom_right = tuple(map(int, box[2]))
            if bottom_right[1] <= 200:
                continue
            # Crop the image using the bounding box coordinates
            cropped_image = image[top_left[1]:bottom_right[1],max(251,top_left[0]):bottom_right[0]]

            if cropped_image is None or cropped_image.size == 0 or abs(cropped_image.shape[1]) <= 300: # x<=700
                # print("Empty image, skipping...")
                continue
            else:
                index = index + 1
                # create folder for each sentence
                cropped_image_folder = os.path.join(file_output_folder, f'cropped_{index:03}')
                if not os.path.exists(cropped_image_folder):
                    os.makedirs(cropped_image_folder)   
                cropped_image_path = os.path.join(cropped_image_folder, f'cropped_setence_{index:03}.png') 
                cv2.imwrite(cropped_image_path, cropped_image)
                # create folder to save each word of a sentence
                new_file = os.path.join(cropped_image_folder, f'cropped_word')
                if not os.path.exists(new_file):
                    os.makedirs(new_file)                
                results_word = reader.readtext(cropped_image_path, height_ths =1.5, slope_ths = 9, width_ths = 0.1) 
                word = [(result[0], result[1]) for result in results_word]  # List of (bounding box, text)
                word.sort(key=lambda x: x[0][0][0]) 
                cnt = 0
                # detect and crop word
                for (bbox, text) in word:
                    cnt = cnt + 1
                    (top_left, top_right, bottom_right, bottom_left) = bbox
                    top_left = tuple(map(int, top_left))
                    bottom_right = tuple(map(int, bottom_right))
                    cropped_word_image = cropped_image[max(0, top_left[1] - 10):min(image.shape[0], bottom_right[1] + 7), top_left[0]:bottom_right[0]]
                    cropped_word_image_path = os.path.join(new_file, f'cropped_word_{cnt:03}.png')
                    cv2.imwrite(cropped_word_image_path, cropped_word_image)                
                # print(f"Image saved to {cropped_image_path}")
        if (index > sentence_per_image): print(file_output_folder) 
print("All images have been processed and cropped images have been saved successfully.")