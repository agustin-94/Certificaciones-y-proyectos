"""
02_filtros.py

Aplicación de filtros y mejora de calidad de imagen:
desenfoque (blur), detección de bordes (Canny), umbralización (threshold)
y operaciones morfológicas. Guarda un collage comparativo.
"""
import os
import cv2
import numpy as np
from _rutas import ruta

def etiquetar(img, texto):
    """Agrega una etiqueta arriba de cada imagen del collage."""
    if len(img.shape) == 2:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    salida = cv2.copyMakeBorder(img, 30, 0, 0, 0, cv2.BORDER_CONSTANT, value=(255, 255, 255))
    cv2.putText(salida, texto, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1, cv2.LINE_AA)
    return salida

def main():
    os.makedirs(ruta("output"), exist_ok=True)

    img = cv2.imread(ruta("assets", "muestra.jpg"))
    gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Desenfoque para reducir ruido (mejora de calidad previa a otros filtros)
    suave = cv2.GaussianBlur(img, (7, 7), 0)

    # Detección de bordes
    bordes = cv2.Canny(gris, 60, 150)

    # Umbralización binaria (útil como paso previo a OCR)
    _, binaria = cv2.threshold(gris, 150, 255, cv2.THRESH_BINARY_INV)

    # Operación morfológica: cierre, para consolidar formas/texto
    kernel = np.ones((3, 3), np.uint8)
    cierre = cv2.morphologyEx(binaria, cv2.MORPH_CLOSE, kernel)

    fila1 = np.hstack([etiquetar(img, "Original"), etiquetar(suave, "Blur (GaussianBlur)")])
    fila2 = np.hstack([etiquetar(bordes, "Bordes (Canny)"), etiquetar(cierre, "Umbral + Morfologia")])
    collage = np.vstack([fila1, fila2])

    cv2.imwrite(ruta("output", "02_filtros_collage.jpg"), collage)
    print("Listo. Collage comparativo guardado en output/02_filtros_collage.jpg")

if __name__ == "__main__":
    main()
