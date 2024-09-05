from character import choice_players, register_player
from game import game

def home(user, db):
    while True:
        print(f'Bem vindo, {user.name}!\n1 - Escolher personagem\n2 - Criar novo personagem\n3 - Deslogar')
        choice = input(': ')
        
        if choice == '1':
            chosen_player = choice_players(user, db)
            if chosen_player:
                print(f'Você escolheu o personagem {chosen_player.name}.')
                return game(chosen_player, user)  # Passe chosen_player e user para game
        elif choice == '2':
            register_player(db)
        elif choice == '3':
            print('Deslogando...')
            break
        else:
            print('Opção inválida. Tente novamente.')

