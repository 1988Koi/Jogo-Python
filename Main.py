import copy
import json
import random
import subprocess
import time
from saveload import *
from combat import *
from classdata import statusclass, classlvlreq, Majimaencounters

def cleaning():
    subprocess.run("cls", shell=True)

with open("languages.json", "r", encoding="utf-8") as thingy:
    lang = json.load(thingy)

with open("items.json", "r", encoding="utf-8") as thingamajing:
    items = json.load(thingamajing)

with open("skills.json", "r", encoding="utf-8") as skill:
    skills = json.load(skill)

with open("enemies.json", "r", encoding="utf-8") as enemies:
    enemis = json.load(enemies)

with open("party.json", "r", encoding="utf-8") as part:
    parte = json.load(part)

with open("shops.json", "r", encoding="utf-8") as shope:
    shops = json.load(shope)

with open("chest.json", "r", encoding="utf-8") as cheste:
    chest = json.load(cheste)

with open("recipes.json", "r", encoding="utf-8") as recipese:
    recipes = json.load(recipese)

def mape():
    with open("map.json", "r", encoding="utf-8") as map1:
        map2 = json.load(map1)
        return map2


acceptedclass = {
    "1": "Host",
    "2": "Yakuza",
    "3": "Security",
    "4": "Foreman",
    "5": "Chef",
    "6": "Breaker",
    "7": "Hero",
    "8": "Freelancer",
    "9": "Gentleman",
    "0" : "Dragon",
}

def apply_class_stats(character, new_class):
    base = statusclass[new_class]
    character["class"] = new_class
    character["maxhp"] = base["maxhp"] + character["bonus_hp"]
    character["hp"] = min(character["maxhp"], character["hp"])
    character["maxmana"] = base["maxmana"] + character["bonus_mana"]
    character["mana"] = min(character["maxmana"], character["mana"])
    character["stre"] = base["stre"] + character["bonus_stre"]
    character["luck"] = base["luck"] + character["bonus_luck"]
    character["speed"] = base["speed"]
    character["defe"] = base["defe"]


def byework(character, new_class, statusclass, classlvlreq, items, Majimaencounters):
    if not character.get("is_main_character", False):
        print(f"{character['name']} can't change jobs.")
        return False

    if new_class not in character["unlocked_classes"]:
        print("You haven't unlocked that job yet!")
        return False

    required = Majimaencounters.get(new_class, 0)
    if character["Majima_encounter"] < required:
        print(f"You didn't fight Him, enough times.")
        return False

    if character["lvl"] < classlvlreq[new_class]:
        print(f"You need to be level {classlvlreq[new_class]} to become a {new_class}!")
        return False

    if new_class == character["class"]:
        print("You are already on that job!")
        return False

    apply_class_stats(character, new_class)

    if character["eq_wep"] != "Fists" and character["class"] not in items[character["eq_wep"]]["usableby"]:
        print(f"Your {character['eq_wep']} can't be used as a {new_class}, switching to Fists")
        character["eq_wep"] = "Fists"

    print(f"{character['name']} is now a {new_class}!")
    return True


def cast_out_transition(init_stats, lang, language1):
    cleaning()
    print(lang[language1].get("castout_1", "You go to the docks."))
    time.sleep(2)
    print(lang[language1].get("castout_2", "You wait around, why is no one here?."))
    time.sleep(2)
    print(lang[language1].get("castout_3", "You hear sirens getting closer... and closer..."))
    time.sleep(2)
    print(lang[language1].get("castout_4", "You try to flee..."))
    time.sleep(2)
    print(lang[language1].get("castout_5", "You get shot in the back."))
    time.sleep(2)
    print(".")
    time.sleep(1)
    print("..")
    time.sleep(1)
    print("...")
    time.sleep(2)
    print(lang[language1].get("castout_6", "Someone's dragging you. You're still breathing. Barely."))
    time.sleep(2)

    p = init_stats["party"][0]
    apply_class_stats(p, "Freelancer")
    p["hp"] = p["maxhp"]
    p["mana"] = p["maxmana"]
    p["unlocked_classes"] = ["Freelancer"]
    init_stats["story_flags"]["current_map"] = "someicho"
    init_stats["story_flags"]["chapter"] = 2

    print(lang[language1].get("castout_7", "You are dead to the world now."))
    time.sleep(2)
    print("Chapter 2: At the bottom.")
    time.sleep(3)


