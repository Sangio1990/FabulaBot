import lightbulb

from classes.item import Item
from db.utilsDB import UtilsDB
from secretsData.data import *
from utils.utils import clear_id_from_mention

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
@lightbulb.command("rimuovioggetto", "Rimuovi un oggetto da un inventario di un personaggio")
@lightbulb.implements(lightbulb.SlashCommand)
async def remove_item(ctx: lightbulb.SlashContext) -> None:
    mentioned_id = clear_id_from_mention(ctx.options.menzione)
    char = db.load_character(mentioned_id)
    result = char.delete_item(ctx.options.oggetto)
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
@lightbulb.option("menzione", "Menziona il giocatore a cui assegnare il punto fabula", type=str, required=True)
@lightbulb.option("quantita", "Vuoi assegnarne più di uno?", type=int, required=False)
@lightbulb.command("aggiungipuntofabula", "Aggiungi un punto fabula ad un giocatore")
@lightbulb.implements(lightbulb.SlashCommand)
async def add_fabula(ctx: lightbulb.SlashContext) -> None:
    mentioned_id = clear_id_from_mention(ctx.options.menzione)
    char = db.load_character(mentioned_id)
    result = char.add_fabula(ctx.options.quantita if ctx.options.quantita is not None else 1)
    db.save_character(char, mentioned_id)
    await ctx.respond(result)


@plugin.command
@lightbulb.option("menzione", "Menziona il giocatore a cui rimuovere il punto fabula", type=str, required=True)
@lightbulb.option("quantita", "Vuoi toglierne più di uno?", type=int, required=False)
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