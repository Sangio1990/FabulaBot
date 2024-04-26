import json


class Bond:
    def __init__(self, destination: str, description: str, level: int):
        """
        Initializes a new Bond object.

        Args:
        - destination (str): The destination of the bond.
        - description (str): The description of the bond.
        - level (int): The level of the bond.

        Returns:
        - None
        """
        self.destination = destination
        self.description = description
        self.level = level

    def to_json(self) -> str:
        """
        Converts the bond to a JSON string.

        Returns:
        - str: The JSON string representation of the bond.
        """
        return json.dumps(self.__dict__)
