import csv

from Fortuna import dice, d, RandomValue


class CombatUnit:
    """ Interface """
    name: str
    hit_dice: int
    dam_dice: int
    offence: int
    defense: int

    def __init__(self, level):
        self.level = level
        self.health = max(self.hit_dice, dice(self.level, self.hit_dice))
        self.n_specials = self.level // 5

    def __bool__(self):
        return self.health > 0

    def damage(self):
        return dice(self.level, self.dam_dice)

    def attack(self, other):
        if self.n_specials > 0:
            self.n_specials -= 1
            self.special_attack(other)
        else:
            if d(20) + self.offence > d(20) + other.defense:
                other.health -= self.damage()

    def special_attack(self, other):
        if d(20) + self.offence > d(20) + other.defense:
            other.health -= self.damage() + self.dam_dice


class Barbarian(CombatUnit):
    name = "Barbarian"
    hit_dice = 10
    dam_dice = 6
    offence = 3
    defense = 2

    def special_attack(self, other):
        """ Rampage - imposes disadvantage on the defender """
        disadvantage = min(d(20), d(20)) + other.defense
        if d(20) + self.offence > disadvantage:
            other.health -= self.damage()


class Gladiator(CombatUnit):
    name = "Gladiator"
    hit_dice = 8
    dam_dice = 8
    offence = 2
    defense = 3

    def special_attack(self, other):
        """ Tactical Advantage - grants advantage to the attacker """
        advantage = max(d(20), d(20)) + self.offence
        if advantage > d(20) + other.defense:
            other.health -= self.damage()


class Knight(CombatUnit):
    name = "Knight"
    hit_dice = 12
    dam_dice = 4
    offence = 0
    defense = 5

    def special_attack(self, other):
        """ Strategic Supremacy - grants advantage to the attacker
            and imposes disadvantage on the defender """
        advantage = max(d(20), d(20)) + self.offence
        disadvantage = min(d(20), d(20)) + other.defense
        if advantage > disadvantage:
            other.health -= self.damage()


class Wizard(CombatUnit):
    name = "Wizard"
    hit_dice = 4
    dam_dice = 12
    offence = 5
    defense = 0

    def special_attack(self, other):
        """ Magic Missile - always a hit """
        other.health -= self.damage()


class Warlock(CombatUnit):
    name = "Warlock"
    hit_dice = 8
    dam_dice = 8
    offence = 3
    defense = 2

    def special_attack(self, other):
        """ Demonic Empowerment - deals double damage """
        double_damage = self.damage() + self.damage()
        if d(20) + self.offence > d(20) + other.defense:
            other.health -= double_damage


class Witch(CombatUnit):
    name = "Witch"
    hit_dice = 6
    dam_dice = 10
    offence = 3
    defense = 2

    def special_attack(self, other):
        """ Siphon Soul - heal for the amount of damage dealt """
        damage = self.damage()
        if d(20) + self.offence > d(20) + other.defense:
            other.health -= damage
            self.health += damage


class Archer(CombatUnit):
    name = "Archer"
    hit_dice = 6
    dam_dice = 10
    offence = 4
    defense = 1

    def special_attack(self, other):
        """ Steady Aim - grants advantage to the attacker """
        advantage = max(d(20), d(20)) + self.offence
        if advantage > d(20) + other.defense:
            other.health -= self.damage()


class Ninja(CombatUnit):
    name = "Ninja"
    hit_dice = 4
    dam_dice = 12
    offence = 4
    defense = 1

    def special_attack(self, other):
        """ Ambush - grants a bonus attack to the attacker,
            first attack has advantage,
            second attack has disadvantage """
        first_attack = max(d(20), d(20)) + self.offence
        if first_attack > d(20) + other.defense:
            other.health -= self.damage()
        second_attack = min(d(20), d(20)) + self.offence
        if second_attack > d(20) + other.defense:
            other.health -= self.damage()


class Pirate(CombatUnit):
    name = "Pirate"
    hit_dice = 8
    dam_dice = 8
    offence = 4
    defense = 1


class Templar(CombatUnit):
    name = "Templar"
    hit_dice = 10
    dam_dice = 6
    offence = 1
    defense = 4


class Druid(CombatUnit):
    name = "Druid"
    hit_dice = 8
    dam_dice = 8
    offence = 1
    defense = 4


class Shaman(CombatUnit):
    name = "Shaman"
    hit_dice = 6
    dam_dice = 10
    offence = 1
    defense = 4


def combat(attacker: CombatUnit, defender: CombatUnit):
    while attacker and defender:
        attacker.attack(defender)
        defender.attack(attacker)
    if attacker:
        return attacker.name
    elif defender:
        return defender.name
    else:
        return "Draw"


def campaign():
    random_class = RandomValue((
        Barbarian,
        Gladiator,
        Knight,
        Wizard,
        Warlock,
        Witch,
        Archer,
        Ninja,
        Pirate,
        Templar,
        Druid,
        Shaman,
    ))

    with open('combat_log.csv', 'w') as csv_file:
        file = csv.writer(csv_file, delimiter=',')
        file.writerow((
            "Attacker", "AttackerLevel",
            "Defender", "DefenderLevel",
            "Winner"
        ))
        for _ in range(100000):
            attacker = random_class(dice(1, 20))
            defender = random_class(dice(1, 20))
            file.writerow((
                attacker.name, attacker.level,
                defender.name, defender.level,
                combat(attacker, defender)
            ))


if __name__ == '__main__':
    campaign()
