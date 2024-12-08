import cv2
import numpy as np
import os
##### KHONG CHAY LAI FILE NAY

# Đường dẫn tới thư mục chứa hình ảnh
input_folder = "image/Red/10693040"
output_folder = "processed_images/10693040"

# Tạo thư mục đầu ra nếu chưa tồn tại
os.makedirs(output_folder, exist_ok=True)

# Định nghĩa phạm vi màu đỏ và hồng trong HSV
lower_red1 = np.array([0, 50, 50])    # Đỏ sáng
upper_red1 = np.array([10, 255, 255])
lower_red2 = np.array([170, 50, 50])  # Đỏ đậm
upper_red2 = np.array([180, 255, 255])

# Thêm phạm vi màu hồng vào giữa (từ khoảng 140 đến 170 trong Hue)
lower_pink = np.array([140, 50, 50])  # Hồng sáng
upper_pink = np.array([170, 255, 255]) # Hồng đậm (có thể thay đổi để bao gồm phạm vi rộng hơn)

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

                # Tạo mask cho màu đỏ và hồng
                mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
                mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
                mask_pink = cv2.inRange(hsv, lower_pink, upper_pink)

                # Kết hợp các mask màu đỏ và hồng
                red_pink_mask = cv2.bitwise_or(mask_red1, mask_red2)
                red_pink_mask = cv2.bitwise_or(red_pink_mask, mask_pink)

                # Xử lý hình thái học để mở rộng và làm sạch vùng đỏ/hồng
                dilated_mask = cv2.dilate(red_pink_mask, large_kernel, iterations=1)  # Mở rộng tối đa
                morphed_mask = cv2.morphologyEx(dilated_mask, cv2.MORPH_CLOSE, small_kernel)  # Làm mịn và kết nối

                # Áp dụng inpainting để xóa vùng đỏ và hồng
                image_no_red_pink = cv2.inpaint(image, morphed_mask, inpaintRadius=3, flags=cv2.INPAINT_TELEA)

                # Tạo đường dẫn đầu ra cho thư mục con tương ứng
                relative_folder = os.path.relpath(root, input_folder)
                output_subfolder = os.path.join(output_folder, relative_folder)
                os.makedirs(output_subfolder, exist_ok=True)

                # Lưu hình ảnh đã xử lý
                output_path = os.path.join(output_subfolder, filename)
                cv2.imwrite(output_path, image_no_red_pink)

                print(f"Đã xử lý xong: {filename}. Lưu tại: {output_path}")
            else:
                print(f"Không thể đọc hình ảnh: {filename}")
        else:
            print(f"Bỏ qua tệp không phải là ảnh: {filename}")

print("Hoàn thành xử lý tất cả các ảnh trong thư mục.")
