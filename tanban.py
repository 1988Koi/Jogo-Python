import random
from karaoke import karaoke_game


def _get_bet(lang, language1, money):
    print(lang[language1]["tanban_balance"].format(money=money))
    raw = input("> ").strip()
    if not raw.isdigit():
        print(lang[language1]["tanban_invalid"])
        return None
    bet = int(raw)
    if bet <= 0 or bet > money:
        print(lang[language1]["tanban_invalid"])
        return None
    return bet


def dice_duel(init_stats, lang, language1):
    player = init_stats["party"][0]
    print("\n" + lang[language1]["tanban_dice_intro"])

    while True:
        money = player["money"]
        if money <= 0:
            print(lang[language1]["tanban_no_money"])
            return

        bet = _get_bet(lang, language1, money)
        if bet is None:
            again = input("> (q to quit) ").strip().lower()
            if again == "q":
                return
            continue

        house_roll = random.randint(1, 6)
        print(lang[language1]["tanban_dice_shown"].format(roll=house_roll))
        print(lang[language1]["tanban_dice_guess_prompt"])
        guess = input("> ").strip().lower()

        player_roll = random.randint(1, 6)
        print(lang[language1]["tanban_dice_result"].format(roll=player_roll))

        if guess not in ("h", "l"):
            print(lang[language1]["tanban_invalid"])
            continue

        won = (guess == "h" and player_roll > house_roll) or (guess == "l" and player_roll < house_roll)
        tied = player_roll == house_roll

        if tied:
            print(lang[language1]["tanban_dice_tie"])
        elif won:
            payout = bet * 2
            player["money"] += payout
            print(lang[language1]["tanban_dice_win"].format(amount=payout))
        else:
            player["money"] -= bet
            print(lang[language1]["tanban_dice_lose"].format(amount=bet))

        cont = input(lang[language1]["tanban_play_again"] + " (y/n) > ").strip().lower()
        if cont != "y":
            return


SLOT_SYMBOLS = ["🍒", "🍋", "🔔", "⭐", "7"]
SLOT_WEIGHTS = [35, 30, 20, 10, 5]


def slot_machine(init_stats, lang, language1):
    player = init_stats["party"][0]
    print("\n" + lang[language1]["tanban_slots_intro"])

    while True:
        money = player["money"]
        if money <= 0:
            print(lang[language1]["tanban_no_money"])
            return

        bet = _get_bet(lang, language1, money)
        if bet is None:
            again = input("> (q to quit) ").strip().lower()
            if again == "q":
                return
            continue

        reels = random.choices(SLOT_SYMBOLS, weights=SLOT_WEIGHTS, k=3)
        print(lang[language1]["tanban_slots_spin"])
        print(" [ " + " | ".join(reels) + " ] ")

        if reels[0] == reels[1] == reels[2]:
            multiplier = 10 if reels[0] == "7" else 5
            payout = bet * multiplier
            player["money"] += payout
            print(lang[language1]["tanban_slots_jackpot"].format(amount=payout))
        elif reels[0] == reels[1] or reels[1] == reels[2]:
            payout = bet * 2
            player["money"] += payout
            print(lang[language1]["tanban_slots_win"].format(amount=payout))
        else:
            player["money"] -= bet
            print(lang[language1]["tanban_slots_lose"].format(amount=bet))

        cont = input(lang[language1]["tanban_play_again"] + " (y/n) > ").strip().lower()
        if cont != "y":
            return


def tanban_menu(init_stats, lang, language1):
    in_here = True
    while in_here:
        print("\n" + lang[language1]["tanban_menu"])
        choice = input("> ").strip().lower()

        if choice == "1":
            dice_duel(init_stats, lang, language1)
        elif choice == "2":
            slot_machine(init_stats, lang, language1)
        elif choice == "i":
            in_here = False
        else:
            print(lang[language1]["tanban_invalid"])