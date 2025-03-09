class Enemy:
    def __init__(self,name,hp,atk,dodge_chance,defence,loot,xp_drop,gold_drop):
        self.name = name
        self.hp = hp
        self.ATK = atk
        self.defence = defence
        self.dodge_chance = dodge_chance
        self.loot = loot
        self.xp_drop = xp_drop
        self.gold_drop = gold_drop

    def take_dmg(self,dmg):
        self.hp -= dmg

    def defeated(self):
        if self.hp <= 0:
            print(f"{self.name} has been defeated!")
        return self.hp <= 0

class Boss(Enemy):
    pass

class Mob(Enemy):
    pass

class Chicken(Mob):
    super().__init__(name="Chicken", hp=10, atk=2, defence=1, loot=["Chicken","Feathers"], gold_drop=5, xp_drop=10, dodge_chance=(100*0.10))

class Cow(Mob):
    super().__init__(name="Cow", hp=25, atk=5, defence=3, loot=["Beef","Leather"], gold_drop=10, xp_drop=20, dodge_chance=(100*0.03))

class Boar(Mob):
    super().__init__(name="Boar", hp=40, atk=15, defence=5, loot=["Tusk", "Fur"], gold_drop=35, xp_drop=50, dodge_chance=(100 * 0.07))

class Bear(Mob):
    super().__init__(name="Bear", hp=70, atk=30, defence=10, loot=["Pelt"], gold_drop=70, xp_drop=100, dodge_chance=(100 * 0.03))

class GreatBear(Boss):
    super().__init__(name="Great Bear", hp=400, atk=80, defence=20, loot=["Great Bear Claws", "Great Bear Head"], gold_drop=300, xp_drop=1000, dodge_chance=(100 * 0.01))

class WitheredHusk(Mob):
    super().__init__(name="Withered Husk", hp=50, atk=25, defence=15, loot=["Chicken", "Feathers"], gold_drop=50, xp_drop=150, dodge_chance=(100 * 0.05))

class LoneWanderer(Mob):
    super().__init__(name="Lone Wanderer", hp=75, atk=40, defence=10, loot=["Chicken", "Feathers"], gold_drop=80, xp_drop=200, dodge_chance=(100 * 0.17))

class CursedBandit(Mob):
    super().__init__(name="Cursed Bandit", hp=90, atk=50, defence=25, loot=["Chicken", "Feathers"], gold_drop=150, xp_drop=300, dodge_chance=(100 * 0.15))

class CursedEliteBandit(Mob):
    super().__init__(name="Cursed Elite Bandit", hp=150, atk=90, defence=30, loot=["Chicken", "Feathers"], gold_drop=250, xp_drop=500, dodge_chance=(100 * 0.20))

class LegrondasTheUndeadBandit(Boss):
    super().__init__(name="Legrondas, The Undead Bandit Leader", hp=200, atk=150, defence=40, loot=["Chicken", "Feathers"], gold_drop=1000, xp_drop=2000, dodge_chance=(100 * 0.33))

class GiantLeech(Mob): #Add healing ability
    super().__init__(name="Giant Leech", hp=50, atk=2, defence=1, loot=["Chicken", "Feathers"], gold_drop=5, xp_drop=10, dodge_chance=(100 * 0.05))

class FoulSpecter(Mob):
    super().__init__(name="Foul Specter", hp=20, atk=2, defence=1, loot=["Chicken", "Feathers"], gold_drop=5, xp_drop=10, dodge_chance=(100 * 0.05))

class BogLurker(Mob):
    super().__init__(name="Bog Lurker", hp=20, atk=2, defence=1, loot=["Chicken", "Feathers"], gold_drop=5, xp_drop=10, dodge_chance=(100 * 0.05))

class FetidWitch(Mob):
    super().__init__(name="Fetid Witch", hp=20, atk=2, defence=1, loot=["Chicken", "Feathers"], gold_drop=5, xp_drop=10, dodge_chance=(100 * 0.05))

class TheGrotesqueBasilisk(Boss):
    super().__init__(name="The Grotesque Basilisk", hp=20, atk=2, defence=1, loot=["Chicken", "Feathers"], gold_drop=5, xp_drop=10, dodge_chance=(100 * 0.05))

