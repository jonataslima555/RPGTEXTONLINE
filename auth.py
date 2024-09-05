from models import User
from bcrypt import checkpw, hashpw, gensalt
from os import system
from art import text2art
from colorama import *

tw = '---------------------'

def create_user(name, password, email, db):
    try:
        with db.atomic():
            salt = gensalt()
            hashed = hashpw(password.encode('utf-8'), salt)
            User.create(name=name, email=email, password=hashed)
            system('cls')
            print(f'{tw}\nConta criada com sucesso!\n{tw}')
    except Exception as e:
        print(f'Erro ao criar conta: {e}')
    finally:
        exit()

def register_user(db):
    name = input(f'{tw}\nDigite seu nome\n{tw}\n:')
    password = input(f'{tw}\nDigite sua senha\n{tw}\n:')
    email = input(f'{tw}\nDigite seu email\n{tw}\n:')
    create_user(name, password, email, db)

def login_user(db, home_func):
    system('cls')
    title = text2art("Login")
    print(f'{Fore.GREEN}{title}{Style.RESET_ALL}')
    
    email = input("Digite seu email: ")
    password_attempts = 0
    
    try:
        user = User.get(User.email == email)
    except User.DoesNotExist:
        print(f'{tw}\nUsuário não encontrado com o email: {email}\n{tw}')
        exit()

    while password_attempts < 3:
        password = input('Digite sua senha: ')
    
        if checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            system('cls')
            print(f'{tw}\nLogin bem-sucedido!\n{tw}')
            return home_func(user)
        else:
            system('cls')
            print('Senha incorreta. Tente novamente.')
            password_attempts += 1

    print(f'{tw}\nMuitas tentativas falhadas. Retornando ao menu...\n{tw}')
    exit()
