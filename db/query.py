# Creation Query
# User Tables
create_character_table = """
        CREATE TABLE IF NOT EXISTS Characters (
            discord_id INTEGER PRIMARY KEY NOT NULL,
            name TEXT NOT NULL,
            dex INTEGER NOT NULL,
            vig INTEGER NOT NULL,
            intu INTEGER NOT NULL,
            will INTEGER NOT NULL,
            hp INTEGER NOT NULL,
            mp INTEGER NOT NULL,
            ip INTEGER NOT NULL,
            xp INTEGER NOT NULL,
            fp INTEGER NOT NULL,
            zenit INTEGER NOT NULL,
            classes TEXT,
            inventory TEXT,
            traits TEXT,
            bonds TEXT
        )"""

create_character_trash_table = """
        CREATE TABLE IF NOT EXISTS Characters_thrash (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            discord_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            dex INTEGER NOT NULL,
            vig INTEGER NOT NULL,
            intu INTEGER NOT NULL,
            will INTEGER NOT NULL,
            hp INTEGER NOT NULL,
            mp INTEGER NOT NULL,
            ip INTEGER NOT NULL,
            xp INTEGER NOT NULL,
            fp INTEGER NOT NULL,
            zenit INTEGER NOT NULL,
            classes TEXT,
            inventory TEXT,
            traits TEXT,
            bonds TEXT
        )"""

create_character_classes_table = """
    CREATE TABLE IF NOT EXISTS CharacterClasses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        lvl INTEGER NOT NULL,
        discord_id INTEGER NOT NULL
        FOREIGN KEY (discord_id) REFERENCES Characters (discord_id)
    )"""

# Not used yet
create_character_skills_table = """
    CREATE TABLE IF NOT EXISTS CharacterSkills (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        lvl INTEGER,
        skill_ID INTEGER NOT NULL,
        char_class_id INTEGER NOT NULL,
    )"""

# Data Tables, not used yet
create_classes_table = """
    CREATE TABLE IF NOT EXISTS Classes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        skills TEXT
    )"""

create_skills_table = """
    CREATE TABLE IF NOT EXISTS Skills (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        max_lvl INTEGER
    )"""

create_objects_table = """
    CREATE TABLE IF NOT EXISTS Objects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        value INTEGER
    )"""

create_bonds_table = """
    CREATE TABLE IF NOT EXISTS Bonds (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        level INTEGER NOT NULL
    )"""


# Delete Query
def delete_character_query_builder(user_id):
    return f"""
            DELETE FROM characters
            WHERE discord_id={user_id}
                """


# Saving Query
save_new_character_query = """
            INSERT INTO characters
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """

save_character_query = """
    UPDATE characters 
    SET  
    name = ?,
    dex = ?,
    vig = ?,
    intu = ?,
    will = ?,
    hp = ?,
    mp = ?,
    ip = ?,
    xp = ?,
    fp = ?,
    zenit = ?,
    classes = ?,
    inventory = ?,
    traits = ?,
    bonds = ?
    WHERE discord_id = ?
"""

move_character_to_trash_query = """
    INSERT INTO Characters_thrash (discord_id, name, dex, vig, intu, will, hp, mp, ip, xp, fp, zenit, 
    classes, inventory, traits, bonds) 
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""


# Loading Query
def load_character_query_builder(user_id):
    return f""" SELECT * FROM characters WHERE discord_id={user_id}"""
