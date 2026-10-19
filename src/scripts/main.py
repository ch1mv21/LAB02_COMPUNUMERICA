#Integrantes: Jose Herrera Manuel Soto
#Curso: Computacion Numerica
#Fecha: 18/10/2026

import numpy as np
from biseccion import Biseccion
from falsa_posicion import FalsaPosicion
from punto_fijo import PuntoFijo
from secante import Secante
from newton_raphson import NewtonRaphson
from newton_mejorado import NewtonMejorado
import graficas
import exportar_csv

#Constantes

TOL = 1e-6
MAX_ITER = 100

# Cada caso declara: la función y sus derivadas, la g(x) de punto fijo, el intervalo [a, b]
# (métodos cerrados), la estimación inicial x0 (punto fijo, Newton) y el par de la secante.
# En las raíces simples: x0 = punto medio del intervalo y secante = (a, b).
CASOS = [
    {
        "nombre": "polinomica",
        "categoria": "Polinómica\n(raíz simple)",
        "titulo": r"Polinómica (raíz simple): $f(x)=x^3-x-2$",
        "f": lambda x: x**3 - x - 2,
        "df": lambda x: 3 * x**2 - 1,
        "d2f": lambda x: 6 * x,
        "g": lambda x: np.cbrt(x + 2),                 # x = (x+2)^(1/3)
        "intervalo": (1.0, 2.0), "x0": 1.5, "secante": (1.0, 2.0),
        "rango": (0.5, 2.5),
    },
    {
        "nombre": "raiz_doble",
        "categoria": "Polinómica\n(raíz doble)",
        "titulo": r"Polinómica (raíz doble): $f(x)=(x-2)^2$",
        "f": lambda x: (x - 2)**2,
        "df": lambda x: 2 * (x - 2),
        "d2f": lambda x: 2.0,
        "g": lambda x: (x**2 + 4) / 4,                 # de x^2 - 4x + 4 = 0  ->  x = (x^2+4)/4
        "intervalo": (1.2, 2.8),                       # a y b simétricos: f(a) = f(b) > 0, sin cambio de signo
        "x0": 1.2, "secante": (1.2, 1.5),
        "rango": (1.0, 3.0),
        "raiz": 2.0, "raiz_doble": True,
    },
    {
        "nombre": "logaritmica",
        "categoria": "Logarítmica",
        "titulo": r"Logarítmica: $f(x)=\ln(x)+x-4$",
        "f": lambda x: np.log(x) + x - 4,
        "df": lambda x: 1 / x + 1,
        "d2f": lambda x: -1 / x**2,
        "g": lambda x: 4 - np.log(x),                  # x = 4 - ln(x)
        "intervalo": (2.0, 3.0), "x0": 2.5, "secante": (2.0, 3.0),
        "rango": (1.0, 4.0),
    },
    {
        "nombre": "exponencial",
        "categoria": "Exponencial",
        "titulo": r"Exponencial: $f(x)=e^{-x}-x$",
        "f": lambda x: np.exp(-x) - x,
        "df": lambda x: -np.exp(-x) - 1,
        "d2f": lambda x: np.exp(-x),
        "g": lambda x: np.exp(-x),                     # x = e^(-x)
        "intervalo": (0.0, 1.0), "x0": 0.5, "secante": (0.0, 1.0),
        "rango": (-0.2, 1.2),
    },
    {
        "nombre": "trigonometrica",
        "categoria": "Trigonométrica",
        "titulo": r"Trigonométrica: $f(x)=\cos(x)-x$",
        "f": lambda x: np.cos(x) - x,
        "df": lambda x: -np.sin(x) - 1,
        "d2f": lambda x: -np.cos(x),
        "g": lambda x: np.cos(x),                      # x = cos(x)
        "intervalo": (0.0, 1.0), "x0": 0.5, "secante": (0.0, 1.0),
        "rango": (-0.2, 1.2),
    },
    {
        "nombre": "mixta",
        "categoria": "Mixta",
        "titulo": r"Mixta: $f(x)=\sqrt{x}-\cos(x)$",
        "f": lambda x: np.sqrt(x) - np.cos(x),
        "df": lambda x: 1 / (2 * np.sqrt(x)) + np.sin(x),
        "d2f": lambda x: -1 / (4 * x**1.5) + np.cos(x),
        "g": lambda x: (x + np.cos(x)**2) / 2,         # de x = cos^2(x), promediada con x para que converja rápido
        "intervalo": (0.1, 1.0), "x0": 0.55, "secante": (0.1, 1.0),
        "rango": (0.05, 1.2),
    },
]

# nombre -> (clase, nombre para el CSV, cómo se llama a ejecutar)
METODOS = {
    "Bisección":       (Biseccion,      "biseccion",       lambda m, c: m.ejecutar(*c["intervalo"])),
    "Falsa posición":  (FalsaPosicion,  "falsa_posicion",  lambda m, c: m.ejecutar(*c["intervalo"])),
    "Punto fijo":      (PuntoFijo,      "punto_fijo",      lambda m, c: m.ejecutar(c["g"], c["x0"])),
    "Secante":         (Secante,        "secante",         lambda m, c: m.ejecutar(*c["secante"])),
    "Newton-Raphson":  (NewtonRaphson,  "newton_raphson",  lambda m, c: m.ejecutar(c["df"], c["x0"])),
    "Newton mejorado": (NewtonMejorado, "newton_mejorado", lambda m, c: m.ejecutar(c["df"], c["d2f"], c["x0"])),
}
CERRADOS = ("Bisección", "Falsa posición")