def dungeon(enemy_pool, boss_id, init_stats, lang, language1, skills, items, enemis, can_flee=True):
    total_room = random.randint(5, 15)
    events = ["enemy", "chest", "break", "echest"]
    event_probability = [60, 20, 19, 1]

    bossroom = total_room - 1
    dung_path = random.choices(events, weights=event_probability, k=bossroom)

    pracehorder = lang[language1]["dungen"]
    actualprint = pracehorder.replace("{total_rooms}", str(total_room))
    print(actualprint)

    currentroom = 1

    for event in dung_path:
        print(f"\n Room {currentroom}")

        if event == "enemy":
            cleaning()
            print(lang[language1]["enemye"])
            num_enemies = random.randint(1, 3)
            select_enemy_id = random.choices(enemy_pool, k=num_enemies)
            sucess = combat1(init_stats, select_enemy_id, enemis, lang, language1, skills, items, can_flee=can_flee)

            if sucess != True:
                return False

        elif event == "chest":
            cleaning()
            print(lang[language1]["chest"])
            for drop in chest:
                roll = random.random()
                if roll <= drop["chance"]:
                    drop_enemy = drop["itemid"]
                    print(f"You got a {drop_enemy}!")
                    player_inv = init_stats["party"][0]["inv"]
                    if drop_enemy in player_inv:
                        player_inv[drop_enemy] += 1
                    else:
                        player_inv[drop_enemy] = 1
                        print("Debug Backpack:", init_stats["party"][0]["inv"])
        elif event == "break":
            cleaning()
            print(lang[language1]["break"])
            for member in init_stats["party"]:
                member["hp"] = member["maxhp"]
                member["mana"] = member["maxmana"]
        elif event == "echest":
            cleaning()
            print(lang[language1]["echest"])

        currentroom += 1

    if boss_id is None:
        return True

    print("A boss spawned!")
    sucess = combat1(init_stats, [boss_id], enemis, lang, language1, skills, items, can_flee=False)
    return sucess == True


def tutorial_map(init_stats, lang, language1, map_data):
    pool = map_data["tutorial"]["enemy_pool"]
    in_here = True

    while in_here:
        print("\n" + lang[language1].get("tutorial_map",
              "1: Spar with the new guy\n2: Handle the late payment\n3: Head to the handoff"))
        mapc = input("> ").strip()

        if mapc == "1":
            cleaning()
            combat1(init_stats, [pool[0]], enemis, lang, language1, skills, items, can_flee=False)
        elif mapc == "2":
            cleaning()
            combat1(init_stats, [pool[1]], enemis, lang, language1, skills, items, can_flee=False)
        elif mapc == "3":
            cast_out_transition(init_stats, lang, language1)
            return "someicho"
        else:
            print("Invalid choice!")

    return "tutorial"


