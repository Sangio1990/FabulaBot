import json

import lightbulb

from classes.bond import Bond
from classes.cls import Cls
from classes.item import Item
from utils.utils import deserialize_json_to_object


class Character:
    """
    Class representing a player character.
    """

    def __init__(self,
                 discord_id: int,
                 name: str,
                 dex: int,
                 vig: int,
                 intu: int,
                 will: int,
                 hp: int,
                 mp: int,
                 ip: int,
                 xp: int,
                 fp: int,
                 zenit: int,
                 classes: str,
                 inventory: str,
                 traits: str,
                 bonds: str,
                 ):
        """
        Initializes a new Character object with the specified values.

        Parameters:
        - discord_id (int): The Discord ID of the character.
        - name (str): The name of the character.
        - dex (int): The dexterity value of the character.
        - vig (int): The vigor value of the character.
        - intu (int): The intuition value of the character.
        - will (int): The willpower value of the character.
        - hp (int): The hit points of the character.
        - mp (int): The mind points of the character.
        - ip (int): The inventory points of the character.
        - xp (int): The experience points of the character.
        - fp (int): The fabula points of the character.
        - zenit (int): The zenit value of the character.
        - traits (str): The traits of the character.
        - bond (str): The bond of the character.

        Returns:
        - None
        """

        self.discord_id = discord_id
        self.name = name
        self.dex = dex
        self.vig = vig
        self.intu = intu
        self.will = will
        self.hp = hp
        self.mp = mp
        self.ip = ip
        self.xp = xp
        self.fp = fp
        self.zenit = zenit
        if classes == "":
            self.classes = []
        else:
            self.classes = [deserialize_json_to_object(cls, Cls) for cls in json.loads(classes)]
        if inventory == "":
            self.inventory = []
        else:
            self.inventory = [deserialize_json_to_object(item, Item) for item in json.loads(inventory)]
        self.traits = traits
        if bonds == "":
            self.bonds = []
        else:
            self.bonds = [deserialize_json_to_object(bond, Bond) for bond in json.loads(bonds)]

    def __str__(self):
        """
        Returns a string representing the character.

        Parameters:
        - None

        Returns:
        - str
            A string representing the character including character's name, traits, bonds, fabula points, experience points,
            inventory, inventory points, zenit, characteristics, hit points, mind points, and classes.
        """
        legami = "**Legami:**"
        if self.bonds.__len__() == 0:
            legami += " Nessun legame."
        else:
            for i in range(len(self.bonds)):
                legami += f"\n > **{i + 1})** {self.bonds[i].destination}, {self.bonds[i].description} [{self.bonds[i].level}]"

        cls = "**Classi: **"
        if self.classes.__len__() == 0:
            cls += "Nessuna classe."
        else:
            for i in range(len(self.classes)):
                cls += f"\n > **{i + 1})** {self.classes[i].name} [{self.classes[i].lvl}]"

        items = "**Inventario:**"
        if self.inventory.__len__() == 0:
            items += " Nessun oggetto."
        else:
            for i in range(len(self.inventory)):
                items += f"\n > **{i + 1})** {self.inventory[i].name}"
                if self.inventory[i].quantity > 1:
                    items += f" ({self.inventory[i].quantity})"

        traits = self.traits if self.traits.__len__() > 0 else "Nessun tratto."
        return f"> **Nome**: {self.name}" + \
            f"\n> **Tratti**: {traits}" + \
            f"\n> {legami}" + \
            f"\n> **Punti fabula**: {self.fp}" + \
            f"\n> **Punti exp**: {self.xp}" + \
            f"\n> {items}" + \
            f"\n> **Punti inventario:** {self.ip}" + \
            f"\n> **Zenit:** {self.zenit}" + \
            f"\n> **Carattestistiche:** Des d{self.dex}, Int d{self.intu}, Vig d{self.vig}, Vol d{self.will}" + \
            f"\n> **Punti vita:** {self.hp}" + \
            f"\n> **Punti mente:** {self.mp}" + \
            f"\n> {cls}"

    def bond(self, bond_name: str, bond_description: str, bond_level: int) -> str:
        """
        Adds a bond to the character.

        Parameters:
        - bond_name (str): The destination of the bond.
        - bond_description (str): The description of the bond.
        - bond_level (int): The level of the bond.

        Returns:
        - str: A message indicating the result of adding the bond.

        This method adds a bond to the character with the specified destination, description, and level.
        If the bond with the specified destination already exists, its description and level are updated.
        The method returns a success message if the bond is added or updated, or an error message if the maximum number of bonds is reached.
        """

        bond_name = bond_name.lower().capitalize()
        if self.bonds.__len__() == 0:
            self.bonds.append(Bond(bond_name, bond_description, bond_level))
            return f"Legame con {bond_name} aggiunto con succecco!."

        for bond in self.bonds:
            if bond.destination == bond_name:
                bond.description = bond_description
                bond.level = bond_level
                return f"Legame con {bond_name} aggiornato con successo!."
        if self.bonds.__len__() < 6:
            self.bonds.append(Bond(bond_name, bond_description, bond_level))
            return f"Legame con {bond_name} aggiunto con successo!."
        return "Hai raggiunto il limite massimo di legami."

    def delete_bond(self, bond_name):
        if self.bonds.__len__() == 0:
            return "Non hai alcun legame in scheda, creane uno prima di cancellarne altri"
        else:
            for bond in self.bonds:
                if bond.destination == bond_name:
                    self.bonds.remove(bond)
                    return f"Legame con {bond_name} rimosso con successo"
        return f"Nessun legame con {bond_name} trovato"

    def level_up(self, class_name: str) -> (str, bool):
        """
        Increases the level of the character for the specified class and updates related attributes.

        Parameters:
        - class_name (str): The name of the class for which the character's level is to be increased.

        Returns:
        - tuple (str, bool): A tuple containing a message indicating the result of the level increase and a boolean value
          indicating whether the level increase was successful.

        This method checks if the character has sufficient experience points to increase the level for the specified class.
        If the character has enough experience points, the method decreases the experience points by 10, increases the hit points
        and mind points by 1, and either adds the specified class to the character's list of classes with level 1 or increases
        the level of the existing class by 1. The method returns a success message and a boolean value indicating the success
        of the level increase, or an error message if the character does not have enough experience points or has already
        reached the maximum level for the specified class.
        """

        if self.xp < 10:
            return "Punti esperienza insufficienti, ne servono 10 per aumentare il livello.", False
        else:
            self.xp -= 10
            self.hp += 1
            self.mp += 1
            if class_name not in [cls.name for cls in self.classes]:
                self.classes.append(Cls(class_name, 1))
                return (f"{class_name} acquistata!.\n"
                        f"Usa il comando /bonusclasse per segnare i bonus di acquisizione della tua classe.", True)

            else:
                for cls in self.classes:
                    if cls.name == class_name:
                        if cls.lvl < 10:
                            cls.lvl += 1
                            return f"Hai raggiunto il livello {cls.lvl} di {cls.name}.", True
                        else:
                            return f"Hai già raggiunto il livello 10 per la classe {cls.name}.", False

    def add_bonus(self, bonus: str):
        """
        Increases the specified bonus attribute by 5.

        Parameters:
        - bonus (str): The bonus attribute to be increased. It can be one of the following:
            - "PV": Hit Points
            - "PM": Mind Points
            - "PI": Inventory Points

        Returns:
        - str: A message indicating the success of increasing the bonus attribute.

        This method increases the specified bonus attribute by 5. It takes a string parameter representing the bonus attribute
        and uses a match statement to determine which attribute to increase. After increasing the attribute, it returns a
        success message indicating the attribute has been increased.
        """
        match bonus:
            case "PV":
                self.hp += 5
                return "Punti vita aumentati con successo."
            case "PM":
                self.mp += 5
                return "Punti mente aumentati con successo."
            case "PI":
                self.ip += 2
                return "Punti inventario aumentati con successo."

    def buy_item(self, item_name: str, item_description: str, item_price: int) -> str:
        """
        Buys an item and adds it to the character's inventory.

        Parameters:
        - item_name (str): The name of the item to be bought.
        - item_description (str): The description of the item to be bought.
        - item_price (int): The price of the item to be bought.

        Returns:
        - str: A message indicating the result of the item purchase.

        This method checks if the character has enough zenit to buy the item. If the character has enough zenit, it decreases the zenit by the item price and adds the item to the character's inventory. If the item already exists in the inventory, it increases the quantity of the item. The method returns a success message if the item is bought and added to the inventory, or an error message if the character does not have enough zenit.
        """

        if self.zenit < item_price:
            return "Non hai abbastanza zenit."
        else:
            item_name = item_name.lower().capitalize()
            if item_description != None:
                item_description = item_description.lower().capitalize()
            else:
                item_description = ""
            self.zenit -= item_price
            for item in self.inventory:
                if item.name == item_name:
                    item.quantity += 1
                    return "Oggetto aggiunto con successo."
            self.inventory.append(Item(item_name, item_description, item_price, 1))
            return "Oggetto acquistato con successo."

    def sell_item(self, item_name: str) -> str:
        """
        Sells the specified item from the character's inventory and updates the character's zenit.

        Parameters:
        - item_name (str): The name of the item to be sold.

        Returns:
        - str: A message indicating the result of the item sale.

        This method checks if the character has the specified item in the inventory.
        If the item is found, it checks if the item is sellable.
        If the item is sellable and its quantity is 1, the method adds half of the item's value to the character's zenit and removes the item from the inventory.
        If the item is sellable and its quantity is greater than 1, the method decreases the item's quantity by 1 and adds half of the item's value to the character's zenit. If the item is not sellable, the method returns an error message. If the item is not found in the inventory, the method returns a message indicating that the item was not found.
        """

        if self.inventory.__len__() == 0:
            return "Non hai oggetti da vendere."
        else:
            item_name = item_name.lower().capitalize()
            for item in self.inventory:
                if item.name == item_name:
                    if item.sellable:
                        if item.quantity == 1:
                            self.zenit += item.value / 2
                            self.inventory.remove(item)
                            return "Oggetto venduto con successo."
                        else:
                            item.quantity -= 1
                            self.zenit += item.value / 2
                            return "Oggetto venduto con successo."
                    else:
                        return f"L'oggetto {item_name} non può essere venduto."
            return "Oggetto non trovato."

    def increase_stat(self, stat: str) -> str:
        """
        Increases the specified character attribute based on the provided stat.

        Parameters:
        - stat (str): The attribute to be increased. It can be one of the following:
            - "Destrezza": Dexterity attribute
            - "Vigore": Vigor attribute
            - "Intuito": Intuition attribute
            - "Volontà": Willpower attribute

        Returns:
        - str: A message indicating the success of increasing the specified attribute.

        This method increases the specified character attribute based on the provided stat.
        It uses a match statement to determine which attribute to increase and applies the corresponding logic.
        After increasing the attribute, it returns a message indicating the attribute has been increased.
        If the provided stat does not match any valid attribute, it returns a message indicating that the stat is not valid.
        """

        match stat:
            case "Destrezza":
                self.dex += 2
                return f"Destrezza modificata a d{self.dex}."
            case "Vigore":
                self.vig += 2
                self.hp += 10
                return f"Vigore modificato a d{self.vig}."
            case "Intuito":
                self.intu += 2
                self.mp += 10
                return f"Intuizione modificata a d{self.intu}."
            case "Volontà":
                self.will += 2
                return f"Volontà modificata a d{self.will}."

        return "Stat non valida."

    def add_item(self, item):
        """
        Adds an item to the character's inventory or increases the quantity if the item already exists.

        Parameters:
        - item: The item to be added to the inventory. It should be an instance of the Item class.

        Returns:
        - str: A message indicating the result of adding the item to the inventory.

        This method checks if the specified item already exists in the character's inventory.
        If the item exists, it increases the quantity of the existing item.
        If the item does not exist, it adds the item to the inventory.
        The method returns a success message indicating that the item has been added or its quantity has been increased.
        """

        for i in self.inventory:
            if i.name == item.name:
                i.quantity += item.quantity
                return f"{item.name} aggiunto con successo."
        self.inventory.append(item)
        return f"{item.name} aggiunto con successo."

    def delete_item(self, item: str, quantity: int = 1) -> str:
        """
        Removes the specified item from the character's inventory and updates the quantity if the item exists.

        Parameters:
        - item (str): The name of the item to be removed from the inventory.

        Returns:
        - str: A message indicating the result of the item removal.

        This method checks if the specified item exists in the character's inventory.
        If the item is found, it checks the quantity of the item.
        If the quantity is 1, the method removes the item from the inventory.
        If the quantity is greater than 1, the method decreases the item's quantity by 1.
        If the item is not found in the inventory, the method returns a message indicating that the item was not found.
        """

        if self.inventory.__len__() == 0:
            return "Non hai oggetti da eliminare."
        else:
            item = item.lower().capitalize()
            for i in self.inventory:
                if i.name == item:
                    if i.quantity <= quantity:
                        self.inventory.remove(i)
                        return f"{item} rimosso con successo dall'inventario."
                    else:
                        i.quantity -= quantity
                        return f"{item} rimosso con successo."
            return f"Oggetto {item} non trovato."

    def add_zenit(self, zenit: int) -> str:
        """
            Adds a specified number of zenit to the character.

            Parameters:
            - zenit (int): The number of zenit to add to the character.

            Returns:
            - str: A confirmation message indicating the number of zenit successfully added.
            """

        self.zenit += zenit
        return f"{zenit} zenit aggiunti con successo."

    def remove_zenit(self, zenit: int) -> str:
        """
        Removes the specified amount of zenit from the character's zenit balance.

        Parameters:
        - zenit (int): The amount of zenit to be removed from the character's balance.

        Returns:
        - str: A message indicating the result of the zenit removal.

        This method checks if the specified amount of zenit is available in the character's balance.
        If the character has enough zenit, the method subtracts the specified amount from the character's balance
        and returns a success message indicating the amount of zenit removed.
        If the character does not have enough zenit, the method returns an error message indicating the insufficient zenit balance.
        """

        if zenit > self.zenit:
            return "Il giocatore non possiede abbastanza zenit."
        else:
            self.zenit -= zenit
            return f"{zenit} zenit rimossi con successo."

    def add_fabula(self, quantity: int) -> str:
        """
        Adds a specified quantity of fabula points to the character.

        Parameters:
        - quantity (int): The quantity of fabula points to add to the character.

        Returns:
        - str: A confirmation message indicating that the fabula points have been successfully added.
        """

        self.fp += quantity
        return "Punti fabula aggiunto con successo."

    def remove_fabula(self, quantity: int) -> str:
        """
        Removes the specified quantity of fabula points from the character's balance.

        Parameters:
        - quantity (int): The amount of fabula points to be removed from the character's balance.

        Returns:
        - str: A message indicating the result of the fabula points removal.

        This method checks if the specified amount of fabula points is available in the character's balance.
        If the character has enough fabula points, the method subtracts the specified amount from the character's balance
        and returns a success message indicating the amount of fabula points removed.
        If the character does not have enough fabula points, the method returns an error message indicating the insufficient fabula points balance.
        """
        if quantity > self.fp:
            return "Il giocatore non possiede abbastanza punti fabula."
        else:
            self.fp -= quantity
            return f"{quantity} punti fabula rimossi con successo."

    def change_traits(self, theme: str, identity: str) -> str:
        """
        Changes the character's traits based on the specified theme and identity.

        Parameters:
        - theme (str): The theme of the character.
        - identity (str): The identity of the character.

        Returns:
        - str: A message indicating the result of the trait change.

        This function takes a theme and identity as input and applies the corresponding logic to change the character's traits.
        It uses a match statement to determine which theme and identity to apply and applies the corresponding logic.
        The function returns a message indicating the result of the trait change.
        If the theme or identity is not valid, the function returns a message indicating that the theme or identity is not valid.
        """

        traits = theme + ", " + identity
        self.traits = traits
        return f"Tratti del tuo pg aggiunti."

    def set_pv(self, hp: int) -> str:
        self.hp = hp
        return f"Pv modificati."

    def set_mp(self, mp: int) -> str:
        self.mp = mp
        return f"Mp modificati."

    def set_ip(self, ip: int) -> str:
        self.ip = ip
        return f"Ip modificati."

    def add_exp(self, xp: int) -> str:
        self.xp += xp
        return f"Xp aggiunti con successo."

    def buy_ip(self, ip: int) -> str:
        if self.zenit >= ip*10:
            self.zenit -= ip*10
            return f"{ip} ip acquistati con successo."
        else:
            return "Non hai abbastanza zenit."

    def get_stat(self, stat: str) -> int:
        match stat:
            case "vig":
                return self.vig
            case "dex":
                return self.dex
            case "intu":
                return self.intu
            case "will":
                return self.will



