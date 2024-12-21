# Cadena con secuencias Unicode
cadena = "Esto es un texto con ácentós: \n \u00e1, \u00e9, \u00f3, \u00fa."

# Decodificar las secuencias Unicode
cadena_decodificada = cadena.encode('utf-8')
print(cadena_decodificada)