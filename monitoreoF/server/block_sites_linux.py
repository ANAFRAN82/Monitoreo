import os
import tkinter as tk
from tkinter import messagebox

def block_sites(sites):
    """
    Bloquea los sitios especificados agregándolos al archivo hosts del sistema en Ubuntu.

    :param sites: Lista de sitios a bloquear (ejemplo: ["facebook.com", "gmail.com"]).
    """
    hosts_path = "/etc/hosts"  # Ruta del archivo hosts en sistemas Linux/Ubuntu
    redirect_ip = "172.168.1.154"

    try:
        print(f"Bloqueando los siguientes sitios: {', '.join(sites)}")

        # Leer el archivo actual
        with open(hosts_path, "r") as hosts_file:
            existing_lines = hosts_file.readlines()

        # Escribir nuevas entradas si no existen ya
        with open(hosts_path, "a") as hosts_file:
            for site in sites:
                entry = f"{redirect_ip} {site}\n"
                if entry not in existing_lines:
                    hosts_file.write(entry)
                    print(f"{site} bloqueado exitosamente.")
                else:
                    print(f"{site} ya está bloqueado.")

        messagebox.showinfo("Éxito", "Sitios bloqueados exitosamente.")
    except PermissionError:
        messagebox.showerror(
            "Error de permisos", "No tienes permisos para modificar el archivo hosts. Ejecuta este script con 'sudo'."
        )
    except FileNotFoundError:
        messagebox.showerror("Error", f"El archivo hosts no se encontró en la ruta {hosts_path}.")
    except Exception as e:
        messagebox.showerror("Error inesperado", f"Error al bloquear sitios: {e}")

def bloquear():
    """
    Obtiene la lista de sitios desde el campo de entrada y los bloquea.
    """
    sitios = entry_sites.get().strip()
    if not sitios:
        messagebox.showwarning("Advertencia", "Por favor, ingresa sitios para bloquear.")
        return

    # Convertir la lista de sitios en un formato adecuado
    sitios_lista = [site.strip() for site in sitios.split(",") if site.strip()]
    block_sites(sitios_lista)

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Bloqueador de sitios")
ventana.geometry("450x250")
ventana.resizable(False, False)
ventana.configure(bg="#f0f0f0")

# Estilo de etiquetas y entradas
label_style = {"bg": "#f0f0f0", "fg": "#333", "font": ("Arial", 10)}
entry_style = {"width": 50, "font": ("Arial", 10)}

# Etiqueta de instrucciones
label_instrucciones = tk.Label(ventana, text="Ingresa los sitios a bloquear separados por comas:", **label_style)
label_instrucciones.pack(pady=15)

# Campo de entrada para sitios
entry_sites = tk.Entry(ventana, **entry_style)
entry_sites.pack(pady=5)

# Botón de bloqueo
boton_bloquear = tk.Button(
    ventana, 
    text="Bloquear sitios", 
    command=bloquear, 
    bg="#007BFF", 
    fg="white", 
    font=("Arial", 10, "bold"), 
    width=20
)
boton_bloquear.pack(pady=20)

# Iniciar el bucle principal de la interfaz gráfica
ventana.mainloop()
