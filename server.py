import socket
import threading
import os

# Render'ın atayacağı portu yakalıyoruz, lokalde test için 5000'i kullanır
PORT = int(os.environ.get("PORT", 5000))
HOST = '0.0.0.0'

clients = {}  # {socket: username}

def broadcast(message, sender_socket=None):
    """Tüm bağlı kullanıcılara mesaj gönderir."""
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message)
            except:
                client.close()
                if client in clients:
                    del clients[client]

def handle_client(client_socket):
    while True:
        try:
            header = client_socket.recv(1024)
            if not header:
                break
            broadcast(header, client_socket)
        except:
            break

    if client_socket in clients:
        username = clients[client_socket]
        del clients[client_socket]
        client_socket.close()
        broadcast(f"[Sistem] {username} sohbetten ayrıldı.".encode('utf-8'))

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[*] MSN Sunucusu {PORT} portunda başlatıldı...")

    while True:
        client_socket, address = server.accept()
        print(f"[+] Yeni bağlantı: {address}")
        try:
            username = client_socket.recv(1024).decode('utf-8')
            clients[client_socket] = username
            print(f"[+] Kullanıcı adı: {username}")
            
            thread = threading.Thread(target=handle_client, args=(client_socket,))
            thread.start()
        except:
            client_socket.close()

if __name__ == "__main__":
    start_server()
