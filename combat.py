import json
import random
import subprocess
from saveload import *

def cleaning():
    subprocess.run("cls", shell=True)

with open("items.json", "r", encoding="utf-8") as thingamajing:
    items = json.load(thingamajing)

with open("languages.json", "r", encoding="utf-8") as thingy:
    lang = json.load(thingy)

with open("skills.json", "r", encoding="utf-8") as skill:
    skills = json.load(skill)

with open("enemies.json", "r", encoding="utf-8") as enemies:
    enemis = json.load(enemies)

with open("party.json", "r", encoding="utf-8") as part:
    parte = json.load(part)


class Combatant:
    def __init__(self, chara, isplayer):

        self.chara = chara
        self.defe = chara["defe"]
        self.stre = chara["stre"]
        self.speed = chara["speed"]
        self.status =  "Normal"
        self.isplayer = isplayer

def combatpeople(init_stats):
    
    results = []
    for member in init_stats["party"]:
        results.append(Combatant(member, isplayer=True))

    return results

def combatenemies(enemis, enemy_id):
    enemiespr = []
    for enemy in enemy_id:
        enemiespr.append(Combatant(enemis[str(enemy)].copy(), isplayer=False))

    return enemiespr