import numpy as np
from metodo_base import MetodoRaiz

class FalsaPosicion(MetodoRaiz):
    def ejecutar(self, a, b):
        if self.f(a) * self.f(b) >= 0:
            raise ValueError("El intervalo no presenta cambio de signo.")

        datos = []
        x_prev = a
        for iteracion in range(1, self.max_iter + 1):
            # Fórmula de falsa posición
            x_actual = b - (self.f(b) * (a - b)) / (self.f(a) - self.f(b))
            error = np.abs(x_actual - x_prev)

            datos.append({'iteracion': iteracion, 'raiz': x_actual, 'error': error})

            if np.abs(self.f(x_actual)) < self.tol or error < self.tol:
                break

            if self.f(a) * self.f(x_actual) < 0:
                b = x_actual
            else:
                a = x_actual
            
            x_prev = x_actual

        return x_actual, datos