from peewee import Model, CharField, ForeignKeyField, DecimalField, TextField, BooleanField, IntegerField
from config import db
import json
import os

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    name = CharField()
    password = CharField()
    email = CharField(unique=True)

class Player(BaseModel):
    user = ForeignKeyField(User, backref='players')
    name = CharField(unique=True)
    health = DecimalField(default=100)
    damage = DecimalField(default=15)
    level = IntegerField(default=1)
    xp = DecimalField(default=0)
    class_player = IntegerField()  # 1 Mage - 2 Warrior - 3 Rogue
    dungeons_complets = IntegerField(default=0)  # Número de dungeons concluídas
    gold = DecimalField(default=0)  # Quantidade de ouro do jogador

class Item(BaseModel):
    name = CharField()
    descr = TextField()
    effect = IntegerField() # 1 Damage booster - 2 Health booster - 3 - Dodge booster
    effect_value = DecimalField() # +5 de dano - 5+ vida e etc
    type = IntegerField() # 1 - Armor - 2 Sword - 3 Staff

class Inventory(BaseModel):
    player = ForeignKeyField(Player, backref='inventory')
    item = ForeignKeyField(Item, backref='inventories')
    quantity = IntegerField(default=20)

class EquippedItems(BaseModel):
    player = ForeignKeyField(Player, backref='equipped_items')
    item = ForeignKeyField(Item, backref='equipped_by')
    slot_armor = BooleanField(default=False)  # True if equipped in armor slot
    slot_sword = BooleanField(default=False)  # True if equipped in sword slot
    slot_staff = BooleanField(default=False)  # True if equipped in staff slot

class Enemy(BaseModel):
    name = CharField()
    health = DecimalField(default=20) # De acordo com o level aumenta
    damage = DecimalField(default=10) # De acordo com o level aumenta / 3
    level = IntegerField(default=1)
    descr = TextField()

class Dungeon(BaseModel):
    level_required = IntegerField()

class DungeonEnemy(BaseModel):
    dungeon = ForeignKeyField(Dungeon, backref='dungeon_enemies')
    enemy = ForeignKeyField(Enemy, backref='enemy_dungeons')

class Quest(BaseModel):
    name_quest = CharField()
    gold = DecimalField(default=50)
    level_quest = IntegerField()
    descr_quest = TextField()

class PlayerQuest(BaseModel):
    player = ForeignKeyField(Player, backref='player_quests')
    quest = ForeignKeyField(Quest, backref='quest_players')
    status = BooleanField(default=False)

class Bank(BaseModel):
    player = ForeignKeyField(Player, backref='bank_items')
    slot_items = IntegerField()

with db.atomic():
    db.create_tables([
        User, Player, Item,
        Inventory, EquippedItems,
        Enemy, Dungeon, DungeonEnemy,
        Quest, PlayerQuest, Bank
    ])

def load_monsters_from_json(file_name):
    base_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_path, file_name)
    
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

# Carrega os arquivos JSON usando caminhos relativos
load_monsters_from_json("fantasy_monsters.json")
load_monsters_from_json("monstros.json")
