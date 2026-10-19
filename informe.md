# La raíz que se esconde - Informe de convergencia

Integrantes: Jose Herrera, Manuel Soto

Todos los números de este informe salen de `python src/scripts/main.py` y `python src/scripts/analisis.py`
(CSV en `src/data/`, gráficos en `src/assets/`). Tolerancia `1e-6`, tope de 100 iteraciones.

## 1. Ambiente controlado

| Función | Categoría | Intervalo `[a, b]` | `x0` | Secante `(x0, x1)` | Evidencia de raíz |
|---|---|---|---|---|---|
| `x^3 - x - 2` | Polinómica (raíz simple) | [1, 2] | 1.5 | (1, 2) | f(a)*f(b) = -8 < 0 |
| `(x - 2)^2` | Polinómica (raíz doble) | [1.2, 2.8] | 1.2 | (1.2, 1.5) | f(a)*f(b) = 0.41 > 0 (sin cambio de signo); f(2) = f"(2) = 0 y f no cambia de signo alrededor de 2 -> tangente al eje |
| `ln x + x - 4` | Logarítmica | [2, 3] | 2.5 | (2, 3) | f(a)*f(b) = -0.129 < 0 |
| `e^-x - x` | Exponencial | [0, 1] | 0.5 | (0, 1) | f(a)*f(b) = -0.632 < 0 |
| `cos x - x` | Trigonométrica | [0, 1] | 0.5 | (0, 1) | f(a)*f(b) = -0.460 < 0 |
| `sqrt(x) - cos x` | Mixta | [0.1, 1] | 0.55 | (0.1, 1) | f(a)*f(b) = -0.312 < 0 |

Respaldo gráfico: `src/assets/funcion_<nombre>.png` (intervalo sombreado, signos de f(a) y f(b) y raíz marcada; en la raíz doble, anotación de la tangencia).
Las `g(x)` de punto fijo son: `cbrt(x+2)`, `(x^2+4)/4`, `4 - ln x`, `e^-x`, `cos x` y `(x + cos^2x)/2`
(esta última es `x = cos^2x` promediada con `x` para acelerar la convergencia).

## 2. Resultados (iteraciones)

![Resumen de iteraciones](src/assets/resumen_iteraciones.png)

| Función | Bisección | Falsa posición | Punto fijo | Secante | Newton-Raphson | Newton mejorado |
|---|---|---|---|---|---|---|
| Polinómica (raíz simple), r ~ 1.521380 | 20 | 12 | 7 | 6 | **2** | **2** |
| Polinómica (raíz doble), r = 2 | N/A | N/A | 100* | 13 | 10 | **1** |
| Logarítmica, r ~ 2.926271 | 19 | 4 | 13 | **3** | **3** | **3** |
| Exponencial, r ~ 0.567143 | 20 | 7 | 21 | 4 | **2** | **2** |
| Trigonométrica, r ~ 0.739085 | 20 | 5 | 33 | 4 | **3** | **3** |
| Mixta, r ~ 0.641714 | 20 | 4 | 4 | **3** | **2** | **2** |

`N/A` = no aplica (sin cambio de signo) - `*` = agotó las 100 iteraciones sin alcanzar la tolerancia.

## 3. Preguntas de convergencia

### 3.1 ¿Qué método convergió en menos iteraciones en cada función? ¿Por qué?

- **Raíces simples (5 funciones):** ganan **Newton-Raphson y Newton mejorado** (2-3 iteraciones; en la logarítmica empatan con la secante en 3). Usan la pendiente real de `f` en cada paso y su convergencia es cuadrática: el número de decimales correctos se duplica por iteración.
- **Secante** queda un paso detrás (3-6 iteraciones): aproxima la derivada con dos puntos, por lo que su orden es ~ 1.618.
- **Falsa posición** (4-12) y **punto fijo** (4-33) son lineales; **bisección** necesita 19-20 porque solo reduce el intervalo a la mitad por paso (log2(1/10^-6) ~ 20).
- **Raíz doble:** gana **Newton mejorado con 1 iteración**. Para `f = (x-2)^2` la fórmula `x - f*f"/(f"^2 - f*f"")` da exactamente 2 (ver 3.4).
- Excepción: en la mixta el punto fijo (4 iteraciones) empata con falsa posición. No es mérito del método sino de la `g` elegida: `|g"(r)| ~ 0.02`, de modo que el error se reduce ~50 veces por paso.
  En general la velocidad del punto fijo depende de `|g"(r)|`: 0.14 (polinómica, 7 it.), 0.34 (logarítmica, 13), 0.57 (exponencial, 21), 0.67 (trigonométrica, 33).

### 3.2 ¿Qué orden de convergencia tiene cada método y cómo se refleja en `|error|` vs iteración?

