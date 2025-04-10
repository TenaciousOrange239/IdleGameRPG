class Enemy:
    def __init__(self, name, hp, atk, defence, dodge_chance, loot, xp_drop, gold_drop):
        self.name = name
        self.hp = hp
        self.max_hp = hp  # Store max HP for HP bar calculations
        self.ATK = atk
        self.defence = defence
        self.dodge_chance = dodge_chance  # Percentage chance to dodge attacks
        self.loot = loot  # Dictionary of item:drop_chance pairs
        self.xp_drop = xp_drop
        self.gold_drop = gold_drop

    def take_dmg(self, amount):
        self.hp -= amount
        if self.hp < 0:
            self.hp = 0
        return self.hp <= 0

    def defeated(self):
        if self.hp <= 0:
            print(f"{self.name} has been defeated!")
        return {
            "gold": self.gold_drop,
            "xp": self.xp_drop,
            "loot": self.loot
        }


class Boss(Enemy):
    pass


class Mob(Enemy):
    pass


class Chicken(Mob):
    def __init__(self):
        super().__init__(name="Chicken", hp=10, atk=2, defence=1, loot=["Chicken", "Feathers"],
                         gold_drop=5, xp_drop=10, dodge_chance=(100 * 0.10))


class Cow(Mob):
    def __init__(self):
        super().__init__(name="Cow", hp=25, atk=5, defence=3, loot=["Beef", "Leather"],
                         gold_drop=10, xp_drop=20, dodge_chance=(100 * 0.03))


class Boar(Mob):
    def __init__(self):
        super().__init__(name="Boar", hp=40, atk=15, defence=5, loot=["Tusk", "Fur"],
                         gold_drop=35, xp_drop=50, dodge_chance=(100 * 0.07))


class Bear(Mob):
    def __init__(self):
        super().__init__(name="Bear", hp=70, atk=30, defence=10, loot=["Pelt"],
                         gold_drop=70, xp_drop=100, dodge_chance=(100 * 0.03))


class GreatBear(Boss):
    def __init__(self):
        super().__init__(name="Great Bear", hp=400, atk=80, defence=20,
                         loot=["Great Bear Claws", "Great Bear Head"], gold_drop=300, xp_drop=1000,
                         dodge_chance=(100 * 0.01))


class WitheredHusk(Mob):
    def __init__(self):
        super().__init__(name="Withered Husk", hp=50, atk=25, defence=15, loot=["Chicken", "Feathers"],
                         gold_drop=50, xp_drop=150, dodge_chance=(100 * 0.05))


class LoneWanderer(Mob):
    def __init__(self):
        super().__init__(name="Lone Wanderer", hp=75, atk=40, defence=10, loot=["Chicken", "Feathers"],
                         gold_drop=80, xp_drop=200, dodge_chance=(100 * 0.17))


class CursedBandit(Mob):
    def __init__(self):
        super().__init__(name="Cursed Bandit", hp=90, atk=50, defence=25, loot=["Chicken", "Feathers"],
                         gold_drop=150, xp_drop=300, dodge_chance=(100 * 0.15))


class CursedEliteBandit(Mob):
    def __init__(self):
        super().__init__(name="Cursed Elite Bandit", hp=150, atk=90, defence=30, loot=["Chicken", "Feathers"],
                         gold_drop=250, xp_drop=500, dodge_chance=(100 * 0.20))


class LegrondasTheUndeadBandit(Boss):
    def __init__(self):
        super().__init__(name="Legrondas, The Undead Bandit Leader", hp=200, atk=150, defence=40,
                         loot=["Chicken", "Feathers"], gold_drop=1000, xp_drop=2000, dodge_chance=(100 * 0.33))


class GiantLeech(Mob):
    def __init__(self):
        super().__init__(name="Giant Leech", hp=50, atk=2, defence=1, loot=["Chicken", "Feathers"],
                         gold_drop=5, xp_drop=10, dodge_chance=(100 * 0.05))


class FoulSpecter(Mob):
    def __init__(self):
        super().__init__(name="Foul Specter", hp=20, atk=2, defence=1, loot=["Chicken", "Feathers"],
                         gold_drop=5, xp_drop=10, dodge_chance=(100 * 0.05))


class BogLurker(Mob):
    def __init__(self):
        super().__init__(name="Bog Lurker", hp=20, atk=2, defence=1, loot=["Chicken", "Feathers"],
                         gold_drop=5, xp_drop=10, dodge_chance=(100 * 0.05))


class FetidWitch(Mob):
    def __init__(self):
        super().__init__(name="Fetid Witch", hp=20, atk=2, defence=1, loot=["Chicken", "Feathers"],
                         gold_drop=5, xp_drop=10, dodge_chance=(100 * 0.05))


