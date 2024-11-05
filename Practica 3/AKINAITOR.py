import json
import os
import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk

# Archivo JSON para almacenar los datos del juego
DATABASE_FILE = "base_datos_akinator.json"

# Función para cargar los datos del juego
def cargar_base_datos():
    if os.path.exists(DATABASE_FILE):
        with open(DATABASE_FILE, 'r') as archivo:
            return json.load(archivo)
    else:
        # Pregunta precargada para iniciar el juego
        return {
            "preguntas": {
                "texto": "¿Es un personaje real?",
                "si": None,
                "no": None
            }
        }

# Función para guardar los datos del juego
def guardar_base_datos(base_datos):
    with open(DATABASE_FILE, 'w') as archivo:
        json.dump(base_datos, archivo, indent=4)

class AkinatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Akinator")
        self.base_datos = cargar_base_datos()
        
        # Configuración de la interfaz
        self.root.geometry("1000x700")
        self.background_image = Image.open("fondo.jpg")  # Imagen de fondo
        self.background_image = self.background_image.resize((1000, 700))
        self.background_photo = ImageTk.PhotoImage(self.background_image)
        self.background_label = tk.Label(self.root, image=self.background_photo)
        self.background_label.place(relwidth=1, relheight=1)
        
        self.introduccion_label = tk.Label(self.root, text="¡Bienvenido a Akinator de Coches! Comencemos", font=("Arial", 16), bg="white")
        self.introduccion_label.pack(pady=10)
        
        self.pregunta_label = tk.Label(self.root, text=self.base_datos["preguntas"]["texto"], font=("Arial", 14), bg="white")
        self.pregunta_label.pack(pady=20)
        
        self.boton_si = tk.Button(self.root, text="Sí", font=("Arial", 12), command=lambda: self.responder(True))
        self.boton_si.pack(side="left", padx=50, pady=20)
        
        self.boton_no = tk.Button(self.root, text="No", font=("Arial", 12), command=lambda: self.responder(False))
        self.boton_no.pack(side="right", padx=50, pady=20)
        
        self.nodo_actual = self.base_datos["preguntas"]
        self.camino = []
        self.respuesta_previa = None

    def responder(self, respuesta):
        if isinstance(self.nodo_actual, dict):
            self.camino.append((self.nodo_actual, respuesta))
            if respuesta:
                if self.nodo_actual["si"] is None:
                    self.no_pude_adivinar(True)
                    return
                self.nodo_actual = self.nodo_actual["si"]
            else:
                if self.nodo_actual["no"] is None:
                    self.no_pude_adivinar(False)
                    return
                self.nodo_actual = self.nodo_actual["no"]
        
        if isinstance(self.nodo_actual, dict):
            self.pregunta_label.config(text=self.nodo_actual["texto"])
        else:
            self.pregunta_label.config(text=f"Creo que estás pensando en {self.nodo_actual}. ¿Adiviné correctamente?")
            self.boton_si.config(command=self.acierto)
            self.boton_no.config(command=self.no_pude_adivinar)

    def acierto(self):
        messagebox.showinfo("Akinator", "¡Lo sabía!")
        self.reiniciar_juego()

    def no_pude_adivinar(self, respuesta_previa=None):
        if respuesta_previa is None:
            respuesta_previa = self.respuesta_previa
        else:
            self.respuesta_previa = respuesta_previa
        
        respuesta = messagebox.askyesno("Akinator", "No pude adivinar tu personaje. ¿Quieres enseñarme quién es?")
        if respuesta:
            personaje_nuevo = simpledialog.askstring("Nuevo Personaje", "¿En quién estabas pensando?")
            pregunta_nueva = simpledialog.askstring("Nueva Pregunta", f"Escribe una pregunta para diferenciar a {personaje_nuevo}:")
            respuesta_personaje_nuevo = messagebox.askyesno("Akinator", f"Para {personaje_nuevo}, ¿la respuesta a '{pregunta_nueva}' es sí?")

            # Crear el nuevo nodo de pregunta
            nuevo_nodo = {
                "texto": pregunta_nueva,
                "si": personaje_nuevo if respuesta_personaje_nuevo else None,
                "no": None if respuesta_personaje_nuevo else personaje_nuevo
            }

            nodo_actual, respuesta_previa = self.camino[-1]
            if respuesta_previa:
                if isinstance(nodo_actual["si"], dict):
                    nodo_actual["si"]["no"] = nuevo_nodo
                else:
                    nodo_actual["si"] = nuevo_nodo
            else:
                if isinstance(nodo_actual["no"], dict):
                    nodo_actual["no"]["no"] = nuevo_nodo
                else:
                    nodo_actual["no"] = nuevo_nodo

            guardar_base_datos(self.base_datos)
            messagebox.showinfo("Akinator", "¡Gracias! He aprendido algo nuevo.")
        self.reiniciar_juego()

    def reiniciar_juego(self):
        self.nodo_actual = self.base_datos["preguntas"]
        self.camino = []
        self.respuesta_previa = None
        self.pregunta_label.config(text=self.nodo_actual["texto"])
        self.boton_si.config(command=lambda: self.responder(True))
        self.boton_no.config(command=lambda: self.responder(False))

if __name__ == "__main__":
    root = tk.Tk()
    app = AkinatorApp(root)
    root.geometry("1000x700")
    root.mainloop()