Orden empírico estimado con `p_n = ln(e_(n+1)/e_n) / ln(e_n/e_(n-1))` y `e_n = |x_n - r|` (`src/data/orden_convergencia.csv`):

| Método | Teórico | Empírico (raíces simples) | Cómo se ve en el gráfico (escala log) |
|---|---|---|---|
| Bisección | lineal (factor 1/2) | no es una sucesión monótona; el error cae ~ 1/2 por paso (20 pasos para 10^-6) | descenso en zigzag y lento |
| Falsa posición | lineal | 1.00 | recta de pendiente moderada |
| Punto fijo | lineal (factor `\|g"(r)\|`) | 1.00 | recta; más empinada cuanto menor `\|g"(r)\|` |
| Secante | ~ 1.618 | 1.52 - 1.69 (log., exp., trig.) | curva que se empina cada vez más |
| Newton-Raphson | 2 | 2.00 (log.), 1.997 (trig.) | caída casi vertical en 2-3 puntos |
| Newton mejorado | 2 | 1.999 (log.), 2.005 (trig.) | igual que Newton |

Salvedades: en varias funciones Newton termina en 2 iteraciones, así que no hay puntos suficientes para estimar `p` (celda vacía en el CSV). El 2.40 de la secante en la mixta sale de solo 3 iteraciones y no es confiable.
En escala log, un método lineal dibuja una recta; uno de orden 2 dibuja una curva que cae cada vez más rápido (ver `convergencia_real_<función>.png`).

### 3.3 ¿Qué métodos requieren cambio de signo y cuáles no?

- **Requieren `f(a)*f(b) < 0`:** bisección y falsa posición (métodos cerrados). El código lo valida y lanza `ValueError` -> estado `no aplica`.
- **No lo requieren:** punto fijo, secante, Newton y Newton mejorado (métodos abiertos). Solo piden estimaciones iniciales (más `g`, `f"`, `f""` según el caso), pero a cambio **no garantizan convergencia** (ver 3.5).

### 3.4 Función que toca el eje x (raíz doble)

![Convergencia en la raíz doble](src/assets/convergencia_real_raiz_doble.png)

| Método | Resultado | Error real \|x - 2\| |
|---|---|---|
| Bisección, falsa posición | **No aplican**: f(1.2) = f(2.8) ~ 0.64 > 0, no hay cambio de signo | - |
| Punto fijo | **No converge** (100 it.) | 3.7*10^-2 |
| Secante | 13 it., convergencia **lineal** (p ~ 1.00) | 9.6*10^-4 |
| Newton-Raphson | 10 it., convergencia **lineal** (p ~ 1.00) | 7.8*10^-4 |
| Newton mejorado | **1 it., exacto** | 0 |

Por qué:
- **Cerrados:** al no cruzar el eje, `f` nunca cambia de signo; la raíz existe pero Bolzano no puede garantizarla.
- **Punto fijo:** `g(x) = (x^2+4)/4` tiene `g"(2) = 1`, justo en el límite de convergencia; se acerca de forma sublineal y no alcanza `1e-6` en 100 pasos.
- **Newton y secante:** con raíz doble `f"(r) = 0`, así que se pierde el orden cuadrático y quedan lineales. Para Newton el error se **reduce exactamente a la mitad por iteración** (0.8 -> 0.4 -> ... -> 7.8*10^-4 tras 10 pasos).
- **Newton mejorado:** con `f = (x-2)^2`, `f"^2 - f*f"" = 2(x-2)^2` y `f*f" = 2(x-2)^3`; el paso vale `x - (x-2) = 2`. El método está diseñado para raíces múltiples.

**Advertencia sobre el criterio de parada:** Newton y secante se detienen por `|f(x)| < 10^-6`, pero el error real es ~ 10^-3. Cerca de una raíz doble `f ~ (x-r)^2`, así que `|f| < tol` solo garantiza `|x-r| <~ sqrt(tol) = 10^-3`. El "ok" de estos métodos aquí es menos preciso que en las raíces simples.

### 3.5 ¿Cómo influyen el intervalo y la estimación inicial?

Datos en `src/data/sensibilidad.csv`; gráfico en `src/assets/sensibilidad_x0.png`.

![Sensibilidad a x0](src/assets/sensibilidad_x0.png)

**Intervalo (métodos cerrados), `x^3 - x - 2`:**

| Intervalo | Bisección | Falsa posición |
|---|---|---|
| [1.4, 1.6] | 18 | 5 |
| [1, 2] | 20 | 12 |
| [0, 2] | 21 | 14 |
| [1, 10] | 23 | **100 (no converge)** |
| [-5, 5] | 24 | 75 |

