"""
03_deteccion_rostros.py

Reconocimiento facial con clasificadores Haar Cascade (incluidos en OpenCV).
Sirve tanto para imágenes como para video/webcam (ver comentario al final).

Nota: assets/muestra.jpg es una imagen sintética (formas geométricas) pensada
para probar el pipeline completo sin depender de archivos externos. Para una
detección facial real, reemplazá ese archivo por una foto con caras reales,
o usá directamente 05_captura_rostro_dnn.py con tu webcam/celular.
"""
import os
import cv2
from _rutas import ruta

def main():
    os.makedirs(ruta("output"), exist_ok=True)

    img = cv2.imread(ruta("assets", "muestra.jpg"))
    gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    clasificador = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    rostros = clasificador.detectMultiScale(
        gris, scaleFactor=1.1, minNeighbors=5, minSize=(60, 60)
    )
    print(f"Rostros detectados: {len(rostros)}")

    salida = img.copy()
    for (x, y, w, h) in rostros:
        cv2.rectangle(salida, (x, y), (x + w, y + h), (0, 200, 0), 2)
        cv2.putText(salida, "Rostro", (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 200, 0), 2)

    cv2.imwrite(ruta("output", "03_rostros_detectados.jpg"), salida)
    print("Listo. Resultado guardado en output/03_rostros_detectados.jpg")

    # --- Para usarlo en tiempo real con webcam (fuera del entorno de la demo) ---
    # cap = cv2.VideoCapture(0)
    # while True:
    #     ok, frame = cap.read()
    #     if not ok:
    #         break
    #     gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #     rostros = clasificador.detectMultiScale(gris, 1.1, 5)
    #     for (x, y, w, h) in rostros:
    #         cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 200, 0), 2)
    #     cv2.imshow("Deteccion en vivo", frame)
    #     if cv2.waitKey(1) & 0xFF == ord('q'):
    #         break
    # cap.release()
    # cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