class TheGrotesqueBasilisk(Boss):
    def __init__(self):
        super().__init__(name="The Grotesque Basilisk", hp=20, atk=2, defence=1,
                         loot=["Chicken", "Feathers"], gold_drop=5, xp_drop=10, dodge_chance=(100 * 0.05))


class ServantOfTheBlood(Mob):
    def __init__(self):
        super().__init__(name="Servant Of The Blood", hp=20, atk=2, defence=1, loot=["Chicken", "Feathers"],
                         gold_drop=5, xp_drop=10, dodge_chance=(100 * 0.05))


class BloodstainedSoldier(Mob):
    def __init__(self):
        super().__init__(name="Bloodstained Soldier", hp=20, atk=2, defence=1, loot=["Chicken", "Feathers"],
                         gold_drop=5, xp_drop=10, dodge_chance=(100 * 0.05))


class Hemomancer(Mob):
    def __init__(self):
        super().__init__(name="Hemomancer", hp=20, atk=2, defence=1, loot=["Chicken", "Feathers"],
                         gold_drop=5, xp_drop=10, dodge_chance=(100 * 0.05))


class CrimsonKnight(Mob):
    def __init__(self):
        super().__init__(name="Crimson Knight", hp=20, atk=2, defence=1, loot=["Chicken", "Feathers"],
                         gold_drop=5, xp_drop=10, dodge_chance=(100 * 0.05))


class TheSanguineLord(Boss):
    def __init__(self):
        super().__init__(name="The Sanguine Lord", hp=20, atk=2, defence=1,
                         loot=["Chicken", "Feathers"], gold_drop=5, xp_drop=10, dodge_chance=(100 * 0.05))


class ShadowSwarmedGolem(Mob):
    def __init__(self):
        super().__init__(name="Shadow Swarmed Golem", hp=20, atk=2, defence=1, loot=["Chicken", "Feathers"],
                         gold_drop=5, xp_drop=10, dodge_chance=(100 * 0.05))


class DeathswornBehemoth(Mob):
    def __init__(self):
        super().__init__(name="Deathsworn Behemoth", hp=20, atk=2, defence=1, loot=["Chicken", "Feathers"],
                         gold_drop=5, xp_drop=10, dodge_chance=(100 * 0.05))


class CorruptedWraith(Mob):
    def __init__(self):
        super().__init__(name="Corrupted Wraith", hp=20, atk=2, defence=1, loot=["Chicken", "Feathers"],
                         gold_drop=5, xp_drop=10, dodge_chance=(100 * 0.05))


class DarkenedDrake(Mob):
    def __init__(self):
        super().__init__(name="Darkened Drake", hp=20, atk=2, defence=1, loot=["Chicken", "Feathers"],
                         gold_drop=5, xp_drop=10, dodge_chance=(100 * 0.05))


class RavioliosProtectorOfTheCity(Boss):
    def __init__(self):
        super().__init__(name="Ravioli(os) Protector Of The City", hp=20, atk=2, defence=1,
                         loot=["Glock 20", "Perc-60"], gold_drop=500000, xp_drop=100000,
                         dodge_chance=(100 * 0.30))


class VoidboundKnight(Mob):
    def __init__(self):
        super().__init__(name="Voidbound Knight", hp=20, atk=2, defence=1, loot=["Chicken", "Feathers"],
                         gold_drop=5, xp_drop=10, dodge_chance=(100 * 0.05))


class VoidStalker(Mob):
    def __init__(self):
        super().__init__(name="Void Stalker", hp=20, atk=2, defence=1, loot=["Chicken", "Feathers"],
                         gold_drop=5, xp_drop=10, dodge_chance=(100 * 0.05))


class ArchmageRevenant(Mob):
    def __init__(self):
        super().__init__(name="Archmage Revenant", hp=20, atk=2, defence=1, loot=["Chicken", "Feathers"],
                         gold_drop=5, xp_drop=10, dodge_chance=(100 * 0.05))


class LegionOfDarkness(Mob):
    def __init__(self):
        super().__init__(name="Legion Of Darkness", hp=20, atk=2, defence=1, loot=["Chicken", "Feathers"],
                         gold_drop=5, xp_drop=10, dodge_chance=(100 * 0.05))


class YaoYaoTouchedByTheVoid(Boss):
    def __init__(self):
        super().__init__(name="Yao Yao, Touched By The Void", hp=20, atk=2, defence=1,
                         loot=["Chicken", "Feathers"], gold_drop=5, xp_drop=10, dodge_chance=(100 * 0.05))


class AeneasDarknessAbsolute(Boss):
    def __init__(self):
        super().__init__(name="Aeneas, Darkness Absolute", hp=20, atk=2, defence=1,
                         loot=["Chicken", "Feathers"], gold_drop=5, xp_drop=10, dodge_chance=(100 * 0.05))
