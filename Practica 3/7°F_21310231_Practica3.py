import tkinter as tk
from tkinter import ttk, messagebox
import json
from PIL import Image, ImageTk
import os

class VentanaAgregarCoche:
    def __init__(self, master, juego):
        self.juego = juego
        self.top = tk.Toplevel(master)
        self.top.title("Agregar Nuevo Coche")
        
        # Campos para los datos del coche
        self.campo_marca = tk.Entry(self.top)
        self.campo_modelo = tk.Entry(self.top)
        self.campo_origen = tk.Entry(self.top)
        self.campo_combustible = tk.Entry(self.top)
        self.campo_carroceria = tk.Entry(self.top)
        self.campo_motor = tk.Entry(self.top)

        tk.Label(self.top, text="Marca:").pack()
        self.campo_marca.pack()
        tk.Label(self.top, text="Modelo:").pack()
        self.campo_modelo.pack()
        tk.Label(self.top, text="Origen:").pack()
        self.campo_origen.pack()
        tk.Label(self.top, text="Combustible:").pack()
        self.campo_combustible.pack()
        tk.Label(self.top, text="Carrocería:").pack()
        self.campo_carroceria.pack()
        tk.Label(self.top, text="Motor:").pack()
        self.campo_motor.pack()

        tk.Button(self.top, text="Agregar", command=self.agregar_coche).pack()

    def agregar_coche(self):
        nuevo_coche = {
            "marca": self.campo_marca.get(),
            "modelo": self.campo_modelo.get(),
            "origen": self.campo_origen.get(),
            "combustible": self.campo_combustible.get(),
            "carroceria": self.campo_carroceria.get(),
            "motor": self.campo_motor.get()
        }

        # Validar la entrada
        if all(nuevo_coche.values()):
            self.juego.coches.append(nuevo_coche)
            with open("coches.json", "w", encoding='utf-8') as file:
                json.dump(self.juego.coches, file, ensure_ascii=False, indent=4)

            messagebox.showinfo("Éxito", "Coche agregado exitosamente.")
            self.top.destroy()
        else:
            messagebox.showerror("Error", "Por favor, completa todos los campos.")

