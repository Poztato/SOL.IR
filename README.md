# SOL.IR — Smart Occupancy‑Linked IR A/C Controller

SOL.IR is a hardware-first IoT system that **automatically turns off classroom A/C** when a room is unoccupied—and smartly **pre‑cools** before scheduled classes. It combines **edge devices** mounted on A/C fins (detect actual A/C state and send telemetry) with a **central hub** (decides occupancy and issues IR on/off), supporting both **low-power (sensor fusion)** and **high-power (AI camera)** hub designs.

> **Hackathon Track:** Hardware • **Use Case:** Smart Campus Enhancements

---

## ✨ Why this matters
Universities waste energy when A/C runs in empty rooms, and students/staff lose time dealing with comfort and scheduling mismatches. SOL.IR makes A/C usage **data-driven and automated**, improving comfort while cutting waste.

---

## 🧩 System at a glance

- **Edge Device (per A/C unit)**
  - **Temp sensor** on the outlet fin to confirm A/C is actually cooling.
  - **Micro wind turbine** harvests airflow; also provides a **voltage proxy** for air movement.
  - **IR blaster** (with proper driver transistor) to send power/temperature mode commands to the A/C.
  - **MCU:** Raspberry Pi Pico (current prototype). Bench mode via USB serial; field mode via Pico W / alternative wireless (future).

- **Central Hub (per room)**
  - **Low‑power variant (e.g., Pi Zero W)**: PIR motion + sound sensing (AI audio classifier), temp/humidity, solar trickle charging from indoor lighting. Sensor fusion → occupancy decision.
  - **High‑power variant (e.g., Pi 5)**: Camera + on‑device **people detection** for occupancy counting; temp/humidity for redundancy and fault alerts.
  - **Timetable integration**: Pre‑cool rooms before class start; turn off during long gaps.
  - **Redundancy & fault detection**: Compares edge vs hub temperatures; flags anomalies to the institution portal/app.

- **Interfaces**
  - **IR control** to the A/C (no electrical modifications to existing units).
  - **Campus systems** (HTTP/MQTT) for timetable ingest and notifications.
  - **Web dashboard** (prototype) for live status, override, logs, and alerts.

---

## 🖼️ Architecture & Data Flow

> Diagrams render on GitHub using Mermaid. If they don’t, see PNGs in `/docs/diagrams`.

### Block Diagram

flowchart LR
  subgraph Room["Classroom"]
    subgraph AC["A/C Unit"]
      T[Temp Sensor (Fin)]
      W[Wind Turbine<br/>(harvest + airflow proxy)]
      IR[IR Blaster]
      EDGEPICO["Edge MCU (Pi Pico)"]
      T --> EDGEPICO
      W --> EDGEPICO
      EDGEPICO --> IR
    end
    subgraph HUB["Central Hub"]
      LP[(Low-power Hub:<br/>PIR + Sound AI + T/H)]:::lp
      HP[(High-power Hub:<br/>Camera AI + T/H)]:::hp
    end
    EDGEPICO <---> HUB
    HUB -->|IR Command| IR
  end

  CAMPUS[(Timetable API<br/>/ Portal)] --> HUB
  HUB -->|Alerts / Logs| CAMPUS

  classDef lp fill:#e3fff2,stroke:#00a676;
  classDef hp fill:#e9f0ff,stroke:#4e6cff;
