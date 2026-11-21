import os
import tkinter as tk
from tkinter import ttk

import numpy as np
import tensorflow as tf
from PIL import Image, ImageDraw
from tensorflow.keras.layers import Dense, Flatten, Input
from tensorflow.keras.models import Sequential, load_model

# Ruta del modelo junto a este archivo (así corre desde cualquier carpeta)
CARPETA = os.path.dirname(os.path.abspath(__file__))
RUTA_MODELO = os.path.join(CARPETA, "modelo_mlp.keras")
TAMANO_CANVAS = 280
GROSOR_PINCEL = 18


def preparar_imagen(imagen_pil):
    # Recortamos al rectángulo que contiene el trazo
    caja = imagen_pil.getbbox()
    if caja is None:
        return None
    digito = imagen_pil.crop(caja)

    # Escalamos para que el lado más grande mida 20 px, manteniendo proporción
    ancho, alto = digito.size
    escala = 20.0 / max(ancho, alto)
    nuevo_ancho = max(1, int(round(ancho * escala)))
    nuevo_alto = max(1, int(round(alto * escala)))
    digito = digito.resize((nuevo_ancho, nuevo_alto), Image.Resampling.LANCZOS)

    # Lo pegamos en el centro de un lienzo de 28x28
    lienzo = Image.new("L", (28, 28), 0)
    pos_x = (28 - nuevo_ancho) // 2
    pos_y = (28 - nuevo_alto) // 2
    lienzo.paste(digito, (pos_x, pos_y))

    arreglo = np.asarray(lienzo, dtype="float32") / 255.0

    # Movemos el dígito para que su centro de masa quede en el centro (14, 14)
    ys, xs = np.indices(arreglo.shape)
    masa_total = arreglo.sum()
    if masa_total <= 0:
        return None
    centro_y = (ys * arreglo).sum() / masa_total
    centro_x = (xs * arreglo).sum() / masa_total
    desplazamiento_y = int(round(14 - centro_y))
    desplazamiento_x = int(round(14 - centro_x))
    arreglo = np.roll(arreglo, shift=(desplazamiento_y, desplazamiento_x), axis=(0, 1))

    return arreglo