def check_doable(v: lightbulb.SlashContext.options):
    """
    Verifies if the input data is valid and, if so, creates the character.

    Parameters:
    - v (lightbulb.SlashContext.options): Object containing the options of the slash command.

    Returns:
    - str: A confirmation message or error message related to the character creation.

    This function takes a lightbulb.SlashContext.options object as input and verifies if the input data is valid for creating a character. It extracts the dexterity, vigor, intuition, and willpower values from the input object and checks if they are valid dice values (6, 8, or 10). If the values are valid, it calls the new_character function to create a new character with the specified values and returns a confirmation message. If the values are not valid or not numbers, it returns an error message.
    """
    try:
        dex = int(v.destrezza)
        vig = int(v.vigore)
        intu = int(v.intuito)
        will = int(v.volonta)
        valid_size = [6, 8, 10]
        if dex not in valid_size or vig not in valid_size or intu not in valid_size or will not in valid_size:
            return "The dice values entered are not valid"
    except:
        return "The dice values entered are not numbers"

    return new_character(v.nome, dex, vig, intu, will)


def new_character(name: str, dex: int, vig: int, intu: int, will: int):
    """
    Initializes a new character with the specified values.

    Parameters:
    - name (str): The name of the character.
    - dex (int): The dexterity value of the character.
    - vig (int): The vigor value of the character.
    - intu (int): The intuition value of the character.
    - will (int): The willpower value of the character.

    Returns:
    - Character: A new Character object initialized with the specified values, derived statistics, and fixed statistics.

    This function initializes a new Character object with the specified values for the character's name, dexterity, vigor, intuition, and willpower. It also calculates the derived statistics for hit points and mind points based on the vigor and willpower values. The function returns a new Character object initialized with the specified values and derived/fixed statistics.
    """
    return Character(
        0000,
        name,
        # Attributes
        dex,
        vig,
        intu,
        will,
        # Derived statistics
        vig * 5,  # Hit Points derived from vigor
        will * 5,  # Magic Points derived from willpower
        # Fixed statistics
        6,  # Initial value for some statistic
        50,  # Initial value for some statistic
        3,  # Initial value for some statistic
        500,
        "",
        "",
        "",
        ""
    )
