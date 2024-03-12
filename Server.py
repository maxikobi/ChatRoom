from threading import Thread
import socket

HOST = '0.0.0.0' 
PORT = 8200
clients = []
names = []

def client_name(client):
    index = clients.index(client)
    return names[index]

def disconnect(client):
    name = client_name(client)
    broadcast(name + " has left the chat", client)
    clients.remove(client)
    names.remove(name)
    
def broadcast_all(message):
    broadcast(message, None)
    
def broadcast(message, sender):
    print(message)
    for client in clients:
        if client == sender:
            continue
        client.send(message.encode())
    
def client_listener(client):
    with client:
        name = client.recv(1024).decode()
        broadcast(name + " has joined the chat!", client)
        names.insert(clients.index(client), name)
        while True:
            try:
                data = client.recv(1024)
                if not data:
                    disconnect(client)
                    break
                
                content = data.decode()
                if content == "end":
                    disconnect(client)
                    break
                
                name = client_name(client)
                message = f"{name} said: {content}";
                broadcast(message, client)
            except:
                disconnect(client)
                break

def start():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        print("server is running!")

        while True:
            s.listen()
            conn, addr = s.accept()
            print(f"Connected to: {addr}")
            clients.append(conn)
            cl = Thread(target=client_listener, args=(conn,))
            cl.start()
    
start()      