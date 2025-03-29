class Skill:
    def __init__(self,name,level,xp,max_xp):
        self.name = name
        self.level = level
        self.xp = xp
        self.max_xp = max_xp

    def train_skill(self):
        pass

class Mining(Skill):
    super().__init__(name="Mining", level=0, xp=0)