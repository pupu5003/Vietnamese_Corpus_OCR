import os
from vietocr.tool.config import Cfg
from vietocr.tool.predictor import Predictor
from PIL import Image
import re

# Load the default configuration
config = Cfg.load_config_from_name('vgg_seq2seq')

# Customize the configuration (optional)
config['weights'] = "vgg_seq2seq.pth"  # Pretrained weights
config['device'] = 'cpu'  # Use 'cuda' for GPU, or 'cpu' for CPU
config['predictor']['beamsearch'] = False  # Set True for beamsearch decoding

detector = Predictor(config)

# Path to the folder containing cropped images
folder_path = 'image_crop/10693454'  # Replace with your actual folder path

# List to store OCR results with Vietnamese text only
ocr_results = []

# Function to check if text contains Vietnamese characters
# def contains_vietnamese(text):
#     vietnamese_chars = "ăâêôơưáàảãạắặằẳẵâấầẩẫậéèẻẽẹếềểễệíìỉĩịóòỏõọốồổỗộớờởỡợúùủũụứừửữựýỳỷỹỵ"
#     return all(char in vietnamese_chars for char in text)

def contains_vietnamese(text):
    # Unicode range for Vietnamese characters
    vietnamese_unicode_ranges = [
        (0x00C0, 0x00FF),  # Latin-1 Supplement (includes some Vietnamese characters)
        (0x0102, 0x0103),  # Ă, ă
        (0x00E2, 0x00E3),  # â, ã
        (0x00E1, 0x00E0, 0x00E3, 0x00E2, 0x00E4),  # á, à, ã, â, ä
        (0x00E9, 0x00E8, 0x00E3, 0x00E2),  # é, è, ê, ơ, ư
        (0x00F4, 0x00F5, 0x00FE),  # ô, ơ, ư
        (0x00FA, 0x00F9, 0x00F5),  # ú, ù, ư
        (0x00DD, 0x00FD),  # ý, ỳ
    ]
    
    for char in text:
        if any(start <= ord(char) <= end for start, end in vietnamese_unicode_ranges):
            return True
    return False

def is_quoc_ngu(text):
    # Remove punctuation except hyphens, spaces, and numbers
    text = re.sub(r'[^\w\sÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚÝàáâãèéêìíòóôõùúýĂăĐđĨĩŨũƠơƯưẠ-ỹ\-]', '', text)
    
    # Regular expression for Vietnamese Latin characters only, allowing spaces, hyphens, and numbers
    vietnamese_pattern = r'^[A-Za-zÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚÝàáâãèéêìíòóôõùúýĂăĐđĨĩŨũƠơƯưẠ-ỹ\s\-]+$'
    
    # Check if the cleaned text matches the Vietnamese Latin character pattern
    return bool(re.match(vietnamese_pattern, text))


# Iterate over the images in the folder
for filename in os.listdir(folder_path):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):  # Check for image file extensions
        image_path = os.path.join(folder_path, filename)
        img = Image.open(image_path)

        # Recognize text using VietOCR
        text_results = detector.predict(img)
        if is_quoc_ngu(text_results):
            ocr_results.append((filename, text_results))

# # Print the OCR results containing only Vietnamese text
# for result in ocr_results:
#     print(f"File: {result[0]}, Text: {result[1]}")

ocr_results.sort(key=lambda x: x[0])

# Print the sorted OCR results
for filename, text in ocr_results:
    print(f"Recognized Text for {filename}:", text)
