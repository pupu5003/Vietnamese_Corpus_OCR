import cv2
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# Load the image
image_path = "processed_images_10923624/10923624_page_001.jpeg"  # image/Black/10923624/10923624_page_001.jpeg
image = cv2.imread(image_path)
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Resize the image to reduce computational load
image_small = cv2.resize(image_rgb, (1487, 2000)) #(1487, 2000)
pixels_small = image_small.reshape(-1, 3)

# Use KMeans to find the dominant colors
num_colors = 30  # Number of dominant colors to extract
kmeans = KMeans(n_clusters=num_colors, random_state=42)
kmeans.fit(pixels_small)

# Get dominant colors and their counts
dominant_colors = kmeans.cluster_centers_.astype(int)
dominant_counts = np.bincount(kmeans.labels_)

# Sort colors by frequency
sorted_indices = np.argsort(-dominant_counts)
dominant_colors = dominant_colors[sorted_indices]
dominant_counts = dominant_counts[sorted_indices]

# Display the dominant colors as a pie chart
plt.figure(figsize=(10, 6))
plt.title("Dominant Colors in Image")
plt.pie(dominant_counts, labels=[f"Color {i+1}" for i in range(num_colors)], 
        colors=np.array(dominant_colors) / 255)
plt.show()

# Output dominant colors
print("Dominant Colors (RGB):")
for i, color in enumerate(dominant_colors):
    print(f"Color {i+1}: {color}")
