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
    characters = db.load_all_character()
    level_dict = {}
    class_dict = {}
    for character in characters:
        level = 0
        for cls in character.classes:
            if cls.name not in class_dict:
                class_dict[cls.name] = 1
            else:
                class_dict[cls.name] += 1
            level += cls.lvl
        if level not in level_dict:
            level_dict[level] = 1
        else:
            level_dict[level] += 1

    # Sorting the dicts to get a prettier output string
    level_dict = dict(sorted(level_dict.items()))
    class_dict = dict(sorted(class_dict.items()))

    # Creating the output string
    string = f"**ECCOTI LE STATISTICHE DEL SERVER**:\n " + \
        f"Nel database sono state create **{len(characters)}** schede \n" + \
        f"```\n{'-'*11}\n| LV | N° |\n"
    for level in level_dict:
        string += f"| {'0'+str(level) if level <= 9 else level} | {'0'+str(level_dict[level]) if level_dict[level] <= 9 else level_dict[level]} |\n"
    string += f"{'-'*25}\n" + \
        f"| CLASSE {' '*10}| N° |\n"

    max_space = 16
    for cls in class_dict:
        space_after = 0
        if len(cls) < max_space:
            space_after = (max_space - len(cls))
        string += f"| {cls}{' '*space_after} | {'0'+str(class_dict[cls]) if class_dict[cls] <= 9 else class_dict[cls]} |\n"
    string += f"{'-'*25}```"
    return string
