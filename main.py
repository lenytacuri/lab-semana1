import matplotlib.pyplot as plt
import numpy as np

from src.analisis import recta_minimos_cuadrados, resumen_por_grupo, top_k
from src.carga import URL_DATASET, cargar, limpiar, reporte_nulos

# Paleta de dos series (puntos vs. recta ajustada)
COLOR_PUNTOS = "#2a78d6"
COLOR_RECTA = "#eb6834"


def main() -> None:
    # 1) Reporte de nulos del dataset crudo, antes de limpiar
    df_crudo = cargar(URL_DATASET, na_values=[-200])
    print("=== Reporte de nulos (dataset crudo) ===")
    print(reporte_nulos(df_crudo))

    df_limpio = limpiar(df_crudo)

    # 2) Resumen por grupo sobre el dataset ya limpio: CO y benceno por hora del día
    print("\n=== Resumen por hora del día (CO y benceno) ===")
    resumen = resumen_por_grupo(df_limpio, "Time", ["CO(GT)", "C6H6(GT)"])
    print(resumen)

    # 3) Top 5 horas con mayor concentración de benceno (variable objetivo)
    print("\n=== Top 5 horas con mayor C6H6(GT) ===")
    print(top_k(df_limpio, "C6H6(GT)", 5)[["Date", "Time", "C6H6(GT)"]])

    # 4) Recta de mínimos cuadrados entre CO(GT) y C6H6(GT): comparten origen
    # en el tráfico vehicular (ver Hallazgos de B en el README)
    x = df_limpio["CO(GT)"].to_numpy()
    y = df_limpio["C6H6(GT)"].to_numpy()
    pendiente, intercepto = recta_minimos_cuadrados(x, y)
    print("\n=== Recta de mínimos cuadrados: C6H6(GT) = a * CO(GT) + b ===")
    print(f"Pendiente (a): {pendiente:.3f}")
    print(f"Intercepto (b): {intercepto:.3f}")

    # 5) Gráfico: relación entre CO(GT) y C6H6(GT), con la recta ajustada
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.scatter(x, y, s=10, alpha=0.3, color=COLOR_PUNTOS, label="Observaciones")

    x_recta = np.linspace(x.min(), x.max(), 100)
    y_recta = pendiente * x_recta + intercepto
    ax.plot(x_recta, y_recta, color=COLOR_RECTA, linewidth=2, label="Recta de mínimos cuadrados")

    ax.set_xlabel("CO(GT) — monóxido de carbono (mg/m³)")
    ax.set_ylabel("C6H6(GT) — benceno (µg/m³)")
    ax.set_title("Relación entre CO y benceno en el aire")
    ax.grid(True, color="#d9d9d9", linewidth=0.5)
    ax.legend()

    fig.tight_layout()
    fig.savefig("figura.png")
    print("\nGráfico guardado en figura.png")


if __name__ == "__main__":
    main()
