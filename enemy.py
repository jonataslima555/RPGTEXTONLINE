import json
from models import Enemy
from config import db

def load_monsters_from_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            monsters_data = json.load(f)
        
        with db.atomic():
            for monster in monsters_data['monsters']:
                Enemy.create(
                    name=monster['name'],
                    health=monster['health'],
                    damage=monster['damage'],
                    level=monster['level'],
                    descr=monster['descr']
                )
    except AttributeError as e:
        print(f'Não funcionou... {e}')
    
load_monsters_from_json(r"C:\Users\Pichau\projects\rpg-class-python\monstros.json")

import json

def criar_monstros():
    monstros = []
    nomes = ["Urso Pardo", "Troll das Cavernas", "Esqueleto"]
    descricoes = [
        "Um urso grande e feroz com garras afiadas.",
        "Uma criatura enorme e forte que vive nas profundezas das cavernas.",
        "Restos animados de um guerreiro caído, movidos por magia negra."
    ]

    # Criar 30 monstros de nível 1
    for i in range(30):
        monstro = {
            "name": f"{nomes[i % 3]} {i + 1}",
            "health": 20 + (i % 3) * 2,
            "damage": 5 + (i % 3),
            "level": 1,
            "descr": descricoes[i % 3]
        }
        monstros.append(monstro)
    
    # Criar monstros de nível 2 a 15
    for level in range(2, 16):
        for i in range(30):
            monstro = {
                "name": f"{nomes[i % 3]} {30 * (level - 1) + i + 1}",
                "health": 20 + (level - 1) * 10 + (i % 3) * 2,
                "damage": 5 + (level - 1) * 2 + (i % 3),
                "level": level,
                "descr": descricoes[i % 3]
            }
            monstros.append(monstro)
    
    with open('monstros.json', 'w') as file:
        json.dump({"monsters": monstros}, file, indent=4)

#criar_monstros()