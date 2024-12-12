import json
import os
import re
import glob
data_dict = {
    # id: sentences per page, wide_crop, margin_x, margin_y, width_ths_pass, json, width_ths_word_2, first_word_distance, last_word_distance
    10693040: (12, 400, 250, 120, 10, 'data/BichCauKyNgo.json', 0.1, 90, 150,54),      
    10693454: (11, 400, 200, 10, 10, 'data/ChinhPhuNgam.json', 0.1,90 , 150, 38),       
    10695896: (12, 200, 290, 10, 10, 'data/CungOanNgamKhuc.json', 0, 90, 150,30),      
    10723635: (12, 550, 230, 100, 10, 'data/TrinhThu.json', 0.3, 90, 150,73),    
    10709453: (12, 400, 250, 120, 10, 'data/NhiThapTuHieuDienAm.json', 0.1, 90, 150,32),  
    10722993: (12, 400, 250, 120, 10, 'data/ThuDaLuHoaiNgamKhuc.json', 0.1, 90, 150,13),
    10933018: (12, 400, 250, 120, 10, 'data/NhiDoMai.json', 0.1, 90, 150,67),
}

#load json dictionary
with open('dictionary/dict.json', 'r', encoding='utf-8') as file:
    dictionary = json.load(file)


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
folder = 'processed_images/10933018'  
pdf_id = os.path.basename(folder) 
num_page = data_dict[10933018][9]

dict = parse_json(data_dict[10933018][5])


# Set the base folder and iterate over the pages and j values
base_folder = f'image_crop/{pdf_id}'
j = -1
for i in range(1, num_page + 1):  # Iterating through pages
    page_folder = f'{base_folder}/{pdf_id}_page_{i:03}'
    directories = [d for d in os.listdir(page_folder)]
    directories.sort()
    for cropped_folder in directories:
        j = j + 1
        s = ""
        cropped_folder_path = os.path.join(page_folder, cropped_folder + "/" + "cropped_word")
        if os.path.exists(cropped_folder_path):  # Ensure the cropped_word folder exists
            sentence = dict[j]
            #print(sentence)
            words = re.split(r'[ -]+', sentence)
            directories_2 = [d for d in os.listdir(cropped_folder_path)]
            directories_2.sort()
            # Iterate through all files in the cropped_word folder
            for i, file in enumerate(directories_2):
                file_path = os.path.join(cropped_folder_path, file)
                
                if os.path.isfile(file_path):  # Ensure it's a file
                    name = words[i % len(words)]
                    clean_word = re.sub(r'[^\w\s]', '', name)
                    if clean_word in dictionary:
                        clean_word = dictionary[clean_word]
                    s += clean_word + ' '
                    new_file_name = f"{clean_word}.png"
                    new_file_path = os.path.join(cropped_folder_path, new_file_name)

                    # Check if the file already exists
                    counter = 0
                    while os.path.exists(new_file_path):
                        counter += 1
                        new_file_name = f"{clean_word}_{counter}.png"
                        new_file_path = os.path.join(cropped_folder_path, new_file_name)
                    
                    # Rename the file
                    os.rename(file_path, new_file_path)
                    print(f'Renamed file: {file_path} to {new_file_path}')
        
        txt_path = os.path.join(page_folder, cropped_folder)
        result = cropped_folder.split('_')[1]
        pattern = f"{txt_path}/cropped_sentence_text_{result}.txt"
        with open(pattern, 'w', encoding='utf-8') as f:
            f.write(s)