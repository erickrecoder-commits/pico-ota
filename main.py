import urequests
import json
import machine
import time

# Leer ID local de la tarjeta
try:
with open("config.json", "r") as f:
    config = json.load(f)
    DEVICE_ID = config.get("device_id", "PICO_SIN_ID")
except:
DEVICE_ID = "PICO_SIN_ID"

# REEMPLAZA ESTA IP POR LA IP QUE OBTUVISTE EN EL PASO 1
SERVER_URL = "http://192.168.0.112:5000/api/telemetria"

while True:
payload = {
    "device_id": DEVICE_ID,
    "temperatura": 24.5
}

try:
    headers = {'Content-Type': 'application/json'}
    res = urequests.post(SERVER_URL, data=json.dumps(payload), headers=headers)
    print(f"[{DEVICE_ID}] ¡Datos enviados! Código HTTP:", res.status_code)
    res.close()
except Exception as e:
    print(f"[{DEVICE_ID}] Buscando servidor en la PC...", e)
    
time.sleep(5)