def someicho_map(init_stats, lang, language1, map_data, playerOV):
    pool = map_data["someicho"]["enemy_pool"]
    boss = map_data["someicho"]["boss"]
    mission1Started = False
    mission1Complete = False
    mission2started = False
    mission2Complete = False
    in_here = True

    while in_here:
        playerlvl = init_stats["party"][0]["lvl"]
        print("\n" + lang[language1]["map1"])
        mapc = input("> ").strip()

        if mapc == "0":
            save(init_stats)
            print(lang[language1]["bye"])
            return "quit"

        elif mapc == "1":
            if playerlvl >= 1 and (mission1Started == False or mission1Complete == True):
                print("You enter the cafe...")
                print("You grab a menu")
                print("10 dollars for some french fries?????")
                out = False
                while not out:
                    print("1. Burger with soda - 30 Dollars - Restores 15 health")
                    print("2. French fries - 10 dollars - restores 5 health")
                    print("3. Soda - 5 dollars - restores 2 health")
                    print("Type i to quit.")
                    choice = input("> ").strip()
                    menu = {
                        "1": "Burger with soda",
                        "2": "French Fries",
                        "3": "Soda",
                        "i": "leave"
                    }

                    menuchoices = {
                        "Burger with soda": {"heal": 15, "cost": 30},
                        "French Fries": {"heal": 5, "cost": 10},
                        "Soda": {"heal": 2, "cost": 5}
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
            elif playerlvl >= 1 and (mission1Started == True and mission1Complete == False):
                print("You enter the cafe...")
                print("You grab a menu")
                print("10 dollars for some french fries?????")
                print("At the corner of your eye you see someone...")
                print("You pull the evnelope with the info")
                print("You see that everything matches perfectly...")
                print("Do you attack him?")
                print("Type y for yes and n for no.")
                choice1 = input("> ").strip()
                if choice1 == "yes" or choice1 == "y":
                    print("You approach the guy...")
                    print("You start discussing with him")
                    time.sleep(2)
                    barpool = [11]
                    select_enemy_id = random.choices(barpool, k=1)
                    combat1(init_stats, select_enemy_id, enemis, lang, language1, skills, items)
                    init_stats["party"][0]["money"] += 10
                elif choice1 == "no" or choice1 == "n":
                    out = False
                    print("You decide that now is not the time.")
                    while not out:
                        print("1. Burger with soda - 30 Dollars - Restores 15 health")
                        print("2. French fries - 10 dollars - restores 5 health")
                        print("3. Soda - 5 dollars - restores 2 health")
                        print("Type i to quit.")
                        choice = input("> ").strip()
                        menu = {
                                "1": "Burger with soda",
                                "2": "French Fries",
                                "3": "Soda",
                                "i": "leave"
                                }
                        menuchoices = {
                                "Burger with soda": {"heal": 15, "cost": 30},
                                "French Fries": {"heal": 5, "cost": 10},
                                "Soda": {"heal": 2, "cost": 5}
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
            if playerlvl >= 5:
                cleaning()
                print("The workshop is cluttered with scrap and half-finished frames.")
                craftable = list(recipes.keys())
                for i, item_name in enumerate(craftable, start=1):
                    recipe = recipes[item_name]
                    mats_str = ", ".join(f"{qty}x {mat}" for mat, qty in recipe["materials"].items())
                    print(f"{i}: {item_name} - needs {mats_str}, {recipe['cost']} money")
                print("Type i to leave")

                choice = input("> ").strip()
                if choice.lower() == "i":
                    pass
                elif choice.isdigit() and 0 < int(choice) <= len(craftable):
                    item_name = craftable[int(choice) - 1]
                    recipe = recipes[item_name]
                    inv = init_stats["party"][0]["inv"]

                    has_materials = all(inv.get(mat, 0) >= qty for mat, qty in recipe["materials"].items())
                    has_money = init_stats["party"][0]["money"] >= recipe["cost"]

                    if has_materials and has_money:
                        for mat, qty in recipe["materials"].items():
                            inv[mat] -= qty
                            if inv[mat] == 0:
                                del inv[mat]
                        init_stats["party"][0]["money"] -= recipe["cost"]
                        inv[item_name] = inv.get(item_name, 0) + 1
                        print(f"You crafted a {item_name}!")
                    elif not has_materials:
                        print("You don't have the materials for that.")
                    else:
                        print("You can't afford that.")
                else:
                    print("Invalid choice!")
            else:
                print("\n" + lang[language1]["lowlv"])

        elif mapc == "3":
            if playerlvl >= 5:
                cleaning()
                combat1(init_stats, [6], enemis, lang, language1, skills, items)
            else:
                print("\n" + lang[language1]["lowlv"])

        elif mapc == "4":
            if playerlvl >= 1:
                already_recruited = any(member["name"] == "Gordon" for member in init_stats["party"])
                if already_recruited and mission1Complete:
                    print("How about a beer?")
                if mission1Complete == False and already_recruited and mission1Started == False:
                    print("The bartender calls you over")
                    print("You approach and he says")
                    print("Hey, you are one of Gordon's friend? \n You nod")
                    print("Look um... I got a... job... for you, if you know what I mean... \n I'll pay nicely.")
                    print("Just take out an old rival of mine, sounds good?")
                    print("Type y for yes and n to no.")
                    print("Suggested level to be: 5")
                    choice = input("> ").strip()
                    if choice == "yes" or choice == "y":
                        print("Good choice kid, here's the info on where to find him and what he looks like.")
                        print("He hands you a envelope containing some places, you are likely to find him at the cafe.")
                        print("Don't kill him, just rough him up real good, ok? And also if he has anything in his person you may have it, I don't care...")
                        mission1Started = True
                    elif choice == "no" or choice == "n":
                        print("That's a shame... if you change your mind you know where to find me.")
                        break
                if mission1Started == True and already_recruited and mission1Complete == True and any(member["name"] == "Kanae" for member in init_stats["party"]):
                    inv = init_stats["party"][0]["inv"]
                    print("Hey, you did pretty good kid, here, your payment \n you got 250 bucks!")
                    init_stats["party"][0]["money"] += 250
                    print("And a little something as a bonus")
                    init_stats["party"][0]["inv"]["Bandana"] = init_stats["party"][0]["inv"].get("Bandana", 0) + 1
                if mission1Complete == True and already_recruited and mission2started == False:
                    print("You enter the bar again")
                    print("The bartender calls you again")
                    print("Hey there... I got another job for you")
                    print("Same deal.")
                    print("You up?")
                    print("Type y for yes and n to no.")
                    print("Suggested level to be: 15")
                    maybe = input("> ").strip()
                    if maybe == "yes" or maybe == "y":
                        print("Great, knew I could count on you, here's the info on where to find him and what he looks like.")
                        print("He hands you a envelope containing some places, you are likely to find him at the club.")
                        print("Don't kill him, just rough him up real good, ok? And also if he has anything in his person you may have it, I don't care...")
                        mission2started = True
                    if mission2Complete == True and already_recruited and mission2started == True:
                        print("Hey, amazing work... say... You've done me a solid 2 times already, why don't I join your little adventure, just tell me what you are doing... \n After some time explaining your story to him he sighs and says \n Alright, that's messed up, I'm in, I'm Philip, nice to meet you.")
                        philip = apply_defaults(copy.deepcopy(parte["philip"]))
                        init_stats["party"].append(philip)
                        init_stats["party"][0]["peoplerec"] += 1
                    elif choice == "no" or choice == "n":
                        print("That's a shame... if you change your mind you know where to find me.")
                        break

                else:
                    print("You drink a little bit of beer, before you hear a man grumbling to himself")
                    time.sleep(2)
                    print("You decide to ask him what happened")
                    time.sleep(2)
                    print("After some time talking you realize he's the one who pulled you out that night")
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
                    gordon = apply_defaults(copy.deepcopy(parte["gordon"]))
                    init_stats["party"].append(gordon)
                    init_stats["party"][0]["peoplerec"] += 1
                    init_stats["story_flags"]["gordon_recruited"] = True
            else:
                print("How your level < than 1?")

        elif mapc == "5":
            if playerlvl >= 1:
                cleaning()
                print("The pawn shop is dim, smells like dust and old money.")
                inv = init_stats["party"][0]["inv"]
                closeshop = False

                while not closeshop:
                    print("1: Buy\n2: Sell\nType i to leave")
                    action = input("> ").strip().lower()

                    if action == "i":
                        closeshop = True
                        continue

                    elif action == "1":
                        stock = list(shops["PAWN_SHOP"].keys())
                        for i, item_name in enumerate(stock, start=1):
                            price = shops["PAWN_SHOP"][item_name]
                            print(f"{i}: {item_name} - {price} money")
                        print("Type i to go back")

                        choice = input("> ").strip()
                        if choice.lower() == "i":
                            continue
                        if choice.isdigit() and 0 < int(choice) <= len(stock):
                            item_name = stock[int(choice) - 1]
                            price = shops["PAWN_SHOP"][item_name]
                            if init_stats["party"][0]["money"] >= price:
                                init_stats["party"][0]["money"] -= price
                                inv[item_name] = inv.get(item_name, 0) + 1
                                print(f"Bought 1x {item_name}!")
                            else:
                                print("You can't afford that.")
                        else:
                            print("Invalid choice!")

                    elif action == "2":
                        sellable = list(inv.keys())
                        if not sellable:
                            print("You don't have anything to sell.")
                            continue

                        for i, item_name in enumerate(sellable, start=1):
                            item_data = items[item_name]
                            value = item_data.get("sellvalue")
                            if value is None:
                                value = item_data.get("stre", 0) * 2
                            count = inv[item_name]
                            print(f"{i}: {item_name} (x{count}) - sells for {value} each")
                        print("Type i to go back")

                        choice = input("> ").strip()
                        if choice.lower() == "i":
                            continue
                        if choice.isdigit() and 0 < int(choice) <= len(sellable):
                            item_name = sellable[int(choice) - 1]

                            if item_name == init_stats["party"][0]["eq_wep"]:
                                print("You can't sell your equipped weapon!")
                                continue

                            item_data = items[item_name]
                            value = item_data.get("sellvalue")
                            if value is None:
                                value = item_data.get("stren", 0) * 2

                            inv[item_name] -= 1
                            if inv[item_name] == 0:
                                del inv[item_name]

                            init_stats["party"][0]["money"] += value
                            print(f"Sold 1x {item_name} for {value} money!")
                        else:
                            print("Invalid choice!")
                    else:
                        print("Invalid choice!")
            else:
                print("\n" + lang[language1]["lowlv"])
                
        elif mapc == "6":
            cleared = dungeon(pool, boss, init_stats, lang, language1, skills, items, enemis)
            if cleared and not init_stats["story_flags"].get("Deisuki_Defeated"):
                init_stats["story_flags"]["Deisuki_Defeated"] = True
                cleaning()
                print("You managed to defeat Malushi.")
                time.sleep(2)
                print("You beat him down for answers. \n and he tells you how it wasn't him who shot you.")
                time.sleep(2)
                print("But before he finishes...")
                time.sleep(2)
                print("He gets shot by a man wearing a raincoat that vanishes by jumping out of a window")
                time.sleep(2)
                print("You try to catch him but he is too fast.")
                print("You contemplate what to do now...")
                time.sleep(1)
                print("Chapter 3: By the books")
                time.sleep(3)

        elif mapc == "7":
            if playerlvl >= map_data["feizhua"]["lvlreq"]:
                cleared = dungeon(map_data["feizhua"]["enemy_pool"], map_data["feizhua"]["boss"], init_stats, lang, language1, skills, items, enemis)
                if cleared and not init_stats["story_flags"].get("Malushi_Defeated"):
                    init_stats["story_flags"]["Malushi_Defeated"] = True
                    cleaning()
                    print("You managed to defeat Malushi.")
                    time.sleep(2)
                    print("You beat him down for answers. \n and he tells you how it wasn't him who shot you.")
                    time.sleep(2)
                    print("But before he finishes...")
                    time.sleep(2)
                    print("He gets shot by a man wearing a raincoat that vanishes by jumping out of a window")
                    time.sleep(2)
                    print("You try to catch him but he is too fast.")
                    print("You contemplate what to do now...")
                    time.sleep(1)
                    print("Chapter 4: Dead man's gamble")
                    time.sleep(3)
            else:
                print("\n" + lang[language1]["lowlv"])

        elif mapc == "8":
            if playerlvl >= map_data["jianqyang_ryu"]["lvlreq"]:
                print("You barge in the Family office, all of Kawashiro's goons surround you.")
                print("There's no way to go but up.")
                time.sleep(3)
                cleared = dungeon(map_data["feizhua"]["enemy_pool"], map_data["feizhua"]["boss"], init_stats, lang, language1, skills, items, enemis)
                if cleared and not init_stats["story_flags"].get("Kawashiro_Defeated"):
                    init_stats["story_flags"]["Kawashiro_defeated"] = True
                    cleaning()
                    print("You finally managed to take down Kawashiro.")
                    time.sleep(2)
                    print("You talk to him, trying to figure out why. \n He explains that he didn't shoot you, he wasn't there the day.")
                    print("He shows you video logs he had")
                    time.sleep(2)
                    print("It shows he was in a restaurant, he never shot you.")
                    time.sleep(2)
                    print("He says that he never wanted to shoot you, and he thought you got killed by the police.")
                    time.sleep(2)
                    print("He asks you about Kine, asks what happened to him.")
                    print("You ask why because you didn't see him that day.")
                    time.sleep(1)
                    print("That's when you realize...")
                    time.sleep(2)
                    print("Chapter 5: The end of the Yakuza")
                    time.sleep(3)
            else:
                print("\n" + lang[language1]["lowlv"])

        elif mapc == "9":
            if playerlvl >= map_data["fuxi_donzen"]["lvlreq"]:
                print("You climb the hospital. \n You see Kina standing at the rooftop \n He looks at you... \n Without even a word he lunges at you...")
                time.sleep(3)
                cleared = dungeon(map_data["fuxi_donzen"]["enemy_pool"], map_data["fuxi_donzen"]["boss"], init_stats, lang, language1, skills, items, enemis)
                if cleared and not init_stats["story_flags"].get("Kine_Defeated"):
                    init_stats["story_flags"]["Kine_defeated"] = True
                    cleaning()
                    print("You finally took down Kine.")
                    time.sleep(2)
                    print("You begin to repeatedly beat him down. \n He tells you that he doesn't regret anything he did.")
                    time.sleep(2)
                    print("You finally deliver the finishing blow")
                    time.sleep(2)
                    print("You grab one of your cigars and smoke peacefully for the first time in weeks.")
                    time.sleep(2)
                    print("I can do anything, I can go anywhere.")
                    time.sleep(1)
                    print("Game end - Thanks for playing.")
                    time.sleep(3)
            else:
                print("\n" + lang[language1]["lowlv"])

        elif mapc == "i":
            player_itemOV = list(playerOV["inv"].keys())

            weaponlist = []
            headgearlist = []
            accesorylist = []

            for i in player_itemOV:
                currentitem = items[i]

                if currentitem["type"] == "weapon":
                    weaponlist.append(i)
                elif currentitem["type"] == "headgear":
                    headgearlist.append(i)
                elif currentitem["type"] == "accessory":
                    accesorylist.append(i)

            closeinv = False

            while not closeinv:
                print("\nType I to quit")
                print("Type A for accessories")
                print("Type H for headgear")
                print("Type W for weapons")

                choice = input("> ").strip().lower()

                if choice == "i":
                    closeinv = True
                    continue

                if choice == "w":
                    current_list = weaponlist
                elif choice == "h":
                    current_list = headgearlist
                elif choice == "a":
                    current_list = accesorylist
                else:
                    print("Invalid choice!")
                    continue

                if not current_list:
                    print("You don't own anything of this type.")
                    continue
                
                print()

                for i, itemname in enumerate(current_list):
                    count = playerOV["inv"][itemname]
                    print(f"{i}: {itemname} (x{count})")

                print("Type the number of what you want to equip.")
                equip = input("> ").strip()

                if not equip.isdigit():
                    print("Please enter a number.")
                    continue

                idx = int(equip)

                if idx < 0 or idx >= len(current_list):
                    print("Invalid number!")
                    continue

                item_name = current_list[idx]
                item = items[item_name]

                if playerOV["class"] not in item["usableby"]:
                    print(f"{playerOV['name']} the {playerOV['class']}" f"can't use {item_name}")
                    continue
                if choice == "w":
                    playerOV["eq_wep"] = item_name
                    print(f"You equipped {item_name}")

                elif choice == "h":
                    playerOV["eq_head"] = item_name
                    print(f"You equipped {item_name}")

                elif choice == "a":
                    playerOV["eq_accessory"] = item_name
                    print(f"{playerOV['name']} equipped {item_name}")

        elif mapc == "u":
            cleaning()
            testpool = [6]
            majima_pool= [12]
            print("You ambushed a random passerby for some quick cash.")
            num_enemies = random.randint(1, 3)
            select_enemy_id = random.choices(testpool, k=num_enemies)
            combat1(init_stats, select_enemy_id, enemis, lang, language1, skills, items)
            chancemaima = random.randint(1, 10)
            if chancemaima > 1:
                print(f"Nhehehehe! Got you again, {init_stats['party'][0]['name']}!")
                select_enemy_id = random.choices(majima_pool, k=1)
                combat1(init_stats, select_enemy_id, enemis, lang, language1, skills, items)

        elif mapc == "d":
            dungeon(map_data["sewer"]["enemy_pool"], map_data["sewer"]["boss"], init_stats, lang, language1, skills, items, enemis)

        elif mapc == "h":
            already_recruited = any(member["name"] == "Kanae" for member in init_stats["party"])
            if already_recruited and mission2started == True:
                print("You enter the club...")
                print("You sit and scan the area \n after some time you notice a guy standing \n you pull the photos the bartender gave you...")
                time.sleep(1)
                print("It's a perfect match... you approach him...")
                time.sleep(1)
                print("Without even a word he immediately swings.")
                club_brawl = [12]
                select_enemy_id = random.choices(club_brawl, k=1)
                combat1(init_stats, select_enemy_id, enemis, lang, language1, skills, items)
            elif already_recruited:
                print("Kanae looks at you \n What's up? Anything new?")
            elif playerlvl >= 3 and mission1Started == False and already_recruited == False:
                print("You sit at a random table...")
                time.sleep(2)
                print("A woman passes by and drops a paper to you.")
                time.sleep(2)
                print("When you read it it says \n (I know who you are, stay here.)")
                print("You stay and wait...")
                time.sleep(2)
                print("After some time she comes back \n she explains how she knows you, and how she wants to help")
                time.sleep(2)
                print("You accept her help")
                print("Kanae joined the party!")
                kanae = apply_defaults(copy.deepcopy(parte["kanae"]))
                init_stats["party"].append(kanae)
                init_stats["party"][0]["peoplerec"] += 1
                init_stats["story_flags"]["kanae_recruited"] = True
                init_stats["story_flags"]["chapter2_lead_found"] = True
            else:
                print("The club seems closed... \n Maybe I should come back later...")

        elif mapc == "p":
            currentslot = 0
            onsts = True
            while onsts:
                active = init_stats["party"][currentslot]
                total_damage = active["stre"] + items[active["eq_wep"]]["stren"]
                total_defense = active["defe"] + items[active["eq_head"]]["defen"] + items[active["eq_accessory"]]["defen"]
                print("Type A and D to change between party members and P to quit")
                print(f"{init_stats["party"][currentslot]["name"]} Stats")
                print(f"HP: {init_stats["party"][currentslot]["hp"]} out of {init_stats["party"][currentslot]["maxhp"]}")
                print(f"Mana: {init_stats["party"][currentslot]["mana"]} out of {init_stats["party"][currentslot]["maxmana"]}")
                print(f"Strenght: {total_damage}")
                print(f"Defense: {total_defense}")
                print(f"lvl: {init_stats["party"][currentslot]["lvl"]}")
                choice = input("> ").strip()
                if choice == "d":
                    currentslot = (currentslot + 1) % len(init_stats["party"])
                if choice == "a":
                    currentslot = (currentslot - 1) % len(init_stats["party"])
                if choice == "p":
                    break

        elif mapc == "j":
            currentslot = 0
            onpts = True
            while onpts:
                active = init_stats["party"][currentslot]
                print("Choose what you want to upgrade")
                print(f"You are currently upgrading {active['name']}")
                print(f"You currently have {active['pts']} points")
                print(f"You currently have {active['xptotal']} out of {lvlup(active["lvl"])} for the next point")
                print(lang[language1]["upgrade"])
                choice = input("> ").strip()
                if choice == "d":
                    currentslot = (currentslot + 1) % len(init_stats["party"])
                if choice == "a":
                    currentslot = (currentslot - 1) % len(init_stats["party"])
                if choice == "j":
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

        elif mapc == "c":
            unlocked = playerOV["unlocked_classes"]
            print("Choose your job")
            for i, job in enumerate(unlocked, start=1):
                marker = " (current)" if job == playerOV["class"] else ""
                print(f"{i}: {job}{marker}")

            choice = input("> ").strip()
            if choice.isdigit() and 0 < int(choice) <= len(unlocked):
                byework(playerOV, unlocked[int(choice) - 1], statusclass, classlvlreq, items, Majimaencounters)
            else:
                print("Invalid choice!")

        elif mapc == "s":
            print("You decide to take a stroll around town.")
            chance = random.randint(1, 10)
            print(f"roll: {chance}")
            jumppool = [4, 5, 6, 7, 8]
            majimapool = [86, 87, 88, 89]
            if chance == 1:
                for enemy_id in ["86", "87", "88", "89"]:
                    enemis[enemy_id]["hp"] = round(enemis[enemy_id]["basehp"] + (init_stats["party"][0]["Majima_encounter"] * 1.15))
                    enemis[enemy_id]["maxhp"] = round(enemis[enemy_id]["basemaxhp"] + (init_stats["party"][0]["Majima_encounter"] * 1.15))
                    for move in enemis[enemy_id]["moveset"]: 
                        move["stre"] = round(move["basestre"] + (init_stats["party"][0]["Majima_encounter"] * 1.10))
                select_enemy_id = random.choices(majimapool, k=1)
                combat1(init_stats, select_enemy_id, enemis, lang, language1, skills, items)
            elif chance == 2:
                print("You found an item lying around!")
                running_chance = 0
                roll = random.random()
                items1 = list(chest["STROLL1"].keys())
                for i, item_name in enumerate(items1, start=1):
                    chance = chest["STROLL1"][item_name]
                    running_chance += chance
                    if running_chance >= roll:
                        print(f"You got a {item_name}")
                        player_inv = init_stats["party"][0]["inv"]
                        if item_name in player_inv:
                            player_inv[item_name] += 1
                        else:
                            player_inv[item_name] = 1
                        break
            elif chance >= 3 or chance <= 4:
                print("You got jumped!")
                select_enemy_id = random.choices(jumppool, k=1)
                combat1(init_stats, select_enemy_id, enemis, lang, language1, skills, items)
            elif chance >= 5 or chance <= 8:
                print("You found some money laying around")
                monay = random.randint(1, 10)
                coolmonay = monay + (init_stats["party"][0]["lvl"] * 1.5)
                init_stats["party"][0]["money"] += coolmonay
            elif chance >= 8 or chance <= 10:
                print("You took the stroll.")
        elif mapc == "test":
            majimapool = [86, 87, 88, 89]
            for enemy_id in ["86", "87", "88", "89"]:
                enemis[enemy_id]["hp"] = round(enemis[enemy_id]["basehp"] + (init_stats["party"][0]["Majima_encounter"] * 1.15))
                enemis[enemy_id]["maxhp"] = round(enemis[enemy_id]["basemaxhp"] + (init_stats["party"][0]["Majima_encounter"] * 1.15))
                for move in enemis[enemy_id]["moveset"]: 
                    move["stre"] = round(move["basestre"] + (init_stats["party"][0]["Majima_encounter"] * 1.10))
            select_enemy_id = random.choices(majimapool, k=1)
            combat1(init_stats, select_enemy_id, enemis, lang, language1, skills, items)
        elif mapc == "Final":
            if init_stats["story_flags"]["Kine_defeated"] == True:
                print("You enter the Family Office again... \n Everything is messy and turned. \n At the patriarch chair you see someone... \n ???: We finally meet \n The Amon will destroy you!")
                Amon = [100]
                select_enemy_id = random.choices(Amon, k=1)
                combat1(init_stats, select_enemy_id, enemis, lang, language1, skills, items)
                print("What? How could I lose to... you!? \n This is NOT over.")
                print("He vanishes...")




        else:
            print("Invalid choice!")

    return "someicho"


MAP_FUNCTIONS = {
    "tutorial": lambda init_stats, lang, language1, map_data, playerOV: tutorial_map(init_stats, lang, language1, map_data),
    "someicho": someicho_map,
}


print("Welcome to the game! / bienvenue á la jeux! / Bem vindo ao jogo!")
print("Select your language / Choisissez votre language / Escolha seu idioma")
print("en for english / fr vers français / pt para português.")

language1 = input("> ").strip().lower()
if language1 not in lang:
    print("Language not in database or you wrote it wrong, oh well, english it is!")
    language1 = "en"
print("\n" + lang[language1]["loadgame"] + "\n" + lang[language1]["newgame"])
begin1 = input("> ").strip().lower()

if begin1 == "2":
    init_stats = {
        "party": [
            {
                "name": "name",
                "class": "class",
                "maxhp": 18,
                "hp": 18,
                "mana": 3,
                "maxmana": 3,
                "stre": 1,
                "luck": 1,
                "inv": {},
                "xp": 0,
                "defe": 3,
                "lvl": 1,
                "xptotal": 0,
                "status": "Normal",
                "bleed_turns": 0,
                "bleed_dmg": 0,
                "boostdef": 0,
                "last_def_boost": 0,
                "taunt_turns": 0,
                "pts": 0,
                "eq_wep": "Fists",
                "peoplerec": 0,
                "speed": 0,
                "bonus_stre": 0,
                "bonus_hp": 0,
                "bonus_mana": 0,
                "bonus_luck": 0,
                "unlocked_classes": ["Yakuza"],
                "isplayer": True,
                "is_main_character": True,
                "money": 50,
                "AttackUp" : 20,
                "AttackUpTurn" : 2,
                "weakness": [],
                "strong" : [],
                "Majima_encounter" : 0,
            }
        ],
        "story_flags": {
            "current_map": "tutorial",
            "chapter": 1,
            "gordon_recruited": False,
        },
    }

    print("\n" + lang[language1]["nameusr"])
    name1 = input("> ").strip()
    init_stats["party"][0]["name"] = name1

    apply_class_stats(init_stats["party"][0], "Yakuza")
    save(init_stats)
else:
    init_stats = load()
    print("Game loaded.")

map_data = mape()
playerOV = init_stats["party"][0]

current_map = init_stats["story_flags"].get("current_map", "tutorial")

while current_map != "quit":
    handler = MAP_FUNCTIONS[current_map]
    current_map = handler(init_stats, lang, language1, map_data, playerOV)