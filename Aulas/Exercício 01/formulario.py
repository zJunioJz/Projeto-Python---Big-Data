import re

def validar_email(email):

    padrao = r'^\w+([\.-]?\w+)*@\w+([\w.-]?w+)*(\.\w{2,3})+$'

    if re.match(padrao, email):
        return True
    else:
        return False

exemplos_emails = ["usuario@email.com", "outro@email.co.uk", "invalido@.com", "sem_arroba.com"]

for email in exemplos_emails:
    if validar_email(email):
        print(f"{email} é um endereço de e-mail válido.")
    else:
        print(f"{email} não é um endereço de e-mail válido.")