import csv
from itertools import combinations
import joblib
from pandas import DataFrame

from encoder import encodes


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


def prediction_str(attacker, attacker_level, defender, defender_level):
    pred, prob = prediction(attacker, attacker_level, defender, defender_level)
    return f"{pred:>9} {prob:.1%}"


def prediction(attacker, attacker_level, defender, defender_level):
    model = joblib.load("model.joblib")
    basis = DataFrame([{
        "Attacker": encodes(attacker),
        "AttackerLevel": attacker_level,
        "Defender": encodes(defender),
        "DefenderLevel": defender_level
    }])
    pred, *_ = model.predict(basis)
    prob, *_ = model.predict_proba(basis)
    return pred, max(prob)


def make_predictions(group, level_range):
    for levels in combinations(level_range, 2):
        for player_1, player_2 in combinations(group, 2):
            player_1_level, player_2_level = levels
            print(f"\nPrediction: {player_1} {player_1_level} vs {player_2} {player_2_level}")
            print(prediction_str(player_1, player_1_level, player_2, player_2_level))


def prediction_outputs(group, level):
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


def do_all_predictions():
    for level in range(1, 21):
        prediction_outputs(characters, level)


def barb_test():
    for opponent in characters:
        print(f"Barbarian vs {opponent:<9}", end=" => ")
        print(prediction_str("Barbarian", 20, opponent, 20))


if __name__ == '__main__':
    barb_test()
