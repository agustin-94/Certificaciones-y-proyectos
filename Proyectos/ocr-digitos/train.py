"""
Entrenamiento del modelo de reconocimiento de dígitos (OCR).

Usa el dataset MNIST (dígitos manuscritos 0-9, 28x28 px en escala de grises)
para entrenar una red neuronal simple con Keras. El modelo entrenado se
guarda como `modelo_ocr.h5` y es el que consume `predictor_mqtt.py` para
simular la lectura de dígitos en un entorno industrial (ej. medidores).
"""

import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras


def cargar_datos():
    """Descarga y normaliza el dataset MNIST."""
    (x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()

    # Normalizar los píxeles al rango [0, 1]
    x_train = x_train.astype("float32") / 255.0
    x_test = x_test.astype("float32") / 255.0

    return (x_train, y_train), (x_test, y_test)


def construir_modelo():
    """Define una red neuronal simple para clasificar dígitos 0-9."""
    modelo = keras.Sequential([
        keras.layers.Input(shape=(28, 28)),
        keras.layers.Flatten(),
        keras.layers.Dense(128, activation="relu"),
        keras.layers.Dropout(0.2),
        keras.layers.Dense(10, activation="softmax"),
    ])

    modelo.compile(
        optimizer="adam",
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )
    return modelo


def graficar_historial(historial, salida="assets/entrenamiento.png"):
    """Grafica la precisión y la pérdida durante el entrenamiento."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

    ax1.plot(historial.history["accuracy"], label="Entrenamiento")
    ax1.plot(historial.history["val_accuracy"], label="Validación")
    ax1.set_title("Precisión por época")
    ax1.set_xlabel("Época")
    ax1.set_ylabel("Precisión")
    ax1.legend()
    ax1.grid(alpha=0.3)

    ax2.plot(historial.history["loss"], label="Entrenamiento")
    ax2.plot(historial.history["val_loss"], label="Validación")
    ax2.set_title("Pérdida por época")
    ax2.set_xlabel("Época")
    ax2.set_ylabel("Pérdida")
    ax2.legend()
    ax2.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig(salida, dpi=150)
    print(f"Gráfico de entrenamiento guardado en: {salida}")


def graficar_predicciones_ejemplo(modelo, x_test, y_test, salida="assets/predicciones_ejemplo.png"):
    """Muestra algunos dígitos de test junto con la predicción del modelo."""
    predicciones = modelo.predict(x_test[:10])
    etiquetas_predichas = predicciones.argmax(axis=1)

    fig, axes = plt.subplots(2, 5, figsize=(10, 4))
    for i, ax in enumerate(axes.flat):
        ax.imshow(x_test[i], cmap="gray")
        color = "green" if etiquetas_predichas[i] == y_test[i] else "red"
        ax.set_title(f"Pred: {etiquetas_predichas[i]} (real: {y_test[i]})", color=color, fontsize=9)
        ax.axis("off")

    plt.tight_layout()
    plt.savefig(salida, dpi=150)
    print(f"Ejemplos de predicción guardados en: {salida}")


def main():
    (x_train, y_train), (x_test, y_test) = cargar_datos()

    modelo = construir_modelo()
    modelo.summary()

    historial = modelo.fit(
        x_train, y_train,
        epochs=8,
        validation_split=0.1,
        batch_size=64,
    )

    test_loss, test_acc = modelo.evaluate(x_test, y_test, verbose=0)
    print(f"\nPrecisión en el set de test: {test_acc * 100:.2f}%")

    modelo.save("modelo_ocr.h5")
    print("Modelo guardado como modelo_ocr.h5")

    graficar_historial(historial)
    graficar_predicciones_ejemplo(modelo, x_test, y_test)


if __name__ == "__main__":
    main()
