"""
06_deteccion_manos.py

Detección de manos en tiempo real con MediaPipe: dibuja los 21 puntos de
referencia (landmarks) de cada mano y cuenta cuántos dedos están levantados,
comparando la distancia de la punta de cada dedo a la palma contra la
distancia de su nudillo medio a la palma (si la punta está más lejos que
el medio, el dedo está extendido).

FUENTE DE VIDEO: podés usar la webcam de tu PC, o tu celular como cámara IP
(ver "Usar el celular como webcam" en el README). Configurá FUENTE más abajo.

Controles:
    c   -> guarda una captura del frame actual en capturas/
    q   -> sale
"""
import os
import time
import cv2
import mediapipe as mp
from math import dist
from _rutas import ruta

# --- CONFIGURACIÓN ---
# Opción A) Webcam integrada / USB: probá 0, 1, 2...
# Opción B) Celular como cámara IP (app "IP Webcam" en Android):
#           FUENTE = "http://192.168.0.XX:8080/video"
FUENTE = 0

CARPETA_CAPTURAS = ruta("capturas")

# Puntos de MediaPipe Hands: [nudillo medio, punta] de cada dedo
DEDOS = {
    "indice": [6, 8],
    "mayor": [10, 12],
    "anular": [14, 16],
    "menique": [18, 20],
    "pulgar": [3, 4],
}


def dedos_levantados(landmarks):
    """Devuelve una lista de 0/1 (mismo orden que DEDOS) indicando qué dedos
    están extendidos, comparando distancia punta-palma vs medio-palma."""
    palma = landmarks[0]
    resultado = []
    for medio_idx, punta_idx in DEDOS.values():
        medio = landmarks[medio_idx]
        punta = landmarks[punta_idx]
        d_medio = dist((palma.x, palma.y), (medio.x, medio.y))
        d_punta = dist((palma.x, palma.y), (punta.x, punta.y))
        resultado.append(1 if d_punta > d_medio else 0)
    return resultado


def main():
    os.makedirs(CARPETA_CAPTURAS, exist_ok=True)

    mp_manos = mp.solutions.hands
    manos = mp_manos.Hands(
        static_image_mode=False,
        max_num_hands=2,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7,
    )
    mp_dibujo = mp.solutions.drawing_utils

    puntas_ids = [DEDOS[d][1] for d in DEDOS]  # [8, 12, 16, 20, 4]

    cap = cv2.VideoCapture(FUENTE)
    if not cap.isOpened():
        print(f"No se pudo abrir la fuente de video: {FUENTE}")
        print("Revisá el índice de cámara o la URL del celular (ver README).")
        return

    print("Ventana abierta. Presioná 'c' para capturar, 'q' para salir.")
    contador = 0

    while True:
        ok, frame = cap.read()
        if not ok:
            print("No se pudo leer un frame de la fuente de video.")
            break

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        resultado = manos.process(rgb)

        total_arriba = 0
        if resultado.multi_hand_landmarks:
            for mano in resultado.multi_hand_landmarks:
                estado = dedos_levantados(mano.landmark)
                total_arriba += sum(estado)

                alto, ancho = frame.shape[:2]
                for i, punta_id in enumerate(puntas_ids):
                    lm = mano.landmark[punta_id]
                    cx, cy = int(lm.x * ancho), int(lm.y * alto)
                    color = (0, 255, 0) if estado[i] else (0, 0, 255)
                    cv2.circle(frame, (cx, cy), 8, color, -1)

                mp_dibujo.draw_landmarks(frame, mano, mp_manos.HAND_CONNECTIONS)

        cv2.putText(frame, f"Dedos arriba: {total_arriba}", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        cv2.putText(frame, "c: capturar   q: salir", (20, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2, cv2.LINE_AA)

        cv2.imshow("Deteccion de manos", frame)

        tecla = cv2.waitKey(1) & 0xFF
        if tecla == ord('q') or tecla == 27:
            break
        elif tecla == ord('c'):
            contador += 1
            nombre = os.path.join(CARPETA_CAPTURAS, f"manos_{int(time.time())}_{contador}.jpg")
            cv2.imwrite(nombre, frame)
            print(f"Captura guardada: {nombre}")

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
