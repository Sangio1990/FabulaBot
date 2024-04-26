import json


class Cls:
    def __init__(self, name: str, lvl: int):
        """
        Initializes a new instance of the Cls class.

        Args:
        name (str): The name of the class.
        lvl (int): The level of the class.

        Returns:
        None
        """
        self.name = name
        self.lvl = lvl

    def to_json(self) -> str:
        """
        Converts the class to a JSON string.

        Returns:
        - str: The JSON string representation of the item.
        """
        return json.dumps(self.__dict__)
