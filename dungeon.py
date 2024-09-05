from models import Player, Dungeon, Enemy, DungeonEnemy, db
from peewee import fn
import random
from os import system
from level_logic import calculate_xp, calculate_max_health, calculate_max_damage
from colorama import Fore, Style, init
from art import text2art
from decimal import Decimal
from time import sleep

# Inicializar o colorama
init(autoreset=True)

tw = f'{Fore.CYAN}---------------------{Style.RESET_ALL}'


def get_balanced_enemies(player_level):
    enemies = Enemy.select().where((Enemy.level > player_level) & (Enemy.level <= player_level + 5)).order_by(fn.Random()).limit(10)
    
    if not enemies.exists():
        empty_monster_name = f"Monstro do Vazio {random.randint(1, 100)}"
        empty_monster_descr = "Um monstro do vazio que surge para matar o jogador"
        empty_monster = Enemy.create(name=empty_monster_name, level=player_level, health=100, damage=20, descr=empty_monster_descr)
        return [empty_monster]
    
    return enemies


def vendedor(player):
    system('cls')
    title = text2art("Vendedor")
    print(f'{Fore.YELLOW}{title}{Style.RESET_ALL}')
    
    print(f'{Fore.GREEN}Bem-vindo, {player.name}! Você pode comprar itens para te ajudar na dungeon.{Style.RESET_ALL}')
    print(f'{Fore.CYAN}1 - Aumento de Dano (50 gold)\n2 - Aumento de Vida (50 gold)\n3 - Sair{Style.RESET_ALL}')
    print(f'{tw}\n{Fore.CYAN}Estatísticas atuais do jogador:{Style.RESET_ALL}\n{tw}')
    print(f'{Fore.GREEN}Vida atual: {player.health}{Style.RESET_ALL}')
    print(f'{Fore.YELLOW}Dano atual: {player.damage}{Style.RESET_ALL}')
    choice = input(f'{tw}\nVocê possui: {player.gold} Gold\n{tw}\nO que você deseja comprar?: ')

    if choice == '1':
        if player.gold >= 50:
            bonus_damage = Decimal(random.randint(2, 5)) / Decimal(100)
            max_damage = calculate_max_damage(player)
            player.damage = max_damage + (max_damage * bonus_damage)
            player.gold -= 50
            player.save()
            print(f'{Fore.GREEN}Você comprou um aumento de dano! Agora seu dano aumentou em {bonus_damage * 100:.2f}%{Style.RESET_ALL}')
        else:
            print(f'{Fore.RED}Você não tem gold suficiente!{Style.RESET_ALL}')
            sleep(2)

    elif choice == '2':
        if player.gold >= 50:
            bonus_health = Decimal(random.choice([50, 100]))
            player.health += bonus_health
            player.gold -= 50
            player.save()
            print(f'{Fore.GREEN}Você comprou um aumento de vida! Agora sua vida aumentou em {bonus_health}{Style.RESET_ALL}')
        else:
            print(f'{Fore.RED}Você não tem gold suficiente!{Style.RESET_ALL}')
            sleep(2)
            
    elif choice == '3':
        print(f'{Fore.CYAN}Até mais!{Style.RESET_ALL}')
        return  # Corrigido para retornar normalmente ao fluxo da batalha

    else:
        print(f'{Fore.RED}Opção inválida, tente novamente.{Style.RESET_ALL}')
        sleep(2)
        vendedor(player)  # Repete a função se houver erro
    
    print(f'{Fore.CYAN}Estatísticas atuais do jogador:{Style.RESET_ALL}')
    print(f'{Fore.GREEN}Vida atual: {player.health}{Style.RESET_ALL}')
    print(f'{Fore.YELLOW}Dano atual: {player.damage}{Style.RESET_ALL}')