La bisección crece lentamente (~ log2 de la longitud) y siempre converge mientras haya cambio de signo. Falsa posición es mucho más sensible: con intervalos anchos y función convexa uno de los extremos queda fijo y el otro se acerca muy despacio (con [1, 10] llegó a 1.5172 tras 100 pasos, lejos de 1.52138).

**Estimación inicial (métodos abiertos):**

| Caso | Resultado |
|---|---|
| `x^3-x-2`, Newton, x0 = 1.5 / 1 / 2 / 5 / 0 | 2 / 5 / 4 / 7 / **30** iteraciones (x0 = 0 está lejos y f"(0) = -1 envía el primer paso lejos) |
| `cos x - x`, Newton, x0 = 10 | **no converge** (tras 100 pasos x ~ 64.9); Newton mejorado sí converge, en 21 |
| `ln x + x - 4`, Newton mejorado, x0 = 0.5 o 0.1 | **falla**: el primer paso cae en x < 0, fuera del dominio de ln |
| `ln x + x - 4`, Newton-Raphson, x0 = 0.1 | converge en 5 (sigue siendo robusto aquí) |
| `cos x - x`, punto fijo, cualquier x0  en  [0, 10] | 32-34 iteraciones (`\|g"\| < 1` en todo punto que importa) |
| `(x-2)^2`, punto fijo, x0 = 3 o 5 | **diverge** (`g"(x) = x/2 > 1`) |
| `(x-2)^2`, secante, (1.9, 2.2) | **falla**: los dos puntos son simétricos respecto de 2 y `f(1.8) = f(2.2)` -> división por cero |

Conclusión: una buena `x0` cuesta 2-4 iteraciones; una mala puede multiplicar por 10 el costo o hacer que el método falle. Cuanto más rápido el método, más sensible a `x0`.

### 3.6 ¿Qué método recomendamos según el tipo de función?

| Situación | Recomendación | Razón (con datos) |
|---|---|---|
| Raíz simple, función suave, derivada disponible, buena `x0` | **Newton-Raphson** | 2-3 iteraciones, orden 2 |
| Raíz simple, sin derivada | **Secante** | 3-6 iteraciones, sin calcular `f"` |
| Solo se conoce un intervalo con cambio de signo y se exige garantía | **Bisección** | siempre converge (20 it.), robusta frente a la elección del intervalo |
| Compromiso velocidad / robustez | **Falsa posición** sobre un intervalo ajustado | 4-12 it., pero degradable (100 it. con [1, 10]) |
| Raíz múltiple o sospecha de `f"(r) = 0` | **Newton mejorado** | 1 iteración en `(x-2)^2`; los demás métodos abiertos pierden el orden |
| Punto fijo | Solo si `\|g"(r)\|` es pequeño | 4 a 33 iteraciones según `g`; depende por completo de cómo se despeje |

## 4. Conclusión

**Método por tipo de función.** Para las cinco funciones con raíz simple elegiríamos **Newton-Raphson** (2-3 iteraciones) si se dispone de `f"` y de una estimación razonable, y **secante** (3-6 iteraciones) si no. Si la prioridad es la robustez, **bisección** es la única que nunca falló mientras había cambio de signo, aunque cuesta 19-20 iteraciones; es 7 a 10 veces más lenta que Newton. Para una raíz múltiple elegiríamos **Newton mejorado**, que resolvió `(x-2)^2` en 1 iteración mientras que Newton clásico y secante necesitaron 10 y 13 con error real ~ 10^-3.

**Raíz doble: "tener raíz" no es "cambiar de signo".** En `(x-2)^2` la raíz existe y es exacta (x = 2), pero la curva solo toca el eje: `f(a)*f(b) > 0`. Por eso bisección y falsa posición no aplican y punto fijo no converge. El cambio de signo es una *condición suficiente* para garantizar una raíz (Bolzano), no *necesaria*. Además, la raíz doble degrada a los métodos abiertos: Newton y secante pasan de orden 2 y 1.6 a orden 1, y el criterio `|f| < tol` deja de reflejar el error real (10^-6 en `f` equivale a ~ 10^-3 en `x`).

**Intervalo y estimación inicial.** Al reducir el intervalo de [1, 10] a [1.4, 1.6], falsa posición pasó de **100 iteraciones sin converger** a 5, y bisección de 23 a 18. En los métodos abiertos, mover `x0` de 1.5 a 0 en la polinómica llevó Newton de 2 a 30 iteraciones; en la trigonométrica, `x0 = 10` hizo que Newton no convergiera, y en la logarítmica `x0 <= 0.5` hizo fallar a Newton mejorado. La velocidad de un método abierto se paga con sensibilidad al punto de partida.

**Limitaciones.** Los números dependen de las funciones y de los `x0` e intervalos declarados; el orden empírico se estima con pocas iteraciones (2-6) en los métodos rápidos, así que es una confirmación cualitativa de la teoría, no una medición precisa.
