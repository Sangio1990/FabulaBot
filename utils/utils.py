import json

from secretsData.data import *


def deserialize_json_to_object(json_string: str, class_name):
    data = json.loads(json_string)
    return class_name(**data)


def bool_ita(value: str) -> bool:
    if value.lower() == "si":
        return True
    else:
        return False


def role_name(role_id: int) -> str:
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
    return int(mention.replace("<@!", "").replace("<@", "").replace(">", ""))


def get_user_from_id(mentioned_id: int, ctx):
    return ctx.get_guild().get_member(mentioned_id)