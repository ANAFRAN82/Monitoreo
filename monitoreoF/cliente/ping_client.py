import tkinter as tk
import subprocess
import threading
import socket

# Configuración de red
SERVER_IP = "172.168.3.16"  # Dirección IP del servidor
SERVER_PORT = 9999
ping_process = None
allow_ping = True
packets_sent = 0
packets_received = 0

# Función para realizar ping y monitorear resultados
def monitor_ping(remote_ip):
    global ping_process, packets_sent, packets_received, allow_ping
    packets_sent = 0
    packets_received = 0

    try:
        ping_process = subprocess.Popen(
            ["ping", remote_ip],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        for line in ping_process.stdout:
            if not allow_ping:
                break
            packets_sent += 1
            if "bytes from" in line:
                packets_received += 1
            output_text.insert(tk.END, line)
            output_text.see(tk.END)
    except Exception as e:
        output_text.insert(tk.END, f"Error en ping: {e}\n")
    finally:
        lost_packets = packets_sent - packets_received
        output_text.insert(
            tk.END,
            f"\nPing detenido. Paquetes enviados: {packets_sent}, recibidos: {packets_received}, "
            f"perdidos: {lost_packets}.\n"
        )
        output_text.see(tk.END)

# Iniciar el ping en un hilo separado
def start_ping_thread():
    remote_ip = ip_entry.get()
    threading.Thread(target=monitor_ping, args=(remote_ip,), daemon=True).start()

# Conectar al servidor
def connect_to_server():
    global allow_ping
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((SERVER_IP, SERVER_PORT))
        output_text.insert(tk.END, f"Conectado al servidor {SERVER_IP}:{SERVER_PORT}\n")

        def listen_to_server():
            nonlocal client_socket
            try:
                while True:
                    status = client_socket.recv(1024).decode()
                    allow_ping = (status == "ALLOW")
                    if not allow_ping and ping_process:
                        ping_process.terminate()  # Detener el ping si está en ejecución
            except ConnectionResetError:
                output_text.insert(tk.END, "Desconectado del servidor.\n")
            finally:
                client_socket.close()

        threading.Thread(target=listen_to_server, daemon=True).start()
    except Exception as e:
        output_text.insert(tk.END, f"Error al conectar con el servidor: {e}\n")

# Crear la interfaz gráfica
root = tk.Tk()
root.title("Ping Remoto - Cliente")
root.geometry("400x350")
root.resizable(False, False)
root.configure(bg="#f0f0f0")

# Estilo de etiquetas y entradas
label_style = {"bg": "#f0f0f0", "fg": "#333", "font": ("Arial", 10)}
entry_style = {"width": 25, "font": ("Arial", 10)}

# Campo para ingresar la IP remota
tk.Label(root, text="IP remota:", **label_style).grid(row=0, column=0, padx=10, pady=10, sticky="w")
ip_entry = tk.Entry(root, **entry_style)
ip_entry.grid(row=0, column=1, padx=10, pady=10)

# Botones
tk.Button(root, text="Conectar al Servidor", command=connect_to_server, bg="#007BFF", fg="white", font=("Arial", 10, "bold")).grid(
    row=1, column=0, columnspan=2, padx=10, pady=5
)
tk.Button(root, text="Iniciar Ping", command=start_ping_thread, bg="#28a745", fg="white", font=("Arial", 10, "bold")).grid(
    row=2, column=0, columnspan=2, padx=10, pady=5
)

# Área de texto para la salida
output_text = tk.Text(root, width=50, height=10, font=("Courier New", 10), bg="#fff", fg="#333", borderwidth=2, relief="groove")
output_text.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# Iniciar la aplicación
root.mainloop()
