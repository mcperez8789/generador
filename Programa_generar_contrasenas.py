"""
Generador seguro de contraseñas
- Usa random.SystemRandom / secrets para selección segura.
- Garantiza al menos un carácter de cada categoría seleccionada.
- Calcula una estimación de entropía y clasifica la fuerza.
- Opciones: evitar caracteres ambiguos, copiar al portapapeles, guardar en archivo.
"""

import string
import secrets
import random  # sólo para shuffle usando SystemRandom
import math

# Intentará importar pyperclip (opcional). Si no está, se maneja sin copiar.
try:
    import pyperclip
    PYPERCLIP = True
except Exception:
    PYPERCLIP = False

# Conjunto de caracteres ambiguos que el usuario puede elegir evitar
AMBIGUOS = "Il1O0o"

def construir_pool(usar_mayus, usar_minus, usar_numeros, usar_especiales, evitar_ambiguos):
    """Construye la cadena de caracteres disponible según opciones"""
    pool = ""
    if usar_mayus:
        pool += string.ascii_uppercase
    if usar_minus:
        pool += string.ascii_lowercase
    if usar_numeros:
        pool += string.digits
    if usar_especiales:
        # Excluimos espacios, y dejamos los símbolos típicos
        pool += "!@#$%^&*()-_=+[]{};:,.<>?/\\|~`"
    if evitar_ambiguos:
        # eliminar caracteres ambiguos
        pool = ''.join(ch for ch in pool if ch not in AMBIGUOS)
    return pool

def estimar_entropia(longitud, tam_pool):
    """Estima la entropía (en bits) de la contraseña: longitud * log2(tamaño del pool)"""
    if tam_pool <= 1 or longitud <= 0:
        return 0.0
    return round(longitud * math.log2(tam_pool), 2)

def clasificar_entropia(entropia_bits):
    """Clasifica fuerza según entropía aproximada"""
    if entropia_bits < 28:
        return "Muy débil"
    elif entropia_bits < 36:
        return "Débil"
    elif entropia_bits < 60:
        return "Media"
    elif entropia_bits < 128:
        return "Fuerte"
    else:
        return "Muy fuerte"

def generar_contraseña(segura_random, longitud, usar_mayus, usar_minus, usar_numeros, usar_especiales, evitar_ambiguos):
    """
    Genera la contraseña asegurando que al menos haya un carácter de
    cada categoría seleccionada (si la longitud lo permite).
    - segura_random: objeto con choice() (por ejemplo secrets.SystemRandom o secrets module)
    """

    # Construimos pools por categoría para garantizar inclusión al final
    pool_total = construir_pool(usar_mayus, usar_minus, usar_numeros, usar_especiales, evitar_ambiguos)
    if not pool_total:
        return None, "Error: Debes seleccionar al menos un tipo de carácter."

    pools = []
    if usar_mayus:
        pools.append(''.join(ch for ch in string.ascii_uppercase if (not evitar_ambiguos or ch not in AMBIGUOS)))
    if usar_minus:
        pools.append(''.join(ch for ch in string.ascii_lowercase if (not evitar_ambiguos or ch not in AMBIGUOS)))
    if usar_numeros:
        pools.append(''.join(ch for ch in string.digits if (not evitar_ambiguos or ch not in AMBIGUOS)))
    if usar_especiales:
        especiales = "!@#$%^&*()-_=+[]{};:,.<>?/\\|~`"
        pools.append(''.join(ch for ch in especiales if (not evitar_ambiguos or ch not in AMBIGUOS)))

    # Validación: la longitud debe ser >= número de categorías seleccionadas
    categorias_seleccionadas = len(pools)
    if longitud < categorias_seleccionadas:
        msg = f"Error: La longitud ({longitud}) es menor que la cantidad de categorías seleccionadas ({categorias_seleccionadas})."
        return None, msg

    # Paso 1: asegurar al menos un carácter por categoría
    password_chars = []
    for cat_pool in pools:
        # si por alguna razón la categoría quedó vacía (por evitar ambigüos), saltarla con cuidado
        if not cat_pool:
            continue
        password_chars.append(secrets.choice(cat_pool))

    # Paso 2: completar la contraseña con caracteres aleatorios del pool total
    faltan = longitud - len(password_chars)
    for _ in range(faltan):
        password_chars.append(secrets.choice(pool_total))

    # Paso 3: mezclar los caracteres para que la posición de los obligatorios no sea predecible
    # Usamos random.SystemRandom().shuffle para mantener calidad de aleatoriedad criptográfica en el shuffle.
    rnd = random.SystemRandom()
    rnd.shuffle(password_chars)

    contraseña = ''.join(password_chars)
    entropia = estimar_entropia(longitud, len(pool_total))

    return contraseña, entropia

