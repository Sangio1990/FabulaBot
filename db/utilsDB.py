import datetime
import importlib
import json
import os
import shutil
import typing as t
from sqlite3 import Connection

from lightbulb import LightbulbError

from classes.reward import Reward
from data.data import no_char_found, no_data_found
from db.query import *


class NoCharFound(LightbulbError):
    """
    Exception raised when a character is not found in the database.
    """

    def __init__(self, *args: t.Any) -> None:
        super().__init__(*args)


class NoDataFound(LightbulbError):
    """
    Exception raised when no data is found in the database.
    """

    def __init__(self, *args: t.Any) -> None:
        super().__init__(*args)


class UtilsDB:
    _instance = None
    connection: Connection = None
    c: Connection.cursor = None

    def __new__(cls, *args, **kwargs):
        """
        Create a new instance of UtilsDB if it doesn't already exist.

        Args:
        cls: The class.
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments.

        Returns:
        The new instance of UtilsDB.
        """
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def init_db(self, connection: Connection = None):
        """
        Initialize the database by executing the createTable query and committing the changes.
        """
        self.connection = connection
        self.c = self.connection.cursor()
        self.c.execute(create_character_table)
        # self.c.execute(create_classes_table)
        # self.c.execute(create_skills_table)
        # self.c.execute(create_bonds_table)
        self.c.execute(create_character_trash_table)

        # Reward Table
        self.c.execute("DROP TABLE IF EXISTS rewards_table;")
        self.c.execute(create_rewards_table)
        self.c.execute(populate_rewards_table)

        self.connection.commit()

    def check_if_id_exists(self, user_id):
        """
        Check if a character with the given user ID exists in the database.

        Args:
        user_id: The ID of the user whose character existence needs to be checked.

        Returns:
        True if a character with the given user ID exists in the database, False otherwise.
        """
        self.c.execute(load_character_query_builder(user_id))
        try:
            result = self.c.fetchone()[0]
            return result > 0
        except Exception as e:
            print(e)
            return False

    def save_character(self, character, user_id: int, new=False):
        """
        Save a character to the database.

        Args:
        character: The Character object to be saved.
        user_id: The ID of the user to whom the character belongs.
        new: A boolean indicating whether the character is new or being updated (default is False).

        Notes:
        - The character's classes, bonds, and inventory are serialized to JSON format before saving.
        - If the character is new, a new entry is created in the database; otherwise, the existing entry is updated.

        Returns:
        None

        Raises:
        Any exception raised by the underlying database operation.
        """

        character.classes = json.dumps([cls.to_json() for cls in character.classes])
        character.bonds = json.dumps([bond.to_json() for bond in character.bonds])
        character.inventory = json.dumps([item.to_json() for item in character.inventory])

        if new:
            self.c.execute(save_new_character_query, (
                user_id,
                character.name,
                character.dex,
                character.vig,
                character.intu,
                character.will,
                character.hp,
                character.mp,
                character.ip,
                character.xp,
                character.fp,
                character.zenit,
                character.classes,
                character.inventory,
                character.traits,
                character.bonds
            ))
        else:
            self.c.execute(save_character_query, (
                character.name,
                character.dex,
                character.vig,
                character.intu,
                character.will,
                character.hp,
                character.mp,
                character.ip,
                character.xp,
                character.fp,
                character.zenit,
                character.classes,
                character.inventory,
                character.traits,
                character.bonds,
                user_id))
            self.connection.commit()

    def load_character(self, user_id: int):
        """
        Load a character from the database.

        Args:
        user_id (int): The ID of the character to be loaded.

        Returns:
        Character: The loaded character.

        Raises:
        NoCharFound: If no character is found with the given user ID in the database.

        Notes:
        This method retrieves the character data from the database based on the provided user ID. If the character is not found, it raises a NoCharFound exception. Otherwise, it constructs a Character object from the retrieved data and returns it.
        """
        c = importlib.import_module("classes.character")
        try:
            self.c.execute(load_character_query_builder(user_id))
        except Exception as e:
            print(e)
            raise NoCharFound(no_char_found)

        result = self.c.fetchone()

        if result is None:
            raise NoCharFound(no_char_found)
        character = c.Character(*result)
        return character

    def load_rewards(self, rank: str):
        try:
            self.c.execute(load_rewards_query_builder(rank))
        except Exception as e:
            print(e)
            raise NoDataFound(no_data_found)

        result = self.c.fetchone()

        if result is None:
            raise NoDataFound(no_data_found)
        rewards = Reward(*result)
        return rewards

    def delete_character(self, user_id: int):
        """
        Delete a character from the database.

        Args:
        user_id (int): The ID of the character to be deleted.

        Returns:
        None

        Raises:
        NoCharFound: If no character is found with the given user ID in the database.

        Notes:
        This method first loads the character with the given user ID from the database.
        If the character is found, it moves the character to a trash table and then deletes the character from the main table.
        Finally, it commits the changes to the database.
        If no character is found with the given user ID, it raises a NoCharFound exception.
        """
        character = self.load_character(user_id)
        character.classes = json.dumps([cls.to_json() for cls in character.classes])
        character.bonds = json.dumps([bond.to_json() for bond in character.bonds])
        character.inventory = json.dumps([item.to_json() for item in character.inventory])

        self.c.execute(move_character_to_trash_query, (
            character.discord_id,
            character.name,
            character.dex,
            character.vig,
            character.intu,
            character.will,
            character.hp,
            character.mp,
            character.ip,
            character.xp,
            character.fp,
            character.zenit,
            character.classes,
            character.inventory,
            character.traits,
            character.bonds
        ))
        self.c.execute(delete_character_query_builder(user_id))
        self.connection.commit()

    def backup_db(self):
        try:
            current_date = datetime.datetime.now().strftime("%Y.%m.%d.%H.%M.%S")
            original_db = "db/Iridis.db"
            backup_dir = "db_bck"
            backup_db = os.path.join(backup_dir, f"Iridis.{current_date}.db")

            os.makedirs(backup_dir, exist_ok=True)

            shutil.copy2(original_db, backup_db)
            print(f"Backup del database eseguito con successo: {backup_db}")
        except Exception as e:
            print(f"Errore durante il backup del database: {e}")

        print(f"backup eseguito di {self}")

    def load_all_character(self):
        try:
            self.c.execute(load_all_characters_query)
        except Exception as e:
            print(e)
            raise NoDataFound(no_data_found)
        results = self.c.fetchall()
        if results is None:
            raise NoCharFound(no_char_found)
        characters = []
        c = importlib.import_module("classes.character")
        for result in results:
            character = c.Character(*result)
            characters.append(character)
        return characters
