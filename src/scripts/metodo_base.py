#Integrantes: Jose Herrera Manuel Soto
#Curso: Computacion Numerica
#Fecha: 18/10/2026import os
import os
import csv
from pathlib import Path

RAIZ_PROYECTO = Path(__file__).resolve().parents[2]

class MetodoRaiz:
    def __init__(self, funcion, nombre_funcion, tol=1e-6, max_iter=100):
        self.f = funcion
        self.nombre_funcion = nombre_funcion
        self.tol = tol
        self.max_iter = max_iter

    def guardar_csv_convergencia(self, datos, nombre_metodo):
        carpeta = RAIZ_PROYECTO / "src" / "data"
        os.makedirs(carpeta, exist_ok=True)
        ruta = carpeta / f"{nombre_metodo}_{self.nombre_funcion}_convergencia.csv"
        
        with open(ruta, mode="w", newline="") as archivo:
            writer = csv.DictWriter(archivo, fieldnames=["iteracion", "raiz", "error"])
            writer.writeheader()
            writer.writerows(datos)
        print(f"Datos guardados en: {ruta}")

    def ejecutar(self, *args, **kwargs):
        raise NotImplementedError("Debe implementarse en la clase hija")