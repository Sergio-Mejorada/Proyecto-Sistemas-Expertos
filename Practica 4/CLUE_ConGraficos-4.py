import random
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# Definimos los personajes, locaciones y armas
personajes = [
    {"nombre": "Bob Esponja", "profesion": "Cocinero en el Crustáceo Cascarudo"},
    {"nombre": "Calamardo", "profesion": "Cajero del Crustáceo Cascarudo"},
    {"nombre": "Patricio", "profesion": "Amigo de Bob Esponja"},
    {"nombre": "Arenita", "profesion": "Científica y Karateka"},
    {"nombre": "Plankton", "profesion": "Dueño del Balde de Carnada"}
]

locaciones = ["Crustáceo Cascarudo", "Casa de Bob Esponja", "Laboratorio de Arenita", "Balde de Carnada", "Campo de Medusas"]
armas = ["Burbuja Explosiva", "Cuchillo de Cocina", "Red de Medusas", "Agua Tóxica", "Síndrome de Risa"]

# Historias para cada incidente
historias_casos = {
    "Bob Esponja": [
        "Calamardo estaba harto de las risas constantes de Bob y decidió ponerle fin.",
        "Plankton necesitaba deshacerse de Bob para robarle la fórmula secreta sin interrupciones.",
        "Arenita estaba cansada de los accidentes de Bob arruinando sus experimentos y decidió tomar medidas extremas.",
        "Patricio pensó que Bob le había escondido su helado favorito y se dejó llevar por la ira."
    ],
    "Calamardo": [
        "Bob Esponja intentaba alegrar a Calamardo con su música, pero él no podía soportarlo más.",
        "Patricio pensó que Calamardo había robado su colección de rocas especiales.",
        "Plankton quería que Calamardo se uniera a él en su plan para robar la fórmula secreta, pero él se negó.",
        "Arenita descubrió que Calamardo había saboteado su equipo de investigación, y decidió vengarse."
    ],
    "Patricio": [
        "Bob Esponja accidentalmente aplastó la roca favorita de Patricio, y Patricio no pudo contenerse.",
        "Calamardo estaba molesto porque Patricio invadió su jardín una vez más y decidió actuar.",
        "Arenita sospechaba que Patricio había estropeado su invento más reciente y quiso darle una lección.",
        "Plankton intentó engañar a Patricio para unirse a él, y cuando éste se negó, las cosas se pusieron feas."
    ],
    "Arenita": [
        "Bob Esponja interrumpió el experimento más importante de Arenita, y ella perdió la paciencia.",
        "Calamardo quería demostrar que podía ser más inteligente que Arenita y decidió sabotearla.",
        "Patricio pensó que Arenita le estaba ocultando algún secreto divertido y quiso descubrirlo por la fuerza.",
        "Plankton necesitaba eliminar a Arenita para asegurarse de que no arruinara su próximo plan malvado."
    ],
    "Plankton": [
        "Bob Esponja descubrió otro intento de Plankton por robar la fórmula secreta y quiso detenerlo de una vez por todas.",
        "Calamardo estaba cansado de los constantes ataques de Plankton al Crustáceo Cascarudo y decidió actuar.",
        "Arenita pensó que Plankton podía poner en peligro toda la ciudad con sus experimentos peligrosos.",
        "Patricio creyó que Plankton había robado su bocadillo y no quiso dejarlo escapar."
    ]
}

# Historias para confirmación o negación de paraderos, ajustadas para dar sentido lógico
def generar_historias_paraderos(sospechosos, culpable_nombre):
    paraderos = []
    for sospechoso in sospechosos:
        if sospechoso["nombre"] == culpable_nombre:
            paraderos.append(f"Nadie puede confirmar el paradero de {sospechoso['nombre']} durante el incidente.")
        else:
            locacion_pista = random.choice(locaciones)
            paraderos.append(f"{sospechoso['nombre']} afirma que estaba en {locacion_pista} durante el incidente.")
    return paraderos

# Función para iniciar una partida
def iniciar_partida():
    # Elegir al azar el caso en el que un personaje es víctima de un incidente
    victima = random.choice(personajes)
    sospechosos = [p for p in personajes if p != victima]
    culpable = random.choice(sospechosos)
    arma = random.choice(armas)
    locacion = random.choice(locaciones)

    # Guardar la solución
    solucion = {
        "culpable": culpable["nombre"],
        "arma": arma,
        "locacion": locacion,
        "victima": victima["nombre"]
    }
    
    historias = historias_casos[victima["nombre"]]
    paraderos = generar_historias_paraderos(sospechosos, culpable["nombre"])
    return solucion, sospechosos, historias, paraderos

