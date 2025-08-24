"""
Generador seguro de contraseñas — versión con uso explícito de
Estructuras de datos y funciones (Unidad 4)

Temas aplicados:
 - Tuplas: definición de categorías (constantes inmutables)
 - Listas: construcción y manipulación de caracteres y contraseñas
 - Diccionarios: opciones del usuario y resultados devueltos
 - Funciones: diseño modular con parámetros y valores de retorno
 - Ejecución de funciones: main() y flujo principal
 - Parámetros de función: uso de parámetros posicionales y por nombre

Notas:
 - Usa `secrets` para selección segura y `random.SystemRandom().shuffle` para mezclar.
 - pyperclip es opcional (copiar al portapapeles).
"""

import string
import secrets
import random
import math
from typing import List, Tuple, Dict, Any

# Intento de import opcional
try:
    import pyperclip
    PYPERCLIP = True
except Exception:
    PYPERCLIP = False

# Caracteres ambiguos (como tupla para mostrar uso)
AMBIGUOS: Tuple[str, ...] = tuple("Il1O0o")

# Definición de categorías como tupla de tuplas (nombre, etiqueta, conjunto)
# Usamos tuplas aquí porque la colección de categorías es una constante inmutable.
CATEGORIAS: Tuple[Tuple[str, str, str], ...] = (
    ("mayus", "Mayúsculas", string.ascii_uppercase),
    ("minus", "Minúsculas", string.ascii_lowercase),
    ("num", "Números", string.digits),
    ("esp", "Símbolos", "!@#$%^&*()-_=+[]{};:,.<>?/\\|~`"),
)


def construir_pool_total(opciones: Dict[str, bool], evitar_ambiguos: bool) -> str:
    """Construye la cadena total de caracteres disponible según `opciones`.

    - `opciones` es un diccionario que mapea claves (las de CATEGORIAS) a booleanos.
    - `evitar_ambiguos` indica si se deben quitar caracteres ambiguos.
    """
    partes: List[str] = []  # lista dinámica (estructura lista)
    for clave, etiqueta, chars in CATEGORIAS:
        if opciones.get(clave, False):
            if evitar_ambiguos:
                filtered = ''.join(ch for ch in chars if ch not in AMBIGUOS)
                partes.append(filtered)
            else:
                partes.append(chars)

    # Unir las partes en un string final
    pool_total = ''.join(partes)
    return pool_total


def construir_pools_por_categoria(opciones: Dict[str, bool], evitar_ambiguos: bool) -> List[str]:
    """Devuelve una lista con los pools por categoría seleccionada (empleada para garantizar inclusión)."""
    pools: List[str] = []
    for clave, etiqueta, chars in CATEGORIAS:
        if opciones.get(clave, False):
            if evitar_ambiguos:
                pool = ''.join(ch for ch in chars if ch not in AMBIGUOS)
            else:
                pool = chars
            pools.append(pool)
    return pools


def estimar_entropia(longitud: int, tam_pool: int) -> float:
    """Estima la entropía en bits: longitud * log2(tamaño pool)."""
    if tam_pool <= 1 or longitud <= 0:
        return 0.0
    return round(longitud * math.log2(tam_pool), 2)


def clasificar_entropia(entropia_bits: float) -> str:
    """Clasifica la fuerza a partir de la entropía (misma lógica que antes)."""
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


def generar_contrasena(longitud: int, opciones: Dict[str, bool], evitar_ambiguos: bool,
                        secure_random=secrets, mezclar: bool = True) -> Dict[str, Any]:
    """Genera una contraseña y devuelve un diccionario con resultado.

    Parámetros:
      - longitud: longitud deseada (int)
      - opciones: dict con claves 'mayus','minus','num','esp' -> bool
      - evitar_ambiguos: si True elimina caracteres ambiguos
      - secure_random: objeto con .choice (por defecto secrets)
      - mezclar: si True mezcla la lista antes de unirla

    Retorna:
      Dict con llaves: 'password' (str|None), 'entropy' (float), 'status' ('ok'|'error'), 'message'
    """

    # Pool total y pools por categoría (demostrando listas y luego uso de diccionario para resultado)
    pool_total = construir_pool_total(opciones, evitar_ambiguos)
    if not pool_total:
        return {"password": None, "entropy": 0.0, "status": "error", "message": "Selecciona al menos un tipo de carácter."}

    pools = construir_pools_por_categoria(opciones, evitar_ambiguos)

    # Validación: la longitud debe ser suficiente para incluir al menos 1 por categoría seleccionada
    categorias_seleccionadas = sum(1 for p in pools if p)
    if longitud < categorias_seleccionadas:
        return {"password": None, "entropy": 0.0, "status": "error",
                "message": f"La longitud ({longitud}) es menor que el número de categorías seleccionadas ({categorias_seleccionadas})."}

    caracteres: List[str] = []

    # Asegurar al menos un carácter por categoría
    for cat_pool in pools:
        if cat_pool:
            caracteres.append(secure_random.choice(cat_pool))

    # Completar con caracteres aleatorios del pool total
    faltan = longitud - len(caracteres)
    for _ in range(faltan):
        caracteres.append(secure_random.choice(pool_total))

    # Mezclar si se pide (usamos SystemRandom para shuffle seguro)
    if mezclar:
        rnd = random.SystemRandom()
        rnd.shuffle(caracteres)

    password = ''.join(caracteres)
    entropy = estimar_entropia(longitud, len(set(pool_total)))

    return {"password": password, "entropy": entropy, "status": "ok", "message": ""}


