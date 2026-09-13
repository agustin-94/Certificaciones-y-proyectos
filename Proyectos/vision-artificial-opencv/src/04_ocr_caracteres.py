"""
04_ocr_caracteres.py

Reconocimiento de caracteres (OCR): preprocesamiento con OpenCV
(escala de grises + umbralización, para maximizar el contraste del texto)
y extracción del texto con Tesseract (via pytesseract).

Requiere el binario de Tesseract instalado en el sistema:
    Ubuntu/Debian:  sudo apt-get install tesseract-ocr tesseract-ocr-spa
    Windows:        instalador oficial de UB-Mannheim + agregar al PATH
"""
import os
import cv2
import pytesseract
from _rutas import ruta

def preprocesar_para_ocr(img):
    gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Umbral de Otsu: calcula automáticamente el mejor punto de corte
    _, binaria = cv2.threshold(gris, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return binaria

def main():
    os.makedirs(ruta("output"), exist_ok=True)

    img = cv2.imread(ruta("assets", "muestra.jpg"))
    preprocesada = preprocesar_para_ocr(img)
    cv2.imwrite(ruta("output", "04_ocr_preprocesada.jpg"), preprocesada)

    texto = pytesseract.image_to_string(preprocesada, lang="spa")
    texto = texto.strip()

    print("Texto detectado:")
    print("-" * 40)
    print(texto if texto else "(no se detectó texto)")
    print("-" * 40)

    with open(ruta("output", "04_ocr_resultado.txt"), "w") as f:
        f.write(texto)
    print("Resultado guardado en output/04_ocr_resultado.txt")

if __name__ == "__main__":
    main()