# Clase principal de la interfaz gráfica
def main():
    solucion, sospechosos, historias, paraderos = iniciar_partida()

    # Crear la ventana principal
    root = tk.Tk()
    root.geometry("800x600")
    root.title("Misterio en Fondo de Bikini")

    # Cargar y establecer la imagen de fondo
    bg_image = Image.open("fondo_1.jpg")
    bg_image = bg_image.resize((800, 600), Image.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)

    background_label = tk.Label(root, image=bg_photo)
    background_label.place(relwidth=1, relheight=1)

    # Mostrar la víctima
    lbl_victima = tk.Label(root, text=f"La víctima es: {solucion['victima']}", bg="lightblue", font=("Arial", 14))
    lbl_victima.pack(pady=5, anchor='e', padx=50)

    # Definir intentos restantes
    intentos = [5]

    # Acciones para cada opción
    def mostrar_motivos():
        motivos_texto = "\n".join([f"{sospechoso['nombre']} ({sospechoso['profesion']}): {historias[i]}" for i, sospechoso in enumerate(sospechosos)])
        popup = tk.Toplevel(root)
        popup.title("Motivos de los Sospechosos")
        bg_popup_image = Image.open("FondoEme.jpg")
        bg_popup_image = bg_popup_image.resize((570, 370), Image.LANCZOS)
        popup.bg_popup_photo = ImageTk.PhotoImage(bg_popup_image)
        background_label_popup = tk.Label(popup, image=popup.bg_popup_photo)
        background_label_popup.place(relwidth=1, relheight=1)
        popup.geometry("570x370+300+500")
        text_label = tk.Label(popup, text=motivos_texto, wraplength=570, justify="left", bg='#ffffff', font=("Arial", 10, "bold"))
        text_label.place(relx=0.5, rely=0.5, anchor='center')

    def mostrar_paraderos():
        paraderos_texto = "\n".join(paraderos)
        popup = tk.Toplevel(root)
        popup.title("Paraderos de los Sospechosos")
        bg_popup_image = Image.open("FondoEme_2.jpg")
        bg_popup_image = bg_popup_image.resize((570, 370), Image.LANCZOS)
        popup.bg_popup_photo = ImageTk.PhotoImage(bg_popup_image)
        background_label_popup = tk.Label(popup, image=popup.bg_popup_photo)
        background_label_popup.place(relwidth=1, relheight=1)
        popup.geometry("570x370+600+300")
        text_label = tk.Label(popup, text=paraderos_texto, wraplength=570, justify="left", bg='#ffffff', font=("Arial", 10, "bold"))
        text_label.place(relx=0.5, rely=0.5, anchor='center')

    def hacer_acusacion():
        sospechoso = sospechoso_var.get()
        arma = arma_var.get()
        locacion = locacion_var.get()
        intentos[0] -= 1

        if sospechoso == solucion["culpable"] and arma == solucion["arma"] and locacion == solucion["locacion"]:
            messagebox.showinfo("¡Felicidades!", "¡Has resuelto el misterio correctamente!")
            root.destroy()
            main()
        elif intentos[0] == 0:
            messagebox.showinfo("Fin del Juego", f"Lo siento, se te han acabado los intentos. La solución era: Culpable: {solucion['culpable']}, Arma: {solucion['arma']}, Locación: {solucion['locacion']}")
            root.destroy()
            main()
        else:
            messagebox.showwarning("Incorrecto", f"La acusación es incorrecta. Te quedan {intentos[0]} intentos.")

    # Botones para preguntar
    btn_motivos = tk.Button(root, text="Preguntar Motivos", command=mostrar_motivos, bg="lightyellow")
    btn_motivos.pack(pady=3, anchor='e', padx=50)

    btn_paraderos = tk.Button(root, text="Preguntar Paraderos", command=mostrar_paraderos, bg="lightyellow")
    btn_paraderos.pack(pady=3, anchor='e', padx=50)

    # Campos para hacer la acusación
    sospechoso_var = tk.StringVar(root)
    sospechoso_var.set(sospechosos[0]["nombre"])
    tk.Label(root, text="Selecciona al culpable:", bg="lightblue").pack(anchor='e', padx=50)
    tk.OptionMenu(root, sospechoso_var, *[s["nombre"] for s in sospechosos]).pack(pady=3, anchor='e', padx=50)

    arma_var = tk.StringVar(root)
    arma_var.set(armas[0])
    tk.Label(root, text="Selecciona el arma:", bg="lightblue").pack(anchor='e', padx=50)
    tk.OptionMenu(root, arma_var, *armas).pack(pady=3, anchor='e', padx=50)

    locacion_var = tk.StringVar(root)
    locacion_var.set(locaciones[0])
    tk.Label(root, text="Selecciona la locación:", bg="lightblue").pack(anchor='e', padx=50)
    tk.OptionMenu(root, locacion_var, *locaciones).pack(pady=3, anchor='e', padx=50)

    # Botón para hacer la acusación
    btn_acusar = tk.Button(root, text="Hacer Acusación", command=hacer_acusacion, bg="lightcoral")
    btn_acusar.pack(pady=5, anchor='e', padx=50)

    # Iniciar el loop principal de la interfaz
    root.mainloop()

if __name__ == "__main__":
    main()
