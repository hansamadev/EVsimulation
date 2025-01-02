import numpy as np
import matplotlib.pyplot as plt
import json
import csv
from scipy.interpolate import RegularGridInterpolator
import pandas as pd

# Harici parametre yükleme
with open("config.json", "r") as f:
    config = json.load(f)

# Araç parametreleri (config.json'dan yükleniyor)
P_nominal = config["motor_power"]  # Motor gücü, kW olarak
tau_max = config["max_torque"]
omega_max = config["max_rpm"] * (2 * np.pi / 60)  # Maksimum motor deviri (radyan/s)
E_bat = config["battery_capacity"] * 3600  # kWh'dan J'ye dönüşüm

# Termal parametreler
T_battery = config["initial_battery_temp"]
T_motor = config["initial_motor_temp"]
max_battery_temp = config["max_battery_temp"]
max_motor_temp = config["max_motor_temp"]

# Çevre sıcaklığı (ambient_temp) config dosyasından alınıyor
ambient_temp = config["ambient_temp"]  # Çevre sıcaklığı

# Simülasyon adım süresi
delta_t = config["time_step"]

# Başlangıç durumu
E_bat_remaining = E_bat  # Başlangıçta batarya doluluğu
time = 0  # Başlangıç zamanı
results = []  # Sonuçları saklamak için liste

# 1. **Motor Verim Haritası**
torque_values = np.array([0, 100, 200, 300, 400])  # Tork değerleri (Nm)
rpm_values = np.array([0, 1000, 3000, 5000, 7000])  # RPM değerleri
efficiency_map = np.array([
    [0.80, 0.85, 0.88, 0.90, 0.88],  # 0 Nm
    [0.82, 0.87, 0.90, 0.92, 0.90],  # 100 Nm
    [0.83, 0.88, 0.91, 0.93, 0.91],  # 200 Nm
    [0.81, 0.86, 0.89, 0.91, 0.90],  # 300 Nm
    [0.78, 0.83, 0.87, 0.89, 0.88]   # 400 Nm
])

# Verim haritasını düzenli ızgara interpolasyonu ile oluştur
efficiency_function = RegularGridInterpolator(
    (rpm_values, torque_values), efficiency_map, method='linear'
)

# Motor sıcaklığına göre verim kaybı fonksiyonu (örnek, sıcaklık arttıkça verim azalır)
def efficiency_loss_due_to_temp(T_motor, T_max):
    if T_motor > T_max:
        return 0.9  # %10 verim kaybı
    return 1.0  # Verim kaybı yok

# Motorun ürettiği teorik RPM hesaplaması
def calculate_motor_rpm(P_motor, tau_max, omega_max):
    if P_motor > 0:
        # Güce göre teorik RPM hesaplama
        motor_rpm = min(omega_max, P_motor * 1000 / (tau_max * omega_max))
        return motor_rpm
    return 0  # Güç sıfırsa RPM sıfır

# Motor RPM ve torkunun interpolasyon fonksiyonunun sınırları içinde olup olmadığını kontrol etme
def clamp_values(motor_rpm, motor_torque, rpm_values, torque_values):
    motor_rpm = np.clip(motor_rpm, rpm_values[0], rpm_values[-1])  # RPM sınırlandırma
    motor_torque = np.clip(motor_torque, torque_values[0], torque_values[-1])  # Tork sınırlandırma
    return motor_rpm, motor_torque

