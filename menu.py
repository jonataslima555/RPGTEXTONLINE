from user import login_user, register_user
from os import system
from art import text2art
from colorama import *
from config import db
def menu():
    while True:
        system('cls')
        title = text2art("Bem Vindo!")
        print(f'{Fore.CYAN}{title}{Style.RESET_ALL}')
            
        print('1 - Fazer login\n2 - Criar conta\n3 - Sair\n')
        user_choice = input(': ')
            
        if user_choice == '1':
            login_user(db)  # Remove o return para não sair do loop
        elif user_choice == '2':
            register_user()  # Remove o return para não sair do loop
        elif user_choice == '3':
            print('Saindo...')
            exit()
        else:
            print('Digite 1, 2 ou 3...')
            # O menu continuará sendo exibido após cada ação
