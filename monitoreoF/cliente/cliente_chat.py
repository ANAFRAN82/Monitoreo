import tkinter as tk
from tkinter import messagebox, scrolledtext
import socket
import threading

# Función para iniciar el servidor
def iniciar_servidor(ip, puerto):
    try:
        servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        servidor.bind((ip, int(puerto)))
        servidor.listen(1)
        messagebox.showinfo("Servidor", "Servidor iniciado. Esperando conexión...")

        cliente, direccion = servidor.accept()
        messagebox.showinfo("Servidor", f"Conexión establecida con {direccion}")

        # Hilo para manejar los mensajes recibidos
        threading.Thread(target=recibir_mensajes, args=(cliente,)).start()
        return servidor, cliente
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo iniciar el servidor: {e}")
        return None, None

# Función para iniciar el cliente
def iniciar_cliente(ip, puerto):
    try:
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente.connect((ip, int(puerto)))
        messagebox.showinfo("Cliente", "Conectado al servidor.")

        # Hilo para manejar los mensajes recibidos
        threading.Thread(target=recibir_mensajes, args=(cliente,)).start()
        return cliente
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo conectar al servidor: {e}")
        return None

# Función para enviar mensajes
def enviar_mensaje():
    global conexion
    mensaje = entrada_mensaje.get()
    if mensaje:
        try:
            conexion.send(mensaje.encode('utf-8'))
            area_chat.insert(tk.END, f"Tú: {mensaje}\n")
            entrada_mensaje.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"Error al enviar mensaje: {e}")

# Función para recibir mensajes
def recibir_mensajes(socket_conexion):
    while True:
        try:
            mensaje = socket_conexion.recv(1024).decode('utf-8')
            if mensaje:
                area_chat.insert(tk.END, f"Otro: {mensaje}\n")
        except:
            messagebox.showerror("Error", "Conexión cerrada.")
            break

# Función para inicializar como servidor o cliente
def iniciar_chat():
    global conexion
    ip = entrada_ip.get()
    puerto = entrada_puerto.get()

    if not ip or not puerto:
        messagebox.showerror("Error", "Por favor, completa todos los campos.")
        return

    if modo.get() == "Servidor":
        servidor, cliente = iniciar_servidor(ip, puerto)
        if servidor and cliente:
            conexion = cliente
    elif modo.get() == "Cliente":
        cliente = iniciar_cliente(ip, puerto)
        if cliente:
            conexion = cliente
    else:
        messagebox.showerror("Error", "Selecciona un modo válido.")

# Crear la ventana principal
root = tk.Tk()
root.title("Chat Bidireccional")
root.geometry("500x700")
root.config(bg="#f2f2f2")

conexion = None

# Estilo de fuentes
fuente_titulo = ("Arial", 16, "bold")
fuente_normal = ("Arial", 12)

# Título
titulo = tk.Label(root, text="Chat Bidireccional", font=fuente_titulo, bg="#f2f2f2", fg="#333")
titulo.pack(pady=10)

# Modo de operación
modo = tk.StringVar(value="Servidor")
frame_modo = tk.Frame(root, bg="#f2f2f2")
frame_modo.pack(pady=10)
tk.Label(frame_modo, text="Selecciona el modo:", font=fuente_normal, bg="#f2f2f2").grid(row=0, column=0, columnspan=2, pady=5)
tk.Radiobutton(frame_modo, text="Servidor", variable=modo, value="Servidor", font=fuente_normal, bg="#f2f2f2").grid(row=1, column=0, padx=10)
tk.Radiobutton(frame_modo, text="Cliente", variable=modo, value="Cliente", font=fuente_normal, bg="#f2f2f2").grid(row=1, column=1, padx=10)

# Campos de entrada para configuración
frame_config = tk.Frame(root, bg="#f2f2f2")
frame_config.pack(pady=10)
tk.Label(frame_config, text="IP:", font=fuente_normal, bg="#f2f2f2").grid(row=0, column=0, sticky="e", padx=5, pady=5)
entrada_ip = tk.Entry(frame_config, font=fuente_normal)
entrada_ip.grid(row=0, column=1, padx=5, pady=5)
tk.Label(frame_config, text="Puerto:", font=fuente_normal, bg="#f2f2f2").grid(row=1, column=0, sticky="e", padx=5, pady=5)
entrada_puerto = tk.Entry(frame_config, font=fuente_normal)
entrada_puerto.grid(row=1, column=1, padx=5, pady=5)

# Botón para iniciar el chat
btn_iniciar = tk.Button(root, text="Iniciar Chat", font=fuente_normal, bg="#4caf50", fg="white", command=iniciar_chat)
btn_iniciar.pack(pady=10, ipadx=10, ipady=5)

# Área de chat
area_chat = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=fuente_normal, height=20, bg="#ffffff", fg="#333")
area_chat.pack(fill="both", padx=20, pady=10)

# Entrada para escribir mensajes
entrada_mensaje = tk.Entry(root, font=fuente_normal)
entrada_mensaje.pack(fill="x", padx=20, pady=5)

# Botón para enviar mensajes
btn_enviar = tk.Button(root, text="Enviar", font=fuente_normal, bg="#2196f3", fg="white", command=enviar_mensaje)
btn_enviar.pack(pady=10, ipadx=10, ipady=5)


# Ejecutar la ventana principal
root.mainloop()
