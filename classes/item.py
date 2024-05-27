import json


class Item:
    def __init__(self, name: str, description: str, value: int, quantity: int, sellable: bool = True):
        """
        Initializes an Item object with the provided attributes.

        Parameters:
        - name (str): The name of the item.
        - description (str): The description of the item.
        - value (int): The value of the item.
        - quantity (int): The quantity of the item.
        - sellable (bool, optional): Indicates whether the item is sellable. Defaults to True.

        Returns:
        - None
        """
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

    def __str__(self) -> str:
        """
        Converts the item to a string representation.

        Returns:
        - str: The string representation of the item.
        """
        return (f"**{self.name}** - {self.value}Z\n" +
                (f"**Ne possiedi:** {self.quantity}\n" if self.quantity > 1 else "") +
                f"**Vendibile:** ") + ("Si" if self.sellable else "No") + \
            f"{self.description}"


material_table = {
    "common": Item("Materiale comune", "Materiale usabile per craftare del valore di 50 zenit.", 50, 1, False),
    "rare": Item("Materiale raro", "Materiale usabile per craftare del valore di 150 zenit.", 150, 1, False),
    "epic": Item("Materiale epico", "Materiale usabile per craftare del valore di 250 zenit.", 250, 1, False),
    "legendary": Item("Materiale legendario", "Materiale usabile per craftare del valore di 500 zenit.", 500, 1, False),
}
