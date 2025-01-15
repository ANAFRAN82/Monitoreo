import paramiko
import io
import tkinter as tk
from tkinter import messagebox, filedialog

# Función para conectar y transferir el archivo
def transferir_archivo():
    origen_host = host_origen_entry.get()
    origen_usuario = usuario_origen_entry.get()
    origen_password = password_origen_entry.get()
    archivo_origen = archivo_origen_entry.get()

    destino_host = host_destino_entry.get()
    destino_usuario = usuario_destino_entry.get()
    destino_password = password_destino_entry.get()
    destino_completo = destino_entry.get()

    try:
        # Conexión SSH al origen
        ssh_origen = paramiko.SSHClient()
        ssh_origen.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_origen.connect(hostname=origen_host, username=origen_usuario, password=origen_password)

        # Leer archivo desde origen
        sftp_origen = ssh_origen.open_sftp()
        archivo_memoria = io.BytesIO()
        sftp_origen.getfo(archivo_origen, archivo_memoria)
        archivo_memoria.seek(0)
        sftp_origen.close()
        ssh_origen.close()

        # Conexión SSH al destino
        ssh_destino = paramiko.SSHClient()
        ssh_destino.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_destino.connect(hostname=destino_host, username=destino_usuario, password=destino_password)

        # Crear directorio en destino si no existe
        ssh_destino.exec_command(f"mkdir -p {destino_completo.rsplit('/', 1)[0]}")

        # Transferencia del archivo al destino
        sftp_destino = ssh_destino.open_sftp()
        archivo_memoria.seek(0)
        sftp_destino.putfo(archivo_memoria, destino_completo)
        sftp_destino.close()
        ssh_destino.close()

        messagebox.showinfo("Éxito", "Transferencia exitosa")
    except Exception as e:
        messagebox.showerror("Error", f"Error en la transferencia: {str(e)}")

# Función para abrir un cuadro de diálogo y seleccionar un archivo
def seleccionar_archivo_origen():
    archivo = filedialog.askopenfilename(title="Seleccionar archivo de origen")
    archivo_origen_entry.delete(0, tk.END)
    archivo_origen_entry.insert(0, archivo)

# Función para habilitar o deshabilitar el botón de transferencia
def habilitar_boton():
    campos = [host_origen_entry, usuario_origen_entry, password_origen_entry, archivo_origen_entry,
              host_destino_entry, usuario_destino_entry, password_destino_entry, destino_entry]
    if all(campo.get() for campo in campos):
        btn_transferir.config(state=tk.NORMAL)
    else:
        btn_transferir.config(state=tk.DISABLED)

# Crear ventana principal
root = tk.Tk()
root.title("Transferencia de Archivos por SSH")
root.geometry("600x600")
root.config(bg="#f4f4f4")

# Estilo común
label_style = {"bg": "#f4f4f4", "anchor": "w"}
entry_style = {"relief": tk.SUNKEN, "bd": 2}

# Sección de origen
tk.Label(root, text="Máquina de Origen", font=("Arial", 12, "bold"), bg="#f4f4f4").pack(pady=5)
tk.Label(root, text="IP del origen", **label_style).pack(anchor="w", padx=20)
host_origen_entry = tk.Entry(root, **entry_style)
host_origen_entry.pack(fill="x", padx=20)
host_origen_entry.bind("<KeyRelease>", lambda e: habilitar_boton())

tk.Label(root, text="Usuario del origen", **label_style).pack(anchor="w", padx=20)
usuario_origen_entry = tk.Entry(root, **entry_style)
usuario_origen_entry.pack(fill="x", padx=20)
usuario_origen_entry.bind("<KeyRelease>", lambda e: habilitar_boton())

tk.Label(root, text="Contraseña del origen", **label_style).pack(anchor="w", padx=20)
password_origen_entry = tk.Entry(root, show="*", **entry_style)
password_origen_entry.pack(fill="x", padx=20)
password_origen_entry.bind("<KeyRelease>", lambda e: habilitar_boton())

tk.Label(root, text="Archivo a transferir (origen)", **label_style).pack(anchor="w", padx=20)
archivo_origen_entry = tk.Entry(root, **entry_style)
archivo_origen_entry.pack(fill="x", padx=20)
btn_seleccionar_archivo = tk.Button(root, text="Seleccionar archivo", command=seleccionar_archivo_origen, bg="#0078D4", fg="white")
btn_seleccionar_archivo.pack(pady=5)

# Sección de destino
tk.Label(root, text="Máquina de Destino", font=("Arial", 12, "bold"), bg="#f4f4f4").pack(pady=10)
tk.Label(root, text="IP del destino", **label_style).pack(anchor="w", padx=20)
host_destino_entry = tk.Entry(root, **entry_style)
host_destino_entry.pack(fill="x", padx=20)
host_destino_entry.bind("<KeyRelease>", lambda e: habilitar_boton())

tk.Label(root, text="Usuario del destino", **label_style).pack(anchor="w", padx=20)
usuario_destino_entry = tk.Entry(root, **entry_style)
usuario_destino_entry.pack(fill="x", padx=20)
usuario_destino_entry.bind("<KeyRelease>", lambda e: habilitar_boton())

tk.Label(root, text="Contraseña del destino", **label_style).pack(anchor="w", padx=20)
password_destino_entry = tk.Entry(root, show="*", **entry_style)
password_destino_entry.pack(fill="x", padx=20)
password_destino_entry.bind("<KeyRelease>", lambda e: habilitar_boton())

tk.Label(root, text="Ruta destino (completa)", **label_style).pack(anchor="w", padx=20)
destino_entry = tk.Entry(root, **entry_style)
destino_entry.pack(fill="x", padx=20)
destino_entry.bind("<KeyRelease>", lambda e: habilitar_boton())

# Botón de transferencia
btn_transferir = tk.Button(root, text="Transferir archivo", command=transferir_archivo, state=tk.DISABLED, bg="#0078D4", fg="white")
btn_transferir.pack(pady=20)

# Ejecutar la ventana
root.mainloop()
