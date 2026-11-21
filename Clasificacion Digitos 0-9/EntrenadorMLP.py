import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Input, Flatten, Dense


class EntrenadorMLP:
    def construir_red(self):
        # Construcción del MLP (perceptrón multicapa)
        red = Sequential([
            Input(shape=(28, 28)),
            Flatten(),
            Dense(256, activation="sigmoid"),
            Dense(128, activation="sigmoid"),
            Dense(10, activation="softmax"),
        ])
        red.compile(
            optimizer="adam",
            loss="sparse_categorical_crossentropy",
            metrics=["accuracy"],
        )
        return red

    def graficar_rendimiento(self, historial):
        # Gráficas de precisión y pérdida
        plt.figure(figsize=(12, 5))

        plt.subplot(1, 2, 1)
        plt.plot(historial.history["accuracy"], label="Training Accuracy", color="teal")
        plt.plot(historial.history["val_accuracy"], label="Validation Accuracy", color="tomato")
        plt.title("Training and Validation Accuracy", fontsize=14)
        plt.xlabel("Epochs", fontsize=12)
        plt.ylabel("Accuracy", fontsize=12)
        plt.legend()
        plt.grid(True)

        plt.subplot(1, 2, 2)
        plt.plot(historial.history["loss"], label="Training Loss", color="teal")
        plt.plot(historial.history["val_loss"], label="Validation Loss", color="tomato")
        plt.title("Training and Validation Loss", fontsize=14)
        plt.xlabel("Epochs", fontsize=12)
        plt.ylabel("Loss", fontsize=12)
        plt.legend()
        plt.grid(True)

        plt.suptitle("Model Training Performance", fontsize=16)
        plt.tight_layout()
        plt.show()

    def mostrar_muestra(self, x_train):
        # Vista previa de algunas imágenes de entrenamiento
        fig, ejes = plt.subplots(10, 10, figsize=(8, 8))
        indice = 0
        for fila in range(10):
            for col in range(10):
                ejes[fila][col].imshow(x_train[indice].reshape(28, 28), aspect="auto", cmap="gray")
                ejes[fila][col].axis("off")
                indice += 1
        plt.suptitle("Muestra de dígitos MNIST", fontsize=12)
        plt.tight_layout()
        plt.show()

    def cargar_mnist(self):
        # Carga del dataset MNIST (dígitos 0-9 escritos a mano)
        (x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()

        # Normalización a [0, 1]
        escala_gris = 255
        x_train = x_train.astype("float32") / escala_gris
        x_test = x_test.astype("float32") / escala_gris

        print("Feature matrix (x_train):", x_train.shape)
        print("Target matrix (y_train):", y_train.shape)
        print("Feature matrix (x_test):", x_test.shape)
        print("Target matrix (y_test):", y_test.shape)
        return x_train, y_train, x_test, y_test

    def ejecutar(self):
        x_train, y_train, x_test, y_test = self.cargar_mnist()

        red = self.construir_red()

        # Entrenamiento
        historial = red.fit(
            x_train,
            y_train,
            epochs=10,
            batch_size=2000,
            validation_split=0.2,
        )
        print(historial)

        # Evaluación en el conjunto de prueba
        resultados = red.evaluate(x_test, y_test, verbose=0)
        print("Test loss, Test accuracy:", resultados)

        # Primero curvas, luego la cuadrícula de dígitos
        self.graficar_rendimiento(historial)
        self.mostrar_muestra(x_train)


if __name__ == "__main__":
    EntrenadorMLP().ejecutar()
