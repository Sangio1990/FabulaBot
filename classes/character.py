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
            A string representing the character
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

        return f"> **Nome**: {self.name}" + \
            f"\n> **Tratti**: {self.traits if self.traits.__len__() > 0 else "Nessun tratto."}" + \
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
        - str
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
        match bonus:
            case "PV":
                self.hp += 5
                return "Punti vita aumentati con successo."
            case "PM":
                self.mp += 5
                return "Punti mente aumentati con successo."
            case "PI":
                self.ip += 5
                return "Punti inventario aumentati con successo."

    def buy_item(self, item_name: str, item_description: str, item_price: int) -> str:
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
        for i in self.inventory:
            if i.name == item.name:
                i.quantity += item.quantity
                return f"{item.name} aggiunto con successo."
        self.inventory.append(item)
        return f"{item.name} aggiunto con successo."

    def delete_item(self, item: str) -> str:
        if self.inventory.__len__() == 0:
            return "Non hai oggetti da eliminare."
        else:
            item = item.lower().capitalize()
            for i in self.inventory:
                if i.name == item:
                    if i.quantity == 1:
                        self.inventory.remove(i)
                        return f"{item} rimosso con successo."
                    else:
                        i.quantity -= 1
                        return f"{item} rimosso con successo."
            return f"Oggetto {item} non trovato."

    def add_zenit(self, zenit: int) -> str:
        self.zenit += zenit
        return f"{zenit} zenit aggiunti con successo."

    def remove_zenit(self, zenit: int) -> str:
        if zenit > self.zenit:
            return "Il giocatore non possiede abbastanza zenit."
        else:
            self.zenit -= zenit
            return f"{zenit} zenit rimossi con successo."

    def add_fabula(self, quantity: int) -> str:
        self.fp += quantity
        return "Punti fabula aggiunto con successo."

    def remove_fabula(self, quantity: int) -> str:
        if quantity > self.fp:
            return "Il giocatore non possiede abbastanza punti fabula."
        else:
            self.fp -= quantity
            return f"{quantity} punti fabula rimossi con successo."


def check_doable(v: lightbulb.SlashContext.options):
    """
    Verifies if the input data is valid and, if so, creates the character.

    Parameters:
    - v: lightbulb.SlashContext.options
        Object containing the options of the slash command

    Returns:
    - str
        Confirmation message or error message related to the character creation
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
        vig * 5 + 5,  # Hit Points derived from vigor
        will * 5 + 5,  # Magic Points derived from willpower
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
