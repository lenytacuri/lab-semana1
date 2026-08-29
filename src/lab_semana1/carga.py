import numpy as np
import pandas as pd

URL_DATASET = "https://archive.ics.uci.edu/static/public/360/data.csv"


def cargar(url: str, na_values=None) -> pd.DataFrame:
    return pd.read_csv(url, na_values=na_values)


def reporte_nulos(df: pd.DataFrame) -> pd.DataFrame:
    conteo = df.isna().sum()
    porcentaje = df.isna().mean() * 100
    reporte = pd.DataFrame({"nulos": conteo, "porcentaje": porcentaje})
    return reporte.sort_values("nulos", ascending=False)


def limpiar(df: pd.DataFrame) -> pd.DataFrame:
    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.drop_duplicates()

    columnas_texto = df.select_dtypes(include=["object", "string"]).columns
    for col in columnas_texto:
        df[col] = df[col].str.strip().str.lower()

    for col in df.columns:
        porcentaje_nulos = df[col].isna().mean() * 100
        if porcentaje_nulos == 0:
            continue
        if porcentaje_nulos > 80:
            df = df.drop(columns=col)
        elif pd.api.types.is_numeric_dtype(df[col]):
            df[col] = df[col].fillna(df[col].median())
        else:
            moda = df[col].mode()
            if not moda.empty:
                df[col] = df[col].fillna(moda.iloc[0])

    return df.reset_index(drop=True)


def guardar(df: pd.DataFrame, ruta: str) -> None:
    df.to_parquet(ruta)


def mostrar_head(df: pd.DataFrame, n: int = 10) -> None:
    print(df.head(n))


if __name__ == "__main__":
    df_crudo = cargar(URL_DATASET, na_values=[-200])
    print(reporte_nulos(df_crudo))

    df_limpio = limpiar(df_crudo)
    mostrar_head(df_limpio)
    guardar(df_limpio, "data/limpio.parquet")
