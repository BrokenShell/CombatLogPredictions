import csv
from itertools import combinations
import joblib

from encoder import encodes


def prediction_str(attacker, attacker_level, defender, defender_level):
    pred, prob = prediction(attacker, attacker_level, defender, defender_level)
    return f"Winner: {pred} {100 * prob:.0f}%"


def prediction(attacker, attacker_level, defender, defender_level):
    model = joblib.load("model.joblib")
    pred = model.predict([[
        encodes(attacker), attacker_level,
        encodes(defender), defender_level,
    ]])[0]
    prob = model.predict_proba([[
        encodes(attacker), attacker_level,
        encodes(defender), defender_level,
    ]])[0]
    return pred, max(prob)


def make_preds(group, level_range):
    for levels in combinations(level_range, 2):
        for player_1, player_2 in combinations(group, 2):
            player_1_level, player_2_level = levels
            print(f"\nPrediction: {player_1} {player_1_level} vs {player_2} {player_2_level}")
            print(prediction_str(player_1, player_1_level, player_2, player_2_level))


def pred_output(group, level):
    with open(f"output/predictions-{level}.csv", "w") as csv_file:
        file = csv.writer(csv_file, delimiter=',')
        file.writerow((
            "Attacker", "AttackerLevel",
            "Defender", "DefenderLevel",
            "Prediction", "Confidence",
        ))
        for player_1, player_2 in combinations(group, 2):
            pred, proba = prediction(
                player_1, level,
                player_2, level,
            )
            file.writerow((
                player_1, level,
                player_2, level,
                pred, round(proba, 2),
            ))


def do_all_preds():
    characters = [
        "Barbarian",
        "Gladiator",
        "Knight",
        "Wizard",
        "Warlock",
        "Witch",
        "Archer",
        "Ninja",
        "Pirate",
        "Templar",
        "Druid",
        "Shaman",
    ]
    for level in range(1, 21):
        pred_output(characters, level)


if __name__ == '__main__':
    print(prediction_str("Wizard", 20, "Barbarian", 20))
