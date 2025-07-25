from gomory import ModeloPL, Simulador  # Suponiendo que las clases están en gomory.py

def leer_vector_float(mensaje):
    return list(map(float, input(mensaje).split()))

def leer_matriz(mensaje, filas):
    matriz = []
    print(mensaje)
    for i in range(filas):
        fila = list(map(float, input(f"  Fila {i+1}: ").split()))
        matriz.append(fila)
    return matriz

def main():
    print("\n=== Método de Planos de Corte (Gomory) ===")
    print("Todos los datos deben ingresarse separados por espacios.\n")

    # Número de variables
    n = int(input("Número de variables: "))

    # Función objetivo (maximización → convertimos a minimización)
    c = leer_vector_float(f"Coeficientes de la función objetivo (max Z): ")
    c = [-ci for ci in c]  # Invertimos para minimizar

    # Restricciones
    m = int(input("Número de restricciones: "))
    A = leer_matriz("Coeficientes de las restricciones (Ax <= b):", m)
    b = leer_vector_float("Términos independientes b:")

    # Crear modelo y ejecutar simulador
    modelo = ModeloPL(c, A, b)
    simulador = Simulador(modelo)
    simulador.ejecutar()

if __name__ == "__main__":
    main()
