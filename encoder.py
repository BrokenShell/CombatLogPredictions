def encodes(label):
    lookup = {
        "Barbarian": 0,
        "Gladiator": 1,
        "Knight": 2,
        "Wizard": 3,
        "Warlock": 4,
        "Witch": 5,
        "Archer": 6,
        "Ninja": 7,
        "Pirate": 8,
        "Templar": 9,
        "Druid": 10,
        "Shaman": 11,
    }
    return lookup.get(label, 12)