def start_dungeon(player, user):  # Adiciona o argumento 'user' à função
    player.health = calculate_max_health(player)
    player.save()
    system('cls')
    print(f'{Fore.GREEN}Vida do jogador resetada: {player.health}{Style.RESET_ALL}')
    
    dungeon = Dungeon.create(level_required=player.level)
    
    enemies = get_balanced_enemies(player.level)
    
    if not enemies:
        print(f"{Fore.RED}Erro: Nenhum inimigo foi encontrado para o nível atual do jogador.{Style.RESET_ALL}")
        from game import game
        return game(player, user)
    
    for enemy in enemies:
        DungeonEnemy.create(dungeon=dungeon, enemy=enemy)
    
    print(f'{tw}\n{Fore.YELLOW}Você entrou na dungeon {dungeon.id}, existem 10 inimigos aqui, boa sorte, não morra.{Style.RESET_ALL}\n{tw}')
    
    battle(player, dungeon, user)


def battle(player, dungeon, user):
    enemies = list(DungeonEnemy.select().where(DungeonEnemy.dungeon == dungeon))
    
    battle_count = 0

    print(f"Entrando na batalha, número de inimigos: {len(enemies)}")
    
    for dungeon_enemy in enemies:
        print(f"{tw}")
        if battle_count == 0 or battle_count % 3 == 0 or battle_count == len(enemies) - 1:
            print("Chamando vendedor...")
            vendedor(player)  # Certifique-se que o vendedor não retorna ao menu de forma inesperada
            print("Retornando do vendedor")

        enemy = dungeon_enemy.enemy
        print(f'{tw}\n{Fore.RED}{enemy.name} apareceu! Ele possui {enemy.health} de vida e {enemy.damage} de ataque.{Style.RESET_ALL}\n{tw}')
        
        # Garantir que o loop de batalha é executado
        while enemy.health > 0 and player.health > 0:
            action = input('1 - Atacar\n2 - Defender\n:')
            print(f"Ação escolhida: {action}")
            if action == '1':
                attack(player, enemy)
            elif action == '2':
                defend(player, enemy)
            else:
                print(f'{Fore.RED}Ação inválida. Escolha 1 ou 2.{Style.RESET_ALL}')
        
        if player.health <= 0:
            print(f'{tw}\n{Fore.RED}Você morreu! Dungeon falhou.{Style.RESET_ALL}\n{tw}')
            sleep(2)
            print("Jogador morreu. Retornando ao lobby")
            from game import game
            return game(player, user)
        
        print(f"Inimigo derrotado: {enemy.name}")
        calculate_xp(player, enemy)
        print(f'{tw}\n{Fore.GREEN}Você derrotou {enemy.name}!\n{Style.RESET_ALL}{tw}')
        print(f'{Fore.CYAN}XP Atual: {player.xp}/100{Style.RESET_ALL}')
        
        battle_count += 1
    
    print(f'{tw}\n{Fore.GREEN}Parabéns, você completou a dungeon {dungeon.id}!{Style.RESET_ALL}\n{tw}')
    complete_dungeon(player, dungeon, user)


def attack(player, enemy):
    system('cls')
    player_damage = player.damage
    print(f'{tw}\n{Fore.GREEN}Você atacou {enemy.name} causando {player_damage} de dano.{Style.RESET_ALL}\n{tw}')
    enemy.health -= player_damage
    
    if enemy.health > 0:
        print(f'{tw}\n{Fore.YELLOW}{enemy.name} tem {enemy.health} de vida restante.{Style.RESET_ALL}\n{tw}')
        enemy_attack(player, enemy)


def defend(player, enemy):
    system('cls')
    print(f'{tw}\n{Fore.CYAN}Você defendeu o ataque de {enemy.name}{Style.RESET_ALL}\n{tw}')
    enemy_attack(player, enemy, defending=True)


def enemy_attack(player, enemy, defending=False):
    damage = enemy.damage / 2 if defending else enemy.damage
    print(f'{Fore.RED}{enemy.name} atacou você causando {damage} de dano.{Style.RESET_ALL}')
    player.health -= damage
    print(f'{tw}\n{Fore.YELLOW}Você tem {player.health} de vida restante.{Style.RESET_ALL}\n{tw}')


def complete_dungeon(player, dungeon):
    player.dungeons_complets += 1
    player.save()
    
    with db.atomic():
        DungeonEnemy.delete().where(DungeonEnemy.dungeon == dungeon).execute()
        dungeon.delete_instance()
    
    print(f'{tw}\n{Fore.GREEN}Dungeon concluída! Você agora completou {player.dungeons_complets} dungeons.{Style.RESET_ALL}\n{tw}')
