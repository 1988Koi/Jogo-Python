import json
import random
import subprocess
import time
import copy
from saveload import *
from combat import *

def cleaning():
    subprocess.run("cls", shell=True)

with open("languages.json", "r", encoding="utf-8") as thingy:
    lang = json.load(thingy)

with open("items.json", "r", encoding="utf-8") as thingamajing:
    items = json.load(thingamajing)

with open ("skills.json", "r", encoding="utf-8") as skill:
    skills = json.load(skill)

with open("enemies.json", "r", encoding="utf-8") as enemies:
    enemis = json.load(enemies)

with open ("party.json", "r", encoding="utf-8") as part:
    parte = json.load(part)

def mape():
    with open("map.json", "r", encoding="utf-8") as map1:
        map2 = json.load(map1)
        return map2

def byework(character, new_class, statusclass, items):
    if not character.get("is_main_character",  False):
        print(f"{character['name']} can't change jobs.")
        return False
    
    if new_class not in character["unlocked_classes"]:
        print("You haven't unlocked that job yet!")
        return False

    if new_class == character["class"]:
        print("You are already on that job!")

    base = statusclass[new_class]
    character["class"] = new_class

    character["maxhp"] = base["maxhp"] + character["bonus_hp"]
    character["hp"] = min(character["maxhp"], character["hp"])
    character["maxmana"] = base["maxmana"] + character["bonus_mana"]
    character["mana"] = min(character["maxmana"], character["mana"])
    character["stre"] = base["stre"] + character["bonus_stre"]
    character["luck"] = base["luck"] + character["bonus_luck"]
    character["speed"] = base["speed"]

    if character["eq_wep"] != "Fists" and character["class"] not in items[character["eq_wep"]]["usableby"]:
        print(f"Your {character['eq_wep']} can't be used as a {new_class}, switching to Fists")
        character["eq_wep"] = "Fists"

    print(f"{character['name']} is now a {new_class}!")
    return True


def dungeon(enemy_pool, boss_id):
    total_room = random.randint(5, 15)
    events = ["enemy", "chest", "break", "echest"]
    event_probability = [60, 20, 19, 1]

    bossroom = total_room - 1
    dung_path = random.choices(events, weights=event_probability, k=bossroom)

    
    pracehorder = (lang[language1]["dungen"])
    actualprint = pracehorder.replace("{total_rooms}", str(total_room))
    print(actualprint)

    currentroom = 1

    for event in dung_path:
        print (f"\n Room {currentroom}")

        if event == "enemy":
            cleaning()
            print(lang[language1]["enemye"])
            num_enemies = random.randint(1, 3)
            select_enemy_id = random.choices(enemy_pool, k=num_enemies)
            sucess = combat1(init_stats, select_enemy_id, enemis, lang, language1, skills, items)

            if not sucess:
                return

        elif event == "chest":
            cleaning()
            print(lang[language1]["chest"])
        elif event == "break":
            cleaning()
            print (lang[language1]["break"])
            for member in init_stats["party"]:
                member["hp"] = member["maxhp"]
                member ["mana"] = member["maxmana"]
        elif event == "echest":
            cleaning()
            print (lang[language1]["echest"])

        currentroom += 1

    print ("A boss spawned!")
    sucess = combat1(init_stats, [boss_id], enemis, lang, language1, skills, items, can_flee=False)
    if not sucess:
        return
    


print ("Welcome to the game! / bienvenue á la jeux! / Bem vindo ao jogo!")
print ("Select your language / Choisissez votre language / Escolha seu idioma")
print ("en for english / fr vers français / pt para português.")

language1 = input("> ").strip().lower()
if language1 not in lang:
    print ("Language not in database or you wrote it wrong, oh well, english it is!")
    language1 = "en"
