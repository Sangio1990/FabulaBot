import json

from db.utilsDB import UtilsDB
from secretsData.data import *

db = UtilsDB()


def deserialize_json_to_object(json_string: str, class_name):
    """
      Deserializes a JSON string into an object of the specified class.

      Parameters:
      - json_string (str): The JSON string to deserialize.
      - class_name (type): The class type to instantiate.

      Returns:
      - object: An instance of the specified class populated with data from the JSON string.
      """
    data = json.loads(json_string)
    return class_name(**data)


def bool_ita(value: str) -> bool:
    """
    Converts an Italian string representation of boolean value to a boolean.

    Parameters:
    - value (str): The Italian string representation of boolean value ("si" for True, "no" for False).

    Returns:
    - bool: The boolean value corresponding to the input string ("si" returns True, "no" returns False).
    """
    if value.lower() == "si":
        return True
    else:
        return False


def role_name(role_id: int) -> str:
    """
    Returns the role name based on the provided role ID.

    Parameters:
    - role_id (int): The ID of the role.

    Returns:
    - str: The name of the role corresponding to the input role ID.
           If the role ID matches predefined constants for player, master, or admin roles,
           the corresponding role name is returned. Otherwise, a default message indicating
           an unrecognized role is returned, advising to contact an admin to report the error.
    """
    cr = chosen_region
    if role_id == cr[PLAYER_ROLE]:
        return "Giocatore"
    elif role_id == cr[MASTER_ROLE]:
        return "Master"
    elif role_id == cr[ADMIN_ROLE]:
        return "Amministatore di bot"
    else:
        return "Ruolo non riconosciuto, contatta un admin e segnala questo errore."


def clear_id_from_mention(mention: str) -> int:
    """
    Extracts the user or role ID from a mention string.

    Parameters:
    - mention (str): The mention string to process.

    Returns:
    - int: The extracted ID.
    """
    return int(mention.replace("<@!", "").replace("<@", "").replace(">", ""))


def get_user_from_id(mentioned_id: int, ctx):
    """
    Retrieves a user object from the provided user ID.

    Parameters:
    - mentioned_id (int): The ID of the user to retrieve.
    - ctx: The context object containing information about the command execution.

    Returns:
    - The user object corresponding to the provided user ID.
    """
    return ctx.get_guild().get_member(mentioned_id)


def get_server_statistics() -> str:
    """
    Retrieves and processes statistics about the server's characters.

    Returns:
    - str: A formatted string containing the server's statistics.

    The statistics include:
    - Total number of characters in the database.
    - Distribution of character levels.
    - Distribution of character classes.
    """

    # Fetch all characters from the database
    characters = db.load_all_character()

    # Initialize dictionaries to store level and class distributions
    level_dict = {}
    class_dict = {}

    # Iterate over each character
    for character in characters:
        level = 0

        # Iterate over each class of the character
        for cls in character.classes:
            # Update class distribution
            if cls.name not in class_dict:
                class_dict[cls.name] = 1
            else:
                class_dict[cls.name] += 1

            # Calculate total level of the character
            level += cls.lvl

        # Update level distribution
        if level not in level_dict:
            level_dict[level] = 1
        else:
            level_dict[level] += 1

    # Sort the dictionaries for a prettier output string
    level_dict = dict(sorted(level_dict.items()))
    class_dict = dict(sorted(class_dict.items()))

    # Initialize the output string
    string = f"**ECCOTI LE STATISTICHE DEL SERVER**:\n " + \
             f"Nel database sono state create **{len(characters)}** schede \n" + \
             f"```\n{'-' * 11}\n| LV | N° |\n"

    # Add level distribution to the output string
    for level in level_dict:
        string += f"| {'0' + str(level) if level <= 9 else level} | {'0' + str(level_dict[level]) if level_dict[level] <= 9 else level_dict[level]} |\n"

    # Add class distribution to the output string
    string += f"{'-' * 25}\n" + \
              f"| CLASSE {' ' * 10}| N° |\n"

    max_space = 16
    for cls in class_dict:
        space_after = 0
        if len(cls) < max_space:
            space_after = (max_space - len(cls))
        string += f"| {cls}{' ' * space_after} | {'0' + str(class_dict[cls]) if class_dict[cls] <= 9 else class_dict[cls]} |\n"

    # Close the output string
    string += f"{'-' * 25}```"

    # Return the output string
    return string


def get_character_level(char) -> int:
    """
    Retrieve and return the level of a character in the database.

    Returns:
    - int: The total level of a character in the database.
    """
    total_level = 0  # Initialize the total level

    # Calculate the total level of the character by summing up the levels of all classes
    total_level += sum(cls.lvl for cls in char.classes)

    return total_level  # Return the total level of a char in the database


def get_server_levels() -> str:
    """
    Retrieves and formats a list of characters and their total levels.

    Returns:
    - str: A formatted string containing the character names and their total levels.
           The levels are padded with a leading zero if they are single-digit numbers.

    The function works by:
    1. Fetching all characters from the database.
    2. Initializing an empty string to store the result.
    3. Iterating over each character, calculating their total level, and appending
       the formatted string to the result.
    4. Returning the final result string.
    """
    characters = db.load_all_character()  # Fetch all characters from the database
    result = "```"  # Initialize an empty string to store the result

    characters.sort(key=lambda char: get_character_level(char))

    # Iterate over each character
    for character in characters:
        level = 0  # Initialize the total level for the character

        # Calculate the total level of the character by summing up the levels of all classes
        for cls in character.classes:
            level += cls.lvl

        # Append the formatted string to the result
        result += f"{('0' + level.__str__()) if level <= 9 else level} -> {character.name}\n"

    # Return the final result string
    return result + '```'


def is_item_sellable(buyer, seller, item) -> str:
    if not item.sellable:
        return f"{buyer.mention} non puoi vendere {item.name} perché non è vendibile."
    elif buyer.discord_id == seller.discord_id:
        return f"https://tenor.com/hsCvL7Covmx.gif"
    elif buyer.zenit < item.value:
        return f"{buyer.mention} non ha abbastanza zenit per comprare {item.name}."

    return "ok"


def sell_to_player(buyer_id, seller_id, object) -> bool:
    pass
