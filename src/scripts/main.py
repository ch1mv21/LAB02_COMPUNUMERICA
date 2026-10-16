import numpy as np
from biseccion import Biseccion
# from falsa_posicion import FalsaPosicion
# from punto_fijo import PuntoFijo

if __name__ == '__main__':
    #Definir la función y sus propiedades
    def f_poli(x): 
        return x**3 - x - 2

    print("--- Iniciando búsqueda de raíces ---")

    #Instanciar los métodos
    metodo_bis = Biseccion(funcion=f_poli, nombre_funcion='polinomica_simple')
    
    #Ejecutar y guardar
    try:
        raiz_bis, historial_bis = metodo_bis.ejecutar(1.0, 2.0)
        print(f"Bisección finalizada. Raíz: {raiz_bis}")
        metodo_bis.guardar_csv_convergencia(historial_bis, "biseccion")
    except ValueError as e:
        print(f"Error en bisección: {e}")