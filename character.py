from models import Player, User
from os import system
from art import text2art
from colorama import *

tw = '---------------------'

def create_player(user, name, class_player, db):
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
        return None  # Ou outro retorno apropriado

def register_player(db):
    system('cls')
    title = text2art("Criar Personagem")
    print(f'{Fore.GREEN}{title}{Style.RESET_ALL}')
    email = input('Digite seu email: ')
    name = input('Nome do personagem: ')
    class_player = int(input("Classe do personagem:\n1 - Mago\n2 - Guerreiro\n3 - Ladino\n: "))
    
    user = User.get(User.email == email)  # Obtenha o objeto User aqui
    create_player(user, name, class_player, db)  # Passe o objeto User

def choice_players(user, db):
    try:
        players = Player.select().where(Player.user == user)
        
        class_names = {1: 'Mage', 2: 'Warrior', 3: 'Rogue'}  # Mapear os IDs para os nomes das classes
        
        if players.exists():
            system('cls')
            print(f'{tw}\nPersonagens do usuário {user.name}:\n{tw}')
            for player in players:
                class_name = class_names.get(player.class_player, 'Unknown')
                print(f'ID: {player.id}, Nome: {player.name}, Classe: {class_name}, Nível: {player.level}, XP: {player.xp}, Vida: {player.health}, Dano: {player.damage}')
                print(f'Dungeons completadas: {player.dungeons_complets}, Gold: {player.gold}')
                print(tw)
            
            chosen_id = input('Digite o ID do personagem que você deseja escolher: ')
            chosen_player = Player.get_or_none(Player.id == chosen_id)

            if chosen_player and chosen_player.user == user:
                system('cls')
                print(f'{tw}\nVocê escolheu o personagem {chosen_player.name}!\n{tw}')
                return chosen_player  # Retorna o personagem escolhido
            else:
                print(f'{tw}\nID de personagem inválido ou o personagem não pertence a você.\n{tw}')
                return None
        else:
            print(f'{tw}\nNenhum personagem encontrado para o usuário {user.name}.\n{tw}')
            return None

    except Exception as e:
        print(f'{tw}\nErro ao exibir personagens: {e}\n{tw}')
        return None
