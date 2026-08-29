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

Me sorprendió la cantidad de datos nulos de la variable NMHC(GT), que corresponde a una medición de hidrocarburos no metálicos,
pero leyendo la información del dataset, dice que el instrumento dejo de funcionar durante una gran parte de tiempo durante la medición. Tener datos buenos no es fácil, menos si son datos que se obtienen de manera experimental y tienen carácter científico.

## Decisiones de limpieza

- `-200` se trata como valor nulo (`na_values=[-200]`) al cargar los datos.
- Columnas con más de 80% de nulos se eliminan (caso `NMHC(GT)`, 90.2% nulos).
- Columnas numéricas con nulos por debajo de ese umbral se imputan con la mediana (`CO(GT)`, `NO2(GT)`, `NOx(GT)`, ~17-18% nulos); columnas categóricas se imputan con la moda.
- Se eliminan filas duplicadas y se normaliza texto (`strip` + `lower`) en columnas tipo texto.
- Valores `inf`/`-inf` se reemplazan por nulos antes de imputar.

## Pregunta de investigación 1

`uv sync` puede reconstruir el entorno porque `.venv/` no es la fuente de verdad, es solo el resultado. Lo que sí subo al repo es `uv.lock`, que guarda la versión y el hash exactos de cada dependencia (incluidas las transitivas); con eso `uv sync` descarga esos mismos paquetes y arma un `.venv/` idéntico en cualquier máquina.

## Pregunta de investigación 2

Comprobé la diferencia en mi propia máquina: `pytest` a secas no encontró el comando porque no tenía el `.venv` activado (`command not found: pytest`); si en otro entorno sí lo encuentra, corre con el Python y las versiones de librerías que haya activas en ese momento en mi shell, que no tienen por qué coincidir con lo que fijé en `uv.lock`. En cambio, `uv run pytest` siempre resuelve y usa el `.venv` del proyecto sincronizado contra `uv.lock`, sin que yo tenga que activarlo a mano, así que las pruebas corren con el mismo entorno reproducible sin importar quién las ejecute.