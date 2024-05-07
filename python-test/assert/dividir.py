def dividir(a, b):
    assert b != 0, "El divisor no puede ser cero"
    return a / b

resultado = dividir(10, 2)
print("El resultado de la división es:", resultado)

resultado = dividir(10, 0)  # Esto generará un AssertionError
