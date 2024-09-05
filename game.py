from models import *
from history import history
from dungeon import start_dungeon
from lobby import lobby
from art import text2art
from colorama import *

def game(player, user):
    try:
        title = text2art(f"Bem-vindo, {player.name}!")
        print(f'{Fore.CYAN}{title}{Style.RESET_ALL}')
        print(f'Iniciando o jogo com o personagem {player.name}, do usuário {user.name}.')

        while True:
            choice_player = input('Para onde deseja ir:\n1 - História\n2 - Dungeon\n3 - PVP\n4 - Sair\n: ')
            if choice_player == '1':
                print(f"Entrando no modo História com {player.name}")
                return history(player)  # Verifique se `history` está retornando ao ponto correto
            elif choice_player == '2':
                print(f"Entrando na Dungeon com {player.name}")
                return start_dungeon(player, user)  # Verifique se `start_dungeon` retorna corretamente
            elif choice_player == '3':
                print(f"Entrando no modo PVP (lobby) com {player.name}")
                return lobby(player)  # Verifique se `lobby` está retornando corretamente
            elif choice_player == '4':
                print("Saindo do jogo.")
                exit()
            else:
                print('Digite 1, 2, 3 ou 4...\n')
    
    except User.DoesNotExist:
        print("Usuário não encontrado. Autenticação falhou.")
    except Player.DoesNotExist:
        print("O personagem selecionado não pertence ao usuário autenticado ou não existe.")
    except Exception as e:
        print(f"Ocorreu um erro ao iniciar o jogo: {e}")
        # Adicionar mais detalhes sobre o erro para depuração
        print(f"Detalhes do erro: {str(e)}")
        raise  # Levantar o erro novamente para ver no traceback completo, se necessário
