import json
import random
import subprocess
import time
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
    sucess = combat1(init_stats, [boss_id], enemis, lang, language1, skills)
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
                "lvl" : 1,
                "xptotal" : 0,
                "status" : "Normal",
                "pts" : 0,
                "eq_wep" : "Fists",
                "peoplerec":  0,
            }
        ]
    }
    print("\n" + lang[language1]["nameusr"])
    name1 = input("> ").strip()

    init_stats["party"][0]["name"] = name1
    placeholdername = lang[language1]["nameok"]
    actualname = placeholdername.replace("{name}", name1)
    print ("\n" + actualname)
    save(init_stats)

    print("\n" + lang[language1]["class"])
    print("\n" + lang[language1]["classc"])
    classconf = False

    acceptedclass = {
            "1" : "Hobo",
            "2" : "Magician",
            "3" : "Security",
            "4" : "Foreman",
            "5" : "Chef",
            "6" : "Hero"
        }
    
    statusclass = {
        "Hobo" : {"hp" : 8, "mana": 7, "maxmana" : 7, "stre": 3, "luck": 10},
        "Magician" : {"hp" : 7, "mana": 15, "maxmana" : 15, "stre": 2, "luck": 5},
        "Security" : {"hp" : 10, "mana": 3, "maxmana" : 3, "stre": 10, "luck": 3},
        "Foreman" : {"hp" : 30, "mana": 1, "maxmana" : 1, "stre": 4, "luck": 0},
        "Chef" : {"hp" : 7, "mana": 15, "maxmana" : 15, "stre": 3, "luck": 5},
        "Hero" : {"hp" : 8, "mana": 10, "maxmana" : 10, "stre": 5, "luck": 5},
        "Yakuza" : {"hp" : 10, "mana": 7, "maxmana" : 7, "stre": 8, "luck": 2}
    }

    while not classconf:

        class1 = input("> ").strip().lower()
        if class1 not in acceptedclass:
            print("\n" + lang[language1]["classno"])
            continue

        placeholderclass = lang[language1]["classok"]
        classname = acceptedclass[class1]
        init_stats["party"][0]["class"] = classname
        actualclass = placeholderclass.replace("{class}", classname)
        print ("\n" + actualclass)
        print("\n" + lang[language1]["sure"])

        conf = input("> ").strip().lower()
        if conf == "1":
            classconf = True
        else:
            print("\n" + lang[language1]["classc"])

    chosenclass = init_stats["party"][0]["class"]
    classst = statusclass[chosenclass]

    init_stats["party"][0]["hp"] = classst["hp"]
    init_stats["party"][0]["mana"] = classst["mana"]
    init_stats["party"][0]["stre"] = classst["stre"]
    init_stats["party"][0]["luck"] = classst["luck"]
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
            print(placeholder)
        else:
            print("\n" + lang[language1]["lowlv"])
    elif mapc == "2":
        if playerlvl >= 10:
            print("\n" + lang[language1]["inaid"])
        else: 
            print("\n" + lang[language1]["lowlv"])
    elif mapc == "3":
        if playerlvl >= 10:
            print("")
        else:
            print("\n" + lang[language1]["lowlv"])
    elif mapc == "4":
        already_recruit = False
        for i in init_stats["party"]:
            if "Gordon" == i["name"]:
                already_recruit = True
                print("How about a beer?")
            if already_recruit == False:
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
                init_stats["party"].append(parte["gordon"])
                init_stats["party"][0]["peoplerec"] += 1

    elif mapc == "5":
        cleaning()
        combat1(init_stats, [3], enemis, lang, language1, skills, items)
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
                item_name = weaponlist[int(choice)]
                item_data = items[item_name]
                playerOV["eq_wep"] = item_name
                print (f"You equipped {playerOV['eq_wep']}!")

    elif mapc == "o":
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
                currentslot += 1
                if currentslot - 1 > 4:
                    currentslot = 0
            if choice == "a":
                currentslot -= 1
                if currentslot - 1 < 0:
                    currentslot = 4
            if choice == "o":
                break
            if choice == "1" and active["pts"] > 0:
                print("You upgraded strenght!")
                active["pts"] -= 1
                active["strenght"] += 1
            elif choice == "2" and active["pts"] > 0:
                print("You upgraded HP!")
                active["pts"] -= 1
                active["maxhp"] += 1
                active["hp"] += 1
            elif choice == "3" and active["pts"] > 0:
                print("You upgraded luck!")
                active["pts"] -= 1
                active["luck"] += 1
            elif choice == "4" and active["pts"] > 0:
                print("You upgraded mana!")
                active["pts"] -= 1
                active["maxmana"] += 1
                active["mana"] += 1