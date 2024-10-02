import copy
import hikari
import lightbulb

from classes.item import Item, material_table
from db.utilsDB import UtilsDB
from secretsData.data import *
from utils.utils import clear_id_from_mention, get_user_from_id

plugin = lightbulb.Plugin(name="Comandi Master", description="Comandi disponibili solo ai Master")
plugin.add_checks(lightbulb.checks.has_roles(chosen_region[MASTER_ROLE], chosen_region[ADMIN_ROLE], mode=any))
db = UtilsDB()


def load(bot: lightbulb.BotApp):
    bot.add_plugin(plugin)


def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(plugin)


@plugin.command
@lightbulb.option("vendibile", "L'oggetto è vendibile?", type=bool, required=True)
@lightbulb.option("quantita", "Quantità dell'oggetto da assegnare", type=int, required=True)
@lightbulb.option("prezzo", "Prezzo dell'oggetto da assegnare", type=int, required=True)
@lightbulb.option("descrizione", "Descrizione dell'oggetto da assegnare", type=str, required=False)
@lightbulb.option("nome", "Nome dell'oggetto da assegnare", type=str, required=True)
@lightbulb.option("menzione", "Menziona il giocatore a cui assegnare l'oggetto", type=str, required=True)
@lightbulb.command("assegnaoggetto", "Assegna un oggetto ad un personaggio!")
@lightbulb.implements(lightbulb.SlashCommand)
async def give_item(ctx: lightbulb.SlashContext) -> None:
    mentioned_id = clear_id_from_mention(ctx.options.menzione)
    char = db.load_character(mentioned_id)
    description = ctx.options.descrizione if ctx.options.descrizione != "" else ""
    result = char.add_item(
        Item(ctx.options.nome.lower().capitalize(), description, ctx.options.prezzo, ctx.options.quantita,
             ctx.options.vendibile))
    db.save_character(char, mentioned_id)
    await ctx.respond(result)


@plugin.command
@lightbulb.option("oggetto", "Quale oggetto vuoi eliminare=", type=str, required=True)
@lightbulb.option("menzione", "Menziona il giocatore a cui assegnare l'oggetto", type=str, required=True)
@lightbulb.option("quantita", "Quanti materiali vuoi eliminare?", type=int, required=False)
@lightbulb.command("rimuovioggetto", "Rimuovi un oggetto da un inventario di un personaggio")
@lightbulb.implements(lightbulb.SlashCommand)
async def remove_item(ctx: lightbulb.SlashContext) -> None:
    mentioned_id = clear_id_from_mention(ctx.options.menzione)
    char = db.load_character(mentioned_id)
    result = char.delete_item(ctx.options.oggetto, ctx.options.quantita if ctx.options.quantita is not None else 1)
    db.save_character(char, mentioned_id)
    if result == "Non hai oggetti da eliminare.":
        result = "Non ha oggetti da eliminare."
    await ctx.respond(result)


@plugin.command
@lightbulb.option("zenit", "Quanti zenit vuoi aggiungere?", type=int, required=True)
@lightbulb.option("menzione", "Menziona il giocatore a cui assegnare i zenit", type=str, required=True)
@lightbulb.command("aggiungizenit", "Aggiungi zenit ad un personaggio")
@lightbulb.implements(lightbulb.SlashCommand)
async def add_zenit(ctx: lightbulb.SlashContext) -> None:
    mentioned_id = clear_id_from_mention(ctx.options.menzione)
    char = db.load_character(mentioned_id)
    result = char.add_zenit(ctx.options.zenit)
    db.save_character(char, mentioned_id)
    await ctx.respond(result)


@plugin.command
@lightbulb.option("zenit", "Quanti zenit vuoi aggiungere?", type=int, required=True)
@lightbulb.option("menzione", "Menziona il giocatore a cui rimuovere i zenit", type=str, required=True)
@lightbulb.command("rimuovizenit", "Rimuovi zenit ad un personaggio")
@lightbulb.implements(lightbulb.SlashCommand)
async def add_zenit(ctx: lightbulb.SlashContext) -> None:
    mentioned_id = clear_id_from_mention(ctx.options.menzione)
    char = db.load_character(mentioned_id)
    result = char.remove_zenit(ctx.options.zenit)
    db.save_character(char, mentioned_id)
    await ctx.respond(result)


@plugin.command
@lightbulb.option("quantita", "Vuoi assegnarne più di uno?", type=int, required=False)
@lightbulb.option("menzione", "Menziona il giocatore a cui assegnare il punto fabula", type=str, required=True)
@lightbulb.command("aggiungipuntofabula", "Aggiungi un punto fabula ad un giocatore")
@lightbulb.implements(lightbulb.SlashCommand)
async def add_fabula(ctx: lightbulb.SlashContext) -> None:
    mentioned_id = clear_id_from_mention(ctx.options.menzione)
    char = db.load_character(mentioned_id)
    result = char.add_fabula(ctx.options.quantita if ctx.options.quantita is not None else 1)
    db.save_character(char, mentioned_id)
    await ctx.respond(result)


