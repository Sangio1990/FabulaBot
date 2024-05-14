import random


class Reward:
    def __init__(self, rank: str, zenit: int, materials_rolls: int, no_material: int, common_material: int,
                 rare_material: int, epic_material: int, legendary_material: int):
        self.rank = rank
        self.zenit = zenit
        self.materials_rolls = materials_rolls
        self.no_material = no_material
        self.common_material = common_material
        self.rare_material = rare_material
        self.epic_material = epic_material
        self.legendary_material = legendary_material

    def roll_reward(self) -> list[(int, str)]:
        rewads = []
        for i in range(self.materials_rolls):
            roll = random.randint(1, 20)
            if roll >= self.legendary_material:
                rewads.append((roll, "legendary"))
            elif roll >= self.epic_material:
                rewads.append((roll, "epic"))
            elif roll >= self.rare_material:
                rewads.append((roll, "rare"))
            elif roll >= self.common_material:
                rewads.append((roll, "common"))
            else:
                rewads.append((roll, "no"))
        return rewads

