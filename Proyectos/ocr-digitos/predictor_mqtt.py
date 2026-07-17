"""
Publicador MQTT de dígitos reconocidos por OCR.

Simula (o realiza, si se le pasa una imagen real) el reconocimiento de un
dígito y publica el resultado por MQTT, como lo haría un sensor/lector de
medidores en un entorno industrial IT/OT.

Modo por defecto: simulación (no requiere modelo entrenado ni broker real
corriendo, útil para probar la integración de mensajería).
Modo real: requiere `modelo_ocr.h5` (generado con train.py) y un broker
MQTT accesible.
"""

import json
import random
import time

import numpy as np
import paho.mqtt.client as mqtt

BROKER = "localhost"
PUERTO = 1883
TOPIC = "ocr/digito"
INTERVALO_SEGUNDOS = 3


def conectar_mqtt(broker=BROKER, puerto=PUERTO):
    """Crea y conecta el cliente MQTT. Devuelve None si no se pudo conectar
    (para poder seguir probando la lógica de predicción sin broker activo)."""
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    try:
        client.connect(broker, puerto, 60)
        return client
    except Exception as e:
        print(f"No se pudo conectar al broker MQTT ({broker}:{puerto}): {e}")
        print("Continuando en modo local, sin publicar mensajes.")
        return None


def cargar_modelo(ruta="modelo_ocr.h5"):
    """Carga el modelo entrenado. Se importa keras acá adentro para que el
    modo simulación pueda correr sin tener tensorflow instalado."""
    from tensorflow import keras
    return keras.models.load_model(ruta)


def predecir(modelo, imagen):
    """Recibe una imagen de 28x28 (array de numpy) y devuelve el dígito predicho."""
    imagen = imagen.reshape(1, 28, 28).astype("float32") / 255.0
    pred = modelo.predict(imagen, verbose=0)
    return int(np.argmax(pred))


def publicar(client, digito):
    payload = {"digito": digito, "timestamp": time.time()}
    if client is not None:
        client.publish(TOPIC, json.dumps(payload))
    print("Enviado:", payload)


def correr_simulacion(client, intervalo=INTERVALO_SEGUNDOS):
    """Simula dígitos detectados (sin modelo real) y los publica por MQTT.
    Útil para probar el flujo MQTT/dashboard sin depender del modelo."""
    print("Modo simulación: generando dígitos aleatorios...")
    while True:
        digito = random.randint(0, 9)
        publicar(client, digito)
        time.sleep(intervalo)


def correr_real(client, modelo, imagenes, intervalo=INTERVALO_SEGUNDOS):
    """Recorre una lista/array de imágenes reales, predice cada una con el
    modelo entrenado y publica el resultado."""
    print("Modo real: prediciendo con el modelo entrenado...")
    for imagen in imagenes:
        digito = predecir(modelo, imagen)
        publicar(client, digito)
        time.sleep(intervalo)


if __name__ == "__main__":
    client = conectar_mqtt()

    # Por defecto corre en modo simulación. Para modo real:
    #   modelo = cargar_modelo("modelo_ocr.h5")
    #   correr_real(client, modelo, tus_imagenes)
    try:
        correr_simulacion(client)
    except KeyboardInterrupt:
        print("Publicador detenido.")
    finally:
        if client is not None:
            client.disconnect()