print("\n" + lang[language1]["loadgame"] + "\n" + lang[language1]["newgame"])
begin1 = input("> ").strip().lower()
if begin1 == "2":
    init_stats = {
        "party": [
            {
                "name" : "name",
                "class" : "class",
                "maxhp" : 10,
                "hp" : 10,
                "mana" : 3,
                "maxmana" : 3,
                "stre" : 1,
                "luck" : 1,
                "inv" : {},
                "xp" : 0,
                "defe" : 3,
                "lvl" : 1,
                "xptotal" : 0,
                "status" : "Normal",
                "bleed_turns" : 0,
                "bleed_damage" : 0,
                "boostdef" : 0,
                "pts" : 0,
                "eq_wep" : "Fists",
                "peoplerec":  0,
                "speed" : 0,
                "bonus_stre" : 0,
                "bonus_hp" : 0,
                "bonus_mana" : 0,
                "bonus_luck" : 0,
                "unlocked_classes": [],
                "isplayer" : True,
                "is_main_character" : True,
                "last_def_boost" : 0,
                "taunt_turns": 0,
                "money" : 50,
            }
        ]
    }
    print("\n" + lang[language1]["nameusr"])
    name1 = input("> ").strip()

    init_stats["party"][0]["name"] = name1
    save(init_stats)

    acceptedclass = {
            "1" : "Host",
            "2" : "Yakuza",
            "3" : "Security",
            "4" : "Foreman",
            "5" : "Chef",
            "6" : "Breaker",
            "7" : "Hero"
        }
    
    statusclass = {
        "Host" :      {"hp": 6,  "maxhp": 6,  "mana": 16, "maxmana": 16, "stre": 3, "luck": 6, "speed": 8,  "defe": 0},
        "Yakuza" :    {"hp": 16, "maxhp": 16, "mana": 8,  "maxmana": 8,  "stre": 8, "luck": 3, "speed": 5,  "defe": 3},
        "Security" :  {"hp": 8,  "maxhp": 8,  "mana": 8,  "maxmana": 8,  "stre": 9, "luck": 3, "speed": 6,  "defe": 2},
        "Foreman" :   {"hp": 28, "maxhp": 28, "mana": 5,  "maxmana": 5,  "stre": 5, "luck": 0, "speed": 3,  "defe": 8},
        "Chef" :      {"hp": 11, "maxhp": 11, "mana": 18, "maxmana": 18, "stre": 3, "luck": 6, "speed": 6,  "defe": 2},
        "Breaker" :   {"hp": 8,  "maxhp": 8,  "mana": 6,  "maxmana": 6,  "stre": 6, "luck": 3, "speed": 12, "defe": 1},
        "Hero" :      {"hp": 11, "maxhp": 11, "mana": 11, "maxmana": 11, "stre": 6, "luck": 5, "speed": 7,  "defe": 3},
        "Freelancer": {"hp": 8,  "maxhp": 8,  "mana": 4,  "maxmana": 4,  "stre": 3, "luck": 2, "speed": 4,  "defe": 1},
    }

    classlvlreq = {
        "Host": 2,
        "Yakuza": 5,
        "Security" : 3,
        "Foreman" : 2,
        "Chef" : 4,
        "Breaker" : 3,
        "Hero" : 1,
        "Freelancer" : 0,
    }


    init_stats["party"][0]["class"] = "Freelancer"

    chosenclass = init_stats["party"][0]["class"]
    classst = statusclass[chosenclass]

    init_stats["party"][0]["hp"] = classst["hp"]
    init_stats["party"][0]["maxhp"] = classst["maxhp"]
    init_stats["party"][0]["mana"] = classst["mana"]
    init_stats["party"][0]["maxmana"] = classst["maxmana"]
    init_stats["party"][0]["stre"] = classst["stre"]
    init_stats["party"][0]["luck"] = classst["luck"]
    init_stats["party"][0]["speed"] = classst["speed"]
    init_stats["party"][0]["defe"] = classst["defe"]
    init_stats["party"][0]["unlocked_classes"] = [chosenclass]
    save(init_stats)
else:
    init_stats = load()
    print("Game loaded.")
playerlvl = init_stats["party"][0]["lvl"]
map_data = mape()
playerOV = init_stats["party"][0]
player_itemOV = list(playerOV["inv"].keys())

