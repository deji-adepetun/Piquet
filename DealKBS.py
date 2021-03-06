import HandStatistics
from Hand import Hand


def deal_kbs(state, greedy):
    if any(x for x in state.carte_blanche.values()) and not state.discards[state.player_to_play]:
        return carte_blanche_discard(state)
    elif not state.discards[state.player_to_play]:
        return default_discard(state, greedy)
    elif not state.exchanged[state.player_to_play]:
        exchange_cards(state)
    elif not all(state.declarations.values()):
        return declare_stat(state)
    elif not state.younger_look_up_card and state.players.index(state.player_to_play) == 1:
        return state.younger_peep('peep')
    elif state.hands[state.player_to_play]:
        return play_trick(state)


def carte_blanche_discard(state):
    if state.players.index(state.player_to_play) == 0 and state.carte_blanche[state.player_to_play]:
        if not state.no_of_discards[state.player_to_play]:
            return state.max_discards[state.player_to_play]
        elif state.discards[state.get_next_player(state.player_to_play)]:
            hand = Hand(state.hands[state.player_to_play])
            return HandStatistics.compute_greedy_discard(hand, state.max_discards[state.player_to_play])

    elif state.players.index(state.player_to_play) == 1 and \
            state.carte_blanche[state.get_next_player(state.player_to_play)]:
        if not state.no_of_discards[state.player_to_play]:
            return state.max_discards[state.player_to_play]
        else:
            hand = Hand(state.hands[state.player_to_play])
            return HandStatistics.compute_greedy_discard(hand, state.max_discards[state.player_to_play])

    elif state.players.index(state.player_to_play) == 0 and \
            state.carte_blanche[state.get_next_player(state.player_to_play)]:
        if not state.no_of_discards[state.player_to_play]:
            return state.max_discards[state.player_to_play]
        else:
            hand = Hand(state.hands[state.player_to_play])
            return HandStatistics.compute_greedy_discard(hand, state.max_discards[state.player_to_play])

    elif state.players.index(state.player_to_play) == 1 and state.carte_blanche[state.player_to_play]:
        if not state.no_of_discards[state.player_to_play]:
            return state.max_discards[state.player_to_play]
        else:
            hand = Hand(state.hands[state.player_to_play])
            return HandStatistics.compute_greedy_discard(hand, state.max_discards[state.player_to_play])


def default_discard(state, greedy):
    if not state.no_of_discards[state.player_to_play]:
        return state.max_discards[state.player_to_play]
    else:
        hand = Hand(state.hands[state.player_to_play])
        return HandStatistics.compute_greedy_discard(hand, state.max_discards[state.player_to_play]) if greedy else \
            HandStatistics.compute_discard(
                hand, state.max_discards[state.player_to_play], state.players.index(state.player_to_play))


def exchange_cards(state):
    return 'exchange'


def declare_stat(state):
    if not state.declarations['point']:
        return 'point'
    elif not state.declarations['sequence']:
        return 'sequence'
    elif not state.declarations['set']:
        return 'set'


def play_trick(state):
    hand = state.hands[state.player_to_play]
    if not state.current_trick:
        return sorted(hand)[-1]
    else:
        _, lead_card = state.current_trick[0]
        cards_in_suit = [card for card in hand if card.suit == lead_card.suit]
        if cards_in_suit:
            return sorted(cards_in_suit)[-1]
        else:
            return sorted(hand)[0]