# Simülasyon
while E_bat_remaining > 0 and time < 3600:  # 1 saatlik simülasyon
    # Motor RPM ve tork hesaplaması
    motor_rpm = calculate_motor_rpm(P_nominal, tau_max, omega_max)
    motor_torque = P_nominal * 1000 / motor_rpm if motor_rpm > 0 else 0  # Tork hesaplaması

    # RPM ve tork değerlerini sınırlandır
    motor_rpm, motor_torque = clamp_values(motor_rpm, motor_torque, rpm_values, torque_values)

    # Verim hesaplaması
    eta = float(efficiency_function([motor_rpm, motor_torque]))

    # Motor sıcaklığına göre verim kaybı
    eta *= efficiency_loss_due_to_temp(T_motor, max_motor_temp)

    # Motor gücü ve batarya enerji tüketimi
    P_motor = P_nominal * eta  # Motor gücü, verimli çalışacak şekilde
    E_bat_remaining = max(0, E_bat_remaining - P_motor * delta_t)

    # Termal yönetim
    T_motor += (P_motor * delta_t / 1000)  # Daha hızlı motor sıcaklık artışı
    T_battery += (P_motor * delta_t / E_bat) * 0.3  # Batarya sıcaklık artışı
    T_motor -= 0.1 * (T_motor - ambient_temp) * delta_t
    T_battery -= 0.05 * (T_battery - ambient_temp) * delta_t

    # Aşırı sıcaklık kontrolü
    if T_motor > max_motor_temp:
        P_motor *= 0.5  # Motor sıcaklığı yüksekse gücü düşür
        print("Motor sıcaklığı çok yüksek, güç sınırlandırılıyor.")
    if T_battery > max_battery_temp:
        P_motor *= 0.7  # Batarya sıcaklığı yüksekse gücü düşür
        print("Batarya sıcaklığı çok yüksek, enerji tüketimi düşürülüyor.")

    # Zaman güncelleme
    time += delta_t

    # Sonuçları kaydet
    soc = E_bat_remaining / E_bat * 100
    results.append([time, motor_rpm, P_motor / 1000, soc, T_battery, T_motor])

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
motor_rpms = results_np[:, 1]
powers = results_np[:, 2]
socs = results_np[:, 3]
battery_temps = results_np[:, 4]
motor_temps = results_np[:, 5]

# Motor verimliliği hesaplama
motor_efficiency = [float(efficiency_function([motor_rpm, motor_torque])) for motor_rpm, motor_torque in zip(motor_rpms, powers)]

# Görselleştirme
plt.figure(figsize=(18, 12))

# Motor Verimliliği Grafiği
plt.subplot(3, 2, 1)
plt.plot(times, motor_efficiency, label="Motor Verimliliği", color="blue")
plt.xlabel("Zaman (s)")
plt.ylabel("Verimlilik (%)")
plt.title("Motor Verimliliği Grafiği")
plt.grid()

# Motor Gücü (kW) Grafiği
plt.subplot(3, 2, 2)
plt.plot(times, powers, label="Motor Gücü (kW)", color="orange")
plt.xlabel("Zaman (s)")
plt.ylabel("Motor Gücü (kW)")
plt.title("Motor Gücü Grafiği")
plt.grid()

# Batarya Durumu (SOC) Grafiği
plt.subplot(3, 2, 3)
plt.plot(times, socs, label="SOC (%)", color="green")
plt.xlabel("Zaman (s)")
plt.ylabel("SOC (%)")
plt.title("Batarya Durumu (SOC)")
plt.grid()

# Motor Sıcaklığı (°C) Grafiği
plt.subplot(3, 2, 4)
plt.plot(times, motor_temps, label="Motor Sıcaklığı (°C)", color="purple")
plt.xlabel("Zaman (s)")
plt.ylabel("Motor Sıcaklığı (°C)")
plt.title("Motor Sıcaklığı")
plt.grid()

# Batarya Sıcaklığı (°C) Grafiği
plt.subplot(3, 2, 5)
plt.plot(times, battery_temps, label="Batarya Sıcaklığı (°C)", color="blue")
plt.xlabel("Zaman (s)")
plt.ylabel("Batarya Sıcaklığı (°C)")
plt.title("Batarya Sıcaklığı")
plt.grid()

plt.tight_layout()
plt.show()

# Sonuçları CSV olarak kaydetme
df = pd.DataFrame(results, columns=["Zaman (s)", "Motor RPM", "Motor Gücü (kW)", "SOC (%)", "Batarya Sıcaklığı (°C)", "Motor Sıcaklığı (°C)"])
df.to_csv("simulasyon_sonuclari.csv", index=False)
