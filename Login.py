import tkinter as tk
from customtkinter import *

set_appearance_mode("light")

def login():
    username = entry1.get()
    password = entry2.get()
    if username == "admin" and password == "admin123":
        label_result.configure(text="Login bem-sucedido!", text_color="green")
    else:
        label_result.configure(text="Nome de usuário ou senha incorretos", text_color="red")


janela = CTk()
janela.geometry("700x400")
janela.title("Sistema de login")
janela.iconbitmap("icon.ico")
janela.resizable(False, False)


img = tk.PhotoImage(file="logo.png")
image_widget = tk.Label(master=janela, image=img)
image_widget.place(x=-18, y=0)

# label_tt = CTkLabel(master=janela, text="GEO Ginasio Educacioanl Olimpico\n Isabel Salgado", font=("Roboto", 18), text_color="#00B0F0")
# label_tt.place(x=39, y=10)

frame = CTkFrame(master=janela, width=350, height=396, fg_color=("white", "gray30"))
frame.pack(side=RIGHT)

label = CTkLabel(master=frame, text="Sistema de login", height=110, font=("Roboto", 30))
label.place(x=25, y=5)

entry1 = CTkEntry(master=frame, placeholder_text="Nome do usuário", width=300, font=("Roboto", 14))
entry1.place(x=25, y=105)

label1 = CTkLabel(master=frame, text="O campo nome de usuário é de caráter obrigatório.", text_color="green", font=("Roboto", 11))
label1.place(x=25, y=135)

entry2 = CTkEntry(master=frame, placeholder_text="Senha do usuário", width=300, font=("Roboto", 14))
entry2.place(x=25, y=160)

label2 = CTkLabel(master=frame, text="O campo senha é de caráter obrigatório.", text_color="green", font=("Roboto", 11))
label2.place(x=25, y=190)

chekbox = CTkCheckBox(master=frame, text="Lembrar-me sempre")
chekbox.place(x=25, y=235)

button = CTkButton(master=frame, text="Login", width=300, command=login)
button.place(x=25, y=285)

label_result = CTkLabel(master=frame, text="", font=("Roboto", 12))
label_result.place(x=25, y=320)
janela.mainloop()
