import socket
import threading
import StateMachine

HOST = '172.16.1.240'
PORT = 8200
connection = None
connected = False

def send_message(message):
    if not connected: return
    print(message)
    connection.send(message.encode())

def connect():
    t = threading.Thread(target=connect_thread)
    t.start()

def connect_thread():
    global sock
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((HOST, PORT))
    except:
        StateMachine.current_state.timeout()
        return
    global connection, connected
    connection = sock
    connected = True
    StateMachine.current_state.connected()
        
def recieve():
    t = threading.Thread(target=recieve_thread)
    t.start()
    
def recieve_thread():
    with sock:
        global connected
        while connected:
            try:
                data = sock.recv(1024)
            except:
                StateMachine.current_state.chat_closed()
                connected = False
                break
            if not data:
                connected = False
                break
            if data.decode() == "end":
                StateMachine.current_state.chat_closed()
                connected = False
                break
            StateMachine.current_state.server_input(data.decode())
            
