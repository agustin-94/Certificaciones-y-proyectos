"""
07_distancia_iris.py

Estima la distancia entre la cámara y tu cara usando MediaPipe Face Mesh
(con refine_landmarks=True, que agrega los puntos del iris). La lógica:
el diámetro del iris humano es prácticamente constante entre personas
(~11.7 mm), así que midiendo cuántos píxeles ocupa en la imagen se puede
despejar la distancia real con el modelo simple de una cámara pinhole:

    distancia = (longitud_focal_px * diametro_real_mm) / diametro_en_pixeles

FOCAL_LENGTH_PIXELS es un valor aproximado: para una medición más precisa
habría que calibrar la cámara específica que se use (ver README).

FUENTE DE VIDEO: webcam de PC o celular como cámara IP (ver README).

Controles:
    c   -> guarda una captura del frame actual en capturas/
    q   -> sale
"""
import os
import time
import cv2
import numpy as np
import mediapipe as mp
from _rutas import ruta

# --- CONFIGURACIÓN ---
FUENTE = 0  # 0 = webcam PC, o "http://192.168.0.XX:8080/video" con el celular

CARPETA_CAPTURAS = ruta("capturas")
IRIS_DIAMETRO_MM = 11.7          # diámetro horizontal promedio del iris humano
FOCAL_LENGTH_PIXELS = 300        # valor aproximado; calibrar para mayor precisión
VENTANA_PROMEDIO = 15            # cantidad de frames para suavizar la lectura

# Índices de MediaPipe Face Mesh correspondientes al iris de cada ojo
IRIS_IZQ = [468, 469, 470, 471]
IRIS_DER = [473, 474, 475, 476]


def calcular_distancia(focal_px, diametro_real_mm, diametro_px):
    return (focal_px * diametro_real_mm) / diametro_px


def diametro_iris_px(landmarks, indices, ancho, alto):
    p1 = landmarks[indices[0]]
    p2 = landmarks[indices[2]]
    x1, y1 = p1.x * ancho, p1.y * alto
    x2, y2 = p2.x * ancho, p2.y * alto
    return np.hypot(x2 - x1, y2 - y1)


def main():
    os.makedirs(CARPETA_CAPTURAS, exist_ok=True)

    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,  # necesario para obtener los puntos del iris
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7,
    )
    mp_dibujo = mp.solutions.drawing_utils
    spec = mp_dibujo.DrawingSpec(color=(188, 100, 92), thickness=1, circle_radius=1)

    cap = cv2.VideoCapture(FUENTE)
    if not cap.isOpened():
        print(f"No se pudo abrir la fuente de video: {FUENTE}")
        print("Revisá el índice de cámara o la URL del celular (ver README).")
        return

    print("Ventana abierta. Presioná 'c' para capturar, 'q' para salir.")
    historial = []
    contador = 0

    while True:
        ok, frame = cap.read()
        if not ok:
            print("No se pudo leer un frame de la fuente de video.")
            break

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        resultado = face_mesh.process(rgb)
        alto, ancho = frame.shape[:2]

        if resultado.multi_face_landmarks:
            landmarks = resultado.multi_face_landmarks[0].landmark

            mp_dibujo.draw_landmarks(
                frame, resultado.multi_face_landmarks[0],
                mp_face_mesh.FACEMESH_IRISES, spec, spec
            )

            diametro_px = diametro_iris_px(landmarks, IRIS_IZQ, ancho, alto)
            if diametro_px > 0:
                distancia_cm = calcular_distancia(
                    FOCAL_LENGTH_PIXELS, IRIS_DIAMETRO_MM, diametro_px
                ) / 10.0

                historial.append(distancia_cm)
                if len(historial) > VENTANA_PROMEDIO:
                    historial.pop(0)
                promedio = np.mean(historial)

                cv2.putText(frame, f"Distancia: {promedio:.1f} cm", (20, 40),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        cv2.putText(frame, "c: capturar   q: salir", (20, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2, cv2.LINE_AA)

        cv2.imshow("Distancia por iris", frame)

        tecla = cv2.waitKey(1) & 0xFF
        if tecla == ord('q') or tecla == 27:
            break
        elif tecla == ord('c'):
            contador += 1
            nombre = os.path.join(CARPETA_CAPTURAS, f"iris_{int(time.time())}_{contador}.jpg")
            cv2.imwrite(nombre, frame)
            print(f"Captura guardada: {nombre}")

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
