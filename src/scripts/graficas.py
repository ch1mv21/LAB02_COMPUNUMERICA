#Integrantes: Jose Herrera Manuel Soto
#Curso: Computacion Numerica
#Fecha: 18/10/2026


import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.ticker import MaxNLocator
from pathlib import Path

CARPETA = str(Path(__file__).resolve().parents[2] / "src" / "assets")
PISO = 1e-17  # el error 0 no se puede dibujar en escala log

# Diferenciamos cada uno de los metodos con caracteristicas distintas)
ESTILOS = {
    "Bisección":       dict(color="tab:blue",   marker="o", linestyle="-"),
    "Falsa posición":  dict(color="tab:orange", marker="s", linestyle="--"),
    "Punto fijo":      dict(color="tab:green",  marker="^", linestyle="-."),
    "Secante":         dict(color="tab:red",    marker="D", linestyle=":"),
    "Newton-Raphson":  dict(color="tab:purple", marker="v", linestyle="-"),
    "Newton mejorado": dict(color="tab:brown",  marker="*", linestyle="--"),
}


def _guardar(fig, nombre_archivo):
    os.makedirs(CARPETA, exist_ok=True)
    ruta = f"{CARPETA}/{nombre_archivo}"
    fig.savefig(ruta, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Gráfico guardado en: {ruta}")


def graficar_funcion(caso, raiz):
    """Gráfico 1: la función con su raíz marcada.
    - Raíz simple: se sombrea [a, b] y se marcan f(a) y f(b) (cambio de signo, Bolzano).
    - Raíz doble: se marca la raíz y se señala la tangencia con el eje x."""
    f = caso["f"]
    x = np.linspace(*caso["rango"], 500)
    y = f(x)

    fig, ax = plt.subplots(figsize=(7.5, 4.8))
    ax.plot(x, y, color="tab:blue", linewidth=2, label=r"$f(x)$")
    ax.axhline(0, color="black", linewidth=0.8)

    if caso.get("raiz_doble"):
        ax.plot(raiz, f(raiz), "ro", markersize=9, zorder=5, label=f"Raíz doble: x = {raiz:g}")
        ax.plot(caso["x0"], f(caso["x0"]), "s", color="gray", markersize=8,
                label=f"Estimación inicial $x_0$ = {caso["x0"]:g}")
        ax.annotate("Tangencia: la curva toca el eje x\nsin cruzarlo  ($f(r)=0$ y $f'(r)=0$)",
                    xy=(raiz, 0), xytext=(raiz, 0.35 * y.max()),
                    ha="center", arrowprops=dict(arrowstyle="->"))
    else:
        a, b = caso["intervalo"]
        ax.axvspan(a, b, color="gold", alpha=0.25, label=f"Intervalo [{a:g}, {b:g}]")
        ax.plot([a, b], [f(a), f(b)], "s", color="gray", markersize=8,
                label="$f(a)$ y $f(b)$ (signos opuestos)")
        ax.plot(raiz, 0, "ro", markersize=9, zorder=5, label=f"Raíz: x ≈ {raiz:.6f}")

    ax.set_title(caso["titulo"])
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.grid(alpha=0.3)
    ax.legend()
    _guardar(fig, f"funcion_{caso["nombre"]}.png")


def graficar_convergencia(caso, resultados, tol, raiz=None, error_real=False):
    """Gráfico 2: |error| vs iteración (escala log), un método por curva.
    error_real=False -> |x_n - x_(n-1)| (el error que guarda cada método en su historial)
    error_real=True  -> |x_n - raíz| (necesita la raíz de referencia)"""
    fig, ax = plt.subplots(figsize=(7.5, 4.8))
    sin_datos = []

    for nombre, res in resultados.items():
        historial = res["historial"]
        if not historial:
            sin_datos.append(f"{nombre}: {res["estado"]}")
            continue
        iteraciones = [d["iteracion"] for d in historial]
        if error_real:
            error = np.abs(np.array([d["raiz"] for d in historial]) - raiz)
        else:
            error = np.array([d["error"] for d in historial])
        etiqueta = nombre + (" (no alcanza tol)" if res["estado"] == "no converge" else "")
        ax.semilogy(iteraciones, np.maximum(error, PISO), label=etiqueta, markersize=6, **ESTILOS[nombre])

    ax.axhline(tol, color="gray", linestyle=":", linewidth=1.5, label=f"tol = {tol:g}")
    if sin_datos:
        ax.text(0.98, 0.50, "Sin iteraciones:\n" + "\n".join("• " + s for s in sin_datos),
                transform=ax.transAxes, fontsize=8, ha="right", va="center",
                bbox=dict(boxstyle="round", facecolor="white", alpha=0.85))

    ax.set_title(f"Convergencia: {caso["titulo"]}")
    ax.set_xlabel("Iteración")
    ax.set_ylabel("|error| = |xₙ − raíz|" if error_real else "|error| = |xₙ − xₙ₋₁|")
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.grid(alpha=0.3, which="both")
    ax.legend(fontsize=8)
    prefijo = "convergencia_real" if error_real else "convergencia"
    _guardar(fig, f"{prefijo}_{caso["nombre"]}.png")


def graficar_resumen_iteraciones(casos, resultados, max_iter):
    """Gráfico 3: barras agrupadas con las iteraciones de cada método en cada función.
    N/A = no aplica (sin cambio de signo) · FALLA = el método se detuvo con error · barra rayada = no alcanzó la tolerancia."""
    metodos = list(ESTILOS)
    x = np.arange(len(casos))
    ancho = 0.8 / len(metodos)

    fig, ax = plt.subplots(figsize=(13, 5.5))
    for j, metodo in enumerate(metodos):
        resultados_metodo = [resultados[c["nombre"]][metodo] for c in casos]
        alturas = [len(r["historial"]) for r in resultados_metodo]
        posiciones = x + (j - (len(metodos) - 1) / 2) * ancho
        barras = ax.bar(posiciones, alturas, ancho, label=metodo, color=ESTILOS[metodo]["color"],
                        edgecolor="black", linewidth=0.5)
        for barra, r, n in zip(barras, resultados_metodo, alturas):
            if r["estado"] == "no converge":
                barra.set_hatch("//")
            texto = {"no aplica": "N/A", "falla": "FALLA"}.get(r["estado"], str(n))
            ax.text(barra.get_x() + barra.get_width() / 2, n + 0.8, texto,
                    ha="center", va="bottom", fontsize=8 if r["estado"] in ("ok", "no converge") else 6.5,
                    rotation=90 if r["estado"] == "falla" else 0)

    ax.axhline(max_iter, color="gray", linestyle=":", linewidth=1.5)
    ax.set_xticks(x)
    ax.set_xticklabels([c["categoria"] for c in casos])
    ax.set_ylim(0, max_iter * 1.12)
    ax.set_title("Iteraciones por método y función")
    ax.set_xlabel("Función")
    ax.set_ylabel("Iteraciones")
    ax.grid(axis="y", alpha=0.3)

    handles, _ = ax.get_legend_handles_labels()
    handles += [Patch(facecolor="white", edgecolor="black", hatch="//", label="No alcanzó la tolerancia"),
                Patch(facecolor="none", edgecolor="gray", linestyle=":", label=f"Tope de iteraciones ({max_iter})")]
    ax.legend(handles=handles, ncol=4, loc="upper center", bbox_to_anchor=(0.5, -0.16), fontsize=9)
    _guardar(fig, "resumen_iteraciones.png")
