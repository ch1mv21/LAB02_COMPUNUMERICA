#Integrantes: Jose Herrera Manuel Soto
#Curso: Computacion Numerica
#Fecha: 18/10/2026

import os
import csv
import numpy as np
from pathlib import Path

CARPETA = str(Path(__file__).resolve().parents[2] / "src" / "data")


def guardar_csv_funcion(caso):
    """CSV por función con columnas (x, f(x)), en el mismo rango que se grafica."""
    os.makedirs(CARPETA, exist_ok=True)
    x = np.linspace(*caso["rango"], 400)
    ruta = f"{CARPETA}/{caso["nombre"]}_fx.csv"
    np.savetxt(ruta, np.column_stack((x, caso["f"](x))), delimiter=",", header="x,f(x)", comments="")
    print(f"  CSV de la función guardado en: {ruta}")


def guardar_csv_resumen(casos, resultados, raices):
    """CSV resumen de convergencia: una fila por (función, método).
    error_final = |x_n - x_(n-1)| · error_real = |x_n - raíz de referencia|."""
    os.makedirs(CARPETA, exist_ok=True)
    ruta = f"{CARPETA}/resumen_convergencia.csv"
    campos = ["funcion", "metodo", "estado", "iteraciones", "raiz", "error_final", "error_real", "f_raiz"]
    with open(ruta, mode="w", newline="") as archivo:
        writer = csv.DictWriter(archivo, fieldnames=campos)
        writer.writeheader()
        for caso in casos:
            nombre = caso["nombre"]
            for metodo, res in resultados[nombre].items():
                fila = {"funcion": nombre, "metodo": metodo, "estado": res["estado"],
                        "iteraciones": len(res["historial"]), "raiz": "", "error_final": "",
                        "error_real": "", "f_raiz": ""}
                if res["historial"]:
                    raiz = float(res["raiz"])
                    fila.update(raiz=raiz, error_final=float(res["historial"][-1]["error"]),
                                error_real=abs(raiz - raices[nombre]), f_raiz=float(caso["f"](raiz)))
                writer.writerow(fila)
    print(f"\nResumen de convergencia guardado en: {ruta}")
