# Occupancy Detection Models

## Overview
This directory contains the trained models and export formats for the **occupancy detection system**, which uses a YOLOv11n-based approach for image classification. These models are used by the **High-Powered Hub** to detect people in classrooms and estimate occupancy for automated A/C control.

- **Model Name:** YOLOv11n  
- **Task:** Image Classification (People Detection)   
- **Epochs:** 100  
- **Image Size:** 1280  

---

### **1. weights/**
Contains the original YOLOv11n weights (`.pt`) trained for 100 epochs on 1280×1280 images. These weights are primarily used for:
- Further fine-tuning or retraining.
- Generating additional export formats if needed.

### **2. exports/**
Includes multiple deployment-ready formats:
- **NCNN:** Optimized for lightweight inference on low-powered devices.
- **ONNX:** For interoperability across frameworks and hardware accelerators.
- **TorchScript:** For PyTorch-based inference on devices with Python runtime.

---

## How It Fits Into the System
- The **High-Powered Hub** uses these models to run on-device inference for classroom occupancy detection.
- The **NCNN export** is intended for future low-powered edge devices that may support vision-based detection.
- Outputs from these models feed into the decision engine, which determines whether to turn the A/C on or off based on occupancy thresholds and timetable data.

---
