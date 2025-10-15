import tkinter as tk
from tkinter import scrolledtext
import os
import threading

# --- Tu clase Stack (idéntica a la que ya tienes) ---
class Stack:
    def __init__(self, name):
        self.name = name
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if self.items:
            return self.items.pop()
        else:
            return "La pila está vacía."

    def peek(self):
        if self.items:
            return self.items[-1]
        else:
            return "La pila está vacía."

    def __repr__(self):
        return f"{self.name}: {self.items}"


# --- Función principal de shell ---
class ShellMusical:
    def __init__(self, output_callback):
        self.pilas = {}
        self.archivos = {}
        self.output_callback = output_callback
        self.running = True

    def write(self, text):
        self.output_callback(text + "\n")

    def execute(self, line):
        comando = line.strip().split()
        if not comando:
            return

        cmd = comando[0].lower()

        if cmd == "tok":
            self.write("Cerrando la shell musical...")
            self.running = False
            return

        elif cmd == "do":
            if len(comando) < 2:
                self.write("Uso correcto: DO [nombre_pila]")
                return
            nombre = comando[1]
            if nombre in self.pilas:
                self.write(f"La pila '{nombre}' ya existe.")
            else:
                self.pilas[nombre] = Stack(nombre)
                self.write(f"Pila '{nombre}' creada correctamente.")

        elif cmd == "la":
            if len(comando) < 3:
                self.write("Uso correcto: LA [valor] [nombre_pila]")
                return
            valor, nombre = comando[1], comando[2]
            if nombre not in self.pilas:
                self.write(f"La pila '{nombre}' no existe.")
                return
            self.pilas[nombre].push(valor)
            self.write(f"Valor '{valor}' agregado a '{nombre}'.")

        elif cmd == "si":
            if len(comando) < 2:
                self.write("Uso correcto: SI [nombre_pila]")
                return
            nombre = comando[1]
            if nombre in self.pilas:
                self.write(str(self.pilas[nombre]))
            else:
                self.write(f"La pila '{nombre}' no existe.")

        elif cmd == "do_la":
            if not self.pilas:
                self.write("No has creado ninguna pila.")
            else:
                self.write("Pilas existentes:")
                for nombre, pila in self.pilas.items():
                    self.write(f"  - {nombre}: {pila.items}")

        elif cmd == "sum":
            if len(comando) < 2:
                self.write("Uso correcto: sum [nombre_pila]")
                return
            nombre = comando[1]
            if nombre not in self.pilas:
                self.write(f"La pila '{nombre}' no existe.")
                return
            pila_original = self.pilas[nombre]
            try:
                total = sum(float(x) for x in pila_original.items)
                nueva_pila_nombre = f"{nombre}_sum"
                nueva_pila = Stack(nueva_pila_nombre)
                nueva_pila.push(total)
                self.pilas[nueva_pila_nombre] = nueva_pila
                self.write(f"Suma total: {total}")
                self.write(f"Nueva pila '{nueva_pila_nombre}' creada con el valor de la suma.")
            except ValueError:
                self.write("No todos los elementos en la pila son numéricos.")

        elif cmd == "mkfile":
            if len(comando) < 3:
                self.write("Uso correcto: mkfile [nombre_archivo] [nombre_pila]")
                return
            nombre_archivo, nombre_pila = comando[1], comando[2]
            if nombre_pila not in self.pilas:
                self.write(f"La pila '{nombre_pila}' no existe.")
                return
            contenido = "\n".join(map(str, self.pilas[nombre_pila].items))
            ruta = f"{nombre_archivo}.txt"
            with open(ruta, "w", encoding="utf-8") as f:
                f.write(contenido)
            self.archivos[nombre_archivo] = ruta
            self.write(f"Archivo '{ruta}' creado con el contenido de '{nombre_pila}'.")

        elif cmd == "edit":
            if len(comando) < 2:
                self.write("Uso correcto: edit [nombre_archivo]")
                return
            nombre_archivo = comando[1]
            ruta = self.archivos.get(nombre_archivo, f"{nombre_archivo}.txt")
            if not os.path.exists(ruta):
                self.write("Ese archivo no existe.")
                return
            self.write(f"Editando '{ruta}' (se abrirá en tu editor por defecto).")
            os.system(f"notepad {ruta}" if os.name == "nt" else f"nano {ruta}")

        elif cmd == "ls":
            txt_files = [f for f in os.listdir() if f.endswith(".txt")]
            if not txt_files:
                self.write("No hay archivos .txt en el directorio actual.")
            else:
                self.write("Archivos existentes:")
                for f in txt_files:
                    self.write(f"  - {f}")

        elif cmd == "help":
            self.write("Comandos disponibles:")
            self.write("  DO [nombre_pila]           → crea una pila nueva")
            self.write("  LA [valor] [nombre_pila]   → agrega un valor a la pila")
            self.write("  SI [nombre_pila]           → muestra el contenido de la pila")
            self.write("  DO_LA                      → muestra todas las pilas existentes")
            self.write("  SUM [nombre_pila]          → crea una nueva pila con la suma")
            self.write("  MKFILE [archivo] [pila]    → crea un archivo con el contenido de una pila")
            self.write("  EDIT [archivo]             → abre un archivo para editarlo")
            self.write("  LS                         → lista los archivos .txt existentes")
            self.write("  TOK                        → salir")

        else:
            self.write("Comando no reconocido. Usa 'help' para ver los disponibles.")


# --- Interfaz Tkinter ---
class ShellWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Musical Virtual Machine (M.V.M)")
        self.root.geometry("700x400")

        self.text_area = scrolledtext.ScrolledText(self.root, bg="black", fg="white", insertbackground="white")
        self.text_area.pack(fill="both", expand=True)
        self.text_area.insert("end", "Musical Virtual Machine\nM.V.M\n>>> ")
        # evitar que el usuario borre el historial por error:
        self.text_area.config(state="normal")
        self.text_area.bind("<Return>", self.enter_pressed)

        self.shell = ShellMusical(self.write)
        self.input_buffer = ""

    def write(self, text):
        # escribe sin bloquear, siempre dejamos el widget en estado normal para insertar
        self.text_area.config(state="normal")
        self.text_area.insert("end", text)
        self.text_area.see("end")
        # dejar listo para editar
        self.text_area.config(state="normal")

    def enter_pressed(self, event):
        # obtener todas las líneas y tomar la última (lo que el usuario escribió)
        full_text = self.text_area.get("1.0", "end-1c")
        lines = full_text.splitlines()
        if not lines:
            return "break"

        last_line = lines[-1]

        # si el usuario tiene el prompt ">>> " al inicio, lo quitamos
        if last_line.startswith(">>> "):
            line = last_line[4:]
        else:
            line = last_line

        # insertar nueva línea visualmente (el usuario presionó Enter)
        self.text_area.insert("end", "\n")
        # ejecutar el comando en otro hilo para no bloquear la UI
        threading.Thread(target=self.run_command, args=(line,)).start()
        return "break"

    def run_command(self, command):
        self.shell.execute(command)
        # si el shell sigue activo, mostrar prompt de nuevo
        if self.shell.running:
            self.write(">>> ")
        else:
            # cerrar la ventana si el shell dejó de correr
            self.root.quit()

    def run(self):
        self.root.mainloop()



if __name__ == "__main__":
    ShellWindow().run()
