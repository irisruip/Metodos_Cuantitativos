from gomory import ModeloPL, Simulador

def leer_vector_float(mensaje, n=None):
    while True:
        try:
            entrada = input(mensaje).strip()
            vector = list(map(float, entrada.split()))
            if n and len(vector) != n:
                print(f"⚠️ Debes ingresar exactamente {n} números.")
                continue
            return vector
        except ValueError:
            print("⚠️ Entrada inválida. Intenta nuevamente.")

def leer_matriz_float(filas, columnas):
    matriz = []
    print(f"\nIngresa los coeficientes de las {filas} restricciones (una fila a la vez):")
    for i in range(filas):
        while True:
            try:
                entrada = input(f"  Restricción {i+1}: ").strip()
                fila = list(map(float, entrada.split()))
                if len(fila) != columnas:
                    print(f"⚠️ Debes ingresar exactamente {columnas} coeficientes.")
                    continue
                matriz.append(fila)
                break
            except ValueError:
                print("⚠️ Entrada inválida. Intenta nuevamente.")
    return matriz

def mostrar_modelo(c, A, b):
    print("\n=== Modelo Ingresado ===")
    print("Max Z =", " + ".join([f"{abs(ci)}x{i+1}" if ci >= 0 else f"- {abs(ci)}x{i+1}" 
                             for i, ci in enumerate([-ci for ci in c])]))
    print("Sujeto a:")
    for i, (fila, bi) in enumerate(zip(A, b)):
        restr = " + ".join([f"{coef}x{j+1}" for j, coef in enumerate(fila)])
        print(f"  {restr} <= {bi}")
    print("x ≥ 0 (todas las variables son no negativas)")

def main():
    print("\n=== Método de Planos de Corte (Gomory) ===")
    print("Resuelve un modelo de programación lineal entero usando planos de corte.")
    print("👉 Todos los datos se ingresan separados por espacios.\n")

    n = int(input("Número de variables: "))
    m = int(input("Número de restricciones: "))

    c = leer_vector_float("Coeficientes de la función objetivo (Max Z): ", n)
    A = leer_matriz_float(m, n)
    b = leer_vector_float("Términos independientes (lado derecho de las restricciones): ", m)

    mostrar_modelo(c, A, b)

    modelo = ModeloPL([-ci for ci in c], A, b)  # Convertimos a minimización
    simulador = Simulador(modelo)
    simulador.ejecutar()

if __name__ == "__main__":
    main()

