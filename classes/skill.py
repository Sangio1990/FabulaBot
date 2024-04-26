class Skill:
    def __init__(self, name: str, description: str, lvl: int):
        """
        Initializes an instance of the Abilities class.

        Args:
        name (str): The name of the ability.
        description (str): The description of the ability.
        lvl (int): The level of the ability.

        Returns:
        None
        """
        self.name = name
        self.description = description
        self.lvl = lvl