# Evaluación 2 - La raíz que se esconde

Comparación de seis métodos de búsqueda de raíces (bisección, falsa posición, punto fijo, secante,
Newton-Raphson y Newton-Raphson mejorado) sobre seis funciones de distinta naturaleza, con tolerancia
`1e-6` y tope de 100 iteraciones.

Computacion Numerica lab02
Integrantes: Jose Herrera (rama "Jose Herrera") - Manuel Soto (rama "manv")

Las respuestas a las preguntas de convergencia y la conclusión están en [`informe.md`](informe.md).

## Estructura

```
evaluacion2-busqueda-raices/
|-- README.md
|-- requirements.txt        <- numpy, matplotlib
|-- informe.md              <- respuestas a las preguntas de convergencia + conclusión
`-- src/
    |-- assets/             <- gráficos PNG generados
    |-- data/               <- CSV generados
    `-- scripts/            <- todos los scripts de Python
```

## Entorno (venv)

Requiere Python 3.9 o superior.

```bash
# 1. Clonar y entrar al repositorio
git clone <URL-del-repositorio>
cd evaluacion2-busqueda-raices

# 2. Crear y activar el entorno virtual
python -m venv venv
source venv/bin/activate          # Linux / macOS
venv\Scripts\activate             # Windows (PowerShell / cmd)

# 3. Instalar dependencias
pip install -r requirements.txt
```

## Ejecución

Desde la raíz del repositorio (las rutas de salida no dependen del directorio actual):

```bash
python src/scripts/main.py       # métodos, CSV y gráficos principales
python src/scripts/analisis.py   # orden de convergencia empírico y sensibilidad (x0 e intervalo)
```

Ambos comandos regeneran todo el contenido de `src/data/` y `src/assets/`.

## Qué hace cada script (`src/scripts/`)

| Script | Función |
|---|---|
| `main.py` | Punto de entrada. Define las 6 funciones (con derivadas, `g(x)`, intervalo `[a, b]`, `x0` y par de la secante), verifica el ambiente controlado (Bolzano / tangencia), ejecuta los 6 métodos sobre cada función, imprime la tabla resumen y genera CSV y gráficos. |
| `metodo_base.py` | Clase base `MetodoRaiz`: guarda `f`, `tol` y `max_iter`, y exporta el historial de cada ejecución a CSV. |
| `biseccion.py` | Bisección (método cerrado; exige `f(a)*f(b) < 0`). |
| `falsa_posicion.py` | Falsa posición (método cerrado; exige `f(a)*f(b) < 0`). |
| `punto_fijo.py` | Iteración de punto fijo `x = g(x)`. |
| `secante.py` | Secante (dos estimaciones iniciales, sin derivada). |
| `newton_raphson.py` | Newton-Raphson (usa `f"`). |
| `newton_mejorado.py` | Newton-Raphson mejorado (usa `f"` y `f""`; recupera convergencia rápida en raíces múltiples). |
| `exportar_csv.py` | Genera el CSV `(x, f(x))` de cada función y el CSV resumen de convergencia. |
| `graficas.py` | Gráficos con matplotlib: función con su raíz, convergencia `\|error\|` vs iteración (escala log) y resumen de iteraciones. |
| `analisis.py` | Orden de convergencia empírico y estudio de sensibilidad al intervalo inicial y a `x0`. |

Todos los métodos y funciones usan **numpy**. Criterio de parada: `|f(x_n)| < tol` **o** `|x_n - x_(n-1)| < tol`.

## Salidas generadas

**`src/data/`**
- `<funcion>_fx.csv` - columnas `x, f(x)` (400 puntos) por función.
- `<metodo>_<funcion>_convergencia.csv` - `iteracion, raiz, error` de cada ejecución.
- `resumen_convergencia.csv` - una fila por (función, método): estado, iteraciones, raíz, error final, error real y `f(raíz)`.
- `orden_convergencia.csv` - orden de convergencia empírico por (función, método).
- `sensibilidad.csv` - iteraciones y resultado al cambiar intervalo o `x0`.

**`src/assets/`**
- `funcion_<funcion>.png` - función con su raíz marcada (intervalo sombreado y signos opuestos; tangencia en la raíz doble).
- `convergencia_<funcion>.png` - `|x_n - x_(n-1)|` vs iteración, escala log, todos los métodos.
- `convergencia_real_<funcion>.png` - `|x_n - raíz|` vs iteración, escala log.
- `resumen_iteraciones.png` - iteraciones por método y función.
- `sensibilidad_x0.png` - iteraciones según la estimación inicial.

## Flujo de trabajo con Git

Cada integrante trabaja en su rama y lo evaluado se integra a `main`:

```bash
git checkout -b colaborador1
# ... trabajar, git add, git commit ...
git checkout main
git merge colaborador1
git push origin main
```