# --- Funciones utilitarias para interacción y tareas secundarias ---

def copiar_al_portapapeles(texto: str) -> bool:
    """Intenta copiar al portapapeles. Devuelve True si tuvo éxito."""
    if not PYPERCLIP:
        return False
    try:
        pyperclip.copy(texto)
        return True
    except Exception:
        return False


def guardar_en_archivo(nombre: str, texto: str) -> bool:
    """Guarda `texto` (append) en `nombre`. Retorna True si OK."""
    try:
        with open(nombre, 'a', encoding='utf-8') as f:
            f.write(texto + '\n')
        return True
    except Exception:
        return False


# --- Interfaz básica en consola (separamos lógica en funciones para evidenciar ejecución) ---

def solicitar_opciones_usuario() -> Tuple[int, Dict[str, bool], bool]:
    """Solicita entradas al usuario y retorna (longitud, opciones, evitar_ambiguos)."""
    while True:
        try:
            longitud = int(input("Longitud deseada (ej. 12): ").strip())
            if longitud <= 0:
                print("Ingresa un número mayor que 0.")
                continue
            break
        except ValueError:
            print("Por favor ingresa un entero válido.")

    # Creamos un diccionario con opciones (demostrando uso de diccionarios)
    opciones: Dict[str, bool] = {}
    opciones['mayus'] = input("Incluir mayúsculas? (s/n): ").strip().lower() == 's'
    opciones['minus'] = input("Incluir minúsculas? (s/n): ").strip().lower() == 's'
    opciones['num'] = input("Incluir números? (s/n): ").strip().lower() == 's'
    opciones['esp'] = input("Incluir símbolos especiales? (s/n): ").strip().lower() == 's'
    evitar_ambiguos = input("Evitar caracteres ambiguos (I l 1 O 0 o)? (s/n): ").strip().lower() == 's'

    return longitud, opciones, evitar_ambiguos


def main() -> None:
    print("=== Generador Seguro de Contraseñas — Unidad 4 (estructuras y funciones) ===")

    while True:
        longitud, opciones, evitar_ambiguos = solicitar_opciones_usuario()

        resultado = generar_contrasena(longitud=longitud, opciones=opciones, evitar_ambiguos=evitar_ambiguos)

        if resultado['status'] == 'error':
            print("Error:", resultado['message'])
            if input("¿Intentar con otras opciones? (s/n): ").strip().lower() != 's':
                break
            else:
                continue

        password = resultado['password']
        entropy = resultado['entropy']
        fuerza = clasificar_entropia(entropy)

        print(f"\nContraseña generada: {password}")
        print(f"Estimación de entropía: {entropy} bits -> {fuerza}")

        # Copiar al portapapeles (mostramos función separada)
        if PYPERCLIP:
            if input("¿Copiar al portapapeles? (s/n): ").strip().lower() == 's':
                ok = copiar_al_portapapeles(password)
                print("Copiado." if ok else "No se pudo copiar.")
        else:
            print("(pyperclip no instalado — para habilitar copia: pip install pyperclip)")

        # Guardar en archivo
        if input("¿Guardar la contraseña en un archivo? (s/n): ").strip().lower() == 's':
            nombre = input("Nombre del archivo (ej. contraseñas.txt): ").strip()
            ok = guardar_en_archivo(nombre, password)
            print("Guardado con éxito." if ok else "Error al guardar.")

        if input("\n¿Generar otra contraseña? (s/n): ").strip().lower() != 's':
            print("¡Gracias! 👋")
            break


if __name__ == '__main__':
    main()
