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
- Chạy câu lệnh sau để test 

python test.py --videopath "data_speed/video_test/car_hightway.mp4" --resultpath "car_hightway.mp4"  --pklpath "data_speed/pkl_test/car_hightway.pkl" --widthreal "150" --heightreal "70"

3. File rectification.py
- chuyển từ không gian ảnh sang không gian thực
- funtion matrix_homorgenous(image) return về ma trận H 
