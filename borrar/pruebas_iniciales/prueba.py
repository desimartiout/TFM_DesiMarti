texto = [
    '\n        """\n        Convocatoria de ayuda o  subvención: 795795\n        """\n        ',
    '\n        """\n        Convocatoria de ayuda o  subvención: 795795\n        """\n        '
]

# Sustituimos '\n' por saltos de línea reales y mostramos el contenido
for cadena in texto:
    print(cadena)
    procesado = cadena.replace('\\n', '\n')  # Sustituir '\n' literal por saltos de línea reales
    print(procesado)