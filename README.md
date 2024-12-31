
# **🚗 Electric Vehicle Simulation Project ⚡**

This project aims to simulate the performance of an electric vehicle under different road conditions, analyzing critical parameters such as energy consumption, battery status, motor power, and temperature. The project provides a powerful tool for engineering analyses, training, and research studies. **The code is written in an open and expandable manner. Additional parameters can be added for further detailing.**

---

## **🎯 Purpose**

With this project, you can:

- ⚡ Understand the energy consumption dynamics of electric vehicles.
- 🛣️ Analyze performance data such as speed, power, and temperature on different road segments.
- 🚗 Simulate motor and battery performance under real-world conditions.
- 🧑‍🏫 Assist in the development of vehicle design, optimization, and energy management strategies.

---

## **🔧 What the Project Does**

1. **🛤️ Road Segment-Based Simulation:**
   - Simulates the vehicle's behavior on road segments with varying slope and surface conditions.

2. **🔋 Regenerative Braking:**
   - Calculates energy recovery to the battery during negative traction force situations.

3. **🌡️ Thermal Management:**
   - Models the temperature increase and cooling effects of the motor and battery.
   - Limits power during extreme temperature conditions.

4. **⚙️ Motor Efficiency Map:**
   - Calculates the motor's efficiency based on speed (RPM) and torque values.

5. **📊 Visualization and Saving of Results:**
   - Visualizes parameters such as speed, position, battery status, motor power, and temperature through graphs.
   - Saves simulation results in CSV format.

---

## **📁 Project File Structure**

- **config.json:** A configuration file containing simulation parameters.
- **main.py:** The main Python file that performs the simulation.
- **README.md:** The description and usage guide of the project.

---

## **⚙️ Required Installations**

The following Python libraries are required for the project:
- `numpy`
- `matplotlib`
- `scipy`
- `json`
- `csv`

To install, use the following command:

```bash
pip install numpy matplotlib scipy
```

---

## **📚 Usage Steps**

### 1. **Prepare the config.json File**
Create or edit the `config.json` file containing the simulation parameters. Example structure:

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

### 2. **Run the Simulation**
Start the simulation by running the main Python file:

```bash
python main.py
```

### 3. **Examine the Results**
Once the simulation is complete:
- 📊 Analyze speed, battery status, motor power, and temperature data through graphs.
- 📂 Export data using the `simulation_results.csv` file.

---

## **📐 Input Parameters**

### **Motor and Vehicle Properties**

| Parameter               | Description                                      | Example Value |
|-------------------------|--------------------------------------------------|---------------|
| `motor_power`           | Maximum motor power (Watt)                       | 250000        |
| `max_torque`            | Maximum motor torque (Nm)                        | 400           |
| `max_rpm`               | Maximum motor RPM                                | 7000          |
| `battery_capacity`      | Battery capacity (kWh)                           | 80            |
| `vehicle_mass`          | Vehicle mass (kg)                                | 900           |
| `aero_drag_coeff`       | Aerodynamic drag coefficient                     | 0.24          |
| `frontal_area`          | Vehicle frontal area (m²)                        | 1.6           |

### **Environmental and Road Conditions**

| Parameter               | Description                                      | Example Value |
|-------------------------|--------------------------------------------------|---------------|
| `air_density`           | Air density (kg/m³)                              | 1.2           |
| `traction_coeff`        | Tire-road friction coefficient                   | 1.2           |
| `ambient_temp`          | Ambient temperature (°C)                         | 25            |

### **Thermal Management**

| Parameter               | Description                                      | Example Value |
|-------------------------|--------------------------------------------------|---------------|
| `initial_battery_temp`  | Initial battery temperature (°C)                 | 25            |
| `initial_motor_temp`    | Initial motor temperature (°C)                   | 25            |
| `max_battery_temp`      | Maximum battery temperature (°C)                 | 60            |
| `max_motor_temp`        | Maximum motor temperature (°C)                   | 100           |

### **Road Segments**

| Parameter               | Description                                      | Example Value |
|-------------------------|--------------------------------------------------|---------------|
| `length`                | Length of the road segment (m)                   | 500           |
| `slope`                 | Slope of the road segment (%)                    | 5             |
| `rolling_resistance`    | Rolling resistance coefficient                   | 0.015         |

---

## **📤 Output Parameters**

| Output Parameter        | Description                                      |
|-------------------------|--------------------------------------------------|
| `time`                  | Simulation time (s)                              |
| `velocity`              | Speed (km/h)                                     |
| `position`              | Distance covered (m)                             |
| `soc`                   | Battery state of charge (%)                      |
| `power`                 | Motor power (kW)                                 |
| `torque`                | Torque (Nm)                                      |
| `battery_temp`          | Battery temperature (°C)                         |
| `motor_temp`            | Motor temperature (°C)                           |

---

## **⚠️ Important Notes**

- Ensure that the parameters are filled with realistic values, otherwise the simulation may produce nonsensical results.
- If the battery is completely discharged or the motor/battery temperature rises excessively during the simulation, the simulation will stop.
- You can test different conditions by modifying the road segments.
