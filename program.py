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
eta = 0.95  # Motor Verimi

E_bat = 80 * 3600  # Batarya Kapasitesi (Wh to Joules)
V = 400  # Besleme Gerilimi (V)
I_max = 600  # Maksimum Akım Çekişi (A)

m = 900  # Araç Kütlesi (kg)
C_d = 0.24  # Aerodinamik Sürtünme Katsayısı
A = 1.6  # Araç Kesit Alanı (m^2)
C_rr = 0.01  # Yuvarlanma Direnci Katsayısı

mu = 1.2  # Lastik Yol Tutuş Katsayısı
d_target = 1000  # Hedef mesafe (m)

delta_t = 0.1  # Simülasyon adım süresi (s)

# Başlangıç durumu
v = 0  # Başlangıç hızı (m/s)
d = 0  # Başlangıç pozisyonu (m)
E_bat_remaining = E_bat  # Batarya başlangıç kapasitesi
time = 0  # Zaman sayacı
results = []  # Sonuçları tutmak için

# Simülasyon
while d < d_target and E_bat_remaining > 0:
    # Aerodinamik direnç
    F_drag = 0.5 * rho * C_d * A * v**2

    # Yuvarlanma direnci
    F_rr = C_rr * m * g

    # Maksimum çekiş kuvveti (Lastik limiti ve motor limiti)
    F_traction_max = mu * m * g
    F_motor_max = tau_max * V / (v + 1e-3)  # v -> 0 olduğunda hata önleme
    F_traction = min(F_traction_max, F_motor_max)

    # Net kuvvet ve ivme
    F_net = F_traction - F_drag - F_rr
    a = F_net / m

    # Hız ve pozisyon güncelleme
    v = v + a * delta_t
    d = d + v * delta_t

    # Motor gücü ve batarya enerji tüketimi
    P_motor = F_traction * v / eta
    E_bat_remaining -= P_motor * delta_t

    # Zamanı güncelle ve sonuçları kaydet
    time += delta_t
    results.append([time, v * 3.6, d, E_bat_remaining / 3600])  # Hızı km/h'ye çevir

# Çıktıların gösterimi
times, velocities, distances, socs = zip(*results)

# Zaman, hız, pozisyon, batarya yüzdesi grafikleri
plt.figure(figsize=(12, 8))

plt.subplot(2, 2, 1)
plt.plot(times, velocities, label="Hız (km/h)")
plt.xlabel("Zaman (s)")
plt.ylabel("Hız (km/h)")
plt.title("Hız Grafiği")
plt.grid()

plt.subplot(2, 2, 2)
plt.plot(times, distances, label="Pozisyon (m)", color="orange")
plt.xlabel("Zaman (s)")
plt.ylabel("Pozisyon (m)")
plt.title("Pozisyon Grafiği")
plt.grid()

plt.subplot(2, 2, 3)
plt.plot(times, socs, label="SOC (%)", color="green")
plt.xlabel("Zaman (s)")
plt.ylabel("SOC (%)")
plt.title("Batarya Durumu (SOC)")
plt.grid()

plt.tight_layout()
plt.show()

# Sonuçları CSV olarak kaydetme
with open("simulasyon_sonuclari.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Zaman (s)", "Hız (km/h)", "Pozisyon (m)", "SOC (%)"])
    writer.writerows(results)

# Konsolda temel sonuçları göster
print(f"0-100 km/h Süresi: {next(r[0] for r in results if r[1] >= 100):.2f} s")
print(f"Hedef mesafeyi tamamlama süresi: {time:.2f} s")
print(f"Kalan batarya kapasitesi: {E_bat_remaining / 3600:.2f} kWh")
