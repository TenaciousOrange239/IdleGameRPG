import random

class Player:
    def __init__(self, name, hp, atk, defence, dodge_chance, crit_chance=0, gold=0, xp=0):
        self.name = name
        self.hp = hp  # Changed from HP to hp to match Enemy class
        self.max_hp = hp  # Added max_hp to match Enemy class
        self.ATK = atk
        self.defence = defence
        self.dodge_chance = dodge_chance
        self.crit_chance = crit_chance  # Keep this as it's player-specific
        self.gold = gold
        self.xp = xp
        # You might want to add loot, xp_drop, and gold_drop if needed for gameplay

    # Add the same methods as in Enemy class
    def take_dmg(self, dmg):
        # Copy the logic from Enemy.take_dmg() method
        dodge_roll = random.random() * 100
        if dodge_roll <= self.dodge_chance:
            return False, 0, "dodged"

        actual_dmg = max(1, dmg - self.defence)
        self.hp -= actual_dmg

        