class VentanaReconocimiento:
    def _limpiar(self):
        self.canvas.delete("all")
        self.pincel.rectangle([0, 0, TAMANO_CANVAS, TAMANO_CANVAS], fill=0)
        self.punto_previo = None
        self.etiqueta_prediccion.config(text="-")
        self.etiqueta_confianza.config(text="")
        for i in range(10):
            self.barras[i]["value"] = 0
            self.etiquetas_porcentaje[i].config(text="0.0%")

    def _predecir(self):
        entrada = preparar_imagen(self.imagen)
        if entrada is None:
            return

        # El modelo espera un lote: forma (1, 28, 28)
        probs = self.modelo.predict(np.expand_dims(entrada, axis=0), verbose=0)[0]
        digito = int(np.argmax(probs))

        self.etiqueta_prediccion.config(text=str(digito))
        self.etiqueta_confianza.config(text=f"Confianza: {probs[digito] * 100:.1f}%")

        for i in range(10):
            porcentaje = float(probs[i]) * 100
            self.barras[i]["value"] = porcentaje
            self.etiquetas_porcentaje[i].config(text=f"{porcentaje:.1f}%")

    def _al_soltar(self, evento):
        self.punto_previo = None
        self._predecir()

    def _al_dibujar(self, evento):
        """Dibuja un trazo continuo en el canvas y en la imagen interna."""
        if self.punto_previo is not None:
            x0, y0 = self.punto_previo
            self.canvas.create_line(
                x0,
                y0,
                evento.x,
                evento.y,
                fill="white",
                width=GROSOR_PINCEL,
                capstyle=tk.ROUND,
                smooth=True,
            )
            self.pincel.line([x0, y0, evento.x, evento.y], fill=255, width=GROSOR_PINCEL)

        # Círculo en el punto actual para que los extremos queden redondos
        radio = GROSOR_PINCEL // 2
        self.pincel.ellipse(
            [evento.x - radio, evento.y - radio, evento.x + radio, evento.y + radio],
            fill=255,
        )
        self.punto_previo = (evento.x, evento.y)

    def _armar_interfaz(self):
        panel_resultado = ttk.Frame(self.ventana, padding=12)
        panel_resultado.grid(row=0, column=1, sticky="n")
        panel_dibujo = ttk.Frame(self.ventana, padding=12)
        panel_dibujo.grid(row=0, column=0)

        # --- Resultado (se arma primero en el código) ---
        ttk.Label(panel_resultado, text="Dígito predicho:", font=("Arial", 13)).pack()
        self.etiqueta_prediccion = ttk.Label(
            panel_resultado, text="-", font=("Arial", 64, "bold")
        )
        self.etiqueta_prediccion.pack()
        self.etiqueta_confianza = ttk.Label(panel_resultado, text="", font=("Arial", 11))
        self.etiqueta_confianza.pack(pady=(0, 8))

        # Una barra de probabilidad por cada dígito
        self.barras = []
        self.etiquetas_porcentaje = []
        for digito in range(10):
            fila = ttk.Frame(panel_resultado)
            fila.pack(fill="x", pady=1)
            ttk.Label(fila, text=str(digito), width=2).pack(side="left")
            barra = ttk.Progressbar(fila, length=160, maximum=100)
            barra.pack(side="left", padx=4)
            etiqueta = ttk.Label(fila, text="0.0%", width=7)
            etiqueta.pack(side="left")
            self.barras.append(barra)
            self.etiquetas_porcentaje.append(etiqueta)

        # --- Zona de dibujo ---
        ttk.Label(panel_dibujo, text="Dibuja un número del 0 al 9:").pack()
        self.canvas = tk.Canvas(
            panel_dibujo,
            width=TAMANO_CANVAS,
            height=TAMANO_CANVAS,
            bg="black",
            cursor="pencil",
            highlightthickness=1,
        )
        self.canvas.pack(pady=6)
        self.canvas.bind("<B1-Motion>", self._al_dibujar)
        self.canvas.bind("<ButtonRelease-1>", self._al_soltar)
        ttk.Button(panel_dibujo, text="Borrar", command=self._limpiar).pack(pady=6)

    def __init__(self, ventana, modelo):
        self.ventana = ventana
        self.modelo = modelo
        self.ventana.title("Clasificador de dígitos 0-9 (MLP)")
        self.ventana.resizable(False, False)

        # Imagen interna (PIL) donde se replica lo que dibujas en el canvas
        self.imagen = Image.new("L", (TAMANO_CANVAS, TAMANO_CANVAS), color=0)
        self.pincel = ImageDraw.Draw(self.imagen)
        self.punto_previo = None

        self._armar_interfaz()


def crear_y_entrenar_modelo():
    # Carga MNIST y entrena el MLP que usará la ventana de dibujo
    (x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()

    x_train = x_train.astype("float32") / 255.0
    x_test = x_test.astype("float32") / 255.0

    modelo = Sequential([
        Input(shape=(28, 28)),
        Flatten(),
        Dense(256, activation="sigmoid"),
        Dense(128, activation="sigmoid"),
        Dense(10, activation="softmax"),
    ])

    modelo.compile(
        optimizer="adam",
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )

    modelo.fit(
        x_train,
        y_train,
        epochs=10,
        batch_size=128,
        validation_split=0.2,
    )

    perdida, precision = modelo.evaluate(x_test, y_test, verbose=0)
    print(f"Test loss: {perdida:.4f} | Test accuracy: {precision:.4f}")

    modelo.save(RUTA_MODELO)
    return modelo


def obtener_modelo():
    if os.path.exists(RUTA_MODELO):
        print("Cargando modelo guardado...")
        return load_model(RUTA_MODELO)
    print("No hay modelo guardado, entrenando (tarda un poco)...")
    return crear_y_entrenar_modelo()


if __name__ == "__main__":
    root = tk.Tk()
    modelo = obtener_modelo()
    VentanaReconocimiento(root, modelo)
    root.mainloop()
