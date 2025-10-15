# 🎵 Musical Virtual Machine (M.V.M) 🎵

Una **shell musical interactiva** con interfaz gráfica en **Tkinter**, que implementa operaciones con pilas y utilidades de archivos de texto.  
Los comandos simulan un pequeño *lenguaje musical* (por ejemplo, `DO`, `LA`, `SI`) para crear, manipular y visualizar pilas.

---

## Resumen

El proyecto **Musical Virtual Machine (M.V.M)** permite:
- Crear y gestionar pilas mediante comandos musicales.
- Guardar y editar archivos de texto con los datos de las pilas.
- Utilizar una interfaz tipo consola con diseño retro (texto verde sobre fondo negro).

---

## Arquitectura

El sistema está compuesto por tres clases principales:

### 1. `Stack`
Estructura de datos tipo **LIFO** (Last In, First Out).
- `push(item)`: Inserta un elemento.
- `pop()`: Extrae el último elemento.
- `peek()`: Muestra el elemento superior sin eliminarlo.
- `__repr__`: Devuelve una representación textual como `"name: [items]"`.

### 2. `ShellMusical`
Intérprete de comandos que gestiona pilas y archivos.
- Atributos: `pilas`, `archivos`, `running`.
- `write(text)`: Envía salida a la interfaz.
- `execute(line)`: Analiza y ejecuta un comando.

### 3. `ShellWindow`
Interfaz gráfica desarrollada en **Tkinter**.
- `text_area`: Consola de texto (`ScrolledText`, fondo negro, texto verde).
- `enter_pressed(event)`: Captura la entrada del usuario.
- `run_command(command)`: Ejecuta el comando en un hilo separado.
- `run()`: Inicia el bucle principal de la aplicación.

---

## Entorno de ejecución

| Recurso | Descripción |
|----------|--------------|
| **Lenguaje** | Python 3.x |
| **GUI** | Tkinter |
| **Concurrencia** | Threading para no bloquear la interfaz |
| **Sistema de archivos** | Lectura/escritura de `.txt` en el directorio actual |

---

## Comandos disponibles

| Comando | Sintaxis | Descripción |
|----------|-----------|-------------|
| `DO` | `DO [nombre_pila]` | Crea una nueva pila. |
| `LA` | `LA [valor] [nombre_pila]` | Inserta un valor en la pila. |
| `SI` | `SI [nombre_pila]` | Muestra el contenido de una pila. |
| `DO_LA` | `DO_LA` | Lista todas las pilas existentes. |
| `SUM` | `SUM [nombre_pila]` | Suma los valores numéricos de la pila y crea una nueva con el total. |
| `MKFILE` | `MKFILE [archivo] [pila]` | Crea un `.txt` con el contenido de una pila. |
| `EDIT` | `EDIT [archivo]` | Abre un archivo en el editor por defecto. |
| `LS` | `LS` | Lista todos los `.txt` del directorio actual. |
| `TOK` | `TOK` | Cierra la shell musical. |

---

## Flujo de ejecución

1. Se inicia la ventana `ShellWindow` mostrando el prompt `>>>`.
2. El usuario escribe un comando y presiona **Enter**.
3. El comando se ejecuta en un hilo independiente para no bloquear la interfaz.
4. El intérprete actualiza las estructuras y muestra la salida.
5. Si el comando es `TOK`, la shell se cierra.

---

## Gestión de archivos

- `MKFILE`: crea un archivo `.txt` con los elementos de una pila (uno por línea).
- `EDIT`: abre el archivo en el editor por defecto (`Notepad` en Windows, `nano` en Unix).
- `LS`: lista los archivos `.txt` en el directorio actual.

---

## Manejo de errores

- Validación del número de argumentos.
- Mensajes claros si la pila no existe o está vacía.
- `SUM` valida que todos los elementos sean numéricos.
- `EDIT` verifica la existencia del archivo antes de abrirlo.

---

## Extensibilidad

Para agregar un nuevo comando:
1. Edita el método `execute()` de `ShellMusical`.
2. Agrega un bloque `elif` con el nuevo comando.
3. Usa `self.write()` para imprimir la salida.


---

