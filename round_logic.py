from cards import new_deck, calc_best_total
import game_state as gs

def init_round():
    gs.deck = new_deck()
    gs.player = [gs.deck.pop(), gs.deck.pop()]
    gs.dealer = [gs.deck.pop(), gs.deck.pop()]
    gs.done = False
    gs.rounds += 1
    gs.can_change_bet = False
    gs.show_newround_button = False
    gs.message = f"Bet locked: ${gs.bet}"
    gs.round_active = True

def result_message():
    p = calc_best_total(gs.player)
    d = calc_best_total(gs.dealer)

    gs.show_newround_button = True
    gs.round_active = False

    if gs.dealer_mode == "Heaven":
        if len(gs.player) >= 3 and all(c['rank'] == '7' for c in gs.player[:3]):
            reward = gs.bet * 3
            gs.balance += reward
            return f"Heaven Bonus! 777 — You win +${reward}"

    if p > 21:
        gs.balance -= gs.bet
        gs.can_change_bet = True
        return f"You busted! Dealer wins. -${gs.bet}"

    if d > 21:
        gs.balance += gs.bet
        gs.wins += 1
        gs.can_change_bet = True
        return f"Dealer busted — You win! +${gs.bet}"

    if p == d:
        gs.can_change_bet = True
        return "Push (tie)."

    if p > d:
        gs.balance += gs.bet
        gs.wins += 1
        gs.can_change_bet = True
        return f"You win! +${gs.bet}"

    gs.balance -= gs.bet
    gs.can_change_bet = True
    return f"Dealer wins. -${gs.bet}"
