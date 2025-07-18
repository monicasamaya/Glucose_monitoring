# GLUCOSE MONITORING USING NON-INVASIVE METHOD – IOT INTEGRATION

An IoT-based continuous glucose monitoring system that uses Near-Infrared (NIR) light for painless, real-time blood glucose detection. It avoids conventional finger-pricking by integrating an IR sensor, Arduino, ESP32, and Python-based signal processing for cloud-enabled monitoring.

---

## Table of Contents

- [About the Project](#about-the-project)
- [Motivation](#motivation)
- [Project Objectives](#project-objectives)
- [Hardware Used](#hardware-used)
- [Software Details](#software-details)
- [Future Work](#future-work)

---

## About the Project

This project aims to develop a non-invasive, real-time glucose monitoring system to replace painful and inconvenient finger-prick tests. Using Near-Infrared (NIR) optical sensing, an NIR LED shines through the fingertip while a photodiode detects transmitted light. Glucose absorbs specific NIR wavelengths, altering light intensity received. The photodiode output is amplified using an LM358 circuit and digitized by an Arduino’s ADC. Processed glucose data is filtered, calibrated, and sent via Wi-Fi to ThingSpeak for real-time cloud storage and analysis. An ESP32 also hosts a webpage displaying the readings. This portable, pain-free system showcases IoT’s potential in diabetes care and health monitoring.

---

## Motivation

Diabetes affects over 500 million people globally and demands frequent blood glucose monitoring to avoid severe complications. Traditional finger-prick methods, though accurate, are painful, time-consuming, and often ignored, especially by the elderly and busy individuals. This project aims to replace invasive techniques with a painless, non-invasive glucose monitoring system using **IR spectroscopy** and **IoT integration**. By enabling real-time, wireless data transmission to cloud platforms and mobile devices, our solution promotes proactive, user-friendly, and remote healthcare—contributing toward personalized and smart medical systems.

---

## Project Objectives

<details>
<summary>Click to expand</summary>

- Design a **painless, non-invasive glucose monitor** using NIR light.  
- Use **Arduino** to collect and transmit voltage data.  
- Apply **digital filtering and linear regression in Python** to estimate glucose levels.  
- Enable **wireless communication** with ESP32 for real-time data monitoring.  
- Store and visualize data on the **ThingSpeak cloud platform**.  
- Improve **user comfort, remote access, and long-term tracking**.  

</details>

---

## Hardware Used

- **IR LED & Photodiode Pair**  
- **LM358 Op-Amp Circuit**  
- **Arduino UNO**  
- **ESP32 Dev Module**  
- **Breadboard & Jumper Wires**  
- **USB Cable for Arduino**

---

## Software Details

### Python

Python is a high-level, versatile programming language widely used in IoT and biomedical applications. In this project, Python performs the following:

- Reads analog voltage from Arduino via serial communication  
- Filters raw signals using digital Butterworth filtering  
- Applies linear regression for glucose level calibration  
- Sends real-time glucose values to:
  - ESP32 using WebSocket  
  - ThingSpeak cloud via HTTP request  

Its compatibility with scientific libraries (NumPy, SciPy), easy syntax, and real-time data handling make Python ideal for non-invasive health monitoring systems.

---

### ESP32 Dev Module

The ESP32 is a Wi-Fi and Bluetooth-enabled microcontroller that receives glucose readings from Python and acts as a communication hub. It:

- Creates its own Wi-Fi Access Point for local access  
- Hosts a webpage on port 80 showing live glucose values  
- Runs a WebSocket server to receive data from Python  
- Forwards data to all connected clients and to the cloud  

Its low power usage, real-time connectivity, and ease of use make it perfect for wireless medical IoT applications like this project.

---

### Cloud Integration – ThingSpeak

**ThingSpeak** is an open-source IoT cloud platform by MathWorks used for storing, analyzing, and visualizing sensor data. It supports HTTP/MQTT protocols, provides real-time plotting, and has built-in MATLAB analytics.

In this project, Python sends glucose readings to ThingSpeak via HTTP GET requests using a unique API key. ThingSpeak offers:

- Real-time data visualization with auto-updating charts  
- Remote access via any web browser  
- Secure data handling using API keys  
- Long-term historical data tracking  
- Easy integration with Arduino, ESP32, and Python  
- Potential for adding alerts or AI-based predictions in the future  

It was chosen for its free tier, easy setup, reliability, and perfect fit for academic IoT-based biomedical systems.

---

### Arduino UNO

The Arduino UNO reads analog voltage from the IR sensor and sends it to Python via USB serial. It acts as the data acquisition unit, converting light intensity into voltage for glucose estimation.

---

## Future Work

- Improve calibration by considering skin tone, thickness, and biological factors  
- Use multiple NIR LEDs for better wavelength coverage and accuracy  
- Develop a mobile app for real-time monitoring and alerts  
- Add built-in alert systems for abnormal readings  
- Upgrade the user interface for enhanced usability  

---

