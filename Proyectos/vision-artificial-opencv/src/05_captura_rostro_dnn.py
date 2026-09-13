"""
05_captura_rostro_dnn.py

Detección facial en tiempo real con un modelo DNN (red neuronal SSD sobre
Caffe, mucho más robusta que Haar Cascade) + captura de fotos propias
mientras se detecta el rostro. Pensado para grabar tu propia serie de
capturas y así reemplazar la imagen sintética del script 03.

FUENTE DE VIDEO: podés usar la webcam de tu PC, o tu celular como cámara IP
(ver "Usar el celular como webcam" en el README). Configurá la variable
FUENTE más abajo.

Controles durante la ejecución:
    c   -> guarda una captura del frame actual en capturas/
    q   -> sale
"""
import os
import time
import cv2
from _rutas import ruta

# --- CONFIGURACIÓN ---
# Opción A) Webcam integrada / USB: probá 0, 1, 2... según cuántas cámaras tengas
# Opción B) Celular como cámara IP (con la app "IP Webcam" en Android):
#           FUENTE = "http://192.168.0.XX:8080/video"   <- IP que muestra la app
FUENTE = 0

CARPETA_CAPTURAS = ruta("capturas")
CONF_MINIMA = 0.7


def cargar_modelo():
    prototxt = ruta("modelos", "dnn-caras", "deploy.prototxt")
    pesos = ruta("modelos", "dnn-caras", "res10_300x300_ssd_iter_140000_fp16.caffemodel")
    return cv2.dnn.readNetFromCaffe(prototxt, pesos)


def detectar_rostros(net, frame):
    alto, ancho = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), [104, 117, 123],
                                  swapRB=False, crop=False)
    net.setInput(blob)
    detecciones = net.forward()

    cajas = []
    for i in range(detecciones.shape[2]):
        confianza = detecciones[0, 0, i, 2]
        if confianza > CONF_MINIMA:
            x1 = int(detecciones[0, 0, i, 3] * ancho)
            y1 = int(detecciones[0, 0, i, 4] * alto)
            x2 = int(detecciones[0, 0, i, 5] * ancho)
            y2 = int(detecciones[0, 0, i, 6] * alto)
            cajas.append((x1, y1, x2, y2, confianza))
    return cajas


def main():
    os.makedirs(CARPETA_CAPTURAS, exist_ok=True)
    net = cargar_modelo()

    cap = cv2.VideoCapture(FUENTE)
    if not cap.isOpened():
        print(f"No se pudo abrir la fuente de video: {FUENTE}")
        print("Revisá el índice de cámara o la URL del celular (ver README).")
        return

    print("Ventana de cámara abierta. Presioná 'c' para capturar, 'q' para salir.")
    contador = 0

    while True:
        ok, frame = cap.read()
        if not ok:
            print("No se pudo leer un frame de la fuente de video.")
            break

        frame = cv2.flip(frame, 1)  # efecto espejo, más natural para selfie
        cajas = detectar_rostros(net, frame)

        frame_dibujado = frame.copy()
        for (x1, y1, x2, y2, confianza) in cajas:
            cv2.rectangle(frame_dibujado, (x1, y1), (x2, y2), (0, 220, 0), 2)
            etiqueta = f"Rostro {confianza:.2f}"
            cv2.putText(frame_dibujado, etiqueta, (x1, max(y1 - 10, 20)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 220, 0), 2)

        cv2.putText(frame_dibujado, "c: capturar   q: salir", (10, 25),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2, cv2.LINE_AA)

        cv2.imshow("Deteccion de rostro - DNN", frame_dibujado)

        tecla = cv2.waitKey(1) & 0xFF
        if tecla == ord('q') or tecla == 27:
            break
        elif tecla == ord('c'):
            contador += 1
            nombre = f"{CARPETA_CAPTURAS}/rostro_{int(time.time())}_{contador}.jpg"
            cv2.imwrite(nombre, frame_dibujado)
            print(f"Captura guardada: {nombre}")

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
