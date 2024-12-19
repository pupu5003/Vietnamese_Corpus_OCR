import cv2
import numpy as np
import os
##### KHONG CHAY LAI FILE NAY

# Đường dẫn tới thư mục chứa hình ảnh
input_folder = "image/Black/10923624"
output_folder = "processed_images_10923624"

# Tạo thư mục đầu ra nếu chưa tồn tại
os.makedirs(output_folder, exist_ok=True)

# Phạm vi màu
ranges = [
    (np.array([0, 0, 0]), np.array([145, 255, 150]))
]

# Duyệt qua tất cả các thư mục con và tệp trong thư mục gốc
for root, dirs, files in os.walk(input_folder):
    for filename in files:
        # Đường dẫn đầy đủ tới tệp
        input_path = os.path.join(root, filename)
        
        # Kiểm tra nếu là file ảnh
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
            # Đọc hình ảnh
            image = cv2.imread(input_path)
            
            if image is not None:
                # Chuyển đổi sang không gian màu HSV
                hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
                
                # Tạo mask kết hợp cho các vùng màu đen và xám
                combined_mask = np.zeros(hsv.shape[:2], dtype=np.uint8)

                # Tạo mask từ các phạm vi màu đã định nghĩa
                for (lower, upper) in ranges:
                    mask = cv2.inRange(hsv, lower, upper)
                    combined_mask = cv2.bitwise_or(combined_mask, mask)

                # Xử lý hình thái học để làm sạch và mở rộng vùng mask
                kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
                combined_mask = cv2.morphologyEx(combined_mask, cv2.MORPH_CLOSE, kernel)
                combined_mask = cv2.dilate(combined_mask, kernel, iterations=1)

                # Áp dụng inpainting để xóa các vùng được đánh dấu trong mask
                image_no_black = cv2.inpaint(image, combined_mask, inpaintRadius=3, flags=cv2.INPAINT_TELEA)

                # Tạo đường dẫn đầu ra cho thư mục con tương ứng
                output_subfolder = os.path.join(output_folder, os.path.relpath(root, input_folder))
                os.makedirs(output_subfolder, exist_ok=True)
                output_path = os.path.join(output_subfolder, filename)
                cv2.imwrite(output_path, image_no_black)

                print(f"Đã xử lý xong: {filename}. Lưu tại: {output_path}")
            else:
                print(f"Không thể đọc hình ảnh: {filename}")
        else:
            print(f"Bỏ qua tệp không phải là ảnh: {filename}")

print("Hoàn thành xử lý tất cả các ảnh trong thư mục.")
