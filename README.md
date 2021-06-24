# Speed-Estimate
Speed Estimate

1. File Speed_estimate.py
Giá trị khởi tạo: 
 - loc_before: vị trí xe ở frame trước
 - loc_after : vị trí xe ở frame sau
 - idfr_before: index của frame trước
 - idfr_after: index của frame sau
 - H: ma trận chuyển từ không gian ảnh sang không gian thực
 - fps 
 - coef_x: hệ số hiệu chỉnh m/pixel theo trục x
 - coef_y: hệ số hiệu chỉnh m/pixel theo trục y
 
2. File test.py:
- Thay đổi đường dẫn video và đường dẫn file pkl để chạy test

3. File rectification.py
- chuyển từ không gian ảnh sang không gian thực
- funtion matrix_homorgenous(image) return về ma trận H 
