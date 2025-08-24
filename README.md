# Informe Final — Generador Seguro de Contraseñas

**Proyecto:** Generador Seguro de Contraseñas — Unidad 4

**Desarrolado por:** 
- Monica Chapaca Perez

**Objetivo del programa:** Desarrollar un generador de contraseñas seguro, modular y didáctico que implemente y demuestre conocimientos de la Unidad 4 (Estructuras de datos: tuplas, listas, diccionarios; y Funciones: parámetros, ejecución y retornos). El programa debe garantizar la inclusión de cada categoría de caracteres seleccionada, estimar la entropía y facilitar opciones de copia y guardado.

**Fecha:** 24 de agosto de 2025

---

## Tabla de contenidos
1. Introducción
2. Alcance y objetivos específicos
3. Descripción del código y principales funcionalidades
   - Arquitectura y flujo
   - Funcionalidades principales (detalladas)
4. Mapeo con la Unidad 4 (conceptos aplicados)
   - Tuplas
   - Listas
   - Diccionarios
   - Funciones, parámetros y ejecución
5. Casos de uso y ejemplos prácticos
   - Ejemplos de ejecución y salidas
   - Cálculo de entropía: ejemplos numéricos
6. Plan de pruebas
   - Casos de prueba unitarios
   - Test de producción (batch)
7. Limitaciones del proyecto
8. Análisis de seguridad y buenas prácticas
9. Conclusiones
10. Recomendaciones y trabajo futuro
11. Anexos
    - Firmas de funciones y pseudocódigo
    - Fragmentos de código relevantes

---

## 1. Introducción

Este informe documenta de forma exhaustiva el desarrollo del *Generador Seguro de Contraseñas*, una herramienta implementada en Python que tiene como objetivo proporcionar contraseñas aleatorias de alta calidad criptográfica y, a la vez, servir como ejercicio pedagógico para aplicar las temáticas de la Unidad 4. Se enfatizan las estructuras de datos y las buenas prácticas en el diseño de funciones, separando responsabilidades y devolviendo resultados en estructuras claras (diccionarios), lo que facilita el testeo y la integración.


## 2. Alcance y objetivos específicos

**Alcance**: El proyecto implementa un generador de contraseñas por consola con las siguientes capacidades:
- Selección de tipos de caracteres (mayúsculas, minúsculas, números y símbolos).
- Opción para evitar caracteres ambiguos (I, l, 1, O, 0, o).
- Garantía de inclusión de al menos un carácter por categoría seleccionada (si la longitud lo permite).
- Estimación de entropía y clasificación de la fuerza de la contraseña.
- Opciones de copiar al portapapeles y guardar en un archivo de texto.

**Objetivos específicos**:
- Implementar y documentar el uso de tuplas, listas y diccionarios.
- Estructurar la lógica en funciones con parámetros y retornos claros.
- Usar `secrets` y `random.SystemRandom` para asegurar calidad criptográfica.
- Proveer documentación, pruebas y análisis de seguridad.


## 3. Descripción del código y principales funcionalidades

### 3.1 Arquitectura y flujo general

El programa se organiza en módulos lógicos (funciones) que se invocan desde una función principal `main()`:
1. **Interacción**: `solicitar_opciones_usuario()` — recopila longitud y opciones del usuario.
2. **Generación**: `generar_contrasena(longitud, opciones, evitar_ambiguos, ...)` — núcleo del generador.
3. **Salida**: Mostrar contraseña y entropía; opciones para copiar y guardar.

La función `generar_contrasena` a su vez hace uso de:
- `construir_pool_total(opciones, evitar_ambiguos)` — crea el pool global.
- `construir_pools_por_categoria(opciones, evitar_ambiguos)` — pools por categoría para asegurar inclusión.
- `estimar_entropia(longitud, tam_pool)` — calcula la entropía teórica.
- `clasificar_entropia(entropia)` — clasifica la fuerza en rangos predefinidos.


### 3.2 Funcionalidades principales (detalladas)

