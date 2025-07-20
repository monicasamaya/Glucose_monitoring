import serial
import numpy as np
import scipy.signal as signal
import time
import asyncio
import websockets
import requests
import signal as sys_signal
import sys

try:
    ser = serial.Serial('COM4', 9600, timeout=1)
    time.sleep(2)
except serial.SerialException:
    print("Could not open COM port!")
    sys.exit()

ESP32_IP = "192.168.112.163"
ESP32_PORT = 8765
ESP32_WS_URL = f"ws://{ESP32_IP}:{ESP32_PORT}"

THINGSPEAK_URL = "https://api.thingspeak.com/update"
WRITE_API_KEY = "QT4BGNDH1FUS8TP9"

last_valid_glucose = None
baseline_voltage = None
running = True 

#Baseline Voltage Estimation
def calibrate_baseline(duration=5):
    print("Calibrating baseline... Please DO NOT place your finger.")
    data = []
    ser.reset_input_buffer()
    start_time = time.time()

    while time.time() - start_time < duration:
        try:
            line = ser.readline().decode().strip()
            voltage = float(line)
            data.append(voltage)
        except:
            continue

    if not data:
        print("No data received. Defaulting to 1.7 V")
        return 1.7

    avg = np.mean(data)
    print(f"Baseline voltage set to: {avg:.3f} V")
    return avg

#Glucose Reading & Processing 
def get_glucose_value(duration=5):
    global last_valid_glucose, baseline_voltage
    data = []
    ser.reset_input_buffer()
    start_time = time.time()

    while time.time() - start_time < duration:
        try:
            line = ser.readline().decode().strip()
            voltage = float(line)
            data.append(voltage)
        except:
            continue

    if not data:
        print("No data received!")
        return None

    print(f"Samples: {len(data)}")

    # Filter and smooth
    b, a = signal.butter(2, 0.4, 'low')
    filtered = signal.filtfilt(b, a, data)
    smoothed = np.convolve(filtered, np.ones(5) / 5, mode='valid')

    avg_voltage = np.mean(smoothed)
    print(f"Avg Voltage: {avg_voltage:.3f} V")

    #Reject high voltages (no finger placed)
    if avg_voltage > 1.4:
        print("Please place your finger.")
        return None

    # Finger detection using dynamic baseline
    delta_threshold = 0.05  # 50 mV drop indicates finger
    if avg_voltage > (baseline_voltage - delta_threshold):
        print("Finger not detected.")
        return None

    # Glucose Calibration
    voltage_drop = baseline_voltage - avg_voltage
    if voltage_drop <= 0:
        print("Voltage did not drop. Invalid reading.")
        return None

    # Calibration
    glucose = 53 + (voltage_drop / 0.01) * 1.15
    glucose = round(glucose, 2)
    last_valid_glucose = glucose
    return glucose

# ThingSpeak Upload ===
def send_to_thingspeak(glucose_value):
    payload = {
        'api_key': WRITE_API_KEY,
        'field1': glucose_value
    }
    try:
        response = requests.get(THINGSPEAK_URL, params=payload)
        if response.status_code == 200:
            print(f"Sent to ThingSpeak: {glucose_value}")
    except:
        print("Failed to send to ThingSpeak.")

# Graceful Shutdown 
def shutdown_handler(sig, frame):
    global running
    print("\nShutting down gracefully...")
    running = False
    try:
        ser.close()
    except:
        pass
    sys.exit(0)

sys_signal.signal(sys_signal.SIGINT, shutdown_handler)

# === Main WebSocket Loop ===
async def main():
    global baseline_voltage
    baseline_voltage = calibrate_baseline(duration=5)

    try:
        async with websockets.connect(ESP32_WS_URL) as websocket:
            while running:
                glucose_val = get_glucose_value()
                if glucose_val is not None:
                    print(f"Glucose Level: {glucose_val:.2f} mg/dL")
                    await websocket.send(f"{glucose_val:.2f}")
                    print(f"Sent to ESP32: {glucose_val:.2f} mg/dL")
                    send_to_thingspeak(glucose_val)
                await asyncio.sleep(1)
    except Exception as e:
        print(f"WebSocket Error: {e}")
        shutdown_handler(None, None)

# === Run Everything ===
try:
    asyncio.run(main())
except KeyboardInterrupt:
    shutdown_handler(None, None)
