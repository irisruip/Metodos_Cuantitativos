from fractions import Fraction
from scipy.optimize import linprog
import numpy as np

class ModeloPL:
    def __init__(self, c, A, b):
        self.c = c
        self.A = A
        self.b = b
        self.restricciones = []
        self.solution = None

    def resolver_relajado(self):
        res = linprog(c=self.c, A_ub=self.A, b_ub=self.b, method='highs')
        if res.success:
            self.solution = res
            return res
        else:
            raise Exception("No se pudo resolver el modelo lineal relajado")

    def agregar_plano_corte(self, fila_fracc):
        corte = [x - int(x) for x in fila_fracc[:-1]]
        rhs = fila_fracc[-1] - int(fila_fracc[-1])
        self.A.append(corte)
        self.b.append(rhs)

    def mostrar_solucion(self):
        print("Solución óptima fraccional:")
        for i, x in enumerate(self.solution.x):
            print(f"x{i+1} = {x:.4f}")
        print(f"Valor óptimo: {self.solution.fun:.4f}")

class PlanoCorte:
    @staticmethod
    def necesita_corte(x):
        return any(not np.isclose(xi, round(xi)) for xi in x)

    @staticmethod
    def obtener_fila_frac(solution, A, b):
        for i, val in enumerate(solution.x):
            if not np.isclose(val, round(val)):
                return A[i] + [b[i]]  # fila extendida con b
        return None

class Simulador:
    def __init__(self, modelo):
        self.modelo = modelo

    def ejecutar(self):
        iteracion = 0
        while True:
            iteracion += 1
            print(f"\n--- Iteración {iteracion} ---")
            resultado = self.modelo.resolver_relajado()
            self.modelo.mostrar_solucion()

            if not PlanoCorte.necesita_corte(resultado.x):
                print("Solución entera encontrada.")
                break

            fila_frac = PlanoCorte.obtener_fila_frac(resultado, self.modelo.A, self.modelo.b)
            if fila_frac is not None:
                self.modelo.agregar_plano_corte(fila_frac)
            else:
                print("No se pudo generar un nuevo corte.")
                break
