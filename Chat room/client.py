import socket
import threading
import tkinter
from tkinter import simpledialog, scrolledtext

class Client:
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

        self.msg = tkinter.Tk()
        self.msg.withdraw()

        self.nickname = simpledialog.askstring("Nickname", "Please enter your nickname", parent=self.msg)

        self.gui_done = False
        self.running = True

        gui_thread = threading.Thread(target=self.gui_loop)
        rcv_thread = threading.Thread(target=self.receive)

        gui_thread.start()
        rcv_thread.start()

    def gui_loop(self):
        self.wind = tkinter.Tk()
        self.wind.configure(bg='lightgray')

        self.chat_label = tkinter.Label(self.wind, text="Chat: ", bg='lightgray')
        self.chat_label.config(font=("Arial", 12))
        self.chat_label.pack(padx=20, pady=5)

        self.text_area = scrolledtext.ScrolledText(self.wind)
        self.text_area.config(font=("Arial", 12))
        self.text_area.config(state='normal')
        self.text_area.pack(padx=20, pady=5)

        self.msg_label = tkinter.Label(self.wind, text="Message: ", bg='lightgray')
        self.msg_label.config(font=("Arial", 12))
        self.msg_label.pack(padx=20, pady=5)

        self.input_area = tkinter.Text(self.wind, height=3)
        self.input_area.pack(padx=20, pady=5)

        self.send_button = tkinter.Button(self.wind, text="Send", command=self.write)
        self.send_button.config(font=("Arial", 12))
        self.send_button.pack(padx=20, pady=5)

        self.gui_done = True

        self.wind.protocol("WM_DELETE_WINDOW", self.stop)

        # Display "joined chat" message
        self.text_area.config(state='normal')
        self.text_area.insert('end', f"You joined the chat. as {self.nickname}\n")
        self.text_area.yview('end')
        self.text_area.config(state='disabled')

        self.wind.mainloop()

    def stop(self):
        self.running = False
        self.wind.destroy()
        self.sock.close()
        exit(0)

    def write(self):
        message = f"{self.nickname}: {self.input_area.get('1.0', 'end')}"
        self.sock.send(message.encode('utf-8'))
        self.input_area.delete('1.0', 'end')

    def receive(self):
        while self.running:
            try:
                message = self.sock.recv(1024).decode('utf-8')
                if message.startswith("Enter"):
                    self.sock.send(f"{self.nickname}".encode('utf-8'))
                else:
                    if self.gui_done:
                        self.text_area.config(state='normal')
                        self.text_area.insert('end', f"{message}\n")
                        self.text_area.yview('end')
                        self.text_area.config(state='disabled')

            except ConnectionAbortedError:
                break
            except:
                print("Error")
                self.sock.close()
                break


if __name__ == "__main__":
    Host = '127.0.0.1'
    Port = 7000
    client = Client(Host, Port)
