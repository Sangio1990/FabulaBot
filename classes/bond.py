import json


class Bond:
    def __init__(self, destination: str, description: str, level: int):
        self.destination = destination
        self.description = description
        self.level = level

    def to_json(self) -> str:
        """
        Converts the bond to a JSON string.

        Returns:
        - str: The JSON string representation of the item.
        """
        return json.dumps(self.__dict__)
