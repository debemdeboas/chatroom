from src.client import client

cli = client.Client('dns.chat.debem.dev', [lambda msg: msg_list.insert(tk.END, msg)])

import tkinter as tk

def send_msg(msg: str):
    cli.send(msg)

def send(event = None):
    send_msg(msg.get())
    msg.set('')

def on_closing():
    send_msg('[quit]')
    quit()

root = tk.Tk()
root.title('oi mo')

messages_frame = tk.Frame(root)
msg = tk.StringVar()
msg.set('Escreve aqui mo')
scrollbar = tk.Scrollbar(messages_frame)
msg_list = tk.Listbox(messages_frame, height=25, width=95, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
msg_list.pack(side=tk.LEFT, fill=tk.BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = tk.Entry(root, textvariable=msg)
entry_field.bind('<Return>', send)
entry_field.pack()
send_button = tk.Button(root, text='Send', command=send)
send_button.pack()
root.protocol('WM_DELETE_WINDOW', on_closing)

root.mainloop()