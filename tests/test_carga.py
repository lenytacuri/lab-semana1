import numpy as np
import pandas as pd
import pytest

from lab_semana1.carga import cargar, guardar, limpiar, reporte_nulos


def test_cargar_interpreta_na_values(tmp_path):
    csv = tmp_path / "datos.csv"
    csv.write_text("id,valor\n1,10\n2,-200\n3,?\n")

    df = cargar(str(csv), na_values=["?", -200])

    assert df["valor"].isna().sum() == 2
    assert df.loc[0, "valor"] == 10


def test_reporte_nulos_cuenta_y_ordena():
    df = pd.DataFrame(
        {
            "a": [1, None, None, 4],  # 2/4 = 50% nulos
            "b": [1, 2, 3, 4],  # 0% nulos
            "c": [None, None, None, 4],  # 3/4 = 75% nulos
        }
    )

    reporte = reporte_nulos(df)

    assert list(reporte.index) == ["c", "a", "b"]
    assert reporte.loc["c", "nulos"] == 3
    assert reporte.loc["c", "porcentaje"] == pytest.approx(75.0)
    assert reporte.loc["b", "nulos"] == 0


def test_limpiar_elimina_filas_duplicadas():
    df = pd.DataFrame({"a": [1, 1], "b": ["x", "x"]})

    resultado = limpiar(df)

    assert len(resultado) == 1


def test_limpiar_sin_infinitos_ni_nulos_en_numericas():
    df = pd.DataFrame({"a": [1.0, np.inf, -np.inf, 4.0]})

    resultado = limpiar(df)

    assert not np.isinf(resultado["a"]).any()
    assert not resultado["a"].isna().any()


def test_limpiar_elimina_columna_con_mas_de_80_porciento_nulos():
    df = pd.DataFrame(
        {
            "casi_vacia": [None, None, None, None, None, 1.0],  # 5/6 = 83.3% nulos
            "completa": [1, 2, 3, 4, 5, 6],
        }
    )

    resultado = limpiar(df)

    assert "casi_vacia" not in resultado.columns
    assert "completa" in resultado.columns


def test_limpiar_imputa_mediana_en_columna_numerica_con_pocos_nulos():
    df = pd.DataFrame({"a": [1.0, 2.0, 3.0, None]})  # mediana de [1, 2, 3] = 2.0

    resultado = limpiar(df)

    assert resultado["a"].iloc[3] == pytest.approx(2.0)
    assert not resultado["a"].isna().any()


def test_limpiar_imputa_moda_en_columna_categorica_con_pocos_nulos():
    # "id" evita que la fila con nulo se confunda con un duplicado real
    df = pd.DataFrame(
        {
            "id": [1, 2, 3, 4],
            "categoria": ["rojo", "rojo", "azul", None],
        }
    )

    resultado = limpiar(df)

    assert resultado.loc[resultado["id"] == 4, "categoria"].iloc[0] == "rojo"
    assert not resultado["categoria"].isna().any()


def test_limpiar_normaliza_columnas_de_texto():
    df = pd.DataFrame({"nombre": ["  Ana ", "BOB", "cesar"]})

    resultado = limpiar(df)

    assert resultado["nombre"].tolist() == ["ana", "bob", "cesar"]


def test_limpiar_resetea_el_indice():
    df = pd.DataFrame({"a": [1, 1, 2, 3]})

    resultado = limpiar(df)

    assert list(resultado.index) == list(range(len(resultado)))


def test_guardar_escribe_un_parquet_legible(tmp_path):
    df = pd.DataFrame({"a": [1, 2, 3]})
    ruta = tmp_path / "salida.parquet"

    guardar(df, str(ruta))
    leido = pd.read_parquet(ruta)

    pd.testing.assert_frame_equal(df, leido)
