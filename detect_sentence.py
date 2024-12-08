import cv2
import os
import matplotlib.pyplot as plt
import easyocr
import shutil
import json
import re


data_dict = {
    # id: sentences per page, wide_crop, margin_x, margin_y, width_ths_pass, json, width_ths_word_2, first_word_distance, last_word_distance
    10693040: (12, 400, 250, 120, 10, 'data/BichCauKyNgo.json', 0.01, 90, 150),      
    10693454: (11, 400, 200, 10),       
    10695896: (12, 200, 290, 10),     
    10723635: (12, 550, 230, 100, 10, 'data/TrinhThu.json', 0.3, 90, 150),            
}

def shift_and_insert_image(folder_path, new_image_path, insert_index):
    # List all files in the folder and sort them by numerical order
    existing_files = sorted(
        [f for f in os.listdir(folder_path) if f.startswith('cropped_word_') and f.endswith('.png')],
        key=lambda x: int(x.split('_')[-1].split('.')[0])
    )

    # Shift files from the end to make space
    for file in reversed(existing_files):
        current_index = int(file.split('_')[-1].split('.')[0])
        if current_index >= insert_index:
            new_name = f"cropped_word_{current_index + 1:03}.png"
            os.rename(os.path.join(folder_path, file), os.path.join(folder_path, new_name))

    # Copy the new image to the folder with the correct name
    new_image_name = f"cropped_word_{insert_index:03}.png"
    shutil.copy(new_image_path, os.path.join(folder_path, new_image_name))

def parse_json(json_file):
    with open(json_file, 'r') as f:
        json_data = f.read()
        parsed_json = json.loads(json_data)

    # Extracting all values from each dictionary in the list
    result = []
    for item in parsed_json:
        for key, value in item.items():
            result.extend(value)  
    return result

# Path to the folder containing images
input_folder = 'processed_images/10693040'  
pdf_id = os.path.basename(input_folder) 
output_folder = f'image_crop/{pdf_id}'

sentence_per_image = data_dict[int(pdf_id)][0]
crop_image_wide = data_dict[int(pdf_id)][1]
margin_x = data_dict[int(pdf_id)][2]
margin_y = data_dict[int(pdf_id)][3]
width_ths_pass = data_dict[int(pdf_id)][4]
json_file = parse_json(data_dict[int(pdf_id)][5])
width_ths_word_2 = data_dict[int(pdf_id)][6]
first_word_distance = data_dict[int(pdf_id)][7]
last_word_distance = data_dict[int(pdf_id)][8]
current_sentence = 0

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

