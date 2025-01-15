import tkinter as tk
import socket
import threading

# Configuración de red
SERVER_IP = "172.20.10.2"  # Dirección IP de la máquina controladora
SERVER_PORT = 9999

# Variables globales
ALLOW_PING = True
CLIENT_CONNECTION = None

def handle_client(client_socket):
    global ALLOW_PING
    while True:
        try:
            # Enviar estado actual al cliente
            status = "ALLOW" if ALLOW_PING else "DENY"
            client_socket.send(status.encode())
            threading.Event().wait(1)  # Espera 1 segundo antes de enviar el siguiente estado
        except (ConnectionResetError, BrokenPipeError):
            output_text.insert(tk.END, "Cliente desconectado.\n")
            break

def start_server():
    global CLIENT_CONNECTION
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((SERVER_IP, SERVER_PORT))
    server.listen(1)
    output_text.insert(tk.END, f"Servidor iniciado en {SERVER_IP}:{SERVER_PORT}. Esperando conexión...\n")

    while True:
        client_socket, addr = server.accept()
        CLIENT_CONNECTION = client_socket
        output_text.insert(tk.END, f"Conexión establecida con {addr}.\n")
        threading.Thread(target=handle_client, args=(client_socket,), daemon=True).start()

def allow_ping():
    global ALLOW_PING
    ALLOW_PING = True
    output_text.insert(tk.END, "Ping permitido.\n")

def deny_ping():
    global ALLOW_PING
    ALLOW_PING = False
    output_text.insert(tk.END, "Ping denegado.\n")

# Crear la interfaz gráfica
root = tk.Tk()
root.title("Control de Ping - Servidor")
root.geometry("600x400")  # Tamaño de la ventana
root.config(bg="#2e3b4e")  # Fondo oscuro

# Estilo de los botones
button_style = {
    "font": ("Helvetica", 14),
    "padx": 10,
    "pady": 10,
    "width": 20,
    "height": 2,
    "bd": 3,
    "relief": "raised"
}

# Crear los botones con los estilos
tk.Button(root, text="Permitir Ping", command=allow_ping, bg="green", fg="white", **button_style).grid(row=0, column=0, padx=10, pady=10)
tk.Button(root, text="Denegar Ping", command=deny_ping, bg="red", fg="white", **button_style).grid(row=0, column=1, padx=10, pady=10)

# Crear el área de texto con estilo
output_text = tk.Text(root, width=50, height=15, font=("Courier", 12), bd=5, relief="sunken", bg="#f4f4f4", fg="#333333")
output_text.grid(row=1, column=0, columnspan=2, padx=10, pady=20)

# Iniciar el servidor en un hilo separado
threading.Thread(target=start_server, daemon=True).start()

root.mainloop()
