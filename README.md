# Aprendizaje Autónomo – Generador de Contraseñas

## Ambiente de Desarrollo
El proyecto está implementado en **Python** por su simplicidad y claridad al trabajar la lógica de programación.

**Herramientas necesarias:**
- **Editor:** Visual Studio Code o cualquier otro editor de texto.
- **Versión de Python:** 3.13
- **Librerías:**
  - `random` (incluida por defecto).
  - `pyperclip` para copiar contraseñas al portapapeles:
    ```bash
    pip install pyperclip
    ```

Python es ideal para este tipo de proyectos porque permite enfocarse en los fundamentos sin distraerse con sintaxis compleja.

---

## Manejo de Datos
### a) Variables y Tipos de Datos
- **longitud** (`int`): almacena el número de caracteres deseados para la contraseña.
- **usar_mayus**, **usar_minus**, **usar_numeros**, **usar_especiales** (`bool`): indican si se incluirán ciertos grupos de caracteres.
- **contraseña** (`str`): almacena la contraseña generada.

### b) Inicialización
Cada variable se inicializa con datos que proporciona el usuario:
```python
longitud = int(input("Ingresa la longitud: "))
usar_mayus = input("¿Incluir mayúsculas? (s/n): ") == 's'
```

---

## Operaciones Lógicas y Relacionales
### a) Operaciones lógicas (`and`, `or`, `not`)
Se usan para combinar condiciones:
```python
if not (usar_mayus or usar_minus or usar_numeros or usar_especiales):
    print("Error: Debes seleccionar al menos un tipo de carácter.")
```

### b) Operaciones relacionales (`==`, `!=`, `<`, `>`)
Se emplean para comparar valores y tomar decisiones:
```python
if longitud < 4:
    print("La longitud debe ser mayor o igual a 4")
```

---

## Estructuras Condicionales
Permiten tomar decisiones en función de las opciones del usuario:
```python
if usar_mayus:
    caracteres += string.ascii_uppercase
```
También se utilizan para detectar configuraciones inválidas:
```python
if not caracteres:
    return "Error: Debes seleccionar al menos un tipo de carácter."
```

---

## Estructuras Repetitivas
En este proyecto, la estructura repetitiva `while` se emplea para que el usuario pueda generar varias contraseñas sin reiniciar el programa.

**Funcionamiento:**
1. `while True` mantiene un ciclo infinito.
2. El usuario ingresa longitud y opciones.
3. Se genera y muestra la contraseña.
4. Si el usuario responde 's' a generar otra, el ciclo continúa; cualquier otra respuesta usa `break` para finalizar.

---

## Nota Final
Este sistema pone en práctica:
- Uso de variables y tipos de datos.
- Operaciones lógicas y comparaciones.
- Condicionales para control de flujo.
- Bucles para repetir procesos.

Estos elementos son la base lógica para desarrollar programas más complejos.
