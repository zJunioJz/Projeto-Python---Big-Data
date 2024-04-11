import tkinter as tk
from customtkinter import *
import sqlite3
import hashlib
from home import home

set_appearance_mode("light")

def hash_senha(senha):
    # Hash da senha usando o algoritmo SHA-256
    return hashlib.sha256(senha.encode()).hexdigest()

def login():
    username = entry1.get()
    senha = entry2.get()

    # Verificar se os campos estão preenchidos
    if username and senha:
        # Conectar ao banco de dados
        conn = sqlite3.connect('usuarios.db')
        cursor = conn.cursor()

        # Consulta SQL para buscar o usuário pelo nome de usuário
        cursor.execute("SELECT * FROM usuarios WHERE username = ?", (username,))
        usuarios = cursor.fetchone()

        if usuarios:
            # Extrair o hash da senha do usuário
            senha_hash_armazenada = usuarios[2]

            # Calcular o hash da senha inserida
            senha_hash_inserida = hash_senha(senha)

            # Verificar se os hashes coincidem
            if senha_hash_armazenada == senha_hash_inserida:
                if usuarios[3] == 1:
                    label_result.configure(text="Login bem-sucedido como administrador!", text_color="green")
                else:
                    label_result.configure(text="Login bem-sucedido como usuário comum!", text_color="green")

                janela.destroy()
                home()
            else:
                label_result.configure(text="Senha incorreta", text_color="red")
        else:
            label_result.configure(text="Nome de usuário não encontrado", text_color="red")

        conn.close()
    else:
        label_result.configure(text="Preencha todos os campos", text_color="red")
        label_result.place(x=25, y=75)  

def abrir_tela_cadastro():
    # Ocultar widgets de login
    label.place_forget()
    entry1.place_forget()
    label1.place_forget()
    entry2.place_forget()
    label2.place_forget()
    button.place_forget()
    button_criar_conta.place_forget()
    label_result.place_forget()

    # Exibir widgets de cadastro
    label_cadastro.place(x=25, y=5)
    entry_cadastro1.place(x=25, y=105)
    label_cadastro1.place(x=25, y=135)
    entry_cadastro2.place(x=25, y=160)
    label_cadastro2.place(x=25, y=190)
    check_admin.place(x=25, y=215)
    check_usuario.place(x=150, y=215)
    button_cadastro.place(x=25, y=285)
    button_voltar.place(x=25, y=320)
    label_cadastro_result.place(x=25, y=75)

def cadastrar():
    username = entry_cadastro1.get()
    senha = entry_cadastro2.get()
    admin = var_admin.get()
    usuario = var_usuario.get()

    # Verificar se os campos estão preenchidos
    if username and senha:
        # Conectar ao banco de dados
        conn = sqlite3.connect('usuarios.db')
        cursor = conn.cursor()

        # Verificar se o usuário já existe
        cursor.execute("SELECT * FROM usuarios WHERE username = ?", (username,))
        usuario_existente = cursor.fetchone()

        if usuario_existente:
            label_cadastro_result.configure(text="Nome de usuário já existe", text_color="red")
        else:
            # Hash da senha
            senha_hash = hash_senha(senha)

            # Inserir novo usuário no banco de dados
            cursor.execute("INSERT INTO usuarios (username, senha_hash, admin) VALUES (?, ?, ?)", (username, senha_hash, admin))
            conn.commit()
            conn.close()

            label_cadastro_result.configure(text="Usuário cadastrado com sucesso!", text_color="green")
    else:
        label_cadastro_result.configure(text="Preencha todos os campos", text_color="red")

def voltar_tela_login():
    # Ocultar widgets de cadastro
    label_cadastro.place_forget()
    entry_cadastro1.place_forget()
    label_cadastro1.place_forget()
    entry_cadastro2.place_forget()
    label_cadastro2.place_forget()
    check_admin.place_forget()
    check_usuario.place_forget()
    button_cadastro.place_forget()
    button_voltar.place_forget()
    label_cadastro_result.place_forget()

    # Exibir widgets de login
    label.place(x=25, y=5)
    entry1.place(x=25, y=105)
    label1.place(x=25, y=135)
    entry2.place(x=25, y=160)
    label2.place(x=25, y=190)
    button.place(x=25, y=235)
    label_result.place(x=25, y=75) 

janela = CTk()
janela.geometry("700x400")
janela.title("Sistema de login")
janela.iconbitmap("icon.ico")
janela.resizable(False, False)


img = tk.PhotoImage(file="logo.png")
image_widget = tk.Label(master=janela, image=img)
image_widget.place(x=-18, y=0)

frame = CTkFrame(master=janela, width=350, height=396, fg_color=("white", "gray30"))
frame.pack(side=RIGHT)

label = CTkLabel(master=frame, text="Sistema de login", height=110, font=("Roboto", 30))
label.place(x=25, y=5)

entry1 = CTkEntry(master=frame, placeholder_text="Nome do usuário", width=300, font=("Roboto", 14))
entry1.place(x=25, y=105)

label1 = CTkLabel(master=frame, text="O campo nome de usuário é de caráter obrigatório.", text_color="green", font=("Roboto", 11))
label1.place(x=25, y=135)

entry2 = CTkEntry(master=frame, placeholder_text="Senha do usuário", width=300, font=("Roboto", 14), show="*")
entry2.place(x=25, y=160)

label2 = CTkLabel(master=frame, text="O campo senha é de caráter obrigatório.", text_color="green", font=("Roboto", 11))
label2.place(x=25, y=190)

button = CTkButton(master=frame, text="Login", width=300, command=login)
button.place(x=25, y=285)

label_result = CTkLabel(master=frame, text="", font=("Roboto", 12))
label_result.place(x=25, y=240) 

# Widgets de cadastro
label_cadastro = CTkLabel(master=frame, text="Cadastre-se", height=110, font=("Roboto", 30))
label_cadastro1 = CTkLabel(master=frame, text="Nome do usuário", text_color="green", font=("Roboto", 11))
label_cadastro2 = CTkLabel(master=frame, text="Senha do usuário", text_color="green", font=("Roboto", 11))
entry_cadastro1 = CTkEntry(master=frame, placeholder_text="Nome do usuário", width=300, font=("Roboto", 14))
entry_cadastro2 = CTkEntry(master=frame, placeholder_text="Senha do usuário", width=300, font=("Roboto", 14), show="*")
var_admin = tk.IntVar()
check_admin = CTkCheckBox(master=frame, text="Administrador", variable=var_admin)
var_usuario = tk.IntVar()
check_usuario = CTkCheckBox(master=frame, text="Usuário", variable=var_usuario)
button_cadastro = CTkButton(master=frame, text="Cadastrar", width=300, command=cadastrar)
label_cadastro_result = CTkLabel(master=frame, text="", font=("Roboto", 12))

button_criar_conta = CTkButton(master=frame, text="Criar uma nova conta", width=300, command=abrir_tela_cadastro)
button_criar_conta.place(x=25, y=320)

button_voltar = CTkButton(master=frame, text="Voltar ao Login", width=300, command=voltar_tela_login)

janela.mainloop()
