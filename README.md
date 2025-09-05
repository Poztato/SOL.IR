# SOL.IR — Smart Occupancy‑Linked IR A/C Controller

SOL.IR is a hardware-first IoT system that **automatically turns off classroom A/C** when a room is unoccupied, then smartly **pre‑cools** before scheduled classes. It combines **edge devices** mounted on A/C fins (detect actual A/C state and send telemetry) with a **central hub** (decides occupancy and issues IR on/off), supporting both **low-power (sensor fusion)** and **high-power (AI camera)** hub designs.

> **Hackathon Track:** Hardware • **Use Case:** Smart Campus Enhancements

---

## ✨ Why this matters
Universities waste energy when A/C runs in empty rooms, and students/staff lose time dealing with comfort and scheduling mismatches. SOL.IR makes A/C usage **data-driven and automated**, improving comfort while cutting waste.

---

## 🧩 System overview

- **Edge Device (per A/C unit)**
  - **Temp sensor** on the outlet fin to confirm A/C is actually cooling.
  - **Micro wind turbine** harvests airflow; also provides a **voltage proxy** for air movement.
  - **IR blaster** (with proper driver transistor) to send power/temperature mode commands to the A/C.
  - **MCU:** Raspberry Pi Pico (current prototype). Bench mode via USB serial; field mode via Pico W / alternative wireless (future).

- **Central Hub (per room)**
  - **Low‑power variant (e.g., Pi Pico)**: PIR motion + sound sensing (AI audio classifier), temp/humidity, solar trickle charging from indoor lighting. Sensor fusion → occupancy decision.
  - **High‑power variant (e.g., Pi 5)**: Camera + on‑device **people detection** for occupancy counting; temp/humidity for redundancy and fault alerts.
  - **Timetable integration**: Pre‑cool rooms before class start; turn off during long gaps.
  - **Redundancy & fault detection**: Compares edge vs hub temperatures; flags anomalies to the institution portal/app.

- **Interfaces**
  - **IR control** to the A/C (no electrical modifications to existing units).
  - **Campus systems** (HTTP/MQTT) for timetable ingest and notifications.
  - **Web dashboard** (prototype) for live status, override, logs, and alerts.

---

## 🖼️ Architecture & Data Flow


### Block Diagram

<img width="1267" height="1348" alt="Block Diagram v1 0" src="https://github.com/user-attachments/assets/4b7024ea-5dda-4dd3-9388-242190d88f44" />

---

## 📁 Repository Structure

```
SOL.IR/
├─ hardware/
│  ├─ stl_files/              # 3D prints for all devices
│  ├─ wiring/                 # Fritzing/PNG of wiring
│  └─ photos/                 # Build photos
├─ firmware/
│  ├─ unit-test               # Individual/Compiled unit testing code (MicroPython)
│  └─ pico/                   # Edge device firmware (Pico / MicroPython or C++)
├─ devices/
│  ├─ low_power_hub/          # Pi Zero W code (sensor fusion)
│  ├─ edge_device/            # Edge Device code (IR blasting)
│  └─ high_power_hub/         # Pi 5 code (AI people detection)
├─ models/
│  ├─ crowd_audio_detection/  # Audio-based crowd detection models
│  └─ occupancy_detection/    # Vision-based occupancy detection models
├─ docs/
│  ├─ diagrams/               # Mermaid + exported PNGs
│  └─ reports/                # Power budget, test notes
├─ tools/                     # Calibration, IR learning scripts
└─ README.md
```

---





