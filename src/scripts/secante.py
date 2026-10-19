#Integrantes: Jose Herrera Manuel Soto
#Curso: Computacion Numerica
#Fecha: 18/10/2026

import numpy as np
from metodo_base import MetodoRaiz

class Secante(MetodoRaiz):
    def ejecutar(self, x0, x1):
        datos = []
        x_ant = x0
        x_prev = x1

        for iteracion in range(1, self.max_iter + 1):
            f_ant = self.f(x_ant)
            f_prev = self.f(x_prev)

            if np.abs(f_prev - f_ant) < 1e-15:
                raise ValueError("División por cero en Secante: f(x_n) y f(x_{n-1}) son demasiado cercanos.")

            # Fórmula de la secante
            x_actual = x_prev - f_prev * (x_prev - x_ant) / (f_prev - f_ant)
            error = np.abs(x_actual - x_prev)

            datos.append({"iteracion": iteracion, "raiz": x_actual, "error": error})

            # Verificación de criterio de parada
            if np.abs(self.f(x_actual)) < self.tol or error < self.tol:
                break

            x_ant = x_prev
            x_prev = x_actual

        return x_actual, datos