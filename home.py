# home.py

import tkinter as tk

def logout_and_open_login_window(current_window):
    current_window.destroy()  
    import Login  # Importar o módulo de login
    Login.janela.deiconify()  # Tornar visível a janela de login

def home():
    nova_janela = tk.Tk()
    nova_janela.geometry("1080x720")
    nova_janela.title("Tela Home")

    label = tk.Label(nova_janela, text="Bem-vindo à tela Home!", font=("Roboto", 24))
    label.pack(pady=20)

    button_logout = tk.Button(nova_janela, text="Logout", command=lambda: logout_and_open_login_window(nova_janela))
    button_logout.pack(pady=10)

    nova_janela.mainloop()


# Login.py (Modificar a parte do login)

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
                    
                janela.withdraw()  # Ocultar a janela de login
                home()  # Abrir a tela home

            else:
                label_result.configure(text="Senha incorreta", text_color="red")
        else:
            label_result.configure(text="Nome de usuário não encontrado", text_color="red")

        conn.close()
    else:
        label_result.configure(text="Preencha todos os campos", text_color="red")
        label_result.place(x=25, y=75)  
