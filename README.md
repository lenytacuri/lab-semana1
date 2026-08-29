# Lab Semana 1 - <nombre del dataset>

- Persona A: Leny
- Persona B: Elian
- Dataset: <archive.ics.uci.edu/static/public/360/data.csv>
- Tarea: <regresion | clasificacion> Variable objetivo: <columna>

## Como correr

uv sync
uv run pytest -q
uv run python main.py

## Hallazgos

## Decisiones de limpieza

- `-200` se trata como valor nulo (`na_values=[-200]`) al cargar los datos.
- Columnas con más de 80% de nulos se eliminan (caso `NMHC(GT)`, 90.2% nulos).
- Columnas numéricas con nulos por debajo de ese umbral se imputan con la mediana (`CO(GT)`, `NO2(GT)`, `NOx(GT)`, ~17-18% nulos); columnas categóricas se imputan con la moda.
- Se eliminan filas duplicadas y se normaliza texto (`strip` + `lower`) en columnas tipo texto.
- Valores `inf`/`-inf` se reemplazan por nulos antes de imputar.
