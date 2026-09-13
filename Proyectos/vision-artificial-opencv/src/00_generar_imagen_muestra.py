"""
00_generar_imagen_muestra.py

Genera una imagen de muestra sintética (sin depender de archivos externos)
para poder correr el resto de los scripts de la demo de punta a punta:
un "cartel" con texto (para el módulo de OCR) y una cara simple dibujada
con formas geométricas (para el módulo de detección, a modo ilustrativo).

Para usar reconocimiento facial real, reemplazá assets/muestra.jpg por una
foto real con una o más caras.
"""
import cv2
import numpy as np
from _rutas import ruta

def generar_imagen_muestra(path=None):
    if path is None:
        path = ruta("assets", "muestra.jpg")
    img = np.full((480, 720, 3), (235, 225, 210), dtype=np.uint8)

    # "Cara" simple con formas geométricas, a modo ilustrativo del pipeline
    cv2.circle(img, (180, 220), 90, (200, 180, 160), -1)          # cabeza
    cv2.circle(img, (150, 195), 12, (60, 60, 60), -1)             # ojo izq
    cv2.circle(img, (210, 195), 12, (60, 60, 60), -1)             # ojo der
    cv2.ellipse(img, (180, 250), (35, 15), 0, 0, 180, (60, 60, 60), 3)  # boca

    # Ruido leve para que los filtros de suavizado tengan algo que hacer
    ruido = np.random.randint(0, 25, img.shape, dtype=np.uint8)
    img = cv2.add(img, ruido)

    # Texto para el módulo de OCR
    cv2.putText(img, "OpenCV + IA", (330, 120),
                cv2.FONT_HERSHEY_SIMPLEX, 1.1, (30, 30, 30), 2, cv2.LINE_AA)
    cv2.putText(img, "Reconocimiento de caracteres", (330, 165),
                cv2.FONT_HERSHEY_SIMPLEX, 0.65, (30, 30, 30), 2, cv2.LINE_AA)
    cv2.putText(img, "Curso: Vision Artificial", (330, 200),
                cv2.FONT_HERSHEY_SIMPLEX, 0.65, (30, 30, 30), 2, cv2.LINE_AA)

    cv2.imwrite(path, img)
    print(f"Imagen de muestra generada en: {path}")

if __name__ == "__main__":
    generar_imagen_muestra()