class AkinatorCoches:
    def __init__(self, master):
        self.master = master
        master.title("Akinator de Coches")
        self.coches = self.cargar_coches()
        self.posibles_opciones = []
        self.indice_pregunta = 0
        self.coche_adivinado = None

        # Imagen de fondo
        self.fondo_imagen = Image.open("fondo.jpg").resize((600, 400))
        self.fondo_photo = ImageTk.PhotoImage(self.fondo_imagen)
        self.fondo_label = tk.Label(master, image=self.fondo_photo)
        self.fondo_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Interfaz de juego
        self.introduccion = tk.Label(master, text="¡Bienvenido a Akinator de Coches!", bg="lightblue")
        self.introduccion.pack(pady=20)

        # Pregunta de selección de origen
        self.origen_label = tk.Label(master, text="Selecciona el origen del coche:", bg="lightblue")
        self.origen_label.pack()
        self.origen_seleccion = ttk.Combobox(master, values=["Japonés", "Alemán", "Americano"])
        self.origen_seleccion.pack()
        self.origen_seleccion.bind("<<ComboboxSelected>>", self.filtrar_por_origen)

        self.pregunta_label = tk.Label(master, text="", bg="lightblue")
        self.pregunta_label.pack()

        self.boton_si = tk.Button(master, text="Sí", command=lambda: self.responder("Sí"), state=tk.DISABLED)
        self.boton_si.pack(side=tk.LEFT, padx=20)
        self.boton_no = tk.Button(master, text="No", command=lambda: self.responder("No"), state=tk.DISABLED)
        self.boton_no.pack(side=tk.RIGHT, padx=20)

        # Preguntas basadas en atributos
        self.preguntas = [
            ("¿Es un SUV?", "carroceria", "SUV"),
            ("¿El motor es eléctrico?", "combustible", "Eléctrico"),
            ("¿Tiene motor Turbo?", "motor", "Turbo"),
        ]

        self.preguntas_restantes = self.preguntas.copy()  # Copia de las preguntas restantes

        # Botón para volver a empezar
        self.boton_volver = tk.Button(master, text="Volver a Empezar", command=self.volver_a_empezar)
        self.boton_volver.pack(pady=10)

    def cargar_coches(self):
        if os.path.exists("coches.json"):
            with open("coches.json", "r", encoding='utf-8') as file:
                return json.load(file)
        return []

    def filtrar_por_origen(self, event):
        origen = self.origen_seleccion.get()
        self.posibles_opciones = [coche for coche in self.coches if coche.get("origen") == origen]
        
        if self.posibles_opciones:
            self.indice_pregunta = 0
            self.boton_si.config(state=tk.NORMAL)
            self.boton_no.config(state=tk.NORMAL)
            self.origen_label.config(text="Origen seleccionado: " + origen)
            self.pregunta_label.config(text=self.preguntas[self.indice_pregunta][0])  # Mostrar la primera pregunta
        else:
            self.pregunta_label.config(text="No se encontraron coches con ese origen.")
            self.boton_si.config(state=tk.DISABLED)
            self.boton_no.config(state=tk.DISABLED)

    def responder(self, respuesta):
        if not self.posibles_opciones:
            return

        # Evitar que se salga del índice de preguntas
        if self.indice_pregunta >= len(self.preguntas):
            return

        pregunta, atributo, valor = self.preguntas[self.indice_pregunta]

        if respuesta == "Sí":
            self.posibles_opciones = [coche for coche in self.posibles_opciones if coche.get(atributo) == valor]
        else:
            self.posibles_opciones = [coche for coche in self.posibles_opciones if coche.get(atributo) != valor]

        # Descartar la pregunta actual de las preguntas restantes, solo si está presente
        if (pregunta, atributo, valor) in self.preguntas_restantes:
            self.preguntas_restantes.remove((pregunta, atributo, valor))

        self.indice_pregunta += 1

        # Buscar la siguiente pregunta que aún está disponible
        while self.indice_pregunta < len(self.preguntas) and self.preguntas[self.indice_pregunta] not in self.preguntas_restantes:
            self.indice_pregunta += 1

        if self.indice_pregunta < len(self.preguntas):
            self.pregunta_label.config(text=self.preguntas[self.indice_pregunta][0])
        else:
            # Fin de las preguntas, muestra opciones o pregunta si desea agregar un nuevo coche
            if len(self.posibles_opciones) == 1:
                self.coche_adivinado = self.posibles_opciones[0]
                self.pregunta_label.config(text=f"¿Tu coche es un {self.coche_adivinado['marca']} {self.coche_adivinado['modelo']}?")
                self.boton_si.config(command=self.finalizar_juego_si)
                self.boton_no.config(command=self.agregar_coche)
            else:
                self.pregunta_label.config(text="No pude adivinar tu coche. ¿Te gustaría agregarlo a la base de datos?")
                self.boton_si.config(command=self.agregar_coche)
                self.boton_no.config(command=self.fin_juego)

            self.boton_si.config(state=tk.NORMAL)
            self.boton_no.config(state=tk.NORMAL)

    def finalizar_juego_si(self):
        messagebox.showinfo("¡Adiviné!", f"¡Genial! Adiviné tu coche: {self.coche_adivinado['marca']} {self.coche_adivinado['modelo']}.")

    def agregar_coche(self):
        VentanaAgregarCoche(self.master, self)

    def fin_juego(self):
        messagebox.showinfo("Fin del Juego", "Gracias por jugar. ¡Hasta la próxima!")

    def volver_a_empezar(self):
        self.posibles_opciones = self.coches.copy()  # Reiniciar las posibles opciones
        self.indice_pregunta = 0
        self.coche_adivinado = None
        self.pregunta_label.config(text="")
        self.origen_seleccion.set("")
        self.boton_si.config(state=tk.DISABLED)
        self.boton_no.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    juego = AkinatorCoches(root)
    root.geometry("600x400")
    root.mainloop()
