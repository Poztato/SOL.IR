# High-Powered Hub

## Overview
The High-Powered Hub is the central controller for classroom A/C automation, designed for high-performance boards like the Raspberry Pi 5. It uses a camera and AI-based image classification to detect classroom occupancy and decide whether to turn the A/C on or off.

## Key Features
- **Camera + AI**: Detects people and estimates occupancy.
- **Timetable Integration**: Pre-cools rooms before classes start.
- **Temperature & Humidity Sensor**: Provides redundancy and comfort monitoring.
- **IR Blaster**: Acts as a fallback to control A/C if edge devices fail.
- **Anomaly Detection**: Compares hub and edge device readings to flag errors.

## How It Works
1. Captures classroom images and runs an AI model locally to detect occupancy.
2. Checks occupancy against a minimum threshold and timetable data.
3. Sends IR commands to A/C or instructs edge devices to act.
4. Reports status and alerts to the institution’s portal/app.
