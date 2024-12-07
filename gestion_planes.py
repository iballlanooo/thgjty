import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import csv
import os

# Archivo CSV para almacenar los datos
ARCHIVO_DATOS = "planes.csv"

# Función para cargar datos y actualizar días restantes
def cargar_datos():
    if os.path.exists(ARCHIVO_DATOS):
        with open(ARCHIVO_DATOS, newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            for row in reader:
                # Calcular días restantes
                fecha_vencimiento = datetime.strptime(row[4], "%Y-%m-%d").date()
                dias_restantes = (fecha_vencimiento - datetime.now().date()).days
                # Insertar en la tabla, fechas ocultas internamente
                tree.insert("", "end", values=(row[0], row[1], row[3], dias_restantes, row[6]), tags=(row[2], row[4]))

# Función para guardar datos en el archivo CSV
def guardar_datos():
    with open(ARCHIVO_DATOS, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        for row in tree.get_children():
            values = tree.item(row)["values"]
            fecha_inicio = tree.item(row)["tags"][0]
            fecha_vencimiento = tree.item(row)["tags"][1]
            writer.writerow([values[0], values[1], fecha_inicio, values[2], fecha_vencimiento, values[3], values[4]])

# Función para agregar un nuevo plan
def agregar_plan():
    try:
        nombre = entry_nombre.get()
        telefono = entry_telefono.get()
        dias_plan = int(entry_dias_plan.get())
        nota = entry_nota.get("1.0", "end").strip()

        fecha_inicio = datetime.now().date()
        fecha_vencimiento = fecha_inicio + timedelta(days=dias_plan)
        dias_restantes = (fecha_vencimiento - datetime.now().date()).days

        # Insertar solo columnas visibles, fechas en tags (ocultas)
        tree.insert("", "end", values=(nombre, telefono, dias_plan, dias_restantes, nota), tags=(fecha_inicio, fecha_vencimiento))
        guardar_datos()
        limpiar_campos()
    except ValueError:
        messagebox.showerror("Error", "Por favor, ingresa los días como un número entero.")

# Función para limpiar campos
def limpiar_campos():
    entry_nombre.delete(0, "end")
    entry_telefono.delete(0, "end")
    entry_dias_plan.delete(0, "end")
    entry_nota.delete("1.0", "end")

# Función para eliminar un plan seleccionado
def eliminar_plan():
    selected_item = tree.selection()
    if selected_item:
        tree.delete(selected_item)
        guardar_datos()
    else:
        messagebox.showwarning("Eliminar", "Por favor, selecciona un plan para eliminar.")

# Función para mostrar fechas de inicio y vencimiento
def mostrar_fechas():
    selected_item = tree.selection()
    if selected_item:
        fecha_inicio = tree.item(selected_item)["tags"][0]
        fecha_vencimiento = tree.item(selected_item)["tags"][1]
        # Mostrar fechas en ventana sin sonido
        ventana_fechas = tk.Toplevel(root)
        ventana_fechas.title("Fechas del Plan")
        ventana_fechas.geometry("300x150")
        tk.Label(ventana_fechas, text=f"Fecha de Inicio: {fecha_inicio}", font=("Arial", 12)).pack(pady=10)
        tk.Label(ventana_fechas, text=f"Fecha de Vencimiento: {fecha_vencimiento}", font=("Arial", 12)).pack(pady=10)
        tk.Button(ventana_fechas, text="Cerrar", command=ventana_fechas.destroy).pack(pady=10)
    else:
        messagebox.showwarning("Mostrar Fechas", "Selecciona una fila para ver las fechas.")

# Configuración de la ventana principal
root = tk.Tk()
root.title("Gestión de Planes Automatizada")
root.geometry("950x500")

# Etiquetas y entradas
tk.Label(root, text="Nombre:").grid(row=0, column=0, padx=5, pady=5)
entry_nombre = tk.Entry(root)
entry_nombre.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Teléfono:").grid(row=1, column=0, padx=5, pady=5)
entry_telefono = tk.Entry(root)
entry_telefono.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="Días del Plan:").grid(row=2, column=0, padx=5, pady=5)
entry_dias_plan = tk.Entry(root)
entry_dias_plan.grid(row=2, column=1, padx=5, pady=5)

tk.Label(root, text="Nota:").grid(row=3, column=0, padx=5, pady=5)
entry_nota = tk.Text(root, height=4, width=40)
entry_nota.grid(row=3, column=1, padx=5, pady=5)

# Botones
tk.Button(root, text="Agregar Plan", command=agregar_plan).grid(row=4, column=0, padx=5, pady=5)
tk.Button(root, text="Eliminar Plan", command=eliminar_plan).grid(row=4, column=1, padx=5, pady=5)
tk.Button(root, text="Mostrar Fechas", command=mostrar_fechas).grid(row=4, column=2, padx=5, pady=5)

# Tabla con solo columnas visibles
columns = ("Nombre", "Teléfono", "Días del Plan", "Días Restantes", "Nota")
tree = ttk.Treeview(root, columns=columns, show="headings", height=15)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=120)
tree.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

# Cargar datos existentes
cargar_datos()

# Iniciar la aplicación
root.mainloop()
