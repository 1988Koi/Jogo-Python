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


def print_bars(presentenemies, party):
    for enemy in presentenemies:
        current_hp = max(0, enemy["hp"])
        enemyhpmax = max(0, min(10, (10 * current_hp) // enemy["maxhp"]))
        enemyhpmin = 10 - enemyhpmax
        print(f"{enemy['name']}:  [\033[91m{'█' * enemyhpmax}\033[0m{'░' * enemyhpmin}] {current_hp} / {enemy['maxhp']}")

    for member in party:
        current_hp = max(0, member["hp"])
        hpbarmax = max(0, min(10, (current_hp * 10) // member["maxhp"]))
        hpbarmin = 10 - hpbarmax
        print(f"{member['name']}:[\033[92m{'█' * hpbarmax}\033[0m{'░' * hpbarmin}] {current_hp} / {member['maxhp']}")

        current_mana = max(0, member["mana"])
        manabarmax = max(0, min(10, (current_mana * 10) // member["maxmana"]))
        manabarmin = 10 - manabarmax
        print(f"{member['name']}: [\033[95m{'█' * manabarmax}\033[0m{'░' * manabarmin}] {current_mana} / {member['maxmana']}")


def player_turn(combate, presentenemies, init_stats, lang, language1, skills, items, game_over_flag):
    total_damage = combate["stre"] + items[combate["eq_wep"]]["stren"]
    turn_taken = False

    while not game_over_flag[0] and not turn_taken:
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
                        if total_damage <= (presentenemies[target_index]['defe'] / 2):
                            print(f"{presentenemies[target_index]['name']} managed to resist {combate['name']} attack!")
                        else:
                            presentenemies[target_index]["hp"] -= total_damage
                            combate["mana"] = min(combate["maxmana"], combate["mana"] + 5)
                            print(f"Hit! {presentenemies[target_index]['name']} takes {total_damage} damage.")
                            print("And you got +5 mana!")
                            turn_taken = True
                else:
                    print("Invalid number!")
            else:
                print("Invalid input!")

        elif playerturn == "2":
            print("\n" + lang[language1]["attack"])
            current = combate["class"].lower()
            class_skills = skills[current]
            available = []

            for skil in class_skills:
                if skil["lvlreq"] <= combate["lvl"]:
                    available.append(skil)
                    print(f"{len(available)}: {skil['name']}, cost: {skil['cost']} Description: {skil['desc']}")

            if not available:
                print("No skills available!")
                continue

            skille = input("> ").strip()
            if not skille.isdigit():
                print("Invalid input!")
                continue

            skg = int(skille)
            if not (0 < skg <= len(available)):
                print("Invalid input!")
                continue

            chosen = available[skg - 1]

            if chosen["cost"] > combate["mana"]:
                print("Not enough mana!")
                continue

            if "bringback" in chosen:
                for i, ally in enumerate(init_stats["party"]):
                    if ally["hp"] > 0:
                        print(f"{i + 1}: {ally['name']}")
                    else:
                        print(f"{i + 1}: {ally['name']} DEAD")

                healing_choice = input("> ").strip()
                if healing_choice.isdigit():
                    heal_choice = int(healing_choice)
                    if 0 < heal_choice <= len(init_stats["party"]):
                        ally_index = heal_choice - 1
                        heal_target = init_stats["party"][ally_index]
                        if heal_target["hp"] <= 0:
                            heal_target["hp"] = chosen["bringback"]
                            combate["mana"] -= chosen["cost"]
                            print(f"{heal_target['name']} is back on his feet!")
                            turn_taken = True
                        else:
                            print(f"{heal_target['name']} is already alive!")
                            continue
                    else:
                        print("Invalid number!")
                        continue
                else:
                    print("Invalid input!")
                    continue

            elif "healing" in chosen:
                for i, ally in enumerate(init_stats["party"]):
                    if ally["hp"] > 0:
                        print(f"{i + 1}: {ally['name']}")
                    else:
                        print(f"{i + 1}: {ally['name']} DEAD")

                healing_choice = input("> ").strip()
                if healing_choice.isdigit():
                    heal_choice = int(healing_choice)
                    if 0 < heal_choice <= len(init_stats["party"]):
                        ally_index = heal_choice - 1
                        heal_target = init_stats["party"][ally_index]
                        if heal_target["hp"] > 0:
                            heal_target["hp"] = min(heal_target["maxhp"], heal_target["hp"] + chosen["healing"])
                            combate["mana"] -= chosen["cost"]
                            print(f"Plus {chosen['healing']} on {heal_target['name']}")
                            turn_taken = True
                        else:
                            print(f"{heal_target['name']} cannot be healed due to large damage received!")
                            continue
                    else:
                        print("Invalid number!")
                        continue
                else:
                    print("Invalid input!")
                    continue

            elif "defe" in chosen:
                combate["defe"] += chosen["defe"]
                combate["boostdef"] += chosen["boostdef"]
                print(f"{combate['name']} got a defense boost!")
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
                                continue
                            else:
                                damage = round(total_damage * chosen["dmgmlt"])
                                if damage <= (presentenemies[target_index]["defe"] / 2):
                                    print(f"{presentenemies[target_index]['name']} managed to resist {combate['name']} attack!")
                                else:
                                    presentenemies[target_index]["hp"] -= damage
                                    combate["mana"] -= chosen["cost"]
                                    print(f"Used {chosen['name']}! Dealt {damage} damage.")
                                    turn_taken = True
                        else:
                            print("Invalid number!")
                            continue
                    else:
                        print("Invalid input!")
                        continue

                elif chosen["targettype"] == "all":
                    damage = round(total_damage * chosen["dmgmlt"])
                    combate["mana"] -= chosen["cost"]
                    for enemy in presentenemies:
                        if enemy["hp"] > 0:
                            enemy["hp"] -= damage
                    print("You used a skill that hit everyone!")
                    turn_taken = True
            else:
                print("Invalid skill number!")
                continue

        elif playerturn == "3":
            player_item = list(combate["inv"].keys())
            if not player_item:
                print("Your inventory is empty!")
                continue

            for i, itemname in enumerate(player_item):
                count = combate["inv"][itemname]
                print(f"{i + 1}: {itemname}(x{count})")

            item_choice = input("> ").strip()
            if not item_choice.isdigit():
                print("Invalid input!")
                continue

            choice = int(item_choice) - 1
            if not (0 <= choice < len(player_item)):
                print("Invalid number!")
                continue

            item_name = player_item[choice]
            item_data = items[item_name]

            if item_data["type"] == "heal":
                if item_name == "Stamina Spork":
                    combate["hp"] = combate["hp"] + item_data["value"]
                    print(f"You feel ill -{item_data['value']}")
                else:
                    combate["hp"] = min(combate["maxhp"], combate["hp"] + item_data["value"])
                    print(f"You consumed a nice {item_name} you got +{item_data['value']} health")

            elif item_data["type"] == "mana":
                combate["mana"] = min(combate["maxmana"], combate["mana"] + item_data["value"])
                print(f"You consumed a nice {item_name} and got + {item_data['value']}")

            combate["inv"][item_name] -= 1
            if combate["inv"][item_name] == 0:
                del combate["inv"][item_name]

            turn_taken = True

        else:
            print("Invalid choice, try again.")
            continue

    return turn_taken


def enemy_turn(eatt, presentenemies, init_stats, game_over_flag):
    living_party = [m for m in init_stats["party"] if m["hp"] > 0]

    if not living_party:
        print("You died!")
        game_over_flag[0] = True
        return

    randomchance = random.random()
    running_total = 0
    chosen_attack = None

    for move in eatt["moveset"]:
        running_total += move["chance"]
        if running_total >= randomchance:
            chosen_attack = move
            break

    if chosen_attack is None:
        return

    if chosen_attack["targettype"] == "one":
        unluckyman = random.choice(living_party)
        defenseunluck = unluckyman["defe"] / 2
        if defenseunluck >= chosen_attack["stre"]:
            print(f"{unluckyman['name']} managed to resist {eatt['name']} attack!")
        else:
            unluckyman["hp"] -= chosen_attack["stre"]
            if "statuschance" in chosen_attack:
                statusroll = random.random()
                effective_chance = max(0.0, chosen_attack["statuschance"] - unluckyman["luck"] * 0.2)
                if statusroll <= effective_chance:
                    if chosen_attack["status"] == "Bleed":
                        unluckyman["bleed_turns"] = chosen_attack["bleedturns"]
                        unluckyman["bleed_dmg"] = chosen_attack["bleeddmg"]
                        print(f"{unluckyman['name']} is bleeding!")
                    else:
                        unluckyman["status"] = chosen_attack["status"]
                        print(f"{unluckyman['name']} got hit by {chosen_attack['nameskill']} and was applied {chosen_attack['status']}!")
                else:
                    print(f"{unluckyman['name']} got hit by {chosen_attack['nameskill']} but managed to dodge the debuff!")
            else:
                print(f"{unluckyman['name']} was hit with {chosen_attack['nameskill']}!")

    elif chosen_attack["targettype"] == "all":
        print(f"The enemy used {chosen_attack['nameskill']} on everybody!")
        for member in living_party:
            member["hp"] -= chosen_attack["stre"]
            if "statuschance" in chosen_attack and chosen_attack.get("statustarget") == "ally":
                statusroll = random.random()
                effective_chance = max(0.0, chosen_attack["statuschance"] - unluckyman["luck"] * 0.2)
                if statusroll <= effective_chance:
                    member["status"] = chosen_attack["status"]
                    print(f"{member['name']} got hit and was applied {chosen_attack['status']}!")
                else:
                    print(f"{member['name']} got hit but dodged the debuff!")

        if chosen_attack.get("statustarget") == "self":
            eatt["status"] = chosen_attack["status"]
            print(f"The enemy also got applied with {chosen_attack['status']}")

    elif chosen_attack["targettype"] == "self":
        if "status" in chosen_attack:
            eatt["status"] = chosen_attack["status"]
            print(f"The enemy used {chosen_attack['nameskill']} and got {chosen_attack['status']}!")
        if "status" == "Defenseup":
            eatt["defe"] += chosen_attack["defe"]
            eatt["boostdef"] += chosen_attack["boostdef"]
            print(f"The enemy used {chosen_attack['nameskill']} and got {chosen_attack['status']}!")
        else:
            eatt["hp"] += chosen_attack["heal"]
            print(f"The enemy healed himself using {chosen_attack['nameskill']}")


def combat1(init_stats, enemy_ids, enemies_db, lang, language1, skills, items):
    presentenemies = []
    for eids in enemy_ids:
        presentenemies.append(enemies_db[str(eids)].copy())

    game_over_flag = [False]

    order = []
    for i in init_stats["party"]:
        i["currenttick"] = 1000 // i["speed"]
        i["isplayer"] = True
        order.append(i)
    for a in presentenemies:
        a["currenttick"] = 1000 // a["speed"]
        a["isplayer"] = False
        order.append(a)

    while any(e["hp"] > 0 for e in presentenemies) and not game_over_flag[0]:
        living = [i for i in order if i["hp"] > 0]
        lowest = min(i["currenttick"] for i in living)
        for b in living:
            b["currenttick"] -= lowest

        ready = [i for i in living if i ["currenttick"] <= 0]
        ready.sort(key=lambda x : -x["speed"])
        activechar = ready [0]

        activechar["currenttick"] += 1000 // activechar["speed"]

        print_bars(presentenemies, init_stats["party"])
        print(f"It's {activechar['name']} turn!")

        if activechar["hp"] <= 0:
            activechar["currenttick"] = 1000 // activechar["speed"]
            continue

        if activechar["bleed_turns"] > 0:
            activechar ["hp"] -= ["bleed_dmg"]
            activechar["bleed_turns"] =- 1
            print(f"{activechar['name']} took {activechar['bleed_dmg']} bleed damage!")
            if activechar <= 0:
                activechar["currenttick"] = 1000 // activechar["speed"]
                print(f"{activechar['name']} bled out!")
                continue

        if activechar["boostdef"] > 0:
            activechar["boostdef"] =- 1
            continue

        if activechar["status"] == "Stun":
            who = activechar["name"] if not activechar["isplayer"] else "You"
            print(f"{who} {'is' if not activechar['isplayer'] else 'are'} paralyzed!")
            activechar["status"] = "Normal"
            activechar["currenttick"] = 1000 // activechar["speed"]
            continue

        if activechar["isplayer"]:
            player_turn(activechar, presentenemies, init_stats, lang, language1, skills, items, game_over_flag)
        else:
            enemy_turn(activechar, presentenemies, init_stats, game_over_flag)

        activechar["currenttick"] = 1000 // activechar["speed"]

    print("Combat Finished!")

    if not game_over_flag[0]:
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

            init_stats["party"][0]["money"] += enemy["money"]

        defeated = presentenemies
        for i in init_stats["party"]:
            total_xp = 0
            for e in defeated:
                lvldif = i["lvl"] - e["lvl"]
                if lvldif == 0:
                    total_xp += e["xpdrop"]
                elif lvldif == 1:
                    total_xp += int(e["xpdrop"] * 0.8)
                elif lvldif == 2:
                    total_xp += int(e["xpdrop"] * 0.6)
                elif lvldif == 3:
                    total_xp += int(e["xpdrop"] * 0.4)
                elif lvldif == 4:
                    total_xp += int(e["xpdrop"] * 0.2)
                elif lvldif >= 5:
                    total_xp += int(e["xpdrop"] * 0.00001)
                elif lvldif == -1:
                    total_xp += int(e["xpdrop"] * 1.2)
                elif lvldif == -2:
                    total_xp += int(e["xpdrop"] * 1.4)
                elif lvldif == -3:
                    total_xp += int(e["xpdrop"] * 1.6)
                elif lvldif == -4:
                    total_xp += int(e["xpdrop"] * 1.8)
                elif lvldif <= -5:
                    total_xp += int(e["xpdrop"] * 2.0)

            i["xptotal"] += total_xp
            while i["xptotal"] >= 100:
                i["lvl"] += 1
                i["pts"] += 1
                i["xptotal"] -= 100
                print(f"{i['name']} leveled up to {i['lvl']}")


    return not game_over_flag[0]