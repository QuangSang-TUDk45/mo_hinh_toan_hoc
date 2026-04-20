# ==============================================================================
# ĐỒ ÁN MÔ HÌNH HÓA TOÁN HỌC: DỰ BÁO SỰ PHÁT TRIỂN KHỐI U VÚ
# ==============================================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from sklearn.datasets import load_breast_cancer

# Cài đặt font chữ và style cho đồ thị nhìn chuyên nghiệp (chuẩn báo cáo khoa học)
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams.update({'font.size': 12})

# ==============================================================================
# 1. TIỀN XỬ LÝ DỮ LIỆU (DATA PREPROCESSING)
# ==============================================================================
print("Đang nạp dữ liệu Breast Cancer Wisconsin...")
# Nạp dataset chuẩn từ thư viện scikit-learn
data = load_breast_cancer(as_frame=True)
df = data.frame

# Trong dataset này, target == 0 là Ác tính (Malignant), target == 1 là Lành tính
df_malignant = df[df['target'] == 0]
mean_radius_malignant = df_malignant['mean radius']

print(f"Số ca ác tính tìm thấy: {len(mean_radius_malignant)}")
print(f"Bán kính Min: {mean_radius_malignant.min():.2f}, Max: {mean_radius_malignant.max():.2f}, Mean: {mean_radius_malignant.mean():.2f}")

# HÌNH 4.1: VẼ BIỂU ĐỒ HISTOGRAM TẦN SUẤT BÁN KÍNH
plt.figure(figsize=(8, 5))
plt.hist(mean_radius_malignant, bins=20, color='crimson', edgecolor='black', alpha=0.7)
# plt.title("Hình 4.1: Phân bố Bán kính sinh thiết (mean_radius) của nhóm Ác tính", fontweight='bold')
plt.xlabel("Bán kính (mm)")
plt.ylabel("Tần suất (Số bệnh nhân)")
plt.savefig("Hinh_4_1_Histogram.png", dpi=300, bbox_inches='tight')
plt.close()


# ==============================================================================
# 2. KHỞI TẠO MA TRẬN THAM SỐ & HÀM CHUYỂN ĐỔI (PARAMETERS SETUP)
# ==============================================================================
# Hàm tính Thể tích hình cầu từ Bán kính
def calc_volume(radius):
    return (4/3) * np.pi * (radius**3)

# Khởi tạo tham số y sinh học (Như Bảng 4.1 trong báo cáo)
K = 1_000_000.0        # Sức chứa tối đa K (mm^3) - Ngưỡng tử vong
a_log = 0.025          # Hệ số Logistic
a_gomp = 0.045         # Tốc độ ban đầu Gompertz
beta = 0.003           # Hệ số phân rã Gompertz
t_days = np.linspace(0, 750, 1000) # Trục thời gian: chạy từ ngày 0 đến 750 (1000 điểm)

# KHAI BÁO 2 PHƯƠNG TRÌNH VI PHÂN (ODEs)
def logistic_model(T, t, a, K):
    dTdt = a * T * (1 - T / K)
    return dTdt

def gompertz_model(T, t, a, beta):
    dTdt = a * np.exp(-beta * t) * T
    return dTdt


# ==============================================================================
# 3. MÔ PHỎNG VÀ VẼ CÁC ĐỒ THỊ BÁO CÁO
# ==============================================================================

# ---------------------------------------------------------
# HÌNH 4.2: SO SÁNH LOGISTIC VÀ GOMPERTZ CHO BỆNH NHÂN SỐ 1
# ---------------------------------------------------------
radius_patient_1 = 17.99
T0_patient_1 = calc_volume(radius_patient_1)

# Giải phương trình vi phân bằng RK4 (odeint của scipy)
T_logistic = odeint(logistic_model, T0_patient_1, t_days, args=(a_log, K))
T_gompertz = odeint(gompertz_model, T0_patient_1, t_days, args=(a_gomp, beta))

plt.figure(figsize=(10, 6))
plt.plot(t_days, T_logistic, 'b-', linewidth=2.5, label='Mô hình Logistic')
plt.plot(t_days, T_gompertz, 'r--', linewidth=2.5, label='Mô hình Gompertz')
plt.axhline(K, color='black', linestyle=':', label='Sức chứa tối đa (K = 1,000,000)')
# plt.title("Hình 4.2: So sánh quỹ đạo phát triển khối u (Bệnh nhân tiêu biểu)", fontweight='bold')
plt.xlabel("Thời gian (Ngày)")
plt.ylabel("Thể tích khối u ($mm^3$)")
plt.legend()
plt.savefig("Hinh_4_2_SoSanh.png", dpi=300, bbox_inches='tight')
plt.close()


