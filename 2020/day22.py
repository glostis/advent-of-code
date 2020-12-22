import os
from copy import deepcopy


def play_round(player1, player2, game, round_, talk=False, recurse=False):
    if talk:
        print(f"-- Round {round_} (Game {game}) --")
        print(f"Player 1's deck: {', '.join(map(str, player1))}")
        print(f"Player 2's deck: {', '.join(map(str, player2))}")
    card1 = player1.pop(0)
    card2 = player2.pop(0)

    if talk:
        print(f"Player 1 plays: {card1}")
        print(f"Player 2 plays: {card2}")

    if recurse and len(player1) >= card1 and len(player2) >= card2:
        new_player1 = deepcopy(player1[:card1])
        new_player2 = deepcopy(player2[:card2])
        if talk:
            print("Playing a sub-game...")
        winner, _ = play_game(new_player1, new_player2, game + 1)
        if talk:
            print(f"...anyway, back to game {game}. Player {winner} won")
    else:
        if card1 > card2:
            winner = 1
            if talk:
                print(f"Player 1 wins round {round_} of game {game}!")
        else:
            winner = 2
            if talk:
                print(f"Player 2 wins round {round_} of game {game}!")

    if winner == 1:
        player1.extend([card1, card2])
    else:
        player2.extend([card2, card1])
    if talk:
        print()

    return winner


def compute_score(deck):
    score = 0
    for i, card in enumerate(reversed(deck), 1):
        score += i * card
    return score


def play_game(player1, player2, game=1, recurse=False):
    seen_rounds = set()
    round_ = 1
    while True:
        hash_round = ",".join(map(str, player1)) + "__" + ",".join(map(str, player2))
        if hash_round in seen_rounds:
            winning_deck = player1
            winner = 1
            break
        seen_rounds.add(hash_round)

        play_round(player1, player2, game, round_, recurse=recurse)
        round_ += 1
        if len(player2) == 0:
            winning_deck = player1
            winner = 1
            break
        if len(player1) == 0:
            winning_deck = player2
            winner = 2
            break

    return winner, compute_score(winning_deck)


def main():
    with open(os.path.join("data", "day22.txt")) as f:
        player1 = []
        line = f.readline().strip()
        assert line == "Player 1:"
        while True:
            line = f.readline().strip()
            if line == "":
                break
            line = int(line)
            player1.append(line)

        player2 = []
        line = f.readline().strip()
        assert line == "Player 2:"
        while True:
            line = f.readline().strip()
            if line == "":
                break
            line = int(line)
            player2.append(line)

    print(play_game(deepcopy(player1), deepcopy(player2))[1])
    print(play_game(deepcopy(player1), deepcopy(player2), recurse=True)[1])


if __name__ == "__main__":
    main()
