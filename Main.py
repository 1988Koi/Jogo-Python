import json

with open("languages.json", "r", encoding="utf-8") as thingy:
    lang = json.load(thingy)
def load():
    with open("save.json", "r", encoding="utf-8") as saves1:
        saves0 = json.load(saves1)
def save(stats):
    with open("save.json", "w", encoding="utf-8") as saves2:
        json.dump(stats, saves2)

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
        "stats" : {
            "name" : "name",
            "class" : "class",
            "hp" : 10,
            "mana" : 3,
            "str" : 1,
            "luck" : 1,
            "inv" : "inv",
            "xp" : 0,
            "lvl" : 0,
            "pts" : 10
        }
    }
    print("\n" + lang[language1]["nameusr"])
    name1 = input("> ").strip()

    init_stats["stats"]["name"] = name1
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
        "Hobo" : {"hp" : 8, "mana": 7, "str": 3, "luck": 10},
        "Magician" : {"hp" : 7, "mana": 15, "str": 2, "luck": 5},
        "Security" : {"hp" : 10, "mana": 3, "str": 10, "luck": 3},
        "Foreman" : {"hp" : 30, "mana": 1, "str": 4, "luck": 0},
        "Chef" : {"hp" : 7, "mana": 15, "str": 3, "luck": 5}
    }

    while not classconf:

        class1 = input("> ").strip().lower()
        if class1 not in acceptedclass:
            print("\n" + lang[language1]["classno"])
            continue

        placeholderclass = lang[language1]["classok"]
        classname = acceptedclass[class1]
        init_stats["stats"]["class"] = classname
        actualclass = placeholderclass.replace("{class}", classname)
        print ("\n" + actualclass)
        print("\n" + lang[language1]["sure"])

        conf = input("> ").strip().lower()
        if conf == "1":
            classconf = True
        else:
            print("\n" + lang[language1]["classc"])

    chosenclass = init_stats["stats"]["class"]
    classst = statusclass[chosenclass]

    init_stats["stats"]["hp"] = classst["hp"]
    init_stats["stats"]["mana"] = classst["mana"]
    init_stats["stats"]["str"] = classst["str"]
    init_stats["stats"]["luck"] = classst["luck"]
    save(init_stats)