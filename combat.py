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


def lvlup(lvl):
    return 100 + (lvl - 1) * 10


def apply_inflict(skill, target):
    inflict = skill.get("inflict")
    if not inflict or inflict == "Nothing":
        return
    if inflict == "Bleed":
        target["bleed_turns"] = skill["bleedturns"]
        target["bleed_dmg"] = skill["bleeddmg"]
        print(f"{target['name']} is bleeding!")
    elif inflict == "Stun":
        target["status"] = "Stun"
        print(f"{target['name']} is stunned!")

def get_mult(attack_type, target):
    if not attack_type:
        return 1.0

    weakness = target.get("weakness", [])
    strong = target.get("strong", [])

    if any(t in weakness for t in attack_type):
        return 1.5
    if any(t in strong for t in attack_type):
        return 0.5
    return 1.0

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


def player_turn(combate, presentenemies, init_stats, lang, language1, skills, items, game_over_flag, fled_flag, can_flee=True):

    total_damage = combate["stre"] + items[combate["eq_wep"]]["stren"]
    total_defense = combate["defe"] + items[combate["eq_head"]]["defen"] + items[combate["eq_accessory"]]["defen"]
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
                        weapon_type = items[combate["eq_wep"]].get("dmgtype")
                        mult = get_mult(weapon_type, presentenemies[target_index])
                        effective_dmg = total_damage * mult
                        total = round(effective_dmg)
                        if total <= (presentenemies[target_index]['defe'] / 2):
                            print(f"{presentenemies[target_index]['name']} managed to resist {combate['name']} attack!")
                        else:
                            presentenemies[target_index]["hp"] -= total
                            combate["mana"] = min(combate["maxmana"], combate["mana"] + 5)
                            print(f"Hit! {presentenemies[target_index]['name']} takes {total} damage.")
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

            elif "AttackUp" in chosen:
                init_stats["attackup_turns"] = chosen["bonusattackturn"]
                init_stats["attackup_bonus"] = chosen["bonusattack"]
                if "message" in chosen:
                    print(chosen["message"])
                else:
                    print(f"{init_stats['name']} used {chosen['nameskill']} is getting pumped up!")

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

            elif "defe" in chosen or chosen.get("inflict") == "Taunt":
                if "defe" in chosen:
                    total_defense += items[combate["eq_head"]]["defen"]
                    combate["boostdef"] += chosen["boostdef"]
                    combate["last_def_boost"] = chosen["defe"]
                    print(f"{combate['name']} got a defense boost!")
                if chosen.get("inflict") == "Taunt":
                    combate["taunt_turns"] = chosen["taunt_turns"]
                    print(f"{combate['name']} is taunting the enemies!")
                combate["mana"] -= chosen["cost"]
                turn_taken = True

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
                                mult = get_mult(chosen.get("type", []), presentenemies[target_index])
                                total = round(total_damage * mult)
                                damage = round(total * chosen["dmgmlt"])
                                if damage <= (presentenemies[target_index]["defe"] / 2):
                                    print(f"{presentenemies[target_index]['name']} managed to resist {combate['name']} attack!")
                                else:
                                    presentenemies[target_index]["hp"] -= damage
                                    combate["mana"] -= chosen["cost"]
                                    print(f"Used {chosen['name']}! Dealt {damage} damage.")
                                    apply_inflict(chosen, presentenemies[target_index])
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
                            apply_inflict(chosen, enemy)
                    print("You used a skill that hit everyone!")
                    turn_taken = True
            else:
                print("Invalid skill number!")
                continue

        elif playerturn == "3":
            leader_inv = init_stats["party"][0]["inv"]
            player_item = list(leader_inv.keys())
            if not player_item:
                print("Your inventory is empty!")
                continue

            for i, itemname in enumerate(player_item):
                count = leader_inv[itemname]
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
                if item_name == "Stomina Spork":
                    combate["hp"] = combate["hp"] + item_data["value"]
                    print(f"You feel ill -{item_data['value']}")
                else:
                    combate["hp"] = min(combate["maxhp"], combate["hp"] + item_data["value"])
                    print(f"You consumed a nice {item_name} you got +{item_data['value']} health")

            elif item_data["type"] == "mana":
                combate["mana"] = min(combate["maxmana"], combate["mana"] + item_data["value"])
                print(f"You consumed a nice {item_name} and got + {item_data['value']}")

            leader_inv[item_name] -= 1
            if leader_inv[item_name] == 0:
                del leader_inv[item_name]

            turn_taken = True

        elif playerturn == "4":
            if not can_flee:
                print("You cannot flee from this combat")
                continue

            living_enemies = [e for e in presentenemies if e["hp"] > 0]
            avg_enemy_speed = sum(e["speed"] for e in living_enemies) / len(living_enemies)
            escape_chance = 0.5 + (combate["speed"] - avg_enemy_speed) * 0.02 + combate["luck"] * 0.01
            escape_chance = max(0.1, min(0.9, escape_chance))

            roll = random.random()
            if roll <= escape_chance:
                print(f"{combate['name']} got the party away but lost 25 bucks in the process!")
                init_stats["party"][0]["money"] = max(0, init_stats["party"][0]["money"] - 25)
                fled_flag[0] = True
                turn_taken = True
            else:
                print(f"{combate['name']} tried to run, but couldn't get away!")
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

    if "moveset2" in eatt and not eatt.get("phase2_triggered", False):
        if eatt["hp"] <= eatt["maxhp"] * eatt.get("phase2_threshold", 0.75):
            eatt["moveset"] = eatt["moveset2"]
            eatt["phase2_triggered"] = True
            flavor = eatt.get("phase2_text", "changes stance...")
            print(f"\n{eatt['name']} {flavor}")

    if "moveset3" in eatt and not eatt.get("phase3_triggered", False):
        if eatt["hp"] <= eatt["maxhp"] * eatt.get("phase3_threshold", 0.50):
            eatt["moveset"] = eatt["moveset3"]
            eatt["speed"] = eatt.get("speed3", eatt["speed"])
            eatt["phase3_triggered"] = True
            flavor = eatt.get("phase3_text", "shifts tactics once more...")
            print(f"\n{eatt['name']} {flavor}")

    if "moveset4" in eatt and not eatt.get("phase4_triggered", False):
        if eatt["hp"] <= eatt["maxhp"] * eatt.get("phase4_threshold", 0.25):
            eatt["moveset"] = eatt["moveset4"]
            eatt["phase4_triggered"] = True
            flavor = eatt.get("phase4_text", "shifts tactics one last time...")
            print(f"\n{eatt['name']} {flavor}")

    taunting = [m for m in living_party if m.get("taunt_turns", 0) > 0]

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
        unluckyman = random.choice(taunting) if taunting else random.choice(living_party)
        mult = get_mult(chosen_attack.get("type", []), unluckyman)
        total_defense = unluckyman["defe"] + items[unluckyman["eq_head"]]["defen"]
        effective_stre = chosen_attack["stre"] * mult
        defenseunluck = total_defense / 2
        if defenseunluck >= chosen_attack["stre"]:
            print(f"{unluckyman['name']} managed to resist {eatt['name']} attack!")
        else:
            totaldmg = round(effective_stre)
            unluckyman["hp"] -= totaldmg
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
            total_defense = member["defe"] + items[member["eq_head"]["defe"]]
            mult = get_mult(chosen_attack.get("type", []), member)
            effective_stre = chosen_attack["stre"] * mult
            totaldmg = round(effective_stre)
            member["hp"] -= totaldmg
            if "statuschance" in chosen_attack and chosen_attack.get("statustarget") == "ally":
                statusroll = random.random()
                effective_chance = max(0.0, chosen_attack["statuschance"] - member["luck"] * 0.2)
                if statusroll <= effective_chance:
                    member["status"] = chosen_attack["status"]
                    print(f"{member['name']} got hit and was applied {chosen_attack['status']}!")
                else:
                    print(f"{member['name']} got hit but dodged the debuff!")

        if chosen_attack.get("statustarget") == "self":
            eatt["status"] = chosen_attack["status"]
            print(f"The enemy also got applied with {chosen_attack['status']}")

    elif chosen_attack["targettype"] == "self":
        if chosen_attack.get("status") == "Defenseup":
            eatt["defe"] += chosen_attack["defe"]
            eatt["boostdef"] += chosen_attack["boostdef"]
            eatt["last_def_boost"] = chosen_attack["defe"]
            eatt["status"] = chosen_attack["status"]
            print(f"The enemy used {chosen_attack['nameskill']} and got {chosen_attack['status']}!")
        elif "heal" in chosen_attack:
            eatt["hp"] += chosen_attack["heal"]
            if "message" in chosen_attack:
                print(chosen_attack["message"])
            else:
                print(f"The {eatt['name']} healed himself using {chosen_attack['nameskill']}")
        elif chosen_attack.get("status") == "AttackUp":
            eatt["attackup_turns"] = chosen_attack["bonusattackturn"]
            eatt["attackup_bonus"] = chosen_attack["bonusattack"]
            if "message" in chosen_attack:
                print(chosen_attack["message"])
            else:
                print(f"{eatt['name']} used {chosen_attack['nameskill']} is getting pumped up!")
        elif "status" in chosen_attack:
            eatt["status"] = chosen_attack["status"]
            print(f"The enemy used {chosen_attack['nameskill']} and got {chosen_attack['status']}!")


