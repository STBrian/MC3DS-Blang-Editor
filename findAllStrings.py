import re

def extract_ansi_strings(file_path, min_length=2):
    with open(file_path, "rb") as f:
        # Leer todo el contenido del archivo como bytes
        data = f.read()

    # Buscar cadenas imprimibles usando una expresión regular
    # Rango de caracteres ANSI: 32-126 (imprimibles)
    pattern = rb"[ -~]{" + str(min_length).encode() + rb",}"  # Secuencias ANSI de longitud >= min_length
    matches = re.findall(pattern, data)

    # Convertir las cadenas de bytes a texto (decodificar como ASCII)
    strings = [match.decode("ascii", errors="ignore") for match in matches]
    return strings

if __name__ == "__main__":
    # Ruta al archivo binario
    file_path = "code.bin"

    # Extraer cadenas ANSI
    strings = extract_ansi_strings(file_path)

    # Guardar los resultados en un archivo de texto
    with open("extracted_texts.txt", "w", encoding="utf-8") as output_file:
        for string in strings:
            output_file.write(string + "\n")

    print(f"Se han extraído {len(strings)} cadenas de texto. Revisa 'extracted_texts.txt'.")
