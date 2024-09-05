from models import User, Player
from config import db
from bcrypt import checkpw, hashpw, gensalt
from os import system
from art import text2art
from colorama import *
from navigation import home  # Alteração: importando home de navigation.py

tw = '---------------------'

def create_user(name, password, email):
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
        return

def register_user():
    name = input(f'{tw}\nDigite seu nome\n{tw}\n:')
    password = input(f'{tw}\nDigite sua senha\n{tw}\n:')
    email = input(f'{tw}\nDigite seu email\n{tw}\n:')
    create_user(name, password, email)

def create_player(user, name, class_player):
    try:
        with db.atomic():
            Player.create(
                user=user,  # Usando diretamente o objeto User
                name=name,
                class_player=class_player,
            )
        print(f'{tw}\nPersonagem {name} criado com sucesso!\n{tw}')
    except Exception as e:
        print(f'{tw}\nErro ao criar o personagem: {e}\n{tw}')
    finally:
        return home(user)

def register_player():
    system('cls')
    title = text2art("Criar Conta")
    print(f'{Fore.GREEN}{title}{Style.RESET_ALL}')
    email = input('Digite seu email: ')
    name = input('Nome do personagem: ')
    class_player = int(input("Classe do personagem:\n1 - Mago\n2 - Guerreiro\n3 - Ladino\n: "))
    
    user = User.get(User.email == email)  # Obtenha o objeto User aqui
    create_player(user, name, class_player)  # Passe o objeto User

def login_user(db):
    system('cls')
    title = text2art("Login")
    print(f'{Fore.GREEN}{title}{Style.RESET_ALL}')

    email = input("Digite seu email: ")
    password_attempts = 0
    
    try:
        user = User.get(User.email == email)
    except User.DoesNotExist:
        print(f'---------------------\nUsuário não encontrado com o email: {email}\n---------------------')
        exit()
    
    while password_attempts < 3:
        password = input('Digite sua senha: ')
    
        if checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            system('cls')
            print(f'{tw}\nLogin bem-sucedido!\n{tw}')
            return home(user, db)  # Passa o db como argumento
        else:
            system('cls')
            print('Senha incorreta. Tente novamente.')
            password_attempts += 1

    print(f'{tw}\nMuitas tentativas falhadas. Retornando ao menu...\n{tw}')
    exit()

def choice_players(email):
    try:
        user = User.get(User.email == email)
        players = Player.select().where(Player.user == user)
        
        class_names = {1: 'Mage', 2: 'Warrior', 3: 'Rogue'}  # Mapear os IDs para os nomes das classes
        
        if players.exists():
            system('cls')
            print(f'{tw}\nPersonagens do usuário {user.name}:\n{tw}')
            for player in players:
                # Obter o nome da classe a partir do dicionário
                class_name = class_names.get(player.class_player, 'Unknown')
                
                # Exibir as informações do personagem
                print(f'ID: {player.id}, Nome: {player.name}, Classe: {class_name}, Nível: {player.level}, XP: {player.xp}, Vida: {player.health}, Dano: {player.damage}')
                print(f'Dungeons completadas: {player.dungeons_complets}, Gold: {player.gold}')
                print(tw)
            
            chosen_id = input('Digite o ID do personagem que você deseja escolher: ')
            chosen_player = Player.get_or_none(Player.id == chosen_id)

            # Verifica se o personagem escolhido pertence ao usuário autenticado
            if chosen_player and chosen_player.user == user:
                system('cls')
                print(f'{tw}\nVocê escolheu o personagem {chosen_player.name}!\n{tw}')
                return chosen_player  # Retorna o personagem escolhido
            else:
                print(f'{tw}\nID de personagem inválido ou o personagem não pertence a você. Voltando ao menu inicial.\n{tw}')
                return home(user)
        else:
            print(f'{tw}\nNenhum personagem encontrado para o usuário {user.name}.\n{tw}')
            return None

    except User.DoesNotExist:
        print(f'{tw}\nUsuário com o e-mail {email} não encontrado.\n{tw}')
        return None
    
    except Exception as e:
        print(f'{tw}\nErro ao exibir personagens: {e}\n{tw}')
        return None


# Importação de `home` no `navigation.py` evita o ciclo de importação
