from threading import Thread
import socket
import threading

HOST = '0.0.0.0' 
PORT = 8200
clients = []

def broadcast(message, sender):
    for client in clients:
        if client == sender:
            continue
        client.send(message.encode())
        

    
def client_listener(client):
    with client:
        while True:
            try:
                data = client.recv(1024)
                if not data:
                    clients.remove(client)
                    break
            
                name = data.decode().split("~")[0]
                content = data.decode().split("~")[1]
                if content == "end":
                    print(name + " has left the chat")
                    clients.remove(client)
                    break
                
                message = f"{name} said: {content}";
                print(message)
                broadcast(message, client)
            except:
                print("user left")
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