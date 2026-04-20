# 🧬 Dự Báo Động Lực Học Khối U Vú Bằng Phương Trình Vi Phân (ODEs)

## 📌 Tổng quan dự án
Đồ án này ứng dụng **Mô hình hóa Toán học** để dự báo quỹ đạo phát triển của ung thư vú theo thời gian. Khởi đi từ giới hạn của các phương pháp chẩn đoán lâm sàng hiện tại (chỉ cung cấp dữ liệu tĩnh tại một thời điểm sinh thiết), chúng tôi sử dụng **Phương trình Vi phân Thường (ODEs)** để thổi "sức sống động lực học" vào bộ dữ liệu tĩnh, qua đó dự báo thời điểm bùng phát của khối u và lượng hóa hiệu quả của các phác đồ hóa trị.

## 🧮 Cơ sở Toán học
Dự án sử dụng giải tích số học (Thuật toán Runge-Kutta bậc 4) để giải hai mô hình vi phân kinh điển trong sinh lý học:

1. **Mô hình Logistic:**
   $$\frac{dT}{dt} = aT \left(1 - \frac{T}{K}\right)$$
2. **Mô hình Gompertz (Phù hợp nhất cho khối u đặc):**
   $$\frac{dT}{dt} = a e^{-\beta t} T$$

*Trong đó:* 
* $T_0$: Điều kiện ban đầu (Được nội suy từ Bán kính nhân tế bào trong Dataset).
* $a, \beta$: Hệ số tăng trưởng và phân rã sinh học.
* $K$: Sức chứa tối đa (Ngưỡng tử vong sinh lý).

## 📊 Nguồn Dữ liệu
Dự án sử dụng bộ dữ liệu **Breast Cancer Wisconsin (Diagnostic)**.
* Không cần tải file CSV thủ công. Mã nguồn được tích hợp sẵn API để tự động nạp dữ liệu thông qua thư viện `scikit-learn` (`load_breast_cancer`).
* Tính năng sử dụng chính: Lọc nhóm Ác tính (Malignant) và trích xuất trường `mean_radius` để quy đổi sang Thể tích $T_0$ không gian 3 chiều.

## ⚙️ Cài đặt và Chạy mô phỏng

### 1. Yêu cầu hệ thống
* Python 3.8 trở lên.

### 2. Cài đặt thư viện
Mở Terminal / Command Prompt và chạy lệnh sau để cài đặt các thư viện cần thiết:
```bash
pip install numpy pandas matplotlib scipy scikit-learn
```

### 3. Thực thi mã nguồn
Chạy file Python chính của đồ án:
```bash
python main.py
```

## 📈 Kết quả Đầu ra (Outputs)
Khi chạy thành công, script sẽ tự động tạo ra **04 biểu đồ phân tích (định dạng .png độ phân giải cao)** lưu trực tiếp vào thư mục chứa code, bao gồm:
1. `Hinh_4_1_Histogram.png`: Phân bố bán kính sinh thiết của nhóm bệnh nhân ác tính.
2. `Hinh_4_2_SoSanh.png`: Quỹ đạo so sánh đường cong giải tích giữa Logistic và Gompertz.
3. `Hinh_4_3_CaNhanHoa.png`: Mô phỏng dự báo cá nhân hóa cho 3 mức độ bệnh (Sớm, Trung bình, Muộn).
4. `Hinh_4_4_PhanTichDoNhay.png`: Phân tích độ nhạy - Mô phỏng sự lài ra của đường cong vi phân khi áp dụng Thuốc hóa trị.

Đồng thời, Terminal sẽ in ra kết quả tính toán **Đạo hàm bậc hai (Điểm uốn - Inflection Point)**, chỉ định chính xác "Ngày bùng phát" của khối u để khuyến nghị thời điểm phẫu thuật tối ưu.

## 📖 Tài liệu Tham khảo Chính
* A. R. Sheergojri, P. Iqbal, L. Shafi, và R. Khaliq, A Comprehensive Survey on Various Mathematical Modeling Techniques Used for Tumor Dynamics, Computational Algorithms and Numerical Dimensions, 4(3), 249–262, 2025.
* Norton, A Gompertzian model of human breast cancer growth, Cancer Research, 48(24 Part 1), 7067–7071, 1988.
* N. C. Atuegwu và cộng sự, Predicting Patient-Specific Tumor Dynamics: How Many Measurements Are Necessary?, Cancers, 15(4), 1319, 2023.
* UCI Machine Learning Repository, Breast Cancer Wisconsin (Diagnostic) Data Set, 1995.
---
*Đồ án thuộc môn học Mô hình hóa toàn học - Trường Đại Học Quy Nhơn*
