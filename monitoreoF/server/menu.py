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
ventana.title("Menú de Archivos - Servidor")
ventana.geometry("400x400")

# Etiqueta de título
titulo = tk.Label(ventana, text="Menú de Opciones - Servidor", font=("Arial", 16, "bold"))
titulo.pack(pady=10)

# Lista de archivos del servidor
archivos_servidor = {
    "Transferencia de archivos": "server/server_transferencia.py",
    "Chat": "server/server_chat2.py",
    "Transferencia de archivos": "server/server_transferencia.py",
    "Denegar y permitir ping": "server/ping_manager.py",
     "Bloquear Pagina": "server/server_bloquearpagina.py",
    "Bloquear teclado y mouse": "server/server_bloquearTM.py",
    "Apagar PC": "server/server_apagar.py",
}

# Crear botones para los archivos del servidor
for texto, ruta in archivos_servidor.items():
    boton = tk.Button(ventana, text=texto, font=("Arial", 12), bg="lightgreen", command=lambda r=ruta: ejecutar_archivo(r))
    boton.pack(pady=5, fill=tk.X)

# Botón para salir
boton_salir = tk.Button(ventana, text="Salir", font=("Arial", 12, "bold"), bg="red", fg="white", command=ventana.destroy)
boton_salir.pack(pady=10)

# Ejecutar la aplicación
ventana.mainloop()