class ServantOfTheBlood(Mob):
    super().__init__(name="Servant Of The Blood", hp=20, atk=2, defence=1, loot=["Chicken", "Feathers"], gold_drop=5, xp_drop=10, dodge_chance=(100 * 0.05))

class BloodstainedSoldier(Mob):
    super().__init__(name="Bloodstained Soldier", hp=20, atk=2, defence=1, loot=["Chicken", "Feathers"], gold_drop=5, xp_drop=10, dodge_chance=(100 * 0.05))

class Hemomancer(Mob):
    super().__init__(name="Hemomancer", hp=20, atk=2, defence=1, loot=["Chicken", "Feathers"], gold_drop=5, xp_drop=10, dodge_chance=(100 * 0.05))

class CrimsonKnight(Mob):
    super().__init__(name="Crimson Knight", hp=20, atk=2, defence=1, loot=["Chicken", "Feathers"], gold_drop=5, xp_drop=10, dodge_chance=(100 * 0.05))

class TheSanguineLord(Boss):
    super().__init__(name="The Sanguine Lord", hp=20, atk=2, defence=1, loot=["Chicken", "Feathers"], gold_drop=5, xp_drop=10, dodge_chance=(100 * 0.05))

class ShadowSwarmedGolem(Mob):
    super().__init__(name="Shadow Swarmed Golem", hp=20, atk=2, defence=1, loot=["Chicken", "Feathers"], gold_drop=5, xp_drop=10, dodge_chance=(100 * 0.05))

class DeathswornBehemoth(Mob):
    super().__init__(name="Deathsworn Behemoth", hp=20, atk=2, defence=1, loot=["Chicken", "Feathers"], gold_drop=5, xp_drop=10, dodge_chance=(100 * 0.05))

class CorruptedWraith(Mob):
    super().__init__(name="Corrupted Wraith", hp=20, atk=2, defence=1, loot=["Chicken", "Feathers"], gold_drop=5, xp_drop=10, dodge_chance=(100 * 0.05))

class DarkenedDrake(Mob):
    super().__init__(name="Darkened Drake", hp=20, atk=2, defence=1, loot=["Chicken", "Feathers"], gold_drop=5, xp_drop=10, dodge_chance=(100 * 0.05))

class RavioliosProtectorOfTheCity(Boss):
    super().__init__(name="Raviolios Protector Of The City", hp=20, atk=2, defence=1, loot=["Chicken", "Feathers"], gold_drop=5, xp_drop=10, dodge_chance=(100 * 0.05))

class VoidboundKnight(Mob):
    super().__init__(name="Voidbound Knight", hp=20, atk=2, defence=1, loot=["Chicken", "Feathers"], gold_drop=5, xp_drop=10, dodge_chance=(100 * 0.05))

class VoidStalker(Mob):
    super().__init__(name="Void Stalker", hp=20, atk=2, defence=1, loot=["Chicken", "Feathers"], gold_drop=5, xp_drop=10, dodge_chance=(100 * 0.05))

class ArchmageRevenant(Mob):
    super().__init__(name="Archmage Revenant", hp=20, atk=2, defence=1, loot=["Chicken", "Feathers"], gold_drop=5, xp_drop=10, dodge_chance=(100 * 0.05))

class LegionOfDarkness(Mob):
    super().__init__(name="Legion Of Darkness", hp=20, atk=2, defence=1, loot=["Chicken", "Feathers"], gold_drop=5, xp_drop=10, dodge_chance=(100 * 0.05))

class YaoYaoTouchedByTheVoid(Boss):
    super().__init__(name="Yao Yao, Touched By TheVoid", hp=20, atk=2, defence=1, loot=["Chicken", "Feathers"], gold_drop=5, xp_drop=10, dodge_chance=(100 * 0.05))

class AeneasDarknessAbsolute(Boss):
    super().__init__(name="Aeneas, Darkness Absolute", hp=20, atk=2, defence=1, loot=["Chicken", "Feathers"], gold_drop=5, xp_drop=10, dodge_chance=(100 * 0.05))