in_map = True
while in_map:

    print("\n" + lang[language1]["map1"])
    mapc = input("> ").strip()
    
    if mapc == "0":
        save(init_stats)
        print(lang[language1]["bye"])
        exit()
    elif mapc == "1":
        if playerlvl >= 1:
            print("You enter the cafe...")
            print("You grab a menu")
            print("10 dollars for some french fries?????")
            out = False
            while not out == True:
                print("1. Burger with soda - 30 Dollars - Restores 15 health")
                print("2. French fries - 10 dollars - restores 5 health")
                print("3. Soda - 5 dollars - restores 2 health")
                print("Type i to quit.")
                choice = input ("> ").strip()
                menu = {
                    "1" : "Burger with soda",
                    "2" : "French Fries",
                    "3" : "Soda",
                    "i" : "leave"
                    }
                
                menuchoices = {
                    "Burger with soda" : {"heal": 15, "cost": 30},
                    "French Fries" : {"heal": 5, "cost": 10},
                    "Soda" : {"heal": 2, "cost": 5}
                }
                if choice == "i":
                    out = True
                    break
                if choice not in menu:
                    print("We don't serve that here")
                    continue
                elif choice in menu:
                    food_name = menu[choice]
                    food_stats = menuchoices[food_name]
                    for names in init_stats["party"]:
                        print(f"{names['name']}")
                    print("Who do you want to feed?")
                    feed = input("> ").strip()
                    for member in init_stats["party"]:
                        if member['name'].lower() == feed.lower():
                            if init_stats["party"][0]["money"] < food_stats["cost"]:
                                print("You can't buy that!")
                                break
                            else:
                                member["hp"] = min(member["maxhp"], member["hp"] + food_stats["heal"])
                                init_stats["party"][0]["money"] -= food_stats["cost"]


        else:
            print("\n" + lang[language1]["lowlv"])
    elif mapc == "2":
        if playerlvl >= 10:
            print("\n" + lang[language1]["inaid"])
        else: 
            print("\n" + lang[language1]["lowlv"])
    elif mapc == "3":
        if playerlvl >= 5:
            print("")
        else:
            print("\n" + lang[language1]["lowlv"])
    elif mapc == "4":
        if playerlvl >= 3:
            if any(member["name"] == "Gordon" for member in init_stats["party"]):
                print("How about a beer?")
            else:
                print("You drink a little bit of beer, before you hear a man grumbling to himself")
                time.sleep(2)
                print("You decide to ask him what happened")
                time.sleep(2)
                print("After some time talking you realized he also worked for the same company you got fired from")
                print("You explain how you know they are corrupt and how you want to take revenge.")
                print("He thinks you are insane")
                time.sleep(5)
                print(".")
                time.sleep(1)
                print("..")
                time.sleep(1)
                print("...")
                time.sleep(2)
                print("But he joins your party.")
                print("Gordon Joined the Party!")
                new_member = apply_defaults(copy.deepcopy(parte["gordon"]))
                init_stats["party"].append(new_member)
                init_stats["party"][0]["peoplerec"] += 1
        else:
            print("How your level < than 1?")

    elif mapc == "5":
        cleaning()
        combat1(init_stats, [3], enemis, lang, language1, skills, items)
    elif mapc == "6":
        dungeon([4, 5, 2, 3], 29)
    elif mapc == "i":
        player_itemOV = list(playerOV["inv"].keys())
        weaponlist = []
        closeinv = False
        for i in player_itemOV:
            print("\n to close inventory type I")
            currentitem = items[i]
            if currentitem["type"] == "weapon":
                weaponlist.append(i)
        while not closeinv:
            for i, itemname in enumerate(weaponlist):
                count = playerOV["inv"][itemname]
                print(f"{i}: {itemname}(x{count})")
            choice = input("> ").strip()

            if choice == "i":
                closeinv = True
                continue

            elif choice.isdigit():
                idx = int(choice)
                if 0 <= idx < len(weaponlist):
                    item_name = weaponlist[idx]
                    weapon = items[item_name]
                    if playerOV["class"] not in weapon["usableby"]:
                        print(f"{playerOV['name']} the {playerOV['class']} can't use {item_name}")
                    else:
                        playerOV["eq_wep"] = item_name
                        print(f"You equipped {playerOV['eq_wep']}")

    elif mapc == "p":
        currentslot = 0
        onpts = True
        while onpts == True:
            print("Choose what you want to upgrade")
            active = init_stats["party"][currentslot]
            print(f"You are currently upgrading {active['name']}")
            print(f"You currently have {active['pts']} points")
            print(f"You currently have {active['xptotal']} out of 100 for the next point")
            print(lang[language1]["upgrade"])
            choice = input("> ").strip()
            if choice == "d":
                currentslot = (currentslot + 1) % len(init_stats["party"])
            if choice == "a":
                currentslot = (currentslot - 1) % len(init_stats["party"])
            if choice == "o":
                break
            if choice == "1" and active["pts"] > 0:
                print("You upgraded strength!")
                active["pts"] -= 1
                active["bonus_stre"] += 1
                active["stre"] += 1
            elif choice == "2" and active["pts"] > 0:
                print("You upgraded HP!")
                active["pts"] -= 1
                active["bonus_hp"] += 1
                active["maxhp"] += 1
                active["hp"] += 1
            elif choice == "3" and active["pts"] > 0:
                print("You upgraded luck!")
                active["pts"] -= 1
                active["bonus_luck"] += 1
                active["luck"] += 1
            elif choice == "4" and active["pts"] > 0:
                print("You upgraded mana!")
                active["pts"] -= 1
                active["bonus_mana"] += 1
                active["maxmana"] += 1
                active["mana"] += 1

    elif mapc == "j" :
        if playerlvl < 4:
            print("Level too low")
        else:
            unlocked = playerOV["unlocked_classes"]
            print("Choose your job")
            for i, job in enumerate(unlocked, start=1):
                marker = " (current)" if job == playerOV["class"] else ""
                print(f"{i}: {job}{marker}")

            choice = input("> ").strip()
            if choice.isdigit() and 0 < int(choice) <= len(unlocked):
                byework(playerOV, unlocked[int(choice) - 1], statusclass, items)
            else:
                print("Invalid choice!")