# ---------------------------------------------------------
# HÌNH 4.3: MÔ PHỎNG CÁ NHÂN HÓA (PATIENT-SPECIFIC) CHO 3 CA A, B, C
# ---------------------------------------------------------
T0_A = calc_volume(11.0)
T0_B = calc_volume(17.5)
T0_C = calc_volume(25.0)

# Giải Gompertz cho 3 bệnh nhân
T_gomp_A = odeint(gompertz_model, T0_A, t_days, args=(a_gomp, beta))
T_gomp_B = odeint(gompertz_model, T0_B, t_days, args=(a_gomp, beta))
T_gomp_C = odeint(gompertz_model, T0_C, t_days, args=(a_gomp, beta))

plt.figure(figsize=(10, 6))
plt.plot(t_days, T_gomp_A, 'g-', linewidth=2, label=f'Bệnh nhân A (Phát hiện sớm: {T0_A:.0f} mm³)')
plt.plot(t_days, T_gomp_B, 'darkorange', linewidth=2, label=f'Bệnh nhân B (Trung bình: {T0_B:.0f} mm³)')
plt.plot(t_days, T_gomp_C, 'purple', linewidth=2, label=f'Bệnh nhân C (Phát hiện muộn: {T0_C:.0f} mm³)')
plt.axhline(K, color='black', linestyle=':', label='Ngưỡng tử vong K')

# plt.title("Hình 4.3: Mô phỏng phát triển cá nhân hóa (Mô hình Gompertz)", fontweight='bold')
plt.xlabel("Thời gian (Ngày)")
plt.ylabel("Thể tích khối u ($mm^3$)")
plt.legend()
plt.savefig("Hinh_4_3_CaNhanHoa.png", dpi=300, bbox_inches='tight')
plt.close()


# ---------------------------------------------------------
# TÌM THỜI ĐIỂM BÙNG PHÁT (CHO BẢNG 4.2)
# ---------------------------------------------------------
print("\n--- BẢNG 4.2: TÍNH TOÁN NGÀY BÙNG PHÁT ---")
T_inflection = K / np.e  # K/e khoảng 367,879 mm^3

def find_inflection_day(T_array, t_array, T_target):
    # Tìm index đầu tiên mà Thể tích vượt qua Điểm uốn
    idx = np.where(T_array >= T_target)[0]
    if len(idx) > 0:
        return int(t_array[idx[0]])
    return "> 750"

print(f"Ngưỡng bùng phát (K/e) = {T_inflection:.0f} mm³")
print(f"Bệnh nhân A đạt điểm bùng phát vào: Ngày thứ {find_inflection_day(T_gomp_A, t_days, T_inflection)}")
print(f"Bệnh nhân B đạt điểm bùng phát vào: Ngày thứ {find_inflection_day(T_gomp_B, t_days, T_inflection)}")
print(f"Bệnh nhân C đạt điểm bùng phát vào: Ngày thứ {find_inflection_day(T_gomp_C, t_days, T_inflection)}")


# ---------------------------------------------------------
# HÌNH 4.4: PHÂN TÍCH ĐỘ NHẠY (SENSITIVITY ANALYSIS) TRÊN BN "B"
# ---------------------------------------------------------
# Kịch bản 1: Không can thiệp
T_log_base = odeint(logistic_model, T0_B, t_days, args=(a_log, K))

# Kịch bản 2: Hóa trị tiêu chuẩn (Giảm a đi 15%)
a_log_15 = a_log * 0.85
T_log_15 = odeint(logistic_model, T0_B, t_days, args=(a_log_15, K))

# Kịch bản 3: Hóa trị liều cao (Giảm a đi 30%)
a_log_30 = a_log * 0.70
T_log_30 = odeint(logistic_model, T0_B, t_days, args=(a_log_30, K))

plt.figure(figsize=(10, 6))
plt.plot(t_days, T_log_base, 'r-', linewidth=2, label='Kịch bản 1: Không can thiệp (a gốc)')
plt.plot(t_days, T_log_15, 'orange', linewidth=2, linestyle='--', label='Kịch bản 2: Hóa trị chuẩn (Giảm 15% a)')
plt.plot(t_days, T_log_30, 'green', linewidth=2, linestyle='-.', label='Kịch bản 3: Hóa trị cao (Giảm 30% a)')
plt.axhline(500000, color='gray', linestyle=':', label='Mốc theo dõi (500,000 mm³)')

# plt.title("Hình 4.4: Phân tích độ nhạy - Hiệu quả của Hóa trị liệu (Mô hình Logistic)", fontweight='bold')
plt.xlabel("Thời gian (Ngày)")
plt.ylabel("Thể tích khối u ($mm^3$)")
plt.legend()
plt.savefig("Hinh_4_4_PhanTichDoNhay.png", dpi=300, bbox_inches='tight')
plt.close()

print("\nĐã chạy xong! Các đồ thị đã được lưu thành file .png trong thư mục hiện tại.")
