import json
import random
import subprocess

def cleaning():
    subprocess.run("cls", shell=True)

with open("languages.json", "r", encoding="utf-8") as thingy:
    lang = json.load(thingy)

with open ("skills.json", "r", encoding="utf-8") as skill:
    skills = json.load(skill)

with open("enemies.json", "r", encoding="utf-8") as enemies:
    enemis = json.load(enemies)

with open ("party.json", "r", encoding="utf-8") as part:
    parte = json.load(part)


def load():
    with open("save.json", "r", encoding="utf-8") as saves1:
        saves0 = json.load(saves1)
        return saves0
    
def save(stats):
    with open("save.json", "w", encoding="utf-8") as saves2:
        json.dump(stats, saves2)