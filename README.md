# ESP32-S3 Rocket Thrust Test Stand

A rocket engine thrust measurement and launch sequencing system built on the ESP32-S3.  
Collects real-time thrust data via an HX711 load cell amplifier and exports results as CSV.

---

## 📊 Sample Test Results

| Metric | Value |
|--------|-------|
| Peak Thrust | 19.75 kg (193.7 N) |
| Time to Peak | 2.86 sec |
| Total Burn Time | ~11.9 sec |
| Total Impulse | 28.55 kg·s (280.1 N·s) |

---

## 🔧 Hardware

| Component | Role |
|-----------|------|
| ESP32-S3 DevKit C | Main controller |
| HX711 + Load Cell | Thrust measurement |
| Relay Module | Ignitor control |
| Buzzer | Countdown audio signal |
| RGB LED x4 | State indicator |
| Push Button | Start / stop sequence |

### Pin Map

| Module | Signal | GPIO |
|--------|--------|------|
| HX711 | DT (Data) | 47 |
| HX711 | SCK | 48 |
| Button | I/O | 5 |
| Relay (Ignitor) | IN | 4 |
| Buzzer | I/O | 19 |
| RGB LED | R / G / B | 13 / 12 / 14 |

---

## 🔄 Launch Sequence (State Machine)

```
IDLE → (button press) → COUNTDOWN → (T-0) → FIRING → (button press) → COMPLETE → IDLE
```

| State | LED | Buzzer | Ignitor |
|-------|-----|--------|---------|
| IDLE | OFF | OFF | OFF |
| COUNTDOWN | Green blink (1 s) | Short beep (1 s) | OFF |
| FIRING | Red solid | High-pitch tone x1 | ON |
| COMPLETE | OFF | Beep x2 | OFF |

---

## 🛠️ Development Environment

- **Arduino IDE** 2.3.6
- **ESP32 Board Package** 2.0.18
- **Required Library**: [HX711 by Bogdan Necula](https://github.com/bogde/HX711)

### Arduino IDE Board Settings

```
Board           : ESP32S3 Dev Module
USB CDC On Boot : Enabled
CPU Frequency   : 240 MHz
Flash Size      : 8 MB
Upload Speed    : 921600
```

---

## 📈 Data Analysis (Python)

```bash
pip install pandas matplotlib
python analysis/plot_thrust.py data/example_thrust_data.csv
```

CSV format:
```
timestamp_ms,force_kg
0,-0.0006
98,0.0011
...
```

To save the graph as an image:
```bash
python analysis/plot_thrust.py data/example_thrust_data.csv docs/thrust_result.png
```

---

## ⚠️ Safety Notes

- LED x4 in parallel may exceed GPIO current limits — brightness is software-capped at 20%
- A flyback diode across the relay coil is strongly recommended
- Total current draw approaches USB 2.0 limits (500 mA) — use an external 5 V / 2 A adapter
- Always ensure a clear safety perimeter before arming the ignitor

---
