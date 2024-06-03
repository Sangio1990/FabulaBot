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

create_rewards_table = """CREATE TABLE IF NOT EXISTS rewards_table (
                        "rank" TEXT,
                        zenit INTEGER,
                        materials_rolls INTEGER,
                        no_material INTEGER,
                        common_material INTEGER,
                        rare_material INTEGER,
                        epic_material INTEGER,
                        legendary_material INTEGER
                    );
                    """

populate_rewards_table = """INSERT INTO rewards_table 
                        ("rank",zenit,materials_rolls,no_material,common_material,rare_material,epic_material,legendary_material) 
                        VALUES
                         ('apprendista',0,0,0,0,0,0,0),
                         ('stella nascente',250,2,1,2,30,30,30),
                         ('cavaliere valoroso',400,4,1,2,17,30,30),
                         ('protettore epico',500,6,1,3,12,17,30),
                         ('campione leggendario',800,8,1,5,9,15,20),
                         ('eroe mitico',1000,10,1,4,7,14,19);
                    """


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

load_all_characters_query = """
    SELECT * FROM characters  
"""

# Loading Query
def load_character_query_builder(user_id):
    return f""" SELECT * FROM characters WHERE discord_id={user_id}"""


def load_rewards_query_builder(rank: str):
    return f""" SELECT * FROM rewards_table WHERE rank='{rank}'"""
