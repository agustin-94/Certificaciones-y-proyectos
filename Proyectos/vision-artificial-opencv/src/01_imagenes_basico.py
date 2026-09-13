"""
01_imagenes_basico.py

Fundamentos de carga y manipulación de imágenes con OpenCV:
lectura, conversión de espacio de color, resize, recorte y guardado.
"""
import cv2
import os
from _rutas import ruta

def main():
    ruta_entrada = ruta("assets", "muestra.jpg")
    if not os.path.exists(ruta_entrada):
        raise FileNotFoundError(
            f"No se encontró {ruta_entrada}. Corré primero "
            "00_generar_imagen_muestra.py o reemplazá el archivo por tu propia imagen."
        )

    os.makedirs(ruta("output"), exist_ok=True)

    img = cv2.imread(ruta_entrada)
    print("Dimensiones originales (alto, ancho, canales):", img.shape)

    # Conversión de espacio de color: BGR (nativo de OpenCV) -> escala de grises
    gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(ruta("output", "01_gris.jpg"), gris)

    # Resize manteniendo proporción
    escala = 0.5
    ancho = int(img.shape[1] * escala)
    alto = int(img.shape[0] * escala)
    img_chica = cv2.resize(img, (ancho, alto), interpolation=cv2.INTER_AREA)
    cv2.imwrite(ruta("output", "01_resize.jpg"), img_chica)

    # Recorte (crop) de una región de interés (ROI)
    x, y, w, h = 300, 90, 380, 150
    recorte = img[y:y + h, x:x + w]
    cv2.imwrite(ruta("output", "01_crop_texto.jpg"), recorte)

    print("Listo. Archivos generados en output/: 01_gris.jpg, 01_resize.jpg, 01_crop_texto.jpg")

if __name__ == "__main__":
    main()
