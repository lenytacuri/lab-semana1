import numpy as np


def filtrar(df, columna, umbral):
    return df[df[columna] > umbral]

def resumen_por_grupo(df, col_grupo, cols_num):
    return df.groupby(col_grupo)[cols_num].agg(['mean', 'std', 'count'])

def zscore(matriz):
    return (matriz - matriz.mean(axis=0)) / matriz.std(axis=0)

def top_k(df, columna, k):
    # np.argsort ordena de menor a mayor, tomamos los últimos k y los invertimos
    indices = np.argsort(df[columna].values)[-k:][::-1]
    return df.iloc[indices]

def recta_minimos_cuadrados(x, y):
    # Creamos la matriz de diseño [x, 1] para ajustar y = a*x + b
    A = np.column_stack([x, np.ones_like(x)])
    # Resolvemos por mínimos cuadrados
    solucion, _, _, _ = np.linalg.lstsq(A, y, rcond=None)
    # Devuelve la tupla (a, b)
    return float(solucion[0]), float(solucion[1])