directories = [d for d in os.listdir(input_folder)]
directories.sort()
# Iterate through each image in the input folder
for filename in directories:
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')): 
        image_path = os.path.join(input_folder, filename)
        image = cv2.imread(image_path)
        # image_tmp = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        # _, binary = cv2.threshold(image_tmp, 150, 255, cv2.THRESH_BINARY)
        # cv2.imwrite('enhanced_image.png', binary)
        results = reader.readtext(image_path, height_ths=3, slope_ths=6, width_ths=width_ths_pass)


        # Extract bounding boxes and sort by the top-left y coordinate
        boxes = [(result[0], result[1]) for result in results]  # List of (bounding box, text)
        boxes.sort(key=lambda x: x[0][0][1])  # Sort by the y coordinate of the top-left corner

        # Group boxes and merge as needed (logic as provided in previous step)
        merged_boxes = []
        non_merged_boxes = []  # List for non-merged boxes
        current_group = []
        variance_threshold = 50  # Y-coordinate variance threshold

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
            if bottom_right[1] <= margin_y:
                continue

            if bottom_right[0] <= margin_x:
                continue 

            if top_left[0] < margin_x:
                top_left = (margin_x, top_left[1])

            cropped_image = image[top_left[1]-10:bottom_right[1]+10, max(top_left[0]-130, margin_x):min(bottom_right[0]+200, image.shape[1])]

            if cropped_image is None or cropped_image.size == 0 or abs(cropped_image.shape[1]) <= crop_image_wide: 
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
                results_word = reader.readtext(cropped_image_path, height_ths =1.5, slope_ths = 5, width_ths = width_ths_word_2) 
                word = [(result[0], result[1]) for result in results_word]  # List of (bounding box, text)
                word.sort(key=lambda x: x[0][0][0]) 
                if not word:
                    if os.path.exists(cropped_image_folder):
                        shutil.rmtree(cropped_image_folder)
                    index = index - 1
                    continue

                i=0
                current_sentence = current_sentence + 1
                while i < len(word) - 1:
                    # Calculate the widths of the current box and the next box
                    width_i = word[i][0][2][0] - word[i][0][0][0]
                    width_next = word[i+1][0][2][0] - word[i+1][0][0][0]

                    # Check if the sum of widths is >= 200
                    if width_i + width_next >= 200:
                        i += 1  # Skip merging if the sum of widths is too large
                        continue

                    # Check if the current box intersects with the next box
                    if word[i][0][0][0] <= word[i+1][0][0][0] <= word[i][0][2][0]:
                        # Merge the bounding boxes
                        x_min = min(word[i][0][0][0], word[i+1][0][0][0])
                        y_min = min(word[i][0][0][1], word[i+1][0][0][1])
                        x_max = max(word[i][0][2][0], word[i+1][0][2][0])
                        y_max = max(word[i][0][2][1], word[i+1][0][2][1])

                        # Merge the text associated with the boxes
                        merged_text = word[i][1] + word[i+1][1]

                        # Update the current box with merged values
                        word[i] = ([[x_min, y_min], [x_max, y_min], [x_max, y_max], [x_min, y_max]], merged_text)

                        # Remove the next box since it's merged
                        word.pop(i+1)
                    else:
                        # Move to the next box if no merge occurs
                        i += 1    

                cnt = 0
                # detect and crop word
                for i, (bbox, text) in enumerate(word):
                    (top_left, top_right, bottom_right, bottom_left) = bbox
                    top_left = tuple(map(int, top_left))
                    bottom_right = tuple(map(int, bottom_right))
                    cropped_word_image = cropped_image[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
                    if cropped_word_image is None or cropped_word_image.size == 0: 
                        continue
                    
                    # print(filename, ' ', cropped_word_image.shape[1], ' ', cnt)
                    if cropped_word_image.shape[1] >= 200:
                        # Perform OCR on the oversized crop
                        tmps = reader.readtext(cropped_word_image, height_ths=1, slope_ths=5, width_ths=0.01)
                        # If OCR detects multiple results, save each as a separate image
                        if len(tmps) >= 2:
                            w = [(tmp[0], tmp[1]) for tmp in tmps]  # List of (bounding box, text)
                            w.sort(key=lambda x: x[0][0][0]) 
                            for (bbox, text) in w:
                                cnt = cnt + 1
                                (top_left, top_right, bottom_right, bottom_left) = bbox
                                top_left = tuple(map(int, top_left))
                                bottom_right = tuple(map(int, bottom_right))
                                cropped_word_image_tmp = cropped_word_image[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
                                if cropped_word_image_tmp is None or cropped_word_image_tmp.size == 0: 
                                    continue
                                cropped_word_image_path = os.path.join(new_file, f'cropped_word_{cnt:03}.png')
                                cv2.imwrite(cropped_word_image_path, cropped_word_image_tmp)
                            continue  # Skip saving the original crop since it's split into multiple images

                    cnt = cnt + 1
                    cropped_word_image_path = os.path.join(new_file, f'cropped_word_{cnt:03}.png')
                    cv2.imwrite(cropped_word_image_path, cropped_word_image)  
                
                word_count_ground = len(re.split(r'[ -]+', json_file[current_sentence - 1]))
                if cnt != word_count_ground:
                    # Load the cropped image
                    cropped_image_1 = cv2.imread(cropped_image_path)
                    tmp_cnt = 0
                    distance = 0
                    max_indices = None

                    # Middel words
                    for j in range(1, len(word)):
                        # Calculate the horizontal distance between top-left of current box and top-right of previous box
                        current_distance = word[j][0][0][0] - word[j-1][0][1][0]
                        if current_distance > 150:
                            x_start = int(word[j-1][0][1][0])  # Convert to integer
                            x_end = int(word[j][0][0][0])      # Convert to integer
                            y_start = int(word[j-1][0][1][1])  # Convert to integer
                            y_end = int(word[j][0][3][1])      # Convert to integer

                            # Crop the space between the two boxes
                            cropped_space = cropped_image_1[y_start:y_end, x_start:x_end]

                            # Save the cropped space
                            if cropped_space is not None and cropped_space.size > 0:
                                cnt = cnt + 1
                                tmp_cnt = tmp_cnt + 1
                                cropped_space_temp_path = os.path.join(new_file, f'temp_cropped_space_{tmp_cnt:03}.png')
                                cv2.imwrite(cropped_space_temp_path, cropped_space)
                                # print(f"Temporary cropped space image saved at {cropped_space_temp_path}")

                                # Insert the image at the correct position in the folder
                                shift_and_insert_image(new_file, cropped_space_temp_path, j+1)
                                os.remove(cropped_space_temp_path)  # Clean up temporary file
                    
                    # Last, First word
                    if cnt != word_count_ground:
                        if word and abs(word[0][0][0][0]) > first_word_distance:
                            x_start = 0
                            x_end = int(word[0][0][0][0])
                            y_start = 0
                            y_end = int(cropped_image_1.shape[0])
                            # Crop the space between the two boxes
                            cropped_space = cropped_image_1[y_start:y_end, x_start:x_end]

                            # Save the cropped space
                            if cropped_space is not None and cropped_space.size > 0:
                                cnt = cnt + 1
                                tmp_cnt = tmp_cnt + 1
                                cropped_space_temp_path = os.path.join(new_file, f'temp_cropped_space_{tmp_cnt:03}.png')
                                cv2.imwrite(cropped_space_temp_path, cropped_space)
                                # Insert the image at the correct position in the folder
                                shift_and_insert_image(new_file, cropped_space_temp_path, 1)
                                os.remove(cropped_space_temp_path)  # Clean up temporary file

                        # Last word
                        if word and abs(word[len(word)-1][0][1][0] - cropped_image_1.shape[1]) > last_word_distance:
                            x_start = int(word[len(word)-1][0][1][0])
                            x_end = int(cropped_image_1.shape[1])
                            y_start = 0
                            y_end = int(cropped_image_1.shape[0])
                            # Crop the space between the two boxes
                            cropped_space = cropped_image_1[y_start:y_end, x_start:x_end]

                            # Save the cropped space
                            if cropped_space is not None and cropped_space.size > 0:
                                cnt = cnt + 1
                                tmp_cnt = tmp_cnt + 1
                                cropped_space_temp_path = os.path.join(new_file, f'temp_cropped_space_{tmp_cnt:03}.png')
                                cv2.imwrite(cropped_space_temp_path, cropped_space)
                                # print(f"Temporary cropped space image saved at {cropped_space_temp_path}")
                                file_count = len([f for f in os.listdir(new_file) if os.path.isfile(os.path.join(new_file, f))])
                                shift_and_insert_image(new_file, cropped_space_temp_path, file_count)
                                os.remove(cropped_space_temp_path)  # Clean up temporary file
                        
                if cnt != word_count_ground:
                    print(new_file, ' ', cnt, ' ', word_count_ground, ' ', json_file[current_sentence-1]) #Error file

                cropped_image_text_path = os.path.join(cropped_image_folder, f'cropped_sentence_text_{index:03}.txt')
                text_to_store = json_file[current_sentence-1] 
                with open(cropped_image_text_path, 'w', encoding='utf-8') as txt_file:
                    txt_file.write(text_to_store)
                # print(filename, ' ', index, ' ', cnt, ' ', word_count_ground, ' ', json_file[current_sentence-1])
        if (index != sentence_per_image): 
            current_sentence = current_sentence - (index - sentence_per_image)
            print(file_output_folder) 
print("All images have been processed and cropped images have been saved successfully.")
