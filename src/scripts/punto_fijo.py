#Integrantes: Jose Herrera Manuel Soto
#Curso: Computacion Numerica
#Fecha: 18/10/2026

import numpy as np
from metodo_base import MetodoRaiz

class PuntoFijo(MetodoRaiz):
    def ejecutar(self, g, x0):
        datos = []
        x_prev = x0
        
        for iteracion in range(1, self.max_iter + 1):
            x_actual = g(x_prev)
            error = np.abs(x_actual - x_prev)

            datos.append({"iteracion": iteracion, "raiz": x_actual, "error": error})

            if np.abs(self.f(x_actual)) < self.tol or error < self.tol:
                break
                
            x_prev = x_actual

        return x_actual, datos