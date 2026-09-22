import json
import time
import urequests
import gc

url_servidor = "http://10.20.11.178:5000/api/telemetria"
url_version_git = "https://raw.githubusercontent.com/erickrecoder-commits/pico-ota/refs/heads/main/version.txt"
url_codigo_git = "https://raw.githubusercontent.com/erickrecoder-commits/pico-ota/refs/heads/main/main.py"

def cargar_config():
    try:
        with open("config.json", "r") as f:
            datos = json.load(f)
            return datos.get("device_id", "PICO_01")
    except:
        return "PICO_01"

def cargar_version():
    try:
        with open("version.json", "r") as f:
            datos = json.load(f)
            return datos.get("version", "1.0.0")
    except:
        return "1.0.0"

device_id = cargar_config()
version_actual = cargar_version()

print("Iniciando programa en la pico...")
print("Dispositivo:", device_id, "Version actual:", version_actual)

contador = 0

def revisar_ota():
    global version_actual
    res = None
    res_code = None
    try:
        print("Revisando si hay actualizaciones en github...")
        res = urequests.get(url_version_git, timeout=5)
        version_github = res.text.strip()
        res.close()
        res = None

        if version_github and version_github != version_actual and not version_github.startswith("<"):
            print("Nueva version detectada:", version_github)
            print("Descargando nuevo codigo...")
            
            res_code = urequests.get(url_codigo_git, timeout=5)
            nuevo_codigo = res_code.text
            res_code.close()
            res_code = None

            if nuevo_codigo and len(nuevo_codigo) > 50 and not nuevo_codigo.startswith("<"):
                with open("main.py", "w") as f:
                    f.write(nuevo_codigo)

                with open("version.json", "w") as f:
                    json.dump({"version": version_github}, f)

                version_actual = version_github
                print("Codigo actualizado a la version", version_actual)
        else:
            print("El codigo esta actualizado.")
    except Exception as e:
        print("Error al revisar la actualizacion:", e)
    finally:
        if res:
            try: res.close()
            except: pass
        if res_code:
            try: res_code.close()
            except: pass

while True:
    gc.collect()
    datos_telemetria = {
        "device_id": device_id,
        "version": version_actual,
        "mensaje": "Datos de telemetria enviados"
    }

    res = None
    try:
        headers = {"Content-Type": "application/json"}
        res = urequests.post(url_servidor, data=json.dumps(datos_telemetria), headers=headers, timeout=5)
        print("Telemetria enviada. Codigo respuesta:", res.status_code)
        res.close()
        res = None
    except Exception as e:
        print("Buscando servidor en:", url_servidor)

    contador += 1
    if contador >= 3:
        revisar_ota()
        contador = 0

    time.sleep(6)
