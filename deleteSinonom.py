import cv2
import numpy as np
import os

# Đường dẫn tới thư mục chứa hình ảnh
input_folder = "image/10693454"
output_folder = "processed_images/10693454"

# Tạo thư mục đầu ra nếu chưa tồn tại
os.makedirs(output_folder, exist_ok=True)

# Định nghĩa phạm vi màu đỏ trong HSV
lower_red1 = np.array([0, 50, 50])    # Đỏ sáng
upper_red1 = np.array([10, 255, 255])
lower_red2 = np.array([170, 50, 50])  # Đỏ đậm
upper_red2 = np.array([180, 255, 255])

# Duyệt qua từng tệp trong thư mục
for filename in os.listdir(input_folder):
    # Đường dẫn đầy đủ tới tệp
    input_path = os.path.join(input_folder, filename)
    
    # Kiểm tra nếu là file ảnh
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
        # Đọc hình ảnh
        image = cv2.imread(input_path)
        
        if image is not None:
            # Chuyển đổi sang không gian màu HSV
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

            # Tạo mask cho màu đỏ
            mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
            mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
            red_mask = cv2.bitwise_or(mask1, mask2)

            # Mở rộng vùng bị mask để làm mịn biên
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
            dilated_mask = cv2.dilate(red_mask, kernel, iterations=2)

            # Sử dụng inpainting để tái tạo nền
            image_no_red = cv2.inpaint(image, dilated_mask, inpaintRadius=3, flags=cv2.INPAINT_TELEA)

            # Lưu hình ảnh đã xử lý
            output_path = os.path.join(output_folder, filename)
            cv2.imwrite(output_path, image_no_red)

            print(f"Đã xử lý xong: {filename}. Lưu tại: {output_path}")
        else:
            print(f"Không thể đọc hình ảnh: {filename}")
    else:
        print(f"Bỏ qua tệp không phải là ảnh: {filename}")

print("Hoàn thành xử lý tất cả các ảnh trong thư mục.")
