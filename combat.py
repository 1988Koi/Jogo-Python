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

with open ("skills.json", "r", encoding="utf-8") as skill:
    skills = json.load(skill)

with open("enemies.json", "r", encoding="utf-8") as enemies:
    enemis = json.load(enemies)

with open ("party.json", "r", encoding="utf-8") as part:
    parte = json.load(part)

def combat1(init_stats, enemy_ids, enemies_db, lang, language1, skills, items):
    presentenemies = []

    for eids in enemy_ids:
        presentenemies.append(enemies_db[str(eids)].copy())


    game_over = False

    while any(e["hp"] > 0 for e in presentenemies) and not game_over:    
        
        for enemies in presentenemies:
            if enemies["hp"] <= 0:
                continue
            
            current_hp = max(0, enemies["hp"]) 
            enemyhpmax = max(0, min(10, (10 * current_hp) // enemies["maxhp"]))
            enemyhpmin = 10 - enemyhpmax
            print(f"{enemies['name']}:  [\033[91m{'█' * enemyhpmax}\033[0m{'░' * enemyhpmin}] {current_hp} / {enemies['maxhp']}")

        for member in init_stats["party"]:
            current_hp = max(0, member["hp"])
            hpbarmax = max(0, min(10, (current_hp * 10) // member["maxhp"]))
            hpbarmin = 10 - hpbarmax
            print(f"{member['name']}:[\033[92m{'█' * hpbarmax}\033[0m{'░' * hpbarmin}] {current_hp} / {member['maxhp']}")
            
            current_mana = max(0, member["mana"])
            manabarmax = max(0, min(10, (current_mana * 10) // member["maxmana"]))
            manabarmin = 10 - manabarmax
            print(f"{member['name']}: [\033[95m{'█' * manabarmax}\033[0m{'░' * manabarmin}] {current_mana} / {member['maxmana']}")

        for combate in init_stats["party"]:
            if combate["hp"] <= 0:
                continue
                
            turn_completed = False
            total_damage = combate["stre"] + items[combate["eq_wep"]]["stren"]
            
            while not turn_completed and not game_over:
                print("\n" + lang[language1]["combat"])
                playerturn = input("> ").strip().lower()
                
                if playerturn == "1":

                    print("\n" + lang[language1]["attack"])
                    for i, enemy in enumerate(presentenemies):
                        if enemy["hp"] > 0:
                            print(f"{i + 1}: {enemy['name']}")
                        else:
                            print(f"{i + 1}: {enemy['name']} DEAD")

                    target_choice = input("> ").strip()
                    if target_choice.isdigit():
                        choice = int(target_choice)
                        if 0 < choice <= len(presentenemies):
                            target_index = choice - 1
                            if presentenemies[target_index]["hp"] <= 0:
                                print("Enemy already dead! Pick someone else.")
                                continue
                            else:
                                presentenemies[target_index]["hp"] -= total_damage
                                combate["mana"] = min(combate["maxmana"], combate["mana"] + 5)
                                #heal_target["hp"] = min(heal_target["maxhp"], heal_target["hp"] + chosen["healing"])
                                print(f"Hit! {presentenemies[target_index]['name']} takes {total_damage} damage.")
                                print(f"And you got +5 mana!")
                                turn_completed = True
                                break
                        else:
                            print("Invalid number!")
                    else:
                        print("Invalid input!")

                elif playerturn == "2":
                    print("\n" + lang[language1]["attack"])
                    current = combate["class"].lower()
                    class_skills = skills[current]
                    available = []
                    
                    for i, skil in enumerate(class_skills):
                        if skil["lvlreq"] <= combate["lvl"]:
                            available.append(skil)
                            print(f"{len(available)}: {skil['name']}, cost: {skil['cost']} Description: {skil['desc']}")

                    if not available:
                        print("No skills available!")
                        continue

                    skille = input("> ").strip()
                    if skille.isdigit():
                        skg = int(skille)
                        if 0 < skg <= len(available):
                            chosen = available[skg - 1]

                            if "bringback" in chosen:
                                for i, ally in enumerate(init_stats["party"]):
                                    if ally["hp"] > 0:
                                        print(f"{i + 1}: {ally['name']}")
                                    else:
                                        print(f"{i + 1}: {ally ['name']} DEAD")
                                    
                                healing_choice = input("> ").strip()
                                if healing_choice.isdigit():
                                    heal_choice = int(healing_choice)
                                    if 0 < heal_choice <= len(init_stats["party"]):
                                        ally_index = heal_choice - 1
                                        heal_target = init_stats["party"][ally_index]
                                        if heal_target["hp"] <= 0:
                                            heal_target["hp"] = chosen["bringback"]
                                            combate["mana"] -= chosen["cost"]
                                            print (f"{heal_target['name']} is back on his feet!")
                                        else:
                                            print (f"{heal_target['name']} is already alive!")
                                            continue

                            elif "healing" in chosen:
                                for i, ally in enumerate(init_stats["party"]):
                                    if ally["hp"] > 0:
                                        print(f"{i + 1}: {ally['name']}")
                                    else:
                                        print(f"{i + 1}: {ally ['name']} DEAD")
                                    
                                healing_choice = input("> ").strip()
                                if healing_choice.isdigit():
                                    heal_choice = int(healing_choice)
                                    if 0 < heal_choice <= len(init_stats["party"]):
                                        ally_index = heal_choice - 1
                                        heal_target = init_stats["party"][ally_index]
                                        if heal_target["hp"] > 0:
                                            heal_target["hp"] = min(heal_target["maxhp"], heal_target["hp"] + chosen["healing"])
                                            combate["mana"] -= chosen["cost"]
                                            print (f"Plus {chosen['healing']} on {heal_target['name']}")
                                        else:
                                            print (f"{heal_target['name']} cannot be healed due to large damage received!")
                                            continue

                            elif "dmgmlt" in chosen:
                                if chosen["targettype"] == "single":
                                    for i, enemy in enumerate(presentenemies):
                                        if enemy["hp"] > 0:
                                            print(f"{i + 1}: {enemy['name']}")
                                        else:
                                            print(f"{i + 1}: {enemy['name']} DEAD")
                                            
                                    target_choice = input("> ").strip()
                                    if target_choice.isdigit():
                                        choice = int(target_choice)
                                        if 0 < choice <= len(presentenemies):
                                            target_index = choice - 1
                                            
                                            if presentenemies[target_index]["hp"] <= 0:
                                                print("Enemy already dead! Pick someone else.")
                                            else:
                                                if chosen["cost"] <= combate["mana"]:
                                                    damage = round(total_damage * chosen["dmgmlt"])
                                                    presentenemies[target_index]["hp"] -= damage
                                                    combate["mana"] -= chosen["cost"]
                                                    print(f"Used {chosen['name']}! Dealt {damage} damage.")
                                                    turn_completed = True
                                                    break
                                                else:
                                                    print("Not enough Mana!")
                                                    continue
                                        else:
                                            print("Invalid number!")
                                            continue
                                    else:
                                        print("Invalid input!")
                                        continue

                                elif chosen["targettype"] == "all":
                                    if chosen["cost"] >= combate["mana"]:
                                        damage = round(total_damage * chosen["dmgmlt"])
                                        for enemy in presentenemies:
                                            if enemy["hp"] > 0:
                                                enemy["hp"] -= damage
                                                combate["mana"] -= chosen["cost"]
                                                print(f"You used a skill that hit everyone!")
                                                turn_completed = True
                                                break
                                            else:
                                                print("One of the enemies were already dead!")
                                    else:
                                        print("Not enough mana!")
                                        continue
                            else:
                                print("Invalid skill number!")
                                continue
                        else:
                            print("Invalid input!")
                            continue

                elif playerturn == "3":
                    player_item = list(init_stats["party"][0]["inv"].keys())

                    for i, itemname in enumerate(player_item):
                        count = combate["inv"][itemname]
                        print(f"{i + 1}: {itemname}(x{count})")

                    choice = int(input("> ")) -1
                    item_name = player_item[choice]
                    item_data = items[item_name]


                    if item_data["type"] == "heal":
                        if item_name == "Stamina Spork":
                            combate["hp"] = (combate["hp"] + item_data["value"])
                            print(f"You feel ill -{item_data['value']}")
                            combate["inv"][item_name]  -= 1
                            if combate["inv"][item_name] == 0:
                                del(combate["inv"][item_name])
                        else:
                            combate["hp"] = min(combate["maxhp"], combate["hp"] + item_data["value"])
                            print(f"You consumed a nice {item_name} you got +{item_data['value']} health")
                            combate["inv"][item_name]  -= 1
                            if combate["inv"][item_name] == 0:
                                del(combate["inv"][item_name])
                            
                    elif item_data["type"] == "mana":
                        combate["mana"] = min(combate["maxmana"], combate["mana"] + item_data["value"])
                        print(f"You consumed a nice {item_name} and got + {item_data['value']}")
                    combate["inv"][item_name] -= 1
                    if combate["inv"][item_name] == 0:
                        del(combate["inv"][item_name])

                    turn_completed = True

                else:
                    print("Invalid choice, try again.")
                    continue
                    
            if not any(e["hp"] > 0 for e in presentenemies):
                break

        if any(e["hp"] > 0 for e in presentenemies):
            cleaning()
            for eatt in presentenemies: 
                if eatt["hp"] <= 0:
                    continue

                living_party = []
                chosen_attack = None

                for member in init_stats["party"]:
                    if member["hp"] > 0:
                        living_party.append(member)

                if len(living_party) > 0:
                    runnin_total = 0
                    randomchance = random.random()
                    for i in eatt["moveset"]:
                        runnin_total += i["chance"]
                        if runnin_total >= randomchance:
                            chosen_attack = i
                            if chosen_attack["targettype"] == "one":
                                unluckyman = random.choice(living_party)
                                unluckyman["hp"] -= chosen_attack["stre"]
                                print (f"{unluckyman['name']} got hit by a {chosen_attack['nameskill']}")
                            elif chosen_attack["targettype"] == "all":
                                for e in living_party:
                                    e["hp"] -= chosen_attack["stre"]
                                print(f"everybody got hit by {chosen_attack['nameskill']}!")
                            elif chosen_attack["targettype"] == "self":
                                eatt["status"] = chosen_attack["status"]
                            break

                else:
                    print ("You died!")
                    game_over = True
                    break


    print("Combat Finished!")
    for enemy in presentenemies:
        if "possibledrop" in enemy:
            drop_enemy = enemy["possibledrop"][0]["itemid"]
            print(f"You got a {drop_enemy}!")
            player_inv = init_stats["party"][0]["inv"]
            if drop_enemy in player_inv:
                player_inv[drop_enemy] += 1
            else:
                player_inv[drop_enemy] = 1
                print("Debug Backpack:", init_stats["party"][0]["inv"])
    
    if game_over:
        return False
    else:
        return True