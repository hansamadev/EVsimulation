import numpy as np
import matplotlib.pyplot as plt
import csv

# Sabitler
g = 9.81  # Yer çekimi ivmesi (m/s^2)
rho = 1.2  # Hava yoğunluğu (kg/m^3)

# Kullanıcı tarafından ayarlanabilir giriş parametreleri
P_nominal = 250000  # Motor Nominal Gücü (W)
tau_max = 400  # Maksimum Tork (Nm)
omega_max = 20000 * (2 * np.pi / 60)  # Maksimum Devir (rad/s)
eta = 0.95  # Ortalama Motor Verimi

E_bat = 80 * 3600  # Batarya Kapasitesi (Wh to Joules)
V = 400  # Besleme Gerilimi (V)
I_max = 600  # Maksimum Akım Çekişi (A)

m = 900  # Araç Kütlesi (kg)
C_d = 0.24  # Aerodinamik Sürtünme Katsayısı
A = 1.6  # Araç Kesit Alanı (m^2)
C_rr = 0.01  # Yuvarlanma Direnci Katsayısı
mu = 1.2  # Lastik Yol Tutuş Katsayısı

# Ek özellikler
road_segments = [
    {"length": 500, "slope": 0},      # Düz yol
    {"length": 200, "slope": 5},      # %5 yokuş yukarı
    {"length": 300, "slope": -3}      # %3 yokuş aşağı
]

T_battery = 25  # Başlangıç batarya sıcaklığı (°C)
T_motor = 25    # Başlangıç motor sıcaklığı (°C)
max_battery_temp = 60  # Maksimum batarya sıcaklığı (°C)
max_motor_temp = 100   # Maksimum motor sıcaklığı (°C)

delta_t = 0.1  # Simülasyon adım süresi (s)

# Başlangıç durumu
v = 0  # Başlangıç hızı (m/s)
d = 0  # Başlangıç pozisyonu (m)
E_bat_remaining = E_bat  # Batarya başlangıç kapasitesi
time = 0  # Zaman sayacı
results = []  # Sonuçları tutmak için

# Simülasyon
for segment in road_segments:
    segment_length = segment["length"]
    slope_angle = np.radians(segment["slope"])  # Eğimi radyana çevir

    while d < segment_length and E_bat_remaining > 0:
        # Eğime bağlı kuvvet
        F_slope = m * g * np.sin(slope_angle)

        # Aerodinamik direnç
        F_drag = 0.5 * rho * C_d * A * v**2

        # Yuvarlanma direnci
        F_rr = C_rr * m * g * np.cos(slope_angle)

        # Maksimum çekiş kuvveti
        F_traction_max = mu * m * g
        F_motor_max = min(tau_max * omega_max / (v + 1e-3), P_nominal / (v + 1e-3))
        F_traction = min(F_traction_max, F_motor_max)

        # Net kuvvet ve ivme
        F_net = F_traction - F_drag - F_rr - F_slope
        a = F_net / m

        # Hız ve pozisyon güncelleme
        v = max(v + a * delta_t, 0)  # Hız negatif olamaz
        d += v * delta_t

        # Motor gücü ve batarya enerji tüketimi
        P_motor = max(F_traction * v / eta, 0)
        if F_net < 0 and v > 0:  # Rejeneratif frenleme
            P_recovered = -F_net * v * eta
            E_bat_remaining += P_recovered * delta_t
        else:
            E_bat_remaining -= P_motor * delta_t

        # Termal yönetim
        T_motor += (P_motor * delta_t / 10000)  # Motor ısınma modeli
        T_battery += (P_motor * delta_t / E_bat) * 0.01  # Batarya ısınma modeli

        if T_motor > max_motor_temp:
            print("Motor sıcaklığı çok yüksek, güç sınırlandırılıyor.")
            eta *= 0.8  # Verim düşer
        if T_battery > max_battery_temp:
            print("Batarya sıcaklığı çok yüksek, performans düşürülüyor.")
            F_traction *= 0.9  # Çekiş gücü azaltılır

        # Zamanı güncelle ve sonuçları kaydet
        time += delta_t
        soc = E_bat_remaining / E_bat * 100  # Batarya yüzdesi
        results.append([time, v * 3.6, d, soc, P_motor / 1000, F_traction, T_battery, T_motor])

# Çıktıların ayrıştırılması
times, velocities, distances, socs, powers, torques, battery_temps, motor_temps = zip(*results)

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

# Motor ve Batarya Sıcaklıkları
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
with open("simulasyon_sonuclari_genisletilmis.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Zaman (s)", "Hız (km/h)", "Pozisyon (m)", "SOC (%)", "Güç (kW)", "Tork (Nm)", "Batarya Sıcaklığı (°C)", "Motor Sıcaklığı (°C)"])
    writer.writerows(results)

# Konsolda temel sonuçları göster
print(f"Simülasyon süresi: {time:.2f} s")
print(f"Kalan batarya kapasitesi: {E_bat_remaining / 3600:.2f} kWh")
