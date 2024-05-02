from tkinter import *
import threading
import StateMachine

BG_GRAY = "#ABB2B9"
BG_COLOR = "#17202A"
TEXT_COLOR = "#EAECEE"
 
FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"

def log(text):
    txt_log.config(state=NORMAL)
    txt_log.insert(END, "\n" + text)
    txt_log.config(state=DISABLED)

def send(event=None):
    if not (ent_input.get().isspace() or ent_input.get() == ""):
        StateMachine.current_state.user_input(ent_input.get())
        
 
    ent_input.delete(0, END)
    
def on_closing():
    print("window closed")
    window.quit()

def open_window():
    t = threading.Thread(target=window_thread)
    t.start()
    
def window_thread():
    global window
    window = Tk()
    window.title("Chat Room")
    window.columnconfigure(0, weight=1)
    window.protocol("WM_DELETE_WINDOW", on_closing)
    window.bind('<Return>', send)

    lbl_welcome = Label(window, bg=BG_COLOR, fg=TEXT_COLOR, text="Welcome", font=FONT_BOLD, pady=10, width=20, height=1).grid(row=0)
    
    global txt_log
    txt_log = Text(window, bg=BG_COLOR, fg=TEXT_COLOR, font=FONT, width=60)
    txt_log.insert(END, "Enter Name: ")
    txt_log.config(state=DISABLED)
    txt_log.grid(row=1, column=0, columnspan=2)
 
    global ent_input
    ent_input = Entry(window, bg="#2C3E50", fg=TEXT_COLOR, font=FONT, width=55)
    ent_input.grid(row=2, column=0)
 
    btn_send = Button(window, text="Send", font=FONT_BOLD, bg=BG_GRAY, command=send).grid(row=2, column=1)
    
    window.mainloop()
    
def close_window():
    window.quit()