@plugin.command
@lightbulb.option("quantita", "Vuoi toglierne più di uno?", type=int, required=False)
@lightbulb.option("menzione", "Menziona il giocatore a cui rimuovere il punto fabula", type=str, required=True)
@lightbulb.command("rimuovipuntofabula", "Rimuovi un punto fabula ad un giocatore")
@lightbulb.implements(lightbulb.SlashCommand)
async def remove_fabula(ctx: lightbulb.SlashContext) -> None:
    mentioned_id = clear_id_from_mention(ctx.options.menzione)
    char = db.load_character(mentioned_id)
    result = char.remove_fabula(ctx.options.quantita if ctx.options.quantita is not None else 1)
    db.save_character(char, mentioned_id)
    await ctx.respond(result)


@plugin.command
@lightbulb.option("menzione", "Menziona il giocatore di cui vedere la scheda")
@lightbulb.command("vedischeda", "Vedi la scheda di un personaggio")
@lightbulb.implements(lightbulb.SlashCommand)
async def view_character(ctx: lightbulb.SlashContext) -> None:
    mentioned_id = clear_id_from_mention(ctx.options.menzione)
    char = db.load_character(mentioned_id)
    await ctx.respond(char)


@plugin.command
@lightbulb.option("xp", "Quanti punti esperienza vuoi assegnare?", type=int, required=True)
@lightbulb.option("menzione", "Menziona il giocatore a cui vuoi assegnare punti esperienza", type=str, required=True)
@lightbulb.command("aggiungixp", "Vedi l'inventario di un personaggio")
@lightbulb.implements(lightbulb.SlashCommand)
async def add_exp(ctx: lightbulb.SlashContext) -> None:
    mentioned_id = clear_id_from_mention(ctx.options.menzione)
    char = db.load_character(mentioned_id)
    result = char.add_exp(ctx.options.xp)
    db.save_character(char, mentioned_id)
    await ctx.respond(result)


@plugin.command
@lightbulb.option("giocatore5", "Menziona il quinto giocatore", type=str, required=False)
@lightbulb.option("giocatore4", "Menziona il quarto giocatore", type=str, required=False)
@lightbulb.option("giocatore3", "Menziona il terzo giocatore", type=str, required=False)
@lightbulb.option("giocatore2", "Menziona il secondo giocatore", type=str, required=False)
@lightbulb.option("giocatore1", "Menziona il primo giocatore", type=str, required=True)
@lightbulb.option("xp", "Quanti punti esperienza han guadagnato i tuoi giocatori?", type=int, required=True)
@lightbulb.command("reward", "Assegna i reward di fine sessione")
@lightbulb.implements(lightbulb.SlashCommand)
async def reward(ctx: lightbulb.SlashContext) -> None:
    await ctx.respond("**Calcolo i reward:**")
    xp = ctx.options.xp
    for i in range(1, 6):
        user_option = getattr(ctx.options, f'giocatore{i}')
        if not (user_option is None or user_option == ""):
            mentioned_id = clear_id_from_mention(user_option)
            char = db.load_character(mentioned_id)
            user: hikari.Member = get_user_from_id(mentioned_id, ctx)
            role = set(roles) & set(role.name.lower() for role in user.get_roles())
            reward_row = db.load_rewards("".join(role))
            response = f"**{char.name}**\n```Grado: {''.join(role).title()}\n"
            char.add_exp(xp)
            response += f"Guadagna {xp}XP andando a {char.xp}\n"
            char.add_zenit(reward_row.zenit)
            response += f"Guadagna {reward_row.zenit}Z andando a {char.zenit}\n"
            rewards = reward_row.roll_reward()
            response += f"Guadagna {len(rewards)} oggetti:\n"
            i = 0
            for r in rewards:
                i += 1
                if r[1] == "no":
                    response += f"Il {i}° dado ha fatto {r[0]} quindi riceve un bel niente\n"
                else:
                    material = copy.deepcopy(material_table[r[1]])
                    char.add_item(material)
                    response += f"Il {i}° dado ha fatto {r[0]} quindi riceve un {material.name}\n"
            db.save_character(char, mentioned_id)
            await ctx.bot.rest.create_message(ctx.get_channel(), response + "```\n\n")
    await ctx.bot.rest.create_message(ctx.get_channel(), "**Fine**")


@plugin.command
@lightbulb.option("nomeoggetto", "Scrivi il nome dell'oggetto che vuoi vedere")
@lightbulb.option("menzione", "Menziona il giocatore che possiede l'oggetto che vuoi vedere", type=str, required=True)
@lightbulb.command("masterinfooggetto", "Vedi l'inventario di un personaggio")
@lightbulb.implements(lightbulb.SlashCommand)
async def master_info_item(ctx: lightbulb.SlashContext) -> None:
    mentioned_id = clear_id_from_mention(ctx.options.menzione)
    char = db.load_character(mentioned_id)
    result = char.info_item(ctx.options.nomeoggetto)
    await ctx.respond(result)
