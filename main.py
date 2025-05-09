import requests
import time
from datetime import datetime
import os

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID_FITM = int(os.getenv("CHAT_ID_FITM"))
CHAT_ID_GRUPO = int(os.getenv("CHAT_ID_GRUPO"))

def enviar_mensaje(texto, destino='grupo'):
    chat_id = CHAT_ID_GRUPO if destino == 'grupo' else CHAT_ID_FITM
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    data = {'chat_id': chat_id, 'text': texto}
    response = requests.post(url, data=data)
    print(response.json())
    return response.ok

def programar_recordatorio(mensaje, fecha_hora, destino='fitm'):
    print(f"⏳ Recordatorio programado para {fecha_hora}...")
    while True:
        ahora = datetime.now()
        if ahora >= fecha_hora:
            enviar_mensaje(mensaje, destino)
            print("✅ Recordatorio enviado.")
            break
        time.sleep(30)

def leer_y_programar_desde_txt():
    with open("recordatorios.txt", "r") as file:
        lineas = file.readlines()
    for linea in lineas:
        if '|' not in linea or linea.startswith('#'): continue
        fecha_str, destino, mensaje = linea.strip().split(" | ")
        fecha_hora = datetime.strptime(fecha_str, "%Y-%m-%d %H:%M")
        programar_recordatorio(mensaje, fecha_hora, destino)

leer_y_programar_desde_txt()
