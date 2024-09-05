from decimal import Decimal




def calculate_max_damage(player):
    # Definir o dano base para cada classe
    base_damage = 0

    if player.class_player == 1:  # Mago
        base_damage = 20
    elif player.class_player == 2:  # Guerreiro
        base_damage = 15
    elif player.class_player == 3:  # Ladino
        base_damage = 10

    # O dano máximo é baseado no nível do jogador
    max_damage = base_damage + (player.level * 5)
    return max_damage


def calculate_max_health(player):
    # Definir a vida base para cada classe
    base_health = 100
    health_per_level = 0

    if player.class_player == 1:  # Mago
        health_per_level = 5
    elif player.class_player == 2:  # Guerreiro
        health_per_level = 15
    elif player.class_player == 3:  # Ladino
        health_per_level = 3

    # Vida máxima é baseada no nível atual
    max_health = base_health + (health_per_level * (player.level - 1))
    return max_health






def calculate_xp(player, enemy):
    # Cálculo de XP
    xp_gain = Decimal((enemy.level * enemy.damage) / 5)
    print(f'Você ganhou {xp_gain} de XP derrotando {enemy.name}!')

    # Cálculo de gold
    gold_gain = Decimal((enemy.level * 5) / 5)
    print(f'Você ganhou {gold_gain} de ouro derrotando {enemy.name}!')

    # Adicionando o XP e o ouro ao jogador
    player.xp += xp_gain
    player.gold += gold_gain  # Agora o gold_gain é Decimal

    # Salvando o progresso do jogador no banco de dados
    player.save()

    # Verificar se o jogador atingiu o XP necessário para subir de nível
    level_up(player)


def level_up(player):
    while player.xp >= 100:  # Certificando-se de que pode haver múltiplos níveis ganhos
        player.xp -= 100
        player.level += 1
        
        # Aumentar atributos baseado na classe do jogador
        if player.class_player == 1:  # Mago
            player.health += 5
            player.damage += 15
        elif player.class_player == 2:  # Guerreiro
            player.health += 15
            player.damage += 5
        elif player.class_player == 3:  # Ladino
            player.health += 3
            player.damage += 20
        
        print(f'Parabéns! Você subiu para o nível {player.level}.')
    
    # Salvar o progresso do jogador após o level up
    player.save()
