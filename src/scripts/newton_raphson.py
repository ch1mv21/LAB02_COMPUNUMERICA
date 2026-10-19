#Integrantes: Jose Herrera Manuel Soto
#Curso: Computacion Numerica
#Fecha: 18/10/2026


import numpy as np
from metodo_base import MetodoRaiz

class NewtonRaphson(MetodoRaiz):
    def ejecutar(self, df, x0):
        datos = []
        x_prev = x0

        for iteracion in range(1, self.max_iter + 1):
            f_val = self.f(x_prev)
            df_val = df(x_prev)

            if np.abs(df_val) < 1e-15:
                raise ValueError("La derivada es cercana a cero; Newton-Raphson no puede continuar.")

            # Fórmula de Newton-Raphson
            x_actual = x_prev - (f_val / df_val)
            error = np.abs(x_actual - x_prev)

            datos.append({"iteracion": iteracion, "raiz": x_actual, "error": error})

            # Verificación de criterio de parada
            if np.abs(self.f(x_actual)) < self.tol or error < self.tol:
                break

            x_prev = x_actual

        return x_actual, datos