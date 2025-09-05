# Edge Device

## Overview
The Edge Device is mounted on the A/C unit and monitors its operational state. It uses airflow and temperature sensors to detect if the A/C is running and executes IR commands from the hub to turn the A/C on or off.

## Key Features
- **Temperature Sensor**: Measures A/C output temperature.
- **Airflow Turbine**: Detects airflow and harvests energy for charging.
- **IR Blaster**: Controls A/C based on hub commands.
- **Wireless Communication**: Sends telemetry to the hub via Wi-Fi or BLE.
- **Energy Harvesting**: Charges from A/C airflow for extended uptime.

## How It Works
1. Measures temperature and airflow to infer A/C status.
2. Reports data to the central hub for decision-making.
3. Executes IR commands from the hub to control the A/C.
4. Harvests energy from airflow to maintain battery charge.
