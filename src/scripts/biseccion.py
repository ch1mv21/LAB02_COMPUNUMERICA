#Integrantes: Jose Herrera Manuel Soto
#Curso: Computacion Numerica
#Fecha: 18/10/2026


import numpy as np
from metodo_base import MetodoRaiz

class Biseccion(MetodoRaiz):
    def ejecutar(self, a, b):
        if self.f(a) * self.f(b) >= 0:
            raise ValueError(f"Bisección no aplica: f(a)·f(b) = {self.f(a) * self.f(b):.4g} >= 0 (sin cambio de signo en [{a}, {b}]).")
        datos = []
        x_prev = a
        
        for iteracion in range(1, self.max_iter + 1):
            x_actual = a + (b - a) / 2.0
            error = np.abs(x_actual - x_prev)

            datos.append({"iteracion": iteracion, "raiz": x_actual, "error": error})
            if np.abs(self.f(x_actual)) < self.tol or error < self.tol:
                break

            if self.f(a) * self.f(x_actual) < 0:
                b = x_actual
            else:
                a = x_actual

            x_prev = x_actual 

        return x_actual, datos