import json
import random
import subprocess
from saveload import *
from combat import *

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
            print(lang[language1]["enemye"])
            sucess = combat1(init_stats, enemy_pool, enemis, lang, language1, skills)

            if not sucess:
                break
        elif event == "chest":
            print(lang[language1]["chest"])
        elif event == "break":
            print (lang[language1]["break"])
            for member in init_stats["party"]:
                member["hp"] = member["maxhp"]
                member ["mana"] = member["maxmana"]
        elif event == "echest":
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
        "peoplerec":  0,
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
                "inv" : "inv",
                "xp" : 1,
                "lvl" : 0,
                "pts" : 0
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
            "5" : "Chef"
        }
    
    statusclass = {
        "Hobo" : {"hp" : 8, "mana": 7, "maxmana" : 7, "stre": 3, "luck": 10},
        "Magician" : {"hp" : 7, "mana": 15, "maxmana" : 15, "stre": 2, "luck": 5},
        "Security" : {"hp" : 10, "mana": 3, "maxmana" : 3, "stre": 10, "luck": 3},
        "Foreman" : {"hp" : 30, "mana": 1, "maxmana" : 1, "stre": 4, "luck": 0},
        "Chef" : {"hp" : 7, "mana": 15, "maxmana" : 15, "stre": 3, "luck": 5}
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

in_map = True
while in_map:

    print("\n" + lang[language1]["map1"])
    mapc = input("> ")
    
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
        dungeon([1, 2, 3], 29)