def raiz_referencia(caso):
    """Raíz 'verdadera' para medir el error real: la declarada o una bisección hasta precisión de máquina."""
    if caso.get("raiz") is not None:
        return caso["raiz"]
    a, b = caso["intervalo"]
    f = caso["f"]
    for _ in range(200):
        c = (a + b) / 2
        if f(a) * f(c) <= 0:
            b = c
        else:
            a = c
    return (a + b) / 2


def verificar_ambiente(caso, raiz):
    """Demuestra que hay raíz en el rango: cambio de signo (Bolzano) o tangencia al eje (raíz doble)."""
    f = caso["f"]
    a, b = caso["intervalo"]
    fa, fb = f(a), f(b)
    print(f"\n[{caso["nombre"]}] intervalo [{a}, {b}] | x0 = {caso["x0"]} | secante = {caso["secante"]} "
          f"| tol = {TOL:g} | max_iter = {MAX_ITER}")
    if caso.get("raiz_doble"):
        h = 1e-3
        toca = abs(f(raiz)) < 1e-12 and abs(caso["df"](raiz)) < 1e-12
        sin_cruce = f(raiz - h) * f(raiz + h) > 0
        print(f"  f(a)·f(b) = {fa * fb:.4g} > 0  -> sin cambio de signo: Bolzano no aplica")
        print(f"  f({raiz:g}) = {f(raiz):.1e}, f'({raiz:g}) = {caso['df'](raiz):.1e}, "
              f"f no cambia de signo alrededor de la raíz -> tangente al eje x: {toca and sin_cruce}")
    else:
        if fa * fb >= 0:
            raise ValueError(f"El intervalo de '{caso['nombre']}' no tiene cambio de signo.")
        print(f"  f(a) = {fa:.4f}, f(b) = {fb:.4f}, f(a)·f(b) = {fa * fb:.4f} < 0  -> Bolzano: hay raíz en [a, b]")


def aplicar_metodo(nombre, caso):
    """Ejecuta un método sobre un caso y devuelve su resultado, sin que un fallo detenga al resto.
    estado: 'ok' | 'no converge' (agotó max_iter) | 'no aplica' (método cerrado sin cambio de signo) | 'falla'."""
    clase, archivo, llamar = METODOS[nombre]
    metodo = clase(funcion=caso["f"], nombre_funcion=caso["nombre"], tol=TOL, max_iter=MAX_ITER)
    resultado = {"raiz": np.nan, "historial": [], "estado": "ok", "mensaje": ""}
    try:
        with np.errstate(all="ignore"):
            raiz, historial = llamar(metodo, caso)
    except (ValueError, ZeroDivisionError, OverflowError) as e:
        resultado["estado"] = "no aplica" if nombre in CERRADOS else "falla"
        resultado["mensaje"] = str(e)
        return resultado

    with np.errstate(all="ignore"):
        converge = np.isfinite(raiz) and (abs(caso["f"](raiz)) < TOL or historial[-1]["error"] < TOL)
    resultado.update(raiz=raiz, historial=historial, estado="ok" if converge else "no converge")
    metodo.guardar_csv_convergencia(historial, archivo)
    return resultado


def imprimir_resumen(resultados):
    ancho = 16
    print("\n=== Iteraciones por método y función ===")
    print(f"{"Función":<16}" + "".join(f"{m:>{ancho}}" for m in METODOS))
    for caso in CASOS:
        celdas = []
        for metodo in METODOS:
            res = resultados[caso["nombre"]][metodo]
            if res["estado"] == "no aplica":
                celdas.append("N/A")
            elif res["estado"] == "falla":
                celdas.append("FALLA")
            elif res["estado"] == "no converge":
                celdas.append(f"{len(res["historial"])}*")
            else:
                celdas.append(str(len(res["historial"])))
        print(f"{caso["nombre"]:<16}" + "".join(f"{c:>{ancho}}" for c in celdas))
    print("N/A = no aplica (sin cambio de signo) · FALLA = el método se detuvo con error · "
          "* = agotó el tope de iteraciones sin alcanzar la tolerancia")


if __name__ == "__main__":
    print("--- Iniciando búsqueda de raíces ---")

    resultados, raices = {}, {}
    for caso in CASOS:
        nombre = caso["nombre"]
        raices[nombre] = raiz_referencia(caso)

        verificar_ambiente(caso, raices[nombre])
        exportar_csv.guardar_csv_funcion(caso)

        resultados[nombre] = {m: aplicar_metodo(m, caso) for m in METODOS}
        for m, res in resultados[nombre].items():
            if res["estado"] in ("no aplica", "falla"):
                print(f"  {m}: {res["estado"]} -> {res["mensaje"]}")
            else:
                print(f"  {m}: raíz = {res["raiz"]:.8f} en {len(res["historial"])} iteraciones ({res["estado"]})")

        graficas.graficar_funcion(caso, raices[nombre])
        graficas.graficar_convergencia(caso, resultados[nombre], TOL, raices[nombre])
        graficas.graficar_convergencia(caso, resultados[nombre], TOL, raices[nombre], error_real=True)

    exportar_csv.guardar_csv_resumen(CASOS, resultados, raices)
    imprimir_resumen(resultados)
    graficas.graficar_resumen_iteraciones(CASOS, resultados, MAX_ITER)
