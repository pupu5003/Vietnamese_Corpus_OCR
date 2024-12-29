import json
import os

def count_poem_lines_and_words(file_path):
    # Load the JSON file
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    total_lines = 0
    total_words = 0

    for part in data:
        for title, lines in part.items():
            for line in lines:
                # Exclude lines containing ellipses (\u22ef) and skip empty lines
                if '\u22ef' in line or not line.strip():
                    continue

                # Count the line
                total_lines += 1

                # Count words in the line, excluding '\u22ef'
                words = [word for word in line.split() if word != '\u22ef']
                total_words += len(words)

    return total_lines, total_words

# Specify the folder path
folder_path = 'data/'

# Initialize overall counts
overall_lines = 0
overall_words = 0

# Process each JSON file in the folder
for file_name in os.listdir(folder_path):
    if file_name.endswith('.json'):  # Only process JSON files
        file_path = os.path.join(folder_path, file_name)
        lines_count, words_count = count_poem_lines_and_words(file_path)
        print(f"File: {file_name}")
        print(f"  Number of lines: {lines_count}")
        print(f"  Number of words: {words_count}")
        overall_lines += lines_count
        overall_words += words_count

# Print overall totals
print(f"Overall Total Lines: {overall_lines}")
print(f"Overall Total Words: {overall_words}")
