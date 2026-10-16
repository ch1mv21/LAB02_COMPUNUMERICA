import os
import csv
import numpy as np

class MetodoRaiz:
    def __init__(self, funcion, nombre_funcion, tol=1e-6, max_iter=100):
        self.f = funcion
        self.nombre_funcion = nombre_funcion
        self.tol = tol
        self.max_iter = max_iter

    def guardar_csv_convergencia(self, datos, nombre_metodo):
        os.makedirs('src/data', exist_ok=True)
        ruta = f'src/data/{nombre_metodo}_{self.nombre_funcion}_convergencia.csv'
        
        with open(ruta, mode='w', newline='') as archivo:
            writer = csv.DictWriter(archivo, fieldnames=['iteracion', 'raiz', 'error'])
            writer.writeheader()
            writer.writerows(datos)
        print(f"Datos guardados en: {ruta}")

    def ejecutar(self, *args, **kwargs):
        #Este método será sobrescrito por las clases hijas
        raise NotImplementedError("Debe implementarse en la clase hija")