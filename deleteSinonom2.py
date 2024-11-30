import cv2
import numpy as np
import os

# Đường dẫn tới thư mục chứa hình ảnh
input_folder = "image/Black"
output_folder = "processed_images"

# Tạo thư mục đầu ra nếu chưa tồn tại
os.makedirs(output_folder, exist_ok=True)

# Phạm vi màu đen (broadened to capture more variations of black)
lower_black = np.array([0, 0, 0])     # Màu đen đậm
upper_black = np.array([180, 255, 50])  # Màu đen nhạt (tăng giá trị V để bao gồm xám đậm)

# Tăng kích thước kernel để mở rộng vùng mask
large_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))  # Kernel lớn hơn
small_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))    # Kernel nhỏ hơn

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

                # Tạo mask cho màu đen (cải thiện phạm vi màu đen)
                mask_black = cv2.inRange(hsv, lower_black, upper_black)

                # Mở rộng mask để bao phủ toàn bộ vùng màu đen
                dilated_mask = cv2.dilate(mask_black, large_kernel, iterations=2)  # Mở rộng tối đa hơn
                morphed_mask = cv2.morphologyEx(dilated_mask, cv2.MORPH_CLOSE, small_kernel)  # Làm mịn và kết nối

                # Kiểm tra mask để xác nhận rằng vùng đen đã được phát hiện
                # cv2.imshow('Black Mask', morphed_mask)
                # cv2.waitKey(0)

                # Áp dụng inpainting để xóa vùng đen
                image_no_black = cv2.inpaint(image, morphed_mask, inpaintRadius=10, flags=cv2.INPAINT_TELEA)

                # Tạo đường dẫn đầu ra cho thư mục con tương ứng
                relative_folder = os.path.relpath(root, input_folder)
                output_subfolder = os.path.join(output_folder, relative_folder)
                os.makedirs(output_subfolder, exist_ok=True)

                # Lưu hình ảnh đã xử lý
                output_path = os.path.join(output_subfolder, filename)
                cv2.imwrite(output_path, image_no_black)

                print(f"Đã xử lý xong: {filename}. Lưu tại: {output_path}")
            else:
                print(f"Không thể đọc hình ảnh: {filename}")
        else:
            print(f"Bỏ qua tệp không phải là ảnh: {filename}")

print("Hoàn thành xử lý tất cả các ảnh trong thư mục.")