A continuación se describen las funcionalidades clave, la lógica implementada y su propósito:

#### 3.2.1 Construcción del pool de caracteres
- **Función:** `construir_pool_total(opciones, evitar_ambiguos)`
- **Entrada:** diccionario `opciones` con claves `mayus`, `minus`, `num`, `esp`; booleano `evitar_ambiguos`.
- **Salida:** cadena con todos los caracteres disponibles.
- **Descripción:** Recorre la tupla de `CATEGORIAS` y, cuando la opción está activada, agrega los caracteres al pool. Si `evitar_ambiguos` está activo, filtra los caracteres contenidos en `AMBIGUOS`.
- **Utilidad:** Permite centralizar la selección de caracteres y facilita el cálculo de entropía.


#### 3.2.2 Pools por categoría
- **Función:** `construir_pools_por_categoria(opciones, evitar_ambiguos)`
- **Salida:** lista con las subcadenas por categoría seleccionada.
- **Descripción:** Esta lista es crucial para garantizar que la contraseña incluya al menos un carácter de cada categoría seleccionada (ejecución de la política).


#### 3.2.3 Generación de contraseña garantizando inclusión
- **Función:** `generar_contrasena(longitud, opciones, evitar_ambiguos, secure_random=secrets, mezclar=True)`
- **Salida:** diccionario con llaves `password`, `entropy`, `status`, `message`.
- **Flujo interno:**
  1. Comprueba que el `pool_total` no esté vacío (al menos una categoría seleccionada).
  2. Con `construir_pools_por_categoria` obtiene los pools y cuenta las categorías seleccionadas.
  3. Valida que la `longitud` sea mayor o igual al número de categorías seleccionadas; si no, devuelve error.
  4. Selecciona, de forma segura (objeto `secure_random`), un carácter por cada pool para garantizar inclusión.
  5. Rellena hasta `longitud` con selecciones aleatorias del `pool_total`.
  6. Mezcla la lista de caracteres con `random.SystemRandom().shuffle` para evitar que los caracteres obligatorios queden en posiciones previsibles.
  7. Junta y devuelve la contraseña, junto con la entropía calculada.

**Ventajas:** este enfoque evita contraseñas que, por ejemplo, no contengan símbolos aunque el usuario lo haya pedido, y evita posiciones predecibles.


#### 3.2.4 Estimación y clasificación de entropía
- **Función:** `estimar_entropia(longitud, tam_pool)`
- **Fórmula:** `entropía ≈ longitud * log2(tam_pool)`
- **Función:** `clasificar_entropia(entropia_bits)` — mapea el número de bits a categorías humanas (Muy débil, Débil, Media, Fuerte, Muy fuerte).

**Comentarios:** La entropía es **teórica** y asume selección uniforme e independiente. Se explica en la sección de limitaciones por qué puede diferir de la entropía real.


#### 3.2.5 Interacción: copiar y guardar
- **Copiar:** si está disponible la librería `pyperclip`, el usuario puede copiar la contraseña al portapapeles. Existe la función utilitaria `copiar_al_portapapeles(texto)` que encapsula esta acción.
- **Guardar:** `guardar_en_archivo(nombre, texto)` añade la contraseña en texto plano al archivo indicado.

**Advertencia:** guardar en texto plano es inseguro; se detallan recomendaciones de seguridad en la sección 8.


## 4. Mapeo con la Unidad 4 (conceptos aplicados)

En esta sección se muestra explícitamente cómo el proyecto cubre los temas de la Unidad 4.

### 4.1 Tuplas
- **Uso:** `CATEGORIAS` se define como una tupla de tuplas: `(<clave>, <etiqueta>, <caracteres>)`.
- **Justificación:** las tuplas representan estructuras inmutables y son apropiadas para datos constantes de configuración. Evitan la reasignación accidental durante la ejecución.

### 4.2 Listas
- **Uso:** creación dinámica de `partes` (componentes del pool), `pools` (por categoría) y `caracteres` (lista de caracteres que luego se mezclarán y unirán).
- **Justificación:** la naturaleza mutable de las listas facilita operaciones como append, extend y shuffle que son necesarias para la construcción incremental de la contraseña.

