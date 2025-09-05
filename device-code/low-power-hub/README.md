# Low-Powered Hub

## Overview
The Low-Powered Hub is an energy-efficient controller for A/C automation, built on boards like Raspberry Pi Pico. It uses motion, sound, and environmental sensors to infer occupancy without a camera.

## Key Features
- **Motion Sensor (PIR)**: Detects movement in the classroom.
- **Sound Sensor + AI**: Identifies crowd noise or voices.
- **Temperature & Humidity Sensor**: Monitors comfort and validates edge readings.
- **Solar Trickle Charging**: Maintains power using classroom lighting.
- **IR Blaster**: Provides fallback A/C control.

## How It Works
1. Collects motion, sound, and temperature data to estimate occupancy.
2. Cross-checks edge device readings for redundancy.
3. Uses timetable data to pre-cool rooms before classes.
4. Sends IR commands to A/C if edge devices are unavailable.