def menu():
    print("=== Generador Seguro de Contraseñas (versión mejorada) ===")
    while True:
        # Entrada de longitud con manejo de errores (estructura repetitiva con try/except)
        try:
            longitud = int(input("Longitud deseada (ej. 12): ").strip())
            if longitud <= 0:
                print("Ingresa un número positivo.")
                continue
        except ValueError:
            print("⚠ Error: Debes ingresar un número entero.")
            continue

        # Opciones booleanas
        usar_mayus = input("Incluir mayúsculas? (s/n): ").strip().lower() == 's'
        usar_minus = input("Incluir minúsculas? (s/n): ").strip().lower() == 's'
        usar_numeros = input("Incluir números? (s/n): ").strip().lower() == 's'
        usar_especiales = input("Incluir símbolos especiales? (s/n): ").strip().lower() == 's'
        evitar_ambiguos = input("Evitar caracteres ambiguos (I l 1 O 0 o)? (s/n): ").strip().lower() == 's'

        # Generamos la contraseña
        contraseña, resultado = generar_contraseña(secrets, longitud, usar_mayus, usar_minus, usar_numeros, usar_especiales, evitar_ambiguos)

        if contraseña is None:
            # resultado contiene el mensaje de error
            print(resultado)
            # preguntar si desea volver a intentar
            repetir = input("¿Deseas intentar con otras opciones? (s/n): ").strip().lower()
            if repetir != 's':
                print("Hasta luego.")
                break
            else:
                continue

        # Si la función devolvió entropía (resultado)
        entropia = resultado if isinstance(resultado, float) else None
        if entropia is None:
            # En nuestro diseño normalmente devolvemos entropía; si no, recomputamos
            pool_total = construir_pool(usar_mayus, usar_minus, usar_numeros, usar_especiales, evitar_ambiguos)
            entropia = estimar_entropia(longitud, len(pool_total))

        fuerza = clasificar_entropia(entropia)

        print("\nContraseña generada:", contraseña)
        print(f"Estimación de entropía: {entropia} bits -> {fuerza}")

        # Opción copiar al portapapeles
        if PYPERCLIP:
            copiar = input("¿Copiar al portapapeles? (s/n): ").strip().lower() == 's'
            if copiar:
                try:
                    pyperclip.copy(contraseña)
                    print("¡Contraseña copiada al portapapeles!")
                except Exception as e:
                    print("No se pudo copiar al portapapeles:", e)
        else:
            print("(pyperclip no está instalado — para habilitar copia: pip install pyperclip)")

        # Guardar en archivo opcional
        guardar = input("¿Guardar la contraseña en un archivo de texto? (s/n): ").strip().lower() == 's'
        if guardar:
            nombre_archivo = input("Nombre del archivo (ej. contraseñas.txt): ").strip()
            try:
                with open(nombre_archivo, 'a', encoding='utf-8') as f:
                    f.write(f"{contraseña}\n")
                print("Guardado en", nombre_archivo)
            except Exception as e:
                print("Error al guardar archivo:", e)

        # Preguntar si desea generar otra
        otra = input("\n¿Generar otra contraseña? (s/n): ").strip().lower()
        if otra != 's':
            print("¡Gracias por usar el generador! 👋")
            break

if __name__ == "__main__":
    menu()
