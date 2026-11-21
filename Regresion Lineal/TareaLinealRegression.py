import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import fetch_california_housing

# Configuramos el estilo de las gráficas
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')


def cargar_muestras(cantidad=50):
    # 1. CARGA DE DATOS
    dataset = fetch_california_housing()
    idx_medinc = dataset.feature_names.index("MedInc")

    # X: Ingreso medio del vecindario (MedInc, en decenas de miles de USD)
    # Y: Valor medio de la casa (MedHouseVal, en cientos de miles de USD)
    # Tomamos un subconjunto pequeño (50 muestras) para que se vea claro en la gráfica
    ingresos = dataset.data[:cantidad, idx_medinc]
    precios = dataset.target[:cantidad]
    return ingresos, precios


def descenso_gradiente(x, y, alpha=0.01, iteraciones=5000):
    # 2. INICIALIZACIÓN DE PARÁMETROS
    peso = 0.0
    sesgo = 0.0

    # Hiperparámetros
    # alpha: tasa de aprendizaje ajustada para esta escala
    # iteraciones: épocas de entrenamiento

    # Historial para graficar la evolución del costo
    costos = []

    # 3. ENTRENAMIENTO
    for _ in range(iteraciones):
        # Predicción actual
        y_hat = peso * x + sesgo          # X -> Features     Y -> Labels

        # Cálculo del Costo (MSE con factor 1/2)
        residual = y_hat - y
        mse = np.mean(residual ** 2) / 2.0
        costos.append(mse)

        # Derivadas parciales (Gradientes) de J = 1/(2n) * sum((Y_pred - Y)^2)
        d_peso = np.mean(residual * x)
        d_sesgo = np.mean(residual)

        # Actualización de pesos
        peso = peso - alpha * d_peso
        sesgo = sesgo - alpha * d_sesgo

    return peso, sesgo, costos


def mostrar_ajuste(x, y, peso, sesgo):
    # 4. VISUALIZACIÓN DE RESULTADOS
    fig, ax = plt.subplots(figsize=(9, 5))

    # Dibujar los puntos reales
    ax.scatter(x, y, color="#3D5A80", s=55, label="Datos Reales (California Housing)", zorder=3)

    # Dibujar la línea de tendencia aprendida por el modelo
    linea_x = np.linspace(np.min(x) - 0.4, np.max(x) + 0.4, 120)
    ax.plot(
        linea_x,
        peso * linea_x + sesgo,
        color="#EE6C4D",
        linewidth=2.5,
        label=f"Modelo Lineal: Y = {peso:.2f}X + {sesgo:.2f}",
    )

    # Etiquetas y formato
    ax.set_title("Regresión Lineal From Scratch: Ingreso Medio vs Valor de la Casa")
    ax.set_xlabel("Ingreso medio (MedInc, x $10,000 USD)")
    ax.set_ylabel("Valor medio de la casa (x $100,000 USD)")
    ax.legend()
    fig.tight_layout()
    plt.show()


def mostrar_historial(costos):
    fig, ax = plt.subplots(figsize=(8, 3.5))
    ax.plot(costos, color="#293241", linewidth=2)
    ax.set_title("Evolución de la Función de Costo (Error Cuadrático Medio)")
    ax.set_xlabel("Épocas / Iteraciones")
    ax.set_ylabel("Costo (MSE)")
    fig.tight_layout()
    plt.show()


if __name__ == "__main__":
    x, y = cargar_muestras(50)
    print(f"Datos cargados con éxito: {len(x)} muestras analizadas.")

    peso, sesgo, costos = descenso_gradiente(x, y)
    print("¡Entrenamiento completado!")
    print(f"Ecuación final aprendida: Valor de la casa = {peso:.4f} * (Ingreso medio) + {sesgo:.4f}")

    # Verificación contra la solución exacta de mínimos cuadrados
    w_exacto, b_exacto = np.polyfit(x, y, 1)
    print(f"Solución exacta (np.polyfit):  w = {w_exacto:.4f}, b = {b_exacto:.4f}")

    mostrar_historial(costos)
    mostrar_ajuste(x, y, peso, sesgo)
