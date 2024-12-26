### **README.md**

---

# **Elektrikli Araç Simülasyon Projesi**

Bu proje, elektrikli bir aracın farklı yol koşullarında performansını simüle ederek enerji tüketimi, batarya durumu, motor gücü ve sıcaklık gibi kritik parametreleri analiz etmeyi amaçlar. Proje, mühendislik analizleri, eğitim ve araştırma çalışmaları için güçlü bir araç sunar.

---

## **Kullanım Amacı**

Bu proje:
- Elektrikli araçların enerji tüketim dinamiklerini anlamayı sağlar.
- Farklı yol segmentlerinde aracın hız, güç ve sıcaklık gibi performans verilerini analiz eder.
- Motor ve batarya performansını gerçek dünya koşullarına uygun şekilde simüle eder.
- Araç tasarımı, optimizasyon ve enerji yönetimi stratejilerinin geliştirilmesine yardımcı olur.

---

## **Projenin Yaptıkları**

1. **Yol Segmentlerine Dayalı Simülasyon:**
   - Farklı eğim ve yüzey koşullarına sahip yol segmentlerinde aracın davranışını simüle eder.

2. **Rejeneratif Frenleme:**
   - Negatif çekiş kuvveti durumunda bataryaya enerji geri kazanımını hesaplar.

3. **Termal Yönetim:**
   - Motor ve bataryanın sıcaklık artışını ve soğuma etkisini modeller.
   - Aşırı sıcaklık durumunda gücü sınırlar.

4. **Motor Verim Haritası:**
   - Motorun hız (RPM) ve tork değerlerine bağlı verimliliğini hesaplar.

5. **Sonuçların Görselleştirilmesi ve Kaydedilmesi:**
   - Hız, pozisyon, batarya durumu, motor gücü ve sıcaklık gibi parametreleri grafiklerle görselleştirir.
   - Simülasyon sonuçlarını CSV formatında kaydeder.

---

## **Proje Dosya Yapısı**

- **config.json:** Simülasyon parametrelerini içeren bir yapılandırma dosyası.
- **main.py:** Simülasyonu gerçekleştiren ana Python dosyası.
- **simulasyon_sonuclari.csv:** Simülasyon çıktılarının kaydedildiği dosya.
- **README.md:** Projenin açıklama ve kullanım kılavuzu.

---

## **Gerekli Kurulumlar**

Proje için aşağıdaki Python kütüphaneleri gereklidir:
- `numpy`
- `matplotlib`
- `scipy`
- `json`
- `csv`

Kurulum için aşağıdaki komutu kullanabilirsiniz:
```bash
pip install numpy matplotlib scipy
```

---

## **Kullanım Adımları**

### 1. **config.json Dosyasını Hazırlayın**
Simülasyon parametrelerini içeren `config.json` dosyasını oluşturun veya düzenleyin. Örnek yapı:
```json
{
    "motor_power": 250000,
    "max_torque": 400,
    "max_rpm": 7000,
    "battery_capacity": 80,
    "vehicle_mass": 900,
    "aero_drag_coeff": 0.24,
    "frontal_area": 1.6,
    "air_density": 1.2,
    "traction_coeff": 1.2,
    "ambient_temp": 25,
    "initial_battery_temp": 25,
    "initial_motor_temp": 25,
    "max_battery_temp": 60,
    "max_motor_temp": 100,
    "time_step": 0.1,
    "road_segments": [
        {"length": 500, "slope": 0, "rolling_resistance": 0.01},
        {"length": 200, "slope": 5, "rolling_resistance": 0.015},
        {"length": 300, "slope": -3, "rolling_resistance": 0.01}
    ]
}
```

### 2. **Simülasyonu Çalıştırın**
Ana Python dosyasını çalıştırarak simülasyonu başlatın:
```bash
python main.py
```

### 3. **Sonuçları İnceleyin**
Simülasyon tamamlandığında:
- Grafikler aracılığıyla hız, batarya durumu, motor gücü ve sıcaklık verilerini analiz edin.
- `simulasyon_sonuclari.csv` dosyasını kullanarak verileri dışa aktarın.

---

## **Giriş Parametreleri**

### **Motor ve Araç Özellikleri**
| Parametre               | Açıklama                                         | Örnek Değer |
|-------------------------|-------------------------------------------------|-------------|
| `motor_power`           | Motorun maksimum gücü (Watt)                   | 250000      |
| `max_torque`            | Motorun maksimum torku (Nm)                    | 400         |
| `max_rpm`               | Motorun maksimum devri (RPM)                   | 7000        |
| `battery_capacity`      | Batarya kapasitesi (kWh)                       | 80          |
| `vehicle_mass`          | Araç kütlesi (kg)                              | 900         |
| `aero_drag_coeff`       | Aerodinamik sürtünme katsayısı                 | 0.24        |
| `frontal_area`          | Araç ön kesit alanı (m²)                       | 1.6         |

### **Çevre ve Yol Koşulları**
| Parametre               | Açıklama                                         | Örnek Değer |
|-------------------------|-------------------------------------------------|-------------|
| `air_density`           | Hava yoğunluğu (kg/m³)                         | 1.2         |
| `traction_coeff`        | Lastik yol tutuş katsayısı                     | 1.2         |
| `ambient_temp`          | Çevre sıcaklığı (°C)                           | 25          |

### **Termal Yönetim**
| Parametre               | Açıklama                                         | Örnek Değer |
|-------------------------|-------------------------------------------------|-------------|
| `initial_battery_temp`  | Batarya başlangıç sıcaklığı (°C)                | 25          |
| `initial_motor_temp`    | Motor başlangıç sıcaklığı (°C)                  | 25          |
| `max_battery_temp`      | Bataryanın maksimum sıcaklığı (°C)              | 60          |
| `max_motor_temp`        | Motorun maksimum sıcaklığı (°C)                 | 100         |

### **Yol Segmentleri**
| Parametre               | Açıklama                                         | Örnek Değer |
|-------------------------|-------------------------------------------------|-------------|
| `length`                | Yol segmentinin uzunluğu (m)                    | 500         |
| `slope`                 | Yol segmentinin eğimi (%)                       | 5           |
| `rolling_resistance`    | Yuvarlanma direnci katsayısı                    | 0.015       |

---

## **Çıkış Parametreleri**

| Çıkış Parametresi       | Açıklama                                         |
|-------------------------|-------------------------------------------------|
| `time`                  | Simülasyon süresi (s)                           |
| `velocity`              | Hız (km/h)                                      |
| `position`              | Kat edilen mesafe (m)                           |
| `soc`                   | Batarya doluluk oranı (%)                       |
| `power`                 | Motor gücü (kW)                                 |
| `torque`                | Tork (Nm)                                       |
| `battery_temp`          | Batarya sıcaklığı (°C)                          |
| `motor_temp`            | Motor sıcaklığı (°C)                            |

---

## **Önemli Notlar**

- Parametreleri gerçekçi değerlerle doldurun, aksi takdirde simülasyon mantıksız sonuçlar verebilir.
- Simülasyon sırasında batarya tamamen boşalırsa veya motor/batarya sıcaklığı aşırı yükselirse simülasyon durdurulacaktır.
- Yol segmentlerini değiştirerek farklı koşulları test edebilirsiniz.

