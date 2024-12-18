import os

# Get the current directory
# directory = 'image_crop/10723635/10723635_page_014/cropped_002/cropped_word'

file_paths = []

# Open the aaa.txt file for reading
with open('error/10729022.txt', 'r') as file:
    for line in file:
        parts = line.split()
        for part in parts:
            if part.startswith('image_crop'):
                file_paths.append(part)

# List all PNG files in the directory
for directory in file_paths:
    files = [f for f in os.listdir(directory) if f.endswith('.png')]
    files.sort()

    # Loop through each file and rename it
    for index, file in enumerate(files, start=1):
        # Create the new name using zero-padded numbers
        new_name = f"crop_word_{index:03d}.png"
        # Get the full path of the current and new file names
        old_file = os.path.join(directory, file)
        new_file = os.path.join(directory, new_name)
        # Rename the file
        os.rename(old_file, new_file)
        print(f"Renamed: {file} to {new_name}")