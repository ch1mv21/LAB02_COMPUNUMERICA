"""Análisis complementario para el informe:
  1. Orden de convergencia empírico de cada método (con el error real |x_n - raíz|).
  2. Sensibilidad al intervalo inicial [a, b] y a la estimación inicial x0.

Se ejecuta después (o en vez) de main.py:  python src/scripts/analisis.py
No toca los CSV de convergencia generados por main.py.
"""
import csv
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

import main
from main import CASOS, METODOS, TOL, MAX_ITER, raiz_referencia

RAIZ_PROYECTO = Path(__file__).resolve().parents[2]
DATA = RAIZ_PROYECTO / "src" / "data"
ASSETS = RAIZ_PROYECTO / "src" / "assets"


def correr(nombre_metodo, caso, args_override=None):
    """Ejecuta un método sin escribir CSV. Devuelve (estado, raiz, historial, mensaje)."""
    clase = METODOS[nombre_metodo][0]
    metodo = clase(funcion=caso["f"], nombre_funcion=caso["nombre"], tol=TOL, max_iter=MAX_ITER)
    c = dict(caso)
    if args_override:
        c.update(args_override)
    try:
        with np.errstate(all="ignore"):
            raiz, hist = METODOS[nombre_metodo][2](metodo, c)
    except (ValueError, ZeroDivisionError, OverflowError) as e:
        return ("no aplica" if nombre_metodo in main.CERRADOS else "falla"), np.nan, [], str(e)
    with np.errstate(all="ignore"):
        ok = np.isfinite(raiz) and (abs(caso["f"](raiz)) < TOL or hist[-1]["error"] < TOL)
    return ("ok" if ok else "no converge"), raiz, hist, ""


# ---------------------------------------------------------------- 1. orden empírico
def orden_empirico(errores):
    """p_n = ln(e_{n+1}/e_n) / ln(e_n/e_{n-1}), usando solo errores > 1e-14 (ruido de máquina)."""
    e = np.array([x for x in errores if x > 1e-14])
    if len(e) < 3:
        return np.nan
    p = np.log(e[2:] / e[1:-1]) / np.log(e[1:-1] / e[:-2])
    p = p[np.isfinite(p)]
    return float(np.median(p)) if len(p) else np.nan


def tabla_orden():
    filas = []
    for caso in CASOS:
        r = raiz_referencia(caso)
        for m in METODOS:
            estado, _, hist, _ = correr(m, caso)
            if not hist:
                filas.append((caso["nombre"], m, estado, "", ""))
                continue
            err = np.abs(np.array([d["raiz"] for d in hist]) - r)
            filas.append((caso["nombre"], m, estado, len(hist), orden_empirico(err)))
    with open(DATA / "orden_convergencia.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["funcion", "metodo", "estado", "iteraciones", "orden_empirico"])
        for fila in filas:
            w.writerow([*fila[:4], "" if fila[4] == "" or np.isnan(fila[4]) else f"{fila[4]:.3f}"])
    print(f"Guardado: {DATA / "orden_convergencia.csv"}")


# ---------------------------------------------------------------- 2. sensibilidad
# (función, método, parámetro cambiado, lista de valores)
def escenarios():
    """Cada escenario: (funcion, tipo, etiqueta, override)."""
    esc = []
    esc += [("polinomica", "intervalo", f"[{a}, {b}]", {"intervalo": (a, b)})
            for a, b in [(1.0, 2.0), (1.4, 1.6), (0.0, 2.0), (1.0, 10.0), (-5.0, 5.0)]]
    esc += [("polinomica", "x0", f"x0={x}", {"x0": x, "secante": (x, x + 0.5)})
            for x in [1.5, 1.0, 2.0, 5.0, 0.0]]
    esc += [("trigonometrica", "intervalo", f"[{a}, {b}]", {"intervalo": (a, b)})
            for a, b in [(0.0, 1.0), (0.5, 1.0), (-1.0, 1.0), (0.0, 3.0)]]
    esc += [("trigonometrica", "x0", f"x0={x}", {"x0": x, "secante": (x, x + 0.5)})
            for x in [0.5, 0.0, 1.0, 3.0, 10.0]]
    esc += [("logaritmica", "x0", f"x0={x}", {"x0": x, "secante": (x, x + 0.5)})
            for x in [2.5, 1.0, 0.5, 0.1, 5.0, 10.0]]
    esc += [("raiz_doble", "x0", f"x0={x}", {"x0": x, "secante": (x, x + 0.3)})
            for x in [1.2, 0.0, 1.9, 3.0, 5.0]]
    return esc


def tabla_sensibilidad():
    por_nombre = {c["nombre"]: c for c in CASOS}
    filas = []
    for fn, tipo, etiqueta, over in escenarios():
        caso = por_nombre[fn]
        r = raiz_referencia(caso)
        usados = main.CERRADOS if tipo == "intervalo" else tuple(m for m in METODOS if m not in main.CERRADOS)
        for m in usados:
            estado, raiz, hist, msg = correr(m, caso, over)
            # ¿converge a la raíz esperada? (con 1e-3 de tolerancia para raíz doble)
            llega = estado == "ok" and abs(raiz - r) < (5e-3 if caso.get("raiz_doble") else 1e-4)
            filas.append(dict(funcion=fn, tipo=tipo, escenario=etiqueta, metodo=m, estado=estado,
                              iteraciones=len(hist), raiz=float(raiz) if np.isfinite(raiz) else "",
                              llega_a_raiz=llega))
    with open(DATA / "sensibilidad.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(filas[0]))
        w.writeheader()
        w.writerows(filas)
    print(f"Guardado: {DATA / "sensibilidad.csv"}")
    return filas


def graficar_sensibilidad(filas):
    """Barras: iteraciones vs x0 para los métodos abiertos en la función trigonométrica y la logarítmica."""
    fig, axes = plt.subplots(1, 2, figsize=(13, 4.8))
    for ax, fn in zip(axes, ["trigonometrica", "logaritmica"]):
        sub = [f for f in filas if f["funcion"] == fn and f["tipo"] == "x0"]
        etiquetas = list(dict.fromkeys(f["escenario"] for f in sub))
        metodos = list(dict.fromkeys(f["metodo"] for f in sub))
        ancho = 0.8 / len(metodos)
        for j, m in enumerate(metodos):
            alturas, malos = [], []
            for e in etiquetas:
                fila = next(f for f in sub if f["escenario"] == e and f["metodo"] == m)
                alturas.append(fila["iteraciones"])
                malos.append(not fila["llega_a_raiz"])
            pos = np.arange(len(etiquetas)) + (j - (len(metodos) - 1) / 2) * ancho
            barras = ax.bar(pos, alturas, ancho, label=m, color=main.graficas.ESTILOS[m]["color"],
                            edgecolor="black", linewidth=0.5)
            for b, mal, n in zip(barras, malos, alturas):
                if mal:
                    b.set_hatch("//")
                    ax.text(b.get_x() + b.get_width() / 2, n + 0.5, "X", ha="center", fontsize=8, color="red")
        ax.set_xticks(np.arange(len(etiquetas)))
        ax.set_xticklabels(etiquetas, rotation=20)
        ax.set_title(f"Sensibilidad a la estimación inicial: {fn}")
        ax.set_xlabel("Estimación inicial")
        ax.set_ylabel("Iteraciones")
        ax.grid(axis="y", alpha=0.3)
    axes[0].legend(fontsize=8)
    fig.text(0.5, -0.07, "Barra rayada con X = no convergió a la raíz esperada (falló, divergió o se detuvo en otra raíz)",
             ha="center", fontsize=9)
    ASSETS.mkdir(parents=True, exist_ok=True)
    fig.savefig(ASSETS / "sensibilidad_x0.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Gráfico guardado en: {ASSETS / "sensibilidad_x0.png"}")


if __name__ == "__main__":
    DATA.mkdir(parents=True, exist_ok=True)
    tabla_orden()
    graficar_sensibilidad(tabla_sensibilidad())
