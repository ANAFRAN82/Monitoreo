import os
import tkinter as tk
from tkinter import messagebox

# Función para ejecutar un archivo Python
def ejecutar_archivo(ruta):
    try:
        os.system(f"python3 {ruta}")
    except Exception as e:
        messagebox.showerror("Error", f"Error al ejecutar {ruta}: {e}")

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Menú de Archivos - Cliente")
ventana.geometry("400x300")

# Etiqueta de título
titulo = tk.Label(ventana, text="Menú de Opciones - Cliente", font=("Arial", 16, "bold"))
titulo.pack(pady=10)

# Lista de archivos del cliente
archivos_cliente = {
    "Chat": "cliente/cliente_chat.py",
    "Transferencia de archivos": "cliente/cliente_transferencia.py",
    "Denegar y permitir ping": "cliente/ping_client.py",
}

# Crear botones para los archivos del cliente
for texto, ruta in archivos_cliente.items():
    boton = tk.Button(ventana, text=texto, font=("Arial", 12), bg="lightblue", command=lambda r=ruta: ejecutar_archivo(r))
    boton.pack(pady=5, fill=tk.X)

# Botón para salir
boton_salir = tk.Button(ventana, text="Salir", font=("Arial", 12, "bold"), bg="red", fg="white", command=ventana.destroy)
boton_salir.pack(pady=10)

# Ejecutar la aplicación
ventana.mainloop()
