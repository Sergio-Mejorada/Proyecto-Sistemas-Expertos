#Sergio Alejandro Mejorada Gonzalez
#21310231  7° F1
#Proyecto Sistema Experto 
# _*_ codificación: cp1252 _*_
# _*_ cdoing: 850 _*_
# _*_ codificación: utf-8 _*_
import os
import sqlite3
from tkinter import Tk, Label, Button, PhotoImage, StringVar, Entry, Radiobutton, IntVar, Toplevel, Listbox, Scrollbar, END

# Crear o conectar a la base de datos
conn = sqlite3.connect("clientes_fallas.db")
cursor = conn.cursor()

# Crear tabla si no existe
cursor.execute("""
CREATE TABLE IF NOT EXISTS historial (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id TEXT NOT NULL,
    tipo_cortina TEXT NOT NULL,
    falla TEXT NOT NULL,
    causa TEXT NOT NULL,
    solucion TEXT NOT NULL
)
""")
conn.commit()

# Sistema Experto para Diagnóstico de Cortinas Metálicas con Interfaz Gráfica

def diagnosticar_falla(tipo_cortina, falla_usuario):
    conocimiento = {
        "electrica": {
            "no abre": {"Causa": "Motor dañado o sin energía", "Solución": "Verificar el fusible del motor y/o la conexión eléctrica."},
            "no sube pero el motor si tiene energia": {"Causa": "Cortina atorada", "Solución": "Verificar que nada al rededor atasque la cortina."},
            "no baja pero el motor si tiene energia": {"Causa": "Obstruccion de guias laterales", "Solución": "Revisar que en las guias laterales no exista nada que obstruya el cierre."},
            "no cierra pero el motor si tiene energia": {"Causa": "Obstruccion de guias laterales", "Solución": "Revisar que en las guias laterales no exista nada que obstruya el cierre."},
            "no baja": {"Causa": "Motor sin energia o botonera dañada", "Solución": "Revisar la conexion del motor y/o verificar que la botonera no tenga un daño."},
            "no cierra": {"Causa": "Motor sin energia o botonera dañada", "Solución": "Revisar la conexion del motor y/o verificar que la botonera no tenga un daño."},
            "ruido al subir": {"Causa": "Falta de lubricación", "Solución": "Aplicar lubricante en guias laterales."},
            "ruido al abrir": {"Causa": "Falta de lubricación", "Solución": "Aplicar lubricante en guias laterales."},
            "ruido al subir la cortina": {"Causa": "Falta de lubricación", "Solución": "Aplicar lubricante en guias laterales."},
            "ruido al abrir la cortina": {"Causa": "Falta de lubricación", "Solución": "Aplicar lubricante en guias laterales."},
            "motor ruidoso al subir": {"Causa": "Falta de lubricación en transmision del motor", "Solución": "Aplicar grasa para cadenas en la transmision del motor."},
            "motor ruidoso al abrir": {"Causa": "Falta de lubricación en transmision del motor", "Solución": "Aplicar grasa para cadenas en la transmision del motor."},
            "motor ruidoso al cerrar": {"Causa": "Falta de lubricación en transmision del motor", "Solución": "Aplicar grasa para cadenas en la transmision del motor."},
            "motor ruidoso al subir la cortina": {"Causa": "Falta de lubricación en transmision del motor", "Solución": "Aplicar grasa para cadenas en la transmision del motor."},
            "motor ruidoso al abrir la cortina": {"Causa": "Falta de lubricación en transmision del motor", "Solución": "Aplicar grasa para cadenas en la transmision del motor."},
            "motor ruidoso al cerrar la cortina": {"Causa": "Falta de lubricación en transmision del motor", "Solución": "Aplicar grasa para cadenas en la transmision del motor."},
            "atorada": {"Causa": "Obstrucción en las guías o suciedad acumulada", "Solución": "Limpie las guías y retire cualquier obstrucción."},
            "la cortina brinca al bajar": {"Causa": "Suciedad acumulada en guias", "Solución": "Limpie las guías y engraselas."}
        },
        "cadena": {
            "no sube": {"Causa": "Mecanismo de cadena atorado", "Solución": "Verificar en que se atoro el mecanismo de la cadena."},
            "no abre": {"Causa": "Cadena rota o mal ajustada", "Solución": "Reparar o ajustar la cadena."},
            "no baja": {"Causa": "Causa" "Obstruccion de guias laterales", "Solución": "Revisar que en las guias laterales no exista nada que obstruya el cierre."},
            "ruido": {"Causa": "Falta de lubricación", "Solución": "Aplicar lubricante a las guias laterales."},
            "mecanismo ruidoso al abrir": {"Causa": "Falta de lubricación en transmision del motor", "Solución": "Aplicar grasa en los engranes del mecanismo de cadena."},
            "mecanismo ruidoso al cerrar": {"Causa": "Falta de lubricación en transmision del motor", "Solución": "Aplicar grasa en los engranes del mecanismo de cadena."},
            "atorada": {"Causa": "Obstrucción en las guías", "Solución": "Limpie las guías y retire cualquier obstrucción."}
        }
    }

    tipo = "electrica" if tipo_cortina == 1 else "cadena"
    for clave, diagnostico in conocimiento[tipo].items():
        if clave in falla_usuario.lower():
            return diagnostico

    return {"Causa": "No se encontró un diagnóstico", "Solución": "Por favor, consulte con un técnico especializado de MEXICORT."}

