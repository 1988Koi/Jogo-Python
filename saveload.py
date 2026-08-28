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

DEFAULT_MEMBER = {
    "hp": 10,
    "maxhp": 10,
    "mana": 5,
    "maxmana": 5,
    "stre": 1,
    "luck": 1,
    "defe": 0,
    "speed": 5,
    "xp": 0,
    "lvl": 1,
    "xptotal": 0,
    "pts": 0,
    "status": "Normal",
    "bleed_turns": 0,
    "bleed_dmg": 0,
    "boostdef": 0,
    "last_def_boost": 0,
    "taunt_turns": 0,
    "eq_wep": "Fists",
    "eq_head" : "Nothing",
    "eq_accessory" : "Nothing",
    "peoplerec": 0,
    "isplayer": True,
    "money": 50,
    "bonus_stre": 0,
    "bonus_hp": 0,
    "bonus_mana": 0,
    "bonus_luck": 0,
    "is_main_character": False,
    "weakness": [],
    "strong" : [],
    "AttackUp" : 20,
    "AttackUpTurn" : 2,
    "Majima_encounter" : 0,
}

def apply_defaults(member):
    for key, value in DEFAULT_MEMBER.items():
        if key not in member:
            member[key] = value.copy() if isinstance(value, (dict, list)) else value

    if "unlocked_classes" not in member:
        member["unlocked_classes"] = [member.get("class", "Freelancer")]

    return member

def fill_missing_fields(stats):
    party = stats.get("party", [])
    for i, member in enumerate(party):
        apply_defaults(member)

    if party:
        party[0]["is_main_character"] = True
        if "inv" not in party[0]:
            party[0]["inv"] = {}

    return stats


def load():
    with open("save.json", "r", encoding="utf-8") as saves1:
        saves0 = json.load(saves1)
    saves0 = fill_missing_fields(saves0)
    return saves0
    
def save(stats):
    with open("save.json", "w", encoding="utf-8") as saves2:
        json.dump(stats, saves2)