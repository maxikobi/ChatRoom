import StateMachine
import Networking
import Graphics

name = ""

class enter_name_state:
    def enter(self):
        Graphics.open_window()

    def user_input(self, message):
        Graphics.log(message)
        global name
        name = message
        StateMachine.switch_state(try_connect_state())
        
class try_connect_state:
    def enter(self):
        Graphics.log("Waiting for connection...")
        Networking.connect()
        
    def user_input(self, message):
        pass
    
    def timeout(self):
        Graphics.log("couldn't connect! connection timed out!")
        
    def connected(self):
        Graphics.log("Connected")
        Networking.send_message(name)
        StateMachine.switch_state(connected_state())
        
class connected_state():
    
    def enter(self):
        Networking.recieve()
        
    def user_input(self, message):
        if message == "end":
            Graphics.log("You left the chat")
            Networking.connected = False
        else:
            Graphics.log(f"You Said {message}")
            Networking.send_message(message)
    
    def server_input(self, message):
        Graphics.log(message)
    
    def chat_closed(self):
        Graphics.log("server has closed the chat")
        
    




