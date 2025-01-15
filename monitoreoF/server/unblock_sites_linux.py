import os
import tkinter as tk
from tkinter import messagebox

def unblock_sites(sites):
    """
    Desbloquea los sitios especificados eliminándolos del archivo hosts del sistema en Ubuntu.
    
    :param sites: Lista de sitios a desbloquear (ejemplo: ["facebook.com", "gmail.com", "youtube.com"]).
    """
    hosts_path = "/etc/hosts"  # Ruta del archivo hosts en sistemas Linux/Ubuntu
    redirect_ip = "172.168.2.235"  # La IP que se utiliza para bloquear los sitios
    
    try:
        print(f"Intentando desbloquear los siguientes sitios: {', '.join(sites)}")

        # Leer y filtrar el archivo hosts
        with open(hosts_path, "r+") as hosts_file:
            lines = hosts_file.readlines()
            hosts_file.seek(0)

            # Escribir solo las líneas que no contienen los sitios bloqueados con la IP de redirección
            for line in lines:
                if not any(site in line for site in sites) or redirect_ip not in line:
                    hosts_file.write(line)

            # Truncar el archivo para eliminar cualquier contenido residual
            hosts_file.truncate()

        messagebox.showinfo("Éxito", "Sitios desbloqueados exitosamente.")
    except PermissionError:
        messagebox.showerror(
            "Error de permisos", "No tienes permisos para modificar el archivo hosts. Ejecuta este script con 'sudo'."
        )
    except FileNotFoundError:
        messagebox.showerror("Error", f"El archivo hosts no se encontró en la ruta {hosts_path}.")
    except Exception as e:
        messagebox.showerror("Error inesperado", f"Error al desbloquear sitios: {e}")

def desbloquear():
    """
    Obtiene la lista de sitios desde el campo de entrada y los desbloquea.
    """
    sitios = entry_sites.get().strip()
    if not sitios:
        messagebox.showwarning("Advertencia", "Por favor, ingresa sitios para desbloquear.")
        return

    # Convertir la lista de sitios en un formato adecuado
    sitios_lista = [site.strip() for site in sitios.split(",") if site.strip()]
    unblock_sites(sitios_lista)

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Desbloqueador de sitios")
ventana.geometry("400x250")
ventana.config(bg="#f4f4f9")  # Fondo de color suave

# Etiqueta de instrucciones
label_instrucciones = tk.Label(ventana, text="Ingresa los sitios a desbloquear separados por comas:",
                                font=("Arial", 12), bg="#f4f4f9", fg="#333333")
label_instrucciones.pack(pady=15)

# Campo de entrada para sitios
entry_sites = tk.Entry(ventana, width=50, font=("Arial", 12), bd=2, relief="solid")
entry_sites.pack(pady=5)

# Botón de desbloqueo
boton_desbloquear = tk.Button(ventana, text="Desbloquear sitios", command=desbloquear,
                              bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), relief="raised", bd=4)
boton_desbloquear.pack(pady=20)

# Iniciar el bucle principal de la interfaz gráfica
ventana.mainloop()
