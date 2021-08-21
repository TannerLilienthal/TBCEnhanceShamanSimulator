# Weapon dictionary with stats.
# Weapon Name: [Bot End Dmg, Top End Dmg, Speed]

weapons = {"Dragonmaw": [172, 320, 2.7],
           "Bloodskull Destroyer": [130, 243, 2.6]}


def get_weapons():
    return list(weapons)


def get_weapon_stats(weapon):
    return weapons[weapon]
