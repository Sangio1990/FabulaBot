import json

from utils.utils import deserialize_json_to_object


class Item:
    def __init__(self, name: str, description: str, value: int, quantity: int, sellable: bool = True):
        self.name = name
        self.description = description
        self.value = value
        self.quantity = quantity
        self.sellable = sellable

    def to_json(self) -> str:
        """
        Converts the item to a JSON string.

        Returns:
        - str: The JSON string representation of the item.
        """
        return json.dumps(self.__dict__)