def procesar_entrada():
    cliente_id = cliente_id_var.get()
    if len(cliente_id) != 6 or not cliente_id.isdigit():
        causa.set("Por favor, ingrese un ID de cliente válido de 6 dígitos.")
        solucion.set("")
        return

    tipo_cortina = tipo_var.get()
    falla_usuario = entrada.get()
    diagnostico = diagnosticar_falla(tipo_cortina, falla_usuario)

    causa.set(f"Causa probable: {diagnostico['Causa']}")
    solucion.set(f"Solución sugerida: {diagnostico['Solución']}")

    # Guardar en la base de datos
    tipo_cortina_texto = "electrica" if tipo_cortina == 1 else "cadena"
    cursor.execute("""
    INSERT INTO historial (cliente_id, tipo_cortina, falla, causa, solucion)
    VALUES (?, ?, ?, ?, ?)
    """, (cliente_id, tipo_cortina_texto, falla_usuario, diagnostico['Causa'], diagnostico['Solución']))
    conn.commit()

def ver_historial():
    ventana_historial = Toplevel()
    ventana_historial.title("Historial de Fallas")
    ventana_historial.geometry("1400x400")

    listbox = Listbox(ventana_historial, font=("Arial", 12), width=125, height=20)
    listbox.pack(side="left", fill="y")

    scrollbar = Scrollbar(ventana_historial)
    scrollbar.pack(side="right", fill="y")

    listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox.yview)

    cursor.execute("SELECT * FROM historial")
    registros = cursor.fetchall()
    for registro in registros:
        listbox.insert(END, f"ID: {registro[0]} | Cliente: {registro[1]} | Tipo: {registro[2]} | Falla: {registro[3]} | Causa: {registro[4]} | Solución: {registro[5]}")

    def borrar_registro():
        seleccionado = listbox.curselection()
        if seleccionado:
            registro = listbox.get(seleccionado)
            registro_id = int(registro.split('|')[0].split(':')[1].strip())
            cursor.execute("DELETE FROM historial WHERE id = ?", (registro_id,))
            conn.commit()
            listbox.delete(seleccionado)

    def borrar_todo():
        cursor.execute("DELETE FROM historial")
        conn.commit()
        listbox.delete(0, END)

    boton_borrar = Button(ventana_historial, text="Borrar Registro", font=("Arial", 12), command=borrar_registro)
    boton_borrar.pack(pady=10)

    boton_borrar_todo = Button(ventana_historial, text="Borrar Todo", font=("Arial", 12), command=borrar_todo)
    boton_borrar_todo.pack(pady=10)

def reiniciar_pantalla():
    cliente_id_var.set("")
    entrada.delete(0, END)
    causa.set("")
    solucion.set("")

def crear_interfaz():
    # Crear ventana principal
    global ventana
    ventana = Tk()
    ventana.title("Sistema Experto: Cortinas Metálicas")
    ventana.geometry("800x600")

    # Imagen de fondo
    ruta_fondo = "fondo.png"  # Reemplazar con la ruta de la imagen de fondo
    if os.path.exists(ruta_fondo):
        fondo = PhotoImage(file=ruta_fondo)
        fondo_label = Label(ventana, image=fondo)
        fondo_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Título
    titulo = Label(ventana, text="Diagnóstico de Cortinas Metálicas MEXICORT", font=("Arial", 20), bg="silver")
    titulo.pack(pady=10)

    # ID de cliente
    global cliente_id_var
    cliente_id_var = StringVar()
    cliente_id_label = Label(ventana, text="Ingrese el ID del cliente (6 dígitos):", font=("Arial", 12), bg="silver")
    cliente_id_label.pack(pady=5)
    cliente_id_entry = Entry(ventana, font=("Arial", 12), textvariable=cliente_id_var, width=20)
    cliente_id_entry.pack(pady=5)

    # Selección de tipo de cortina
    global tipo_var
    tipo_var = IntVar(value=1)  # 1 para eléctrica, 2 para cadena
    tipo_label = Label(ventana, text="Seleccione el tipo de cortina:", font=("Arial", 12), bg="silver")
    tipo_label.pack(pady=5)
    electrica_rb = Radiobutton(ventana, text="Eléctrica", variable=tipo_var, value=1, font=("Arial", 12), bg="silver")
    electrica_rb.pack(pady=5)
    cadena_rb = Radiobutton(ventana, text="De cadena", variable=tipo_var, value=2, font=("Arial", 12), bg="silver")
    cadena_rb.pack(pady=5)

    # Pregunta al usuario
    pregunta = Label(ventana, text="¿Cuál es la falla de tu cortina metálica?", font=("Arial", 12), bg="silver")
    pregunta.pack(pady=10)

    # Entrada de texto
    global entrada
    entrada = Entry(ventana, font=("Arial", 12), width=50)
    entrada.pack(pady=5)

    # Botón para procesar
    boton_procesar = Button(ventana, text="Diagnosticar", font=("Arial", 12), command=procesar_entrada)
    boton_procesar.pack(pady=10)

    # Botón para ver historial
    boton_historial = Button(ventana, text="Ver Historial", font=("Arial", 12), command=ver_historial)
    boton_historial.pack(pady=10)

    # Etiquetas para mostrar diagnóstico
    global causa, solucion
    causa = StringVar()
    solucion = StringVar()
    causa_label = Label(ventana, textvariable=causa, font=("Arial", 12), bg="silver", wraplength=500, justify="left")
    solucion_label = Label(ventana, textvariable=solucion, font=("Arial", 12), bg="silver", wraplength=500, justify="left")
    causa_label.pack(pady=10)
    solucion_label.pack(pady=10)

    # Botón de reiniciar
    boton_reiniciar = Button(ventana, text="Reiniciar", font=("Arial", 12), command=reiniciar_pantalla)
    boton_reiniciar.pack(pady=10)
    


    # Botón de salida
    boton_salir = Button(ventana, text="Salir", font=("Arial", 12), command=ventana.quit)
    boton_salir.pack(pady=10)

    ventana.mainloop()

if __name__ == "__main__":
    crear_interfaz()
    conn.close()
