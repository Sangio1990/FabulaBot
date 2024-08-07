import json
# Carica il JSON dal file
with open('data/classes.json', 'r', encoding='utf-8') as file:
    cls_json = json.load(file)

# Constants
TOKEN = "token"
GUILD = "guild"
PLAYER_ROLE = "player_role"
MASTER_ROLE = "master_role"
ADMIN_ROLE = "admin_role"
CLASSES = list(cls_json.keys())

STATS = {"Vigore": "vig", "Intuito": "intu", "Volontà": "will", "Destrezza": "dex"}
BOOL_ITA = ["si", "no"]
new_char_dice_values = ["6", "8", "10"]
char_dice_values = ["6", "8", "10", "12"]
roles = ["apprendista", "stella nascente", "cavaliere valoroso", "protettore epico", "campione leggendario",
         "eroe mitico"]

# Error messages
no_char_found = "Non ho trovato nessun personaggio, sicuro di averlo creato?"
no_data_found = "Non ho trovato nessun dato nel database, contatta un amministratore."