### 4.3 Diccionarios
- **Uso:** `opciones` para representar la configuración del usuario y el `resultado` (retorno de `generar_contrasena`) que contiene múltiples valores con claves semánticas.
- **Justificación:** los diccionarios proporcionan un acceso semántico y ordenado a múltiples atributos, lo que mejora la claridad del código y facilita su integración.

### 4.4 Funciones y parámetros
- **Uso:** diseño modular con funciones pequeñas y cohesionadas. Ejemplos: `construir_pool_total`, `construir_pools_por_categoria`, `estimar_entropia`, `generar_contrasena`, `copiar_al_portapapeles`, `guardar_en_archivo`.
- **Parámetros:** uso de parámetros por nombre (`longitud=...`) y parámetros con valores por defecto (`secure_random=secrets`, `mezclar=True`).
- **Retorno múltiple:** en lugar de valores globales, `generar_contrasena` retorna un diccionario, una práctica que mejora el control de errores y la testabilidad.


## 5. Casos de uso y ejemplos prácticos

A continuación se muestran ejemplos de ejecución y resultados esperados que se pueden incluir en el `README.md` del repositorio.

### 5.1 Ejemplo 1 — Generación con mayúsculas y minúsculas
**Entrada**:
- Longitud: 12
- Mayúsculas: S
- Minúsculas: S
- Números: N
- Símbolos: N
- Evitar ambiguos: N

**Salida ejemplo**:
```
Contraseña generada: qGmTrHeKzWpQ
Estimación de entropía: 67.85 bits -> Fuerte
```

### 5.2 Ejemplo 2 — Generación con todas las categorías y evitar ambiguos
**Entrada**:
- Longitud: 14
- Mayúsculas: S
- Minúsculas: S
- Números: S
- Símbolos: S
- Evitar ambiguos: S

**Salida ejemplo**:
```
Contraseña generada: t9@G7v#HpR2sM
Estimación de entropía: 82.54 bits -> Fuerte
```

> Nota: las contraseñas mostradas son ejemplos ilustrativos — la ejecución produce cadenas aleatorias cada vez.


### 5.3 Cálculo de entropía — ejemplos numéricos
Suponga pools: 26 (minúsculas), 52 (mayús+minús), 62 (+números), 94 (+símbolos).
- 8 caracteres con pool=26 → 8 * log2(26) ≈ 37.6 bits (Media)
- 12 caracteres con pool=62 → 12 * log2(62) ≈ 71.45 bits (Fuerte)

Estos cálculos ayudan a justificar recomendaciones de longitud mínima para distintas políticas.


## 6. Plan de pruebas

### 6.1 Casos de prueba unitarios (sugeridos para pytest)
- `test_construir_pool_total_sin_ambiguos()` — comprobar que `AMBIGUOS` se filtra.
- `test_construir_pools_por_categoria()` — verificar que devuelve pools correctos según `opciones`.
- `test_generar_contrasena_longitud_insuficiente()` — verificar que se devuelve `status='error'` si `longitud < categorias`.
- `test_generar_contrasena_inclusion()` — verificar que la contraseña generada contiene al menos un carácter de cada categoría seleccionada.
- `test_estimar_entropia_valores_limite()` — comprobar comportamiento ante entradas 0 o negativas.

### 6.2 Test de integración / producción
- **Batch**: generar 1000 contraseñas con una configuración dada y analizar la distribución de caracteres (frecuencia por categoría y por carácter).
- **Resistencia**: comprobar tiempos de generación y comportamiento de memoria bajo cargas altas.


## 7. Limitaciones del proyecto

1. **Entropía teórica vs. entropía real**: la fórmula usada asume selección uniforme — los patrones humanos o políticas específicas alteran la entropía real.
2. **Almacenamiento inseguro**: guardar en texto plano es peligroso si el archivo no se protege adecuadamente.
3. **Interfaz limitada**: la CLI es funcional pero no adecuada para usuarios no técnicos.
4. **No hay auditoría ni logging seguro**: no se registran eventos de forma segura para auditoría.
5. **Clipboard**: ocupar el portapapeles sin limpieza automática puede exponer contraseñas.
6. **No se validan políticas complejas** (p. ej. reglas corporativas de mínimo/máximo por categoría más detalladas).
7. **Cobertura limitada de caracteres unicode**: el soporte está basado en ASCII y símbolos comunes; alfabetos extendidos no se contemplan por defecto.


## 8. Análisis de seguridad y buenas prácticas

### 8.1 Puntos de seguridad implementados
- Uso de `secrets` para selección criptográficamente segura.
- Uso de `random.SystemRandom().shuffle` para mezcla segura.
- Garantía de inclusión de las categorías solicitadas por el usuario.

### 8.2 Riesgos y mitigaciones
- **Riesgo:** almacenar contraseñas en texto plano.  
  **Mitigación:** almacenar solo en formato cifrado (por ejemplo AES-GCM con clave derivada de una contraseña maestra) o exportar en formatos compatibles con gestores que cifran los datos.

- **Riesgo:** exposición en portapapeles.  
  **Mitigación:** limpiar portapapeles automáticamente después de N segundos; mostrar advertencia al usuario.

- **Riesgo:** contraseña mostrada en pantalla, disponible en historiales de terminal.  
  **Mitigación:** ofrecer opción para que la contraseña no se muestre y/o que se exporte directamente a un archivo cifrado.


## 9. Conclusiones

El proyecto satisface los objetivos pedagógicos y técnicos planteados: demuestra con claridad el uso de tuplas, listas y diccionarios, y aplica buenas prácticas en el diseño de funciones y en la generación criptográfica aleatoria de contraseñas. Si bien el sistema es robusto desde el punto de vista criptográfico en la generación, hay áreas importantes (almacenamiento, interfaz, auditoría) que deben reforzarse antes de considerar el uso en un entorno productivo.


## 10. Recomendaciones y trabajo futuro

**Prioritarias**:
- No guardar contraseñas en texto plano: implementar cifrado con biblioteca `cryptography`.
- Añadir limpieza del portapapeles y advertencias al usuario.
- Añadir `argparse` y modo batch para integración en pipelines.

**Mejoras de usabilidad**:
- Interfaz gráfica o web (Tkinter / Flask + React) para mejorar adopción por usuarios no técnicos.
- Integración con gestores de contraseñas y formatos de importación/exportación (CSV, JSON con cifrado).

**Mejoras de calidad**:
- Implementar pruebas unitarias y CI (GitHub Actions).
- Ejecutar análisis de aleatoriedad estadístico (test de monobit, runs, etc.) si se pretende certificar aleatoriedad.


## 11. Anexos

### 11.1 Firmas de funciones clave (resumen)
```py
def construir_pool_total(opciones: Dict[str, bool], evitar_ambiguos: bool) -> str: ...

def construir_pools_por_categoria(opciones: Dict[str, bool], evitar_ambiguos: bool) -> List[str]: ...

def estimar_entropia(longitud: int, tam_pool: int) -> float: ...

def generar_contrasena(longitud: int, opciones: Dict[str, bool], evitar_ambiguos: bool,
                        secure_random=secrets, mezclar: bool = True) -> Dict[str, Any]: ...

def copiar_al_portapapeles(texto: str) -> bool: ...

def guardar_en_archivo(nombre: str, texto: str) -> bool: ...
```


### 11.2 Fragmento ejemplar — generación garantizada
```py
# Selección obligatoria por categoría
caracteres = []
for cat_pool in pools:
    if cat_pool:
        caracteres.append(secure_random.choice(cat_pool))
# Completar
for _ in range(longitud - len(caracteres)):
    caracteres.append(secure_random.choice(pool_total))
# Mezclar
rnd = random.SystemRandom(); rnd.shuffle(caracteres)
password = ''.join(caracteres)
```


---
 

*Fin del informe.*

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