def combat1(init_stats, enemy_ids, enemies_db, lang, language1, skills, items, can_flee=True):
    presentenemies = []
    for eids in enemy_ids:
        presentenemies.append(enemies_db[str(eids)].copy())

    game_over_flag = [False]
    fled_flag = [False]

    order = []
    for i in init_stats["party"]:
        i["currenttick"] = 1000 // i["speed"]
        i["isplayer"] = True
        order.append(i)
    for a in presentenemies:
        a["currenttick"] = 1000 // a["speed"]
        a["isplayer"] = False
        order.append(a)

    while any(e["hp"] > 0 for e in presentenemies) and not game_over_flag[0] and not fled_flag[0]:
        living = [i for i in order if i["hp"] > 0]
        lowest = min(i["currenttick"] for i in living)
        for b in living:
            b["currenttick"] -= lowest

        ready = [i for i in living if i["currenttick"] <= 0]
        ready.sort(key=lambda x: -x["speed"])

        for activechar in ready:
            if activechar["hp"] <= 0:
                continue

            print_bars(presentenemies, init_stats["party"])
            print(f"It's {activechar['name']}'s turn!")

            if activechar["bleed_turns"] > 0:
                activechar["hp"] -= activechar["bleed_dmg"]
                activechar["bleed_turns"] -= 1
                print(f"{activechar['name']} took {activechar['bleed_dmg']} bleed damage!")
                if activechar["hp"] <= 0:
                    activechar["currenttick"] = 1000 // activechar["speed"]
                    print(f"{activechar['name']} bled out!")
                    continue

            if activechar["boostdef"] > 0:
                activechar["boostdef"] -= 1
                if activechar["boostdef"] == 0:
                    activechar["defe"] -= activechar.get("last_def_boost", 0)
                    activechar["last_def_boost"] = 0
                    print(f"{activechar['name']}'s defense boost wore off!")

            if activechar.get("taunt_turns", 0) > 0:
                activechar["taunt_turns"] -= 1

            if activechar["status"] == "Stun":
                who = activechar["name"] if not activechar["isplayer"] else "You"
                print(f"{who} {'is' if not activechar['isplayer'] else 'are'} paralyzed!")
                activechar["status"] = "Normal"
                activechar["currenttick"] = 1000 // activechar["speed"]
                continue

            if activechar["isplayer"]:
                player_turn(activechar, presentenemies, init_stats, lang, language1, skills, items, game_over_flag, fled_flag, can_flee)
            else:
                enemy_turn(activechar, presentenemies, init_stats, game_over_flag)

            activechar["currenttick"] = 1000 // activechar["speed"]

            if game_over_flag[0] or fled_flag[0] or not any(e["hp"] > 0 for e in presentenemies):
                break

    print("Combat Finished!")

    if fled_flag[0]:
        print("You managed to get away safely!")
        return "fled"

    if not game_over_flag[0]:
        for enemy in presentenemies:
            if "possibledrop" in enemy:
                for drop in enemy["possibledrop"]:
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
            if enemy["eid"] == 12:
                init_stats["party"][0]["Majima_encounter"] += 1

        for i in range(len(init_stats["party"])):
            if "Charismatic Photo" in init_stats["party"][i]["eq_accessory"]:
                init_stats["party"][0]["hp"] -= 2
                print(f"You got hit, brah {init_stats["party"][0]["hp"]}")
                #init_stats["party"][0]["money"] += (enemy["money"] * 2)
            else:
                init_stats["party"][0]["money"] += enemy["money"]
                print(f"You got money, brah {init_stats["party"][0]["money"]}")

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
            while i["xptotal"] >= lvlup(i["lvl"]):
                i["xptotal"] -= lvlup(i["lvl"])
                i["lvl"] += 1
                i["pts"] += 1
                print(f"{i['name']} leveled up to {i['lvl']}")

    return not game_over_flag[0]