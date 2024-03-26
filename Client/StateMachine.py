from States import enter_name_state

def start():
    global current_state
    switch_state(enter_name_state())
    
def switch_state(new_state):
    global current_state
    current_state = new_state
    new_state.enter()
