import socket
import threading

HOST = '172.16.0.124'
PORT = 8200
connection = None
connected = False
name = input("Enter Name: ")

def send_message(message):
    if not connected: return
    data = name + "~" + message
    connection.send(data.encode())
    

def console_input():
    while True:
        inp = input()#"Enter message: ")
        if not connected:
            break
        send_message(inp)
        
def start():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        print("Waiting for connection...")
        try:
            sock.connect((HOST, PORT))
        except:
            print("couldn't connect! connection timed out!")
            return
        print("Connected")
        global connection, connected
        connection = sock
        connected = True
        t = threading.Thread(target=console_input)
        t.start()
        
        while True:
            data = sock.recv(1024)
            if not data:
                connected = False
                break
            if data.decode() == "end":
                print("server has closed the chat")
                connected = False
                break
            print(f"Server Said: {data.decode( )}")
            
start()
