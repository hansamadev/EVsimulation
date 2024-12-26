import numpy as np
import matplotlib.pyplot as plt
import json
import csv
from scipy.interpolate import interp2d  # 2D interpolasyon için

# Harici parametre yükleme
with open("config.json", "r") as f:
    config = json.load(f)

# Araç parametreleri
P_nominal = config["motor_power"]
tau_max = config["max_torque"]
omega_max = config["max_rpm"] * (2 * np.pi / 60)
E_bat = config["battery_capacity"] * 3600

# Araç dinamikleri
m = config["vehicle_mass"]
C_d = config["aero_drag_coeff"]
A = config["frontal_area"]
rho = config["air_density"]
mu = config["traction_coeff"]
ambient_temp = config["ambient_temp"]

# Termal parametreler
T_battery = config["initial_battery_temp"]
T_motor = config["initial_motor_temp"]
max_battery_temp = config["max_battery_temp"]
max_motor_temp = config["max_motor_temp"]

# Yol segmentleri
road_segments = config["road_segments"]

# Simülasyon adım süresi
delta_t = config["time_step"]

# Başlangıç durumu
v = 0
d = 0
E_bat_remaining = E_bat
time = 0
results = []

# 1. **Motor Verim Haritası**
# Tork (Nm) ve hız (RPM) değerlerine göre verim tablosu
torque_values = np.array([0, 100, 200, 300, 400])  # Tork değerleri
rpm_values = np.array([0, 1000, 3000, 5000, 7000])  # Hız değerleri (RPM)
efficiency_map = np.array([
    [0.80, 0.85, 0.88, 0.90, 0.88],  # 0 Nm
    [0.82, 0.87, 0.90, 0.92, 0.90],  # 100 Nm
    [0.83, 0.88, 0.91, 0.93, 0.91],  # 200 Nm
    [0.81, 0.86, 0.89, 0.91, 0.90],  # 300 Nm
    [0.78, 0.83, 0.87, 0.89, 0.88],  # 400 Nm
])

# Verim haritasını interpolasyon fonksiyonuna dönüştür
efficiency_function = interp2d(rpm_values, torque_values, efficiency_map, kind='linear')

# Simülasyon
for segment in road_segments:
    segment_start_distance = d
    segment_length = segment["length"]
    slope_angle = np.radians(segment["slope"])
    C_rr = segment.get("rolling_resistance", 0.01)

    while d - segment_start_distance < segment_length and E_bat_remaining > 0:
        # Eğime bağlı kuvvet
        F_slope = m * 9.81 * np.sin(slope_angle)

        # Aerodinamik direnç
        F_drag = 0.5 * rho * C_d * A * v**2

        # Yuvarlanma direnci
        F_rr = C_rr * m * 9.81 * np.cos(slope_angle)

        # Maksimum çekiş kuvveti
        F_traction_max = mu * m * 9.81
        F_motor_max = min(tau_max * omega_max / (v + 1e-3), P_nominal / (v + 1e-3))
        F_traction = min(F_traction_max, F_motor_max)

        # Hız ve tork hesaplaması
        motor_rpm = (v * 60) / (2 * np.pi)  # Hızdan RPM'e dönüşüm
        motor_torque = F_traction / (tau_max / omega_max)  # Kuvvetten torka

        # Verim interpolasyonu
        eta = float(efficiency_function(motor_rpm, motor_torque))

        # Net kuvvet ve ivme
        F_net = F_traction - F_drag - F_rr - F_slope
        a = F_net / m

        # Hız ve pozisyon güncelleme
        v = max(v + a * delta_t, 0)
        d += v * delta_t

        # Motor gücü ve batarya enerji tüketimi
        P_motor = max(F_traction * v / eta, 0)
        if F_net < 0 and v > 0 and E_bat_remaining < E_bat:
            P_recovered = -F_net * v * eta
            E_bat_remaining = min(E_bat, E_bat_remaining + max(P_recovered * delta_t, 0))
        else:
            E_bat_remaining = max(0, E_bat_remaining - P_motor * delta_t)

        # Termal yönetim
        T_motor += (P_motor * delta_t / 10000)
        T_battery += (P_motor * delta_t / E_bat) * 0.01
        T_motor -= 0.1 * (T_motor - ambient_temp) * delta_t
        T_battery -= 0.05 * (T_battery - ambient_temp) * delta_t

        # Aşırı sıcaklık kontrolü
        if T_motor > max_motor_temp:
            F_traction *= 0.5
            print("Motor sıcaklığı çok yüksek, güç sınırlandırılıyor.")
        if T_battery > max_battery_temp:
            P_motor *= 0.7
            print("Batarya sıcaklığı çok yüksek, enerji tüketimi düşürülüyor.")

        # Zaman güncelleme
        time += delta_t

        # Sonuçları kaydet
        soc = E_bat_remaining / E_bat * 100
        results.append([time, v * 3.6, d, soc, P_motor / 1000, F_traction, T_battery, T_motor])

        # Simülasyon durdurma koşulları
        if E_bat_remaining <= 0:
            print("Simülasyon durduruldu: Batarya tamamen boşaldı.")
            break
        if T_motor > max_motor_temp or T_battery > max_battery_temp:
            print("Simülasyon durduruldu: Aşırı sıcaklık.")
            break

# Çıktıların ayrıştırılması
results_np = np.array(results)
times = results_np[:, 0]
velocities = results_np[:, 1]
distances = results_np[:, 2]
socs = results_np[:, 3]
powers = results_np[:, 4]
torques = results_np[:, 5]
battery_temps = results_np[:, 6]
motor_temps = results_np[:, 7]

# Görselleştirme
plt.figure(figsize=(18, 12))

# Hız Grafiği
plt.subplot(3, 2, 1)
plt.plot(times, velocities, label="Hız (km/h)")
plt.xlabel("Zaman (s)")
plt.ylabel("Hız (km/h)")
plt.title("Hız Grafiği")
plt.grid()

# Pozisyon Grafiği
plt.subplot(3, 2, 2)
plt.plot(times, distances, label="Pozisyon (m)", color="orange")
plt.xlabel("Zaman (s)")
plt.ylabel("Pozisyon (m)")
plt.title("Pozisyon Grafiği")
plt.grid()

# Batarya Durumu (SOC)
plt.subplot(3, 2, 3)
plt.plot(times, socs, label="SOC (%)", color="green")
plt.xlabel("Zaman (s)")
plt.ylabel("SOC (%)")
plt.title("Batarya Durumu (SOC)")
plt.grid()

# Güç Grafiği
plt.subplot(3, 2, 4)
plt.plot(times, powers, label="Güç (kW)", color="red")
plt.xlabel("Zaman (s)")
plt.ylabel("Güç (kW)")
plt.title("Motor Gücü")
plt.grid()

# Termal Yönetim
plt.subplot(3, 2, 5)
plt.plot(times, battery_temps, label="Batarya Sıcaklığı (°C)", color="blue")
plt.plot(times, motor_temps, label="Motor Sıcaklığı (°C)", color="purple")
plt.xlabel("Zaman (s)")
plt.ylabel("Sıcaklık (°C)")
plt.title("Termal Yönetim")
plt.legend()
plt.grid()

plt.tight_layout()
plt.show()

# Sonuçları CSV olarak kaydetme
with open("simulasyon_sonuclari.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Zaman (s)", "Hız (km/h)", "Pozisyon (m)", "SOC (%)", "Güç (kW)", "Tork (Nm)", "Batarya Sıcaklığı (°C)", "Motor Sıcaklığı (°C)"])
    writer.writerows(